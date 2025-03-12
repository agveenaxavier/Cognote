from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import pytesseract
from PIL import Image
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import PyPDF2
from models import db, User, Note, Tag
import magic
from pathlib import Path

# Set the explicit path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///eduvision.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path):
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(str(Path(file_path)))
    
    if 'pdf' in file_type:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
    elif 'image' in file_type:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    return ''

@app.route('/')
def home():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(user_id=current_user.id).all()
        tags = Tag.query.filter_by(user_id=current_user.id).all()
        return render_template('index.html', notes=notes, tags=tags)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password_hash, request.form.get('password')):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            text = extract_text_from_file(filepath)
            title = request.form.get('title', filename)
            tags = request.form.getlist('tags')
            
            note = Note(
                title=title,
                content=text,
                file_path=filepath,
                file_type=file.filename.rsplit('.', 1)[1].lower(),
                user_id=current_user.id
            )
            
            for tag_name in tags:
                tag = Tag.query.filter_by(name=tag_name, user_id=current_user.id).first()
                if not tag:
                    tag = Tag(name=tag_name, user_id=current_user.id)
                    db.session.add(tag)
                note.tags.append(tag)
            
            db.session.add(note)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'text': text,
                'note_id': note.id
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/search', methods=['POST'])
@login_required
def search():
    query = request.json.get('query', '').lower()
    tag_filter = request.json.get('tag')
    
    notes_query = Note.query.filter_by(user_id=current_user.id)
    
    if tag_filter:
        notes_query = notes_query.filter(Note.tags.any(name=tag_filter))
    
    if query:
        notes_query = notes_query.filter(Note.content.ilike(f'%{query}%'))
    
    notes = notes_query.all()
    return jsonify({
        'results': [{
            'id': note.id,
            'title': note.title,
            'content': note.content,
            'tags': [tag.name for tag in note.tags],
            'created_at': note.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for note in notes]
    })

@app.route('/export/<int:note_id>')
@login_required
def export_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
        
    return jsonify({
        'title': note.title,
        'content': note.content,
        'tags': [tag.name for tag in note.tags],
        'created_at': note.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

import os
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_upload_file(file):
    """Save uploaded file and return filepath"""
    if not file or file.filename == '':
        raise ValueError('No file selected')
    
    if not allowed_file(file.filename):
        raise ValueError('Only PDF, JPG, JPEG, and PNG files are allowed')
    
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return filepath

def cleanup_file(filepath):
    """Remove uploaded file after processing"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        print(f"Error cleaning up file: {e}")

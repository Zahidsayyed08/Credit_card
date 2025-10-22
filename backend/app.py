from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from parsers.statement_parser import StatementParser
from utils.file_handler import allowed_file, save_upload_file, cleanup_file
from config import config

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Enable CORS
CORS(app, resources={
    r"/api/*": {
        "origins": app.config['CORS_ORIGINS'],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Create uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Credit Card Statement Parser API is running'
    }), 200

@app.route('/api/issuers', methods=['GET'])
def get_issuers():
    """Return list of supported credit card issuers"""
    issuers = [
        {
            'id': 'chase',
            'name': 'Chase',
            'logo': '🏦',
            'description': 'Chase Bank credit cards'
        },
        {
            'id': 'amex',
            'name': 'American Express',
            'logo': '💳',
            'description': 'American Express cards'
        },
        {
            'id': 'capital_one',
            'name': 'Capital One',
            'logo': '🏛️',
            'description': 'Capital One credit cards'
        },
        {
            'id': 'discover',
            'name': 'Discover',
            'logo': '🔍',
            'description': 'Discover card statements'
        },
        {
            'id': 'citi',
            'name': 'Citibank',
            'logo': '🌍',
            'description': 'Citibank credit cards'
        }
    ]
    return jsonify(issuers), 200

@app.route('/api/parse', methods=['POST'])
def parse_statement():
    """Parse credit card statement from PDF or image"""
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        issuer = request.form.get('issuer')
        
        if not issuer:
            return jsonify({'error': 'No issuer specified'}), 400
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only PDF, JPG, JPEG, and PNG files are allowed'}), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({'error': 'File size exceeds 10MB limit'}), 400
        
        # Save file
        filepath = save_upload_file(file)
        
        # Parse statement using OCR and Gemini
        parser = StatementParser(issuer)
        result = parser.parse(filepath)
        
        # Check for parsing errors
        if 'error' in result:
            cleanup_file(filepath)
            return jsonify(result), 400
        
        # Clean up
        cleanup_file(filepath)
        
        return jsonify(result), 200
    
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Error parsing statement: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred while parsing the statement'}), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File size exceeds 10MB limit'}), 413

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=5000, host='0.0.0.0')

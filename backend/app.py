from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Временное хранилище заметок 
notes = []
current_id = 1

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервера"""
    return jsonify({'status': 'ok', 'message': 'Flask server is running'})

@app.route('/api/notes', methods=['GET'])
def get_notes():
    """Получить все заметки"""
    return jsonify(notes)

@app.route('/api/notes', methods=['POST'])
def create_note():
    """Создать новую заметку"""
    global current_id
    
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    # Создаем простую заметку
    new_note = {
        'id': current_id,
        'title': data.get('title'),
        'content': data.get('content', ''),
        'status': 'active',
        'labels': data.get('labels', []),
        'created_at': '2024-01-01T00:00:00',  # Временная метка
        'updated_at': '2024-01-01T00:00:00'
    }
    
    notes.append(new_note)
    current_id += 1
    
    return jsonify(new_note), 201

if __name__ == '__main__':
    print("=== Day 1: Basic Flask Setup ===")
    print("Server starting on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /api/health     - Check server status")
    print("  GET  /api/notes      - Get all notes")
    print("  POST /api/notes      - Create new note")
    print("\nTesting commands:")
    print("  curl http://localhost:5000/api/health")
    print("  curl http://localhost:5000/api/notes")
    app.run(debug=True, host='0.0.0.0', port=5000)

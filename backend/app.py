from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Разрешаем запросы от фронтенда

# Путь к JSON базе данных
DB_PATH = 'database/db.json'

def init_database():
    """Инициализация базы данных"""
    if not os.path.exists('database'):
        os.makedirs('database')
    
    if not os.path.exists(DB_PATH):
        initial_data = {
            "tasks": [],
            "labels": [
                {"id": 1, "name": "Учеба", "color": "#a790f9"},
                {"id": 2, "name": "Работа", "color": "#de95eb"},
                {"id": 3, "name": "Срочно", "color": "#fcfc86"},
                {"id": 4, "name": "Проект", "color": "#b5b0fa"},
                {"id": 5, "name": "Отдых", "color": "#a0f699"}
            ]
        }
        save_to_db(initial_data)

def load_from_db():
    """Загрузка данных из JSON"""
    try:
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tasks": [], "labels": []}

def save_to_db(data):
    """Сохранение данных в JSON"""
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==================== HEALTH CHECK ====================
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "message": "Task Manager API is running!"})

# ==================== TASKS API ====================
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Получение всех задач"""
    data = load_from_db()
    return jsonify(data['tasks'])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Создание новой задачи"""
    data = load_from_db()
    task_data = request.json
    
    # Генерируем ID
    task_ids = [task.get('id', 0) for task in data['tasks']]
    new_id = max(task_ids) + 1 if task_ids else 1
    
    new_task = {
        "id": new_id,
        "title": task_data.get('title', ''),
        "description": task_data.get('description', ''),
        "priority": task_data.get('priority', 'medium'),
        "labels": task_data.get('labels', []),
        "completed": task_data.get('completed', False),
        "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if not new_task['title']:
        return jsonify({"error": "Title is required"}), 400
    
    data['tasks'].append(new_task)
    save_to_db(data)
    
    return jsonify(new_task), 201

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Получение задачи по ID"""
    data = load_from_db()
    task = next((task for task in data['tasks'] if task['id'] == task_id), None)
    
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Обновление задачи"""
    data = load_from_db()
    task_index = next((i for i, task in enumerate(data['tasks']) if task['id'] == task_id), None)
    
    if task_index is None:
        return jsonify({"error": "Task not found"}), 404
    
    task_data = request.json
    # Обновляем только переданные поля
    if 'title' in task_data:
        data['tasks'][task_index]['title'] = task_data['title']
    if 'description' in task_data:
        data['tasks'][task_index]['description'] = task_data['description']
    if 'priority' in task_data:
        data['tasks'][task_index]['priority'] = task_data['priority']
    if 'completed' in task_data:
        data['tasks'][task_index]['completed'] = task_data['completed']
    if 'labels' in task_data:
        data['tasks'][task_index]['labels'] = task_data['labels']
    
    save_to_db(data)
    return jsonify(data['tasks'][task_index])

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удаление задачи"""
    data = load_from_db()
    initial_count = len(data['tasks'])
    data['tasks'] = [task for task in data['tasks'] if task['id'] != task_id]
    
    if len(data['tasks']) < initial_count:
        save_to_db(data)
        return jsonify({"message": "Task deleted successfully"})
    else:
        return jsonify({"error": "Task not found"}), 404

# ==================== LABELS API ====================
@app.route('/api/labels', methods=['GET'])
def get_labels():
    """Получение всех меток"""
    data = load_from_db()
    return jsonify(data['labels'])

@app.route('/api/labels', methods=['POST'])
def create_label():
    """Создание новой метки"""
    data = load_from_db()
    label_data = request.json
    
    label_ids = [label.get('id', 0) for label in data['labels']]
    new_id = max(label_ids) + 1 if label_ids else 1
    
    new_label = {
        "id": new_id,
        "name": label_data.get('name', ''),
        "color": label_data.get('color', '#a790f9')
    }
    
    if not new_label['name']:
        return jsonify({"error": "Label name is required"}), 400
    
    data['labels'].append(new_label)
    save_to_db(data)
    
    return jsonify(new_label), 201

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    init_database()
    print("🚀 Task Manager API server starting...")
    print("📊 Database initialized at:", DB_PATH)
    print("🌐 Server running on: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/api/health")
    print("📋 Available endpoints:")
    print("   GET  /api/health")
    print("   GET  /api/tasks")
    print("   POST /api/tasks")
    print("   GET  /api/tasks/{id}")
    print("   PUT  /api/tasks/{id}")
    print("   DELETE /api/tasks/{id}")
    print("   GET  /api/labels")
    print("   POST /api/labels")
    app.run(debug=True, host='0.0.0.0', port=5000)

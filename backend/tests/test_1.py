import json
def test_project_structure():
    import os
   
    required_files = [
        'app.py',
        'requirements.txt',
        'models/note.py',
        'services/note_service.py',
        'services/label_service.py'
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Файл {file_path} не найден"
        print(f"{file_path} найден")
    
    print("Структура проекта корректна")
def test_imports():
    
    import sys
    import os
    
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(tests_dir)  
    sys.path.insert(0, backend_dir)
    try:
        from models.note import Note, NoteStatus
        from services.note_service import NoteService
        from services.label_service import LabelService
        print("Импорты работают")
    except ImportError as e:
        raise AssertionError(f"Ошибка импорта: {e}")
def test_create_note():
    import sys
    import os
    sys.path.insert(0, '.')
    from app import app
    with app.test_client() as client:
       
        response = client.get('/api/health')
        assert response.status_code == 200
        print("/api/health работает")
        
        response = client.get('/api/notes')
        assert response.status_code == 200
        print("GET /api/notes работает")
        
        new_note = {
            'title': 'Тестовая заметка',
            'content': 'Это тестовое содержание'
        }
        
        response = client.post(
            '/api/notes',
            data=json.dumps(new_note),
            content_type='application/json'
        )
        
        assert response.status_code == 201, f"Ожидался код 201, получен {response.status_code}"
        print("POST /api/notes работает")
        
        note_data = json.loads(response.data)
        assert 'id' in note_data
        assert note_data['title'] == new_note['title']
        print(f"Заметка создана с ID: {note_data['id']}")
        
        response = client.get(f'/api/notes/{note_data["id"]}')
        assert response.status_code == 200
        print(f"GET /api/notes/{note_data['id']} работает")
        response = client.delete(f'/api/notes/{note_data["id"]}')
        if response.status_code == 204:
            print(f"DELETE /api/notes/{note_data['id']} работает")



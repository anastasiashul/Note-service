def test_project_structure():
    """Тест структуры проекта"""
    import os
    
    
    required_files = [
        'backend/app.py',
        'backend/requirements.txt'
        
        
    ]
    
    for file_path in required_files:
        assert os.path.exists(file_path), f"Файл {file_path} не найден"
    
    print(" Структура проекта корректна")

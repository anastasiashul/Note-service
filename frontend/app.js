class NoteApp {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.notes = [];
        this.init();
    }

    async init() {
        console.log('NoteApp started');
        
        try {
            const response = await fetch(`${this.apiUrl}/health`);
            if (response.ok) {
                console.log('Server is OK');
                await this.loadNotes();
            }
        } catch (error) {
            console.log('Server not available');
            this.showMessage('Сервер не доступен. Запустите: python app.py', 'error');
        }
        
        this.setupEvents();
    }

    async loadNotes() {
        try {
            const response = await fetch(`${this.apiUrl}/notes`);
            if (response.ok) {
                this.notes = await response.json();
                this.showNotes();
            }
        } catch (error) {
            console.error('Load error:', error);
        }
    }

    setupEvents() {
        document.getElementById('addNoteBtn').onclick = () => this.showForm();
        
        document.getElementById('saveNoteBtn').onclick = () => this.createNote();
        
        document.getElementById('cancelNoteBtn').onclick = () => this.hideForm();
        
        document.getElementById('filterStatus').onchange = () => this.showNotes();
        
        document.getElementById('filterLabel').disabled = true;
    }

    showForm() {
        document.getElementById('noteForm').classList.remove('hidden');
        document.getElementById('noteTitle').focus();
    }

    hideForm() {
        document.getElementById('noteForm').classList.add('hidden');
        document.getElementById('noteTitle').value = '';
        document.getElementById('noteContent').value = '';
        document.getElementById('noteLabels').value = '';
    }

    async createNote() {
        const title = document.getElementById('noteTitle').value.trim();
        const content = document.getElementById('noteContent').value.trim();
        const labels = document.getElementById('noteLabels').value.trim();

        if (!title) {
            alert('Введите заголовок');
            return;
        }

        const noteData = { title, content };
        if (labels) {
            noteData.labels = labels.split(',').map(l => l.trim());
        }

        try {
            const response = await fetch(`${this.apiUrl}/notes`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(noteData)
            });

            if (response.status === 201) {
                const newNote = await response.json();
                this.notes.push(newNote);
                this.hideForm();
                this.showNotes();
                this.showMessage('Заметка создана', 'success');
            }
        } catch (error) {
            console.error('Save error:', error);
            alert('Ошибка при сохранении');
        }
    }

    showNotes() {
        const container = document.getElementById('notesContainer');
        const statusFilter = document.getElementById('filterStatus').value;
        
        let notesToShow = this.notes;
        if (statusFilter) {
            notesToShow = notesToShow.filter(note => note.status === statusFilter);
        }

        if (notesToShow.length === 0) {
            if (this.notes.length === 0) {
                container.innerHTML = '<p class="no-notes">Заметок пока нет</p>';
            } else {
                container.innerHTML = '<p class="no-notes">Нет заметок с таким статусом</p>';
            }
            return;
        }

        container.innerHTML = '';
        notesToShow.forEach(note => {
            const noteDiv = document.createElement('div');
            noteDiv.className = `note ${note.status}`;
            
            const labelsHtml = note.labels && note.labels.length > 0 
                ? `<div class="note-labels">${note.labels.map(l => `<span class="label">${l}</span>`).join('')}</div>`
                : '';
            
            const statusText = {
                active: 'Активная',
                completed: 'Выполнена', 
                archived: 'В архиве'
            }[note.status] || note.status;

            noteDiv.innerHTML = `
                <div class="note-header">
                    <h3 class="note-title">${this.escapeHtml(note.title)}</h3>
                    <span class="note-status ${note.status}">${statusText}</span>
                </div>
                <div class="note-content">${note.content ? this.escapeHtml(note.content) : '<em>Нет текста</em>'}</div>
                ${labelsHtml}
                <div class="note-actions">
                    <button class="btn-edit" onclick="app.editInfo(${note.id})">✏️ Редактировать</button>
                    <button class="btn-delete" onclick="app.deleteInfo(${note.id})">🗑️ Удалить</button>
                </div>
                <div class="note-date">${this.formatDate(note.created_at)}</div>
            `;
            
            container.appendChild(noteDiv);
        });
    }

    escapeHtml(text) {
        if (!text) return '';
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }

    formatDate(dateStr) {
        try {
            const date = new Date(dateStr);
            return date.toLocaleDateString('ru-RU');
        } catch {
            return dateStr || '';
        }
    }

    showMessage(text, type) {
        const msg = document.createElement('div');
        msg.className = type === 'success' ? 'success-message' : 'error-message';
        msg.textContent = text;
        msg.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            border-radius: 5px;
            z-index: 1000;
        `;
        
        document.body.appendChild(msg);
        setTimeout(() => msg.remove(), 3000);
    }

    editInfo(id) {
        alert(`Редактирование заметки ${id}\n\nЭта функция будет доступна позже`);
    }

    deleteInfo(id) {
        alert(`Удаление заметки ${id}\n\nЭта функция будет доступна позже`);
    }
}

let app;
window.onload = () => {
    app = new NoteApp();
    window.app = app;
};
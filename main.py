from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import database

app = FastAPI()


class TaskCreate(BaseModel):
    text: str


# API: Получить задачи
@app.get("/api/tasks")
def get_tasks(db: Session = Depends(database.get_db)):
    return db.query(database.Task).order_by(database.Task.id.desc()).all()


# API: Добавить задачу
@app.post("/api/tasks")
def create_task(task_data: TaskCreate, db: Session = Depends(database.get_db)):
    new_task = database.Task(text=task_data.text.strip(), completed=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# API: Переключить статус
@app.patch("/api/tasks/{task_id}/toggle")
def toggle_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(database.Task).filter(database.Task.id == task_id).first()
    if task:
        task.completed = not task.completed
        db.commit()
        db.refresh(task)
    return task


# API: Удалить задачу
@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(database.Task).filter(database.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return {"status": "ok"}


# Главная страница (HTML, стили и JS отдаются напрямую)
@app.get("/", response_class=HTMLResponse)
def index():
    return """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Мой Планер Задач</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@700&family=Nunito:wght@600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-cream: #F8F3E6;
      --condensed-milk: #FFFBF0;
      --condensed-milk-dark: #F3E7CA;
      --condensed-border: #443527;
      --green-soft: #4A6E4E;
      --green-hover: #3B5B3E;
      --green-light: #E4EDE1;
      --text-main: #382C22;
      --text-muted: #8F8073;
      --danger: #BD4B37;
      --danger-bg: #FBECE8;
      --border: 3px solid var(--condensed-border);
      --shadow: 5px 5px 0px var(--condensed-border);
      --shadow-sm: 3px 3px 0px var(--condensed-border);
      --radius: 20px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg-cream);
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(74, 110, 78, 0.08) 0%, transparent 35%),
        radial-gradient(circle at 85% 85%, rgba(243, 231, 202, 0.6) 0%, transparent 40%),
        radial-gradient(#D6C4AE 1.5px, transparent 1.5px);
      background-size: 100% 100%, 100% 100%, 22px 22px;
      color: var(--text-main);
      font-family: 'Nunito', sans-serif;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding: 48px 16px;
    }

    .planner-card {
      width: 100%;
      max-width: 540px;
      background: var(--condensed-milk);
      border: var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 34px 28px;
      position: relative;
    }

    .planner-card::before {
      content: "";
      position: absolute;
      top: -14px;
      left: 36px;
      width: 76px;
      height: 24px;
      background: var(--green-light);
      border: var(--border);
      border-radius: 8px;
      box-shadow: 2px 2px 0px var(--condensed-border);
    }

    header { margin-bottom: 24px; }

    .title-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }

    h1 {
      font-family: 'Comfortaa', cursive;
      font-size: 28px;
      font-weight: 700;
      letter-spacing: -0.5px;
    }

    .counter-badge {
      background: var(--green-soft);
      color: #FFF;
      font-weight: 800;
      font-size: 14px;
      padding: 4px 14px;
      border-radius: 20px;
      border: 2px solid var(--condensed-border);
      box-shadow: 2px 2px 0px var(--condensed-border);
    }

    .subtitle {
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 700;
      margin-top: 4px;
    }

    .progress-box {
      background: var(--condensed-milk-dark);
      border: var(--border);
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-sm);
    }

    .progress-header {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      font-weight: 800;
      margin-bottom: 8px;
    }

    .progress-track {
      background: #FFF;
      border: 2px solid var(--condensed-border);
      height: 14px;
      border-radius: 12px;
      overflow: hidden;
    }

    .progress-fill {
      background: repeating-linear-gradient(
        45deg,
        var(--green-soft),
        var(--green-soft) 10px,
        #3B5B3E 10px,
        #3B5B3E 20px
      );
      height: 100%;
      width: 0%;
      border-radius: 10px;
      transition: width 0.35s ease;
    }

    .task-form {
      display: flex;
      gap: 10px;
      margin-bottom: 24px;
    }

    .task-input {
      flex: 1;
      padding: 14px 18px;
      background: #FFF;
      border: var(--border);
      border-radius: 14px;
      font-family: inherit;
      font-size: 15px;
      font-weight: 700;
      color: var(--text-main);
      box-shadow: var(--shadow-sm);
      outline: none;
      transition: transform 0.15s, box-shadow 0.15s;
    }

    .task-input:focus {
      transform: translateY(-2px);
      box-shadow: 4px 4px 0px var(--condensed-border);
    }

    .btn-submit {
      background: var(--green-soft);
      color: #FFF;
      border: var(--border);
      border-radius: 14px;
      padding: 0 20px;
      font-family: 'Comfortaa', cursive;
      font-weight: 700;
      font-size: 15px;
      cursor: pointer;
      box-shadow: var(--shadow-sm);
      transition: all 0.15s ease;
    }

    .btn-submit:hover {
      background: var(--green-hover);
      transform: translateY(-2px);
      box-shadow: 4px 4px 0px var(--condensed-border);
    }

    .btn-submit:active {
      transform: translate(2px, 2px);
      box-shadow: 1px 1px 0px var(--condensed-border);
    }

    .tasks-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .task-row {
      background: #FFF;
      border: var(--border);
      border-radius: 14px;
      padding: 12px 14px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: var(--shadow-sm);
      transition: transform 0.15s ease, opacity 0.2s;
    }

    .task-row:hover { transform: translateY(-2px); }

    .task-row.done {
      background: var(--condensed-milk-dark);
      opacity: 0.75;
      border-color: #8C7B6C;
      box-shadow: 2px 2px 0px #8C7B6C;
    }

    .custom-check {
      width: 26px;
      height: 26px;
      border: var(--border);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      background: #FFF;
      flex-shrink: 0;
      transition: background 0.15s;
    }

    .custom-check:hover { background: var(--green-light); }

    .task-row.done .custom-check { background: var(--green-soft); }

    .custom-check svg {
      width: 14px;
      height: 14px;
      stroke: #FFF;
      stroke-width: 3.5;
      fill: none;
      display: none;
    }

    .task-row.done .custom-check svg { display: block; }

    .task-title {
      flex: 1;
      font-size: 15px;
      font-weight: 800;
      color: var(--text-main);
      word-break: break-word;
      cursor: pointer;
    }

    .task-row.done .task-title {
      text-decoration: line-through;
      color: var(--text-muted);
    }

    .btn-trash {
      background: transparent;
      border: none;
      color: var(--danger);
      cursor: pointer;
      padding: 6px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.15s, background 0.15s;
    }

    .btn-trash:hover {
      background: var(--danger-bg);
      transform: scale(1.15);
    }

    .blank-state {
      text-align: center;
      padding: 32px 14px;
      color: var(--text-muted);
      border: 2px dashed #C8B9A6;
      border-radius: 14px;
      font-weight: 700;
      font-size: 14px;
    }
  </style>
</head>
<body>

  <div class="planner-card">
    <header>
      <div class="title-row">
        <h1>Список дел</h1>
        <div class="counter-badge" id="badge-count">0/0</div>
      </div>
      <p class="subtitle">Маленькие шаги каждый день</p>
    </header>

    <div class="progress-box">
      <div class="progress-header">
        <span>Прогресс дня</span>
        <span id="badge-percent">0%</span>
      </div>
      <div class="progress-track">
        <div class="progress-fill" id="progress-bar"></div>
      </div>
    </div>

    <form class="task-form" id="create-form">
      <input 
        type="text" 
        id="new-task-input" 
        class="task-input" 
        placeholder="Напиши задачу сюда..." 
        autocomplete="off"
        required
      >
      <button type="submit" class="btn-submit">+ Создать</button>
    </form>

    <ul class="tasks-list" id="task-container"></ul>

    <div id="blank-view" class="blank-state" style="display: none;">
      Все задачи выполнены! Отличная работа 🌿
    </div>
  </div>

  <script>
    let tasksList = [];

    const taskContainer = document.getElementById('task-container');
    const createForm = document.getElementById('create-form');
    const taskInput = document.getElementById('new-task-input');
    const blankView = document.getElementById('blank-view');
    const progressBar = document.getElementById('progress-bar');
    const badgePercent = document.getElementById('badge-percent');
    const badgeCount = document.getElementById('badge-count');

    async function fetchTasks() {
      try {
        const response = await fetch('/api/tasks');
        tasksList = await response.json();
        updateUI();
      } catch (err) {
        console.error('Ошибка при загрузке:', err);
      }
    }

    createForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const text = taskInput.value.trim();
      if (!text) return;

      try {
        await fetch('/api/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text })
        });
        taskInput.value = '';
        await fetchTasks();
      } catch (err) {
        console.error('Ошибка сохранения:', err);
      }
    });

    async function toggleDone(id) {
      try {
        await fetch(`/api/tasks/${id}/toggle`, { method: 'PATCH' });
        await fetchTasks();
      } catch (err) {
        console.error('Ошибка переключения:', err);
      }
    }

    async function removeTask(id) {
      try {
        await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
        await fetchTasks();
      } catch (err) {
        console.error('Ошибка удаления:', err);
      }
    }

    function updateUI() {
      taskContainer.innerHTML = '';
      blankView.style.display = tasksList.length === 0 ? 'block' : 'none';

      tasksList.forEach(item => {
        const li = document.createElement('li');
        li.className = `task-row ${item.completed ? 'done' : ''}`;

        li.innerHTML = `
          <div class="custom-check" onclick="toggleDone(${item.id})">
            <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>
          </div>
          <span class="task-title" onclick="toggleDone(${item.id})">
            ${escapeMarkup(item.text)}
          </span>
          <button class="btn-trash" onclick="removeTask(${item.id})" title="Удалить">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        `;
        taskContainer.appendChild(li);
      });

      const total = tasksList.length;
      const doneCount = tasksList.filter(t => t.completed).length;
      const ratio = total === 0 ? 0 : Math.round((doneCount / total) * 100);

      badgeCount.textContent = `${doneCount}/${total}`;
      progressBar.style.width = `${ratio}%`;
      badgePercent.textContent = `${ratio}%`;
    }

    function escapeMarkup(str) {
      const el = document.createElement('div');
      el.textContent = str;
      return el.innerHTML;
    }

    fetchTasks();
  </script>
</body>
</html>"""


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
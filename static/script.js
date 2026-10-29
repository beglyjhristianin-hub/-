<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Мой Планер Задач</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Comfortaa:wght@700&family=Nunito:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>

  <div class="app-container">
    <header>
      <h1>
        Список дел
        <span class="badge" id="task-badge">0/0</span>
      </h1>
      <p class="subtitle">Маленькие шаги ведут к большим результатам</p>
    </header>

    <div class="progress-section">
      <div class="progress-labels">
        <span>Прогресс</span>
        <span id="progress-percent">0%</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" id="progress-fill"></div>
      </div>
    </div>

    <form class="input-form" id="todo-form">
      <input 
        type="text" 
        id="todo-input" 
        class="input-field" 
        placeholder="Что нужно сделать?..." 
        autocomplete="off"
        required
      >
      <button type="submit" class="btn-add">Добавить</button>
    </form>

    <ul class="todo-list" id="todo-list"></ul>
    
    <div id="empty-state" class="empty-state" style="display: none;">
      Все дела выполнены! Самое время отдохнуть ☕
    </div>
  </div>

  <script src="/static/script.js"></script>
</body>
</html>
function selectCategory(category, element) {
    // Словарь с названиями и маршрутами
    const categories = {
        'smartphone': { name: 'Смартфон', endpoint: 'get /smartphone_for' },
        'notebook': { name: 'Ноутбук', endpoint: 'get /notebook_for' },
        'tv': { name: 'Телевизор', endpoint: 'get /tv_for' },
        'tablet': { name: 'Планшет', endpoint: 'get /tablet_for' },
        'smartwatch': { name: 'Умные часы', endpoint: 'get /watch_for' },
        'headphones': { name: 'Наушники', endpoint: 'get /headphones_for' },
        'camera': { name: 'Фотоаппарат', endpoint: 'get /camera_for' },
        'printer': { name: 'Принтер', endpoint: 'get /printer_for' },
        'monitor': { name: 'Монитор', endpoint: 'get /monitor_for' },
        'keyboard': { name: 'Клавиатура', endpoint: 'get /keyboard_for' },
        'mouse': { name: 'Мышь', endpoint: 'get /mouse_for' },
        'speaker': { name: 'Колонка', endpoint: 'get /speaker_for' },
        'router': { name: 'Роутер', endpoint: 'get /router_for' },
        'console': { name: 'Игровая консоль', endpoint: 'get /console_for' },
        'ebook': { name: 'Электронная книга', endpoint: 'get /ebook_for' }
    };
    
    const cat = categories[category];
    if (!cat) return;
    
    // Меняем маршрут
    document.getElementById('currentEndpoint').innerHTML = cat.endpoint;
    
    // Показываем результат
    let result = document.getElementById('selectionResult');
    document.getElementById('selectedCategory').innerHTML = cat.name;
    result.style.display = 'block';
    
    // Сбрасываем цвета у всех кнопок
    let buttons = document.querySelectorAll('.category-btn');
    buttons.forEach(btn => {
        btn.style.background = '#f8f9fa';
        btn.style.color = '#495057';
    });
    
    // Подсвечиваем выбранную кнопку
    if (element) {
        element.style.background = '#0066cc';
        element.style.color = 'white';
    }
    
    // Лог в консоль
    console.log(`Выбрано: ${cat.name} | ${cat.endpoint}`);
}

// Для проверки что js загрузился
console.log('JS работает! 🐒');
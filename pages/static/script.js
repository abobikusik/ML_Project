function selectCategory(category, element) {
    
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
}

// Для проверки что js загрузился
console.log('JS работает! 🐒');
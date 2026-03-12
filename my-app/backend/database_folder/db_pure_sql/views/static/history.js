//Константы для отображения
const CATEGORY_CONFIG = {
    'phone': { icon: '📱', name: 'Смартфон', class: 'category-phone' },
    'laptop': { icon: '💻', name: 'Ноутбук', class: 'category-laptop' },
    'tv': { icon: '📺', name: 'Телевизор', class: 'category-tv' }
};

const STATUS_CONFIG = {
    'completed': { text: '✅ Готово', class: 'status-completed' },
    'pending': { text: '⏳ В обработке', class: 'status-pending' },
    'error': { text: '❌ Ошибка', class: 'status-error' }
};

//Загрузка истории при загрузке страницы
document.addEventListener('DOMContentLoaded', loadHistory);

//Фильтры
document.getElementById('categoryFilter').addEventListener('change', loadHistory);
document.getElementById('statusFilter').addEventListener('change', loadHistory);

let searchTimeout;
document.getElementById('searchInput').addEventListener('input', function () {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(loadHistory, 500);
});

//Функция загрузки истории
async function loadHistory() {
    const category = document.getElementById('categoryFilter').value;
    const status = document.getElementById('statusFilter').value;
    const search = document.getElementById('searchInput').value;

    let url = '/api/history/';
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (status) params.append('status', status);

    const queryString = params.toString();
    if (queryString) url += '?' + queryString;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const requests = await response.json();

        // Фильтруем по поиску на клиенте
        const filtered = search ? requests.filter(req =>
            req.preview && req.preview.toLowerCase().includes(search.toLowerCase())
        ) : requests;

        displayHistory(filtered);
    } catch (error) {
        console.error('Ошибка загрузки истории:', error);
        document.getElementById('historyTableBody').innerHTML = `
                    <tr>
                        <td colspan="5" class="text-center py-4 text-danger">
                            ❌ Ошибка загрузки данных. Пожалуйста, обновите страницу.
                        </td>
                    </tr>
                `;
    }
}

//Отображение истории в таблице
function displayHistory(requests) {
    const tbody = document.getElementById('historyTableBody');

    if (!requests || requests.length === 0) {
        tbody.innerHTML = `
                    <tr>
                        <td colspan="5" class="empty-state">
                            <div class="empty-state-icon">📭</div>
                            <h5>История запросов пуста</h5>
                            <p class="text-muted">Перейдите в раздел "Категории" и создайте первый запрос</p>
                        </td>
                    </tr>
                `;
        return;
    }

    tbody.innerHTML = requests.map(req => {
        //Получаем конфигурацию категории
        const categoryConfig = CATEGORY_CONFIG[req.category_name] || {
            icon: '📦',
            name: req.category_name || 'Неизвестно',
            class: ''
        };

        //Получаем конфигурацию статуса
        const statusConfig = STATUS_CONFIG[req.status] || {
            text: req.status || 'Неизвестно',
            class: ''
        };

        //Форматируем дату
        const date = new Date(req.created_at);
        const formattedDate = date.toLocaleString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });

        return `
                    <tr onclick="showRequestDetails(${req.id})">
                        <td>#${req.id}</td>
                        <td>
                            <span class="category-badge ${categoryConfig.class}">
                                ${categoryConfig.icon} ${categoryConfig.name}
                            </span>
                        </td>
                        <td>${req.preview || '—'}</td>
                        <td>${formattedDate}</td>
                        <td>
                            <span class="status-badge ${statusConfig.class}">
                                ${statusConfig.text}
                            </span>
                        </td>
                    </tr>
                `;
    }).join('');
}

//Показ деталей запроса
async function showRequestDetails(requestId) {
    try {
        const response = await fetch(`/api/history/${requestId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const request = await response.json();

        const modalBody = document.getElementById('modalBody');

        // Получаем конфигурацию категории
        const categoryConfig = CATEGORY_CONFIG[request.category_name] || {
            icon: '📦',
            name: request.category_name || 'Неизвестно'
        };

        // Формируем HTML для характеристик
        let attributesHtml = '';
        if (request.attributes && Object.keys(request.attributes).length > 0) {
            for (const [key, value] of Object.entries(request.attributes)) {
                attributesHtml += `
                                <div class="modal-attr">
                                    <div class="modal-attr-label">${key}:</div>
                                    <div class="modal-attr-value">${value}</div>
                                </div>
                            `;

            }
        }

        //Форматируем дату
        const date = new Date(request.created_at);
        const formattedDate = date.toLocaleString('ru-RU', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });

        modalBody.innerHTML = `
                    <div class="mb-4">
                        <h5>${categoryConfig.icon} ${categoryConfig.name} #${request.id}</h5>
                        <small class="text-muted">${formattedDate}</small>
                    </div>
                    
                    <h6>Введенные характеристики:</h6>
                    ${attributesHtml || '<p class="text-muted">Нет характеристик</p>'}
                    
                    <h6 class="mt-4">Сгенерированное описание:</h6>
                    <div class="generated-text">
                        ${request.generated_text || 'Описание еще не сгенерировано...'}
                    </div>
                `;

        //Показываем модальное окно
        const modal = new bootstrap.Modal(document.getElementById('requestModal'));
        modal.show();

    } catch (error) {
        console.error('Ошибка загрузки деталей:', error);
        alert('Не удалось загрузить детали запроса');
    }
}
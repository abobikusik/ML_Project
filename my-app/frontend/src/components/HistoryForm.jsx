import { useState, useEffect } from "react";

function HistoryForm() {
  const [requests, setRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    category: "",
    status: ""
  });
  const [search, setSearch] = useState("");
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [showModal, setShowModal] = useState(false);

  // Константы для отображения
  const CATEGORY_CONFIG = {
    phone: { icon: '📱', name: 'Смартфон', class: 'category-phone' },
    laptop: { icon: '💻', name: 'Ноутбук', class: 'category-laptop' },
    tv: { icon: '📺', name: 'Телевизор', class: 'category-tv' }
  };

  const STATUS_CONFIG = {
    completed: { text: '✅ Готово', class: 'status-completed' },
    pending: { text: '⏳ В обработке', class: 'status-pending' },
    error: { text: '❌ Ошибка', class: 'status-error' }
  };

  // Загрузка истории при монтировании и изменении фильтров
  useEffect(() => {
    loadHistory();
  }, [filters.category, filters.status]);

  // Debounce для поиска
  useEffect(() => {
    const timer = setTimeout(() => {
      if (requests.length > 0) {
        // Фильтруем уже загруженные запросы на клиенте
        filterRequests();
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [search]);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const loadHistory = async () => {
    setLoading(true);
    let url = `${API_URL}/history/`;
    const params = new URLSearchParams();
    if (filters.category) params.append('category', filters.category);
    if (filters.status) params.append('status', filters.status);

    const queryString = params.toString();
    if (queryString) url += '?' + queryString;

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setRequests(data);
    } catch (error) {
      console.error('Ошибка загрузки истории:', error);
      setRequests([]);
    } finally {
      setLoading(false);
    }
  };

  const filterRequests = () => {
    if (!search.trim()) {
      // Если поиск пустой, показываем все запросы
      loadHistory();
    } else {
      // Фильтруем текущие запросы по поиску
      const filtered = requests.filter(req =>
        req.preview && req.preview.toLowerCase().includes(search.toLowerCase())
      );
      setRequests(filtered);
    }
  };

  const handleFilterChange = (e) => {
    const { id, value } = e.target;
    if (id === 'categoryFilter') {
      setFilters(prev => ({ ...prev, category: value }));
    } else if (id === 'statusFilter') {
      setFilters(prev => ({ ...prev, status: value }));
    }
  };

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
  };

  const showRequestDetails = async (requestId) => {
    try {
      const response = await fetch(`${API_URL}/history/${requestId}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const request = await response.json();
      setSelectedRequest(request);
      setShowModal(true);
    } catch (error) {
      console.error('Ошибка загрузки деталей:', error);
      alert('Не удалось загрузить детали запроса');
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatDateDetailed = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedRequest(null);
  };

  return (
    <>
      <div className="form-card">
        <h2 className="main-title">📋 История запросов</h2>

        {/* Фильтры */}
        <div className="filter-section">
          <div className="row">
            <div className="col-md-4">
              <label className="form-label">Категория</label>
              <select 
                className="form-select" 
                id="categoryFilter"
                value={filters.category}
                onChange={handleFilterChange}
              >
                <option value="">Все категории</option>
                <option value="phone">📱 Смартфоны</option>
                <option value="laptop">💻 Ноутбуки</option>
                <option value="tv">📺 Телевизоры</option>
              </select>
            </div>
            <div className="col-md-4">
              <label className="form-label">Статус</label>
              <select 
                className="form-select" 
                id="statusFilter"
                value={filters.status}
                onChange={handleFilterChange}
              >
                <option value="">Все статусы</option>
                <option value="completed">✅ Завершено</option>
                <option value="pending">⏳ В обработке</option>
                <option value="error">❌ Ошибка</option>
              </select>
            </div>
            <div className="col-md-4">
              <label className="form-label">Поиск</label>
              <input 
                className="form-control" 
                id="searchInput" 
                placeholder="🔍 Поиск по названию товара"
                value={search}
                onChange={handleSearchChange}
              />
            </div>
          </div>
        </div>

        {/* Таблица истории */}
        <div className="history-table">
          <table className="table table-hover mb-0">
            <thead>
              <tr>
                <th>ID</th>
                <th>Категория</th>
                <th>Товар</th>
                <th>Дата</th>
                <th>Статус</th>
              </tr>
            </thead>
            <tbody id="historyTableBody">
              {loading ? (
                <tr>
                  <td colSpan="5" className="text-center py-5">
                    <div className="spinner-border text-primary" role="status">
                      <span className="visually-hidden">Загрузка...</span>
                    </div>
                  </td>
                </tr>
              ) : !requests || requests.length === 0 ? (
                <tr>
                  <td colSpan="5" className="empty-state">
                    <div className="empty-state-icon">📭</div>
                    <h5>История запросов пуста</h5>
                    <p className="text-muted">Перейдите в раздел "Категории" и создайте первый запрос</p>
                  </td>
                </tr>
              ) : (
                requests.map(req => {
                  const categoryConfig = CATEGORY_CONFIG[req.category_name] || {
                    icon: '📦',
                    name: req.category_name || 'Неизвестно',
                    class: ''
                  };
                  const statusConfig = STATUS_CONFIG[req.status] || {
                    text: req.status || 'Неизвестно',
                    class: ''
                  };

                  return (
                    <tr key={req.id} onClick={() => showRequestDetails(req.id)}>
                      <td>#{req.id}</td>
                      <td>
                        <span className={`category-badge ${categoryConfig.class}`}>
                          {categoryConfig.icon} {categoryConfig.name}
                        </span>
                      </td>
                      <td>{req.preview || '—'}</td>
                      <td>{formatDate(req.created_at)}</td>
                      <td>
                        <span className={`status-badge ${statusConfig.class}`}>
                          {statusConfig.text}
                        </span>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Модальное окно с деталями запроса */}
      {showModal && selectedRequest && (
        <div className="modal fade show" style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)' }} tabIndex="-1">
          <div className="modal-dialog modal-lg">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Детали запроса</h5>
                <button type="button" className="btn-close" onClick={closeModal}></button>
              </div>
              <div className="modal-body" id="modalBody">
                <div className="mb-4">
                  <h5>
                    {CATEGORY_CONFIG[selectedRequest.category_name]?.icon || '📦'} 
                    {CATEGORY_CONFIG[selectedRequest.category_name]?.name || selectedRequest.category_name} #{selectedRequest.id}
                  </h5>
                  <small className="text-muted">{formatDateDetailed(selectedRequest.created_at)}</small>
                </div>
                
                <h6>Введенные характеристики:</h6>
                {selectedRequest.attributes && Object.keys(selectedRequest.attributes).length > 0 ? (
                  Object.entries(selectedRequest.attributes).map(([key, value], index) => (
                    <div className="modal-attr" key={index}>
                      <div className="modal-attr-label">{key}:</div>
                      <div className="modal-attr-value">{value}</div>
                    </div>
                  ))
                ) : (
                  <p className="text-muted">Нет характеристик</p>
                )}
                
                <h6 className="mt-4">Сгенерированное описание:</h6>
                <div className="generated-text">
                  {selectedRequest.generated_text || 'Описание еще не сгенерировано...'}
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={closeModal}>Закрыть</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default HistoryForm;
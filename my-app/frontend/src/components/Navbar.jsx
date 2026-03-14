const NavbarCustom = ({ onNavClick, currentPage }) => {
  return (
    <nav className="navbar navbar-expand-lg navbar-custom">
      <div className="container-fluid">
        <a className="navbar-brand" onClick={() => onNavClick("home")}>
          💿 Сервис генерации описания товаров
        </a>

        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <a 
                className={`nav-link ${currentPage === "home" ? "active" : ""}`} 
                onClick={() => onNavClick("home")}>
                🏠 Главная
              </a>
            </li>

            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
              >
                📦 Категории
              </a>

              <ul className="dropdown-menu">
                <li>
                  <a
                    className="dropdown-item"
                    onClick={() => onNavClick("phone")}
                  >
                    📱 Смартфоны
                  </a>
                </li>
                <li>
                  <a
                    className="dropdown-item"
                    onClick={() => onNavClick("laptop")}
                  >
                    💻 Ноутбуки
                  </a>
                </li>
                <li>
                  <a 
                    className="dropdown-item" 
                    onClick={() => onNavClick("tv")}
                  >
                    📺 Телевизоры
                  </a>
                </li>
              </ul>
            </li>

            <li className="nav-item">
              <a
                className={`nav-link ${currentPage === "history" ? "active" : ""}`}
                onClick={() => onNavClick("history")}
              >
                📝 История запросов
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};
// Что бы можно было использовать этот компонент в других файлах
export default NavbarCustom;

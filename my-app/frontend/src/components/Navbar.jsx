import { NavLink } from "react-router-dom";

const NavbarCustom = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-custom">
      <div className="container-fluid">
        <NavLink className="navbar-brand" to="/">
          💿 Сервис генерации описания товаров
        </NavLink>

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
              <NavLink 
                className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`} 
                to="/"
              >
                🏠 Главная
              </NavLink>
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
                  <NavLink className="dropdown-item" to="/phone">
                    📱 Смартфоны
                  </NavLink>
                </li>
                <li>
                  <NavLink className="dropdown-item" to="/laptop">
                    💻 Ноутбуки
                  </NavLink>
                </li>
                <li>
                  <NavLink className="dropdown-item" to="/tv">
                    📺 Телевизоры
                  </NavLink>
                </li>
              </ul>
            </li>

            <li className="nav-item">
              <NavLink 
                className={({ isActive }) => `nav-link ${isActive ? "active" : ""}`} 
                to="/history"
              >
                📝 История запросов
              </NavLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default NavbarCustom;
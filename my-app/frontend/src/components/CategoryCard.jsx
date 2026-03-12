const CategoryCard = ({ onCategoryClick }) => {
  // ФУНКЦИИ НАВИГАЦИИ
  const goToPhoneForm = () => console.log("📱 Форма смартфонов");
  const goToLaptopForm = () => console.log("💻 Форма ноутбуков");
  const goToTvForm = () => console.log("📺 Форма телевизоров");

  return (
    <>
      {/* КАРТОЧКА С КАТЕГОРИЯМИ */}
      <div className="category-card">
        <h2 className="main-title">Выберите категорию</h2>

        {/* КОНТЕЙНЕР С ПРОКРУТКОЙ */}
        <div className="category-buttons-container">
          <div className="category-buttons">
            {/* КНОПКА СМАРТФОН */}
            <div
              id="go_to_phone_form"
              className="category-btn"
              onClick={() => onCategoryClick("phone")}
            >
              <span className="category-icon">📱</span>
              Смартфон
              <span
                style={{ marginLeft: "auto", fontSize: "14px", color: "#999" }}
              >
                →
              </span>
            </div>

            {/* КНОПКА НОУТБУК */}
            <div
              id="go_to_laptop_form"
              className="category-btn"
              onClick={() => onCategoryClick("laptop")}
            >
              <span className="category-icon">💻</span>
              Ноутбук
              <span
                style={{ marginLeft: "auto", fontSize: "14px", color: "#999" }}
              >
                →
              </span>
            </div>

            {/* КНОПКА ТВ */}
            <div
              id="go_to_tv_form"
              className="category-btn"
              onClick={() => onCategoryClick("tv")}
            >
              <span className="category-icon">📺</span>
              Телевизор
              <span
                style={{ marginLeft: "auto", fontSize: "14px", color: "#999" }}
              >
                →
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* ПОДПИСЬ ВНИЗУ */}
      <div style={{ textAlign: "center", color: "#666", marginTop: "20px" }}>
        <small>ООО "ТМЫВ ДЕНЯК"</small>
      </div>
    </>
  );
};
// Что бы можно было использовать этот компонент в других файлах
export default CategoryCard;

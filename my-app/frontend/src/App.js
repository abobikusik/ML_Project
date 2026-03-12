// Functions
import { useState } from "react";
// Forms
import NavbarCustom from "./components/Navbar";
import CategoryCard from "./components/CategoryCard";
import LaptopForm from "./components/LaptopForm";
import PhoneForm from "./components/PhoneForm";
import TvForm from "./components/TvForm";
function App() {
  const [currentPage, setCurrentPage] = useState("home");
  // 'home', 'laptop', 'phone', 'tv'
  return (
    <>
      <NavbarCustom onNavClick={setCurrentPage} />
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6">
            {currentPage === "home" && (
              <CategoryCard onCategoryClick={setCurrentPage} />
            )}
            {currentPage === "laptop" && <LaptopForm />}
            {currentPage === "phone" && <PhoneForm />}
            {currentPage === "tv" && <TvForm />}
          </div>
        </div>
      </div>
    </>
  );
}
// Что бы можно было использовать этот компонент в других файлах
export default App;

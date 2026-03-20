// Functions
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
// Forms
import NavbarCustom from "./components/Navbar";
import CategoryCard from "./components/CategoryCard";
import LaptopForm from "./components/LaptopForm";
import PhoneForm from "./components/PhoneForm";
import TvForm from "./components/TvForm";
import HistoryForm from "./components/HistoryForm";

function App() {
  return (
    <BrowserRouter>
      <NavbarCustom />
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-8 col-lg-6">
            <Routes>
              <Route path="/" element={<CategoryCard />} />
              <Route path="/laptop" element={<LaptopForm />} />
              <Route path="/phone" element={<PhoneForm />} />
              <Route path="/tv" element={<TvForm />} />
              <Route path="/history" element={<HistoryForm />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </div>
        </div>
      </div>
    </BrowserRouter>
  );
}
// Что бы можно было использовать этот компонент в других файлах
export default App;

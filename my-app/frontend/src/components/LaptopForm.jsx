import { useRef } from "react";

function LaptopForm({ onBtnGenerateClick }) {
  // Создаем ref для каждого input
  const laptopBrandRef = useRef(null);
  const laptopModelRef = useRef(null);
  const laptopDiagonalRef = useRef(null);
  const laptopMatrixRef = useRef(null);
  const laptopFrequencyRef = useRef(null);
  const laptopResolutionRef = useRef(null);
  const laptopMaterialRef = useRef(null);
  const laptopWeightRef = useRef(null);
  const laptopProcessorRef = useRef(null);
  const laptopRAMRef = useRef(null);
  const laptopSSDRef = useRef(null);
  const laptopGraphicsCardRef = useRef(null);
  const laptopVRAMRef = useRef(null);
  const laptopBatteryRef = useRef(null);
  const laptopPowerAdapterRef = useRef(null);
  const laptopOSRef = useRef(null);
  // ------------------------------------------------
  const btnLaptopGenerateClick = () => {
    const formData = {
      device: "laptop",
      brand: laptopBrandRef.current?.value || "",
      model: laptopModelRef.current?.value || "",
      diagonal: laptopDiagonalRef.current?.value || "",
      matrix: laptopMatrixRef.current?.value || "",
      frequency: laptopFrequencyRef.current?.value || "",
      resolution: laptopResolutionRef.current?.value || "",
      material: laptopMaterialRef.current?.value || "",
      weight: laptopWeightRef.current?.value || "",
      processor: laptopProcessorRef.current?.value || "",
      ram: laptopRAMRef.current?.value || "",
      ssd: laptopSSDRef.current?.value || "",
      graphicsCard: laptopGraphicsCardRef.current?.value || "",
      vram: laptopVRAMRef.current?.value || "",
      battery: laptopBatteryRef.current?.value || "",
      powerAdapter: laptopPowerAdapterRef.current?.value || "",
      os: laptopOSRef.current?.value || "",
    };
    console.log(formData);
    // TODO: connect to FastApi
    fetch('http://localhost:8000/laptop_form', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
      .then(response => {
        if (!response.ok) throw new Error('Ошибка сервера');
        return response.json();
      })
      .then(data => {
        console.log('Успех:', data);
        alert('Данные отправлены!');
        // TODO: здесь можно перенаправить на страницу истории
      })
      .catch(error => {
        console.error('Ошибка:', error);
        alert('Не удалось отправить данные');
      });
  };
  return (
    <>
      <div className="form-card">
        <h2 className="main-title">
          Введите характеристки для генерации описания Ноутбука
        </h2>

        <div className="row">
          <div className="col">
            <div className="mb-3">
              <label className="form-label">Бренд</label>
              <input
                id="laptopBrand"
                className="form-control"
                placeholder="Apple, Samsung"
                ref={laptopBrandRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Модель</label>
              <input
                id="laptopModel"
                className="form-control"
                placeholder="Mac Air, Pro"
                ref={laptopModelRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Диагональ (дюймы)</label>
              <input
                id="laptopScreen_size"
                className="form-control"
                placeholder="15.6"
                type="number"
                step="0.1"
                ref={laptopDiagonalRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Тип матрицы</label>
              <input
                id="laptopDisplay_type"
                className="form-control"
                placeholder="OLED"
                ref={laptopMatrixRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Частота обновления (Гц)</label>
              <input
                id="laptopScreen_refresh"
                className="form-control"
                placeholder="240"
                type="number"
                ref={laptopFrequencyRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Разрешение экрана</label>
              <input
                id="laptopScreen_resolution"
                className="form-control"
                placeholder="Full HD, 4K"
                ref={laptopResolutionRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Материал корпуса</label>
              <input
                id="laptopMaterial"
                className="form-control"
                placeholder="Алюминий"
                ref={laptopMaterialRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Вес (Кг)</label>
              <input
                id="laptopWeight"
                className="form-control"
                placeholder="1"
                type="number"
                ref={laptopWeightRef}
              />
            </div>
          </div>

          <div className="col">
            <div className="mb-3">
              <label className="form-label">Процессор CPU</label>
              <input
                id="laptopProcessor"
                className="form-control"
                placeholder="AMD Ryzen (3/5/7/9)"
                ref={laptopProcessorRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Оперативная память RAM (Гб)</label>
              <input
                id="laptopRAM"
                className="form-control"
                placeholder="16"
                type="number"
                ref={laptopRAMRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Накопитель SSD (Гб)</label>
              <input
                id="laptopSSD"
                className="form-control"
                placeholder="256"
                type="number"
                ref={laptopSSDRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Видеокарта</label>
              <input
                id="laptopGraphics_card"
                className="form-control"
                placeholder="NVIDIA GeForce RTX 3050/4060/4090"
                ref={laptopGraphicsCardRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Видеопамять VRAM (Гб)</label>
              <input
                id="laptopVRAM"
                className="form-control"
                placeholder="8"
                type="number"
                ref={laptopVRAMRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Ёмкость батареи (Вт/ч)</label>
              <input
                id="laptopBattery"
                className="form-control"
                placeholder="72.4"
                type="number"
                step="0.1"
                ref={laptopBatteryRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Блок питания (Вт)</label>
              <input
                id="laptopPower_adapter"
                className="form-control"
                placeholder="230"
                type="number"
                ref={laptopPowerAdapterRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Предустановленная ОС</label>
              <input
                id="laptopOS"
                className="form-control"
                placeholder="Windows 11, macOS, Linux"
                ref={laptopOSRef}
              />
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col"></div>
          <div className="col">
            <div
              id="generateLaptopBtn"
              className="generate-btn"
              onClick={() => {
                btnLaptopGenerateClick();
                onBtnGenerateClick("history");
              }}
            >
              Сгенерировать
            </div>
          </div>
          <div className="col"></div>
        </div>
      </div>
    </>
  );
}

export default LaptopForm;

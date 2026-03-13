import { useRef } from "react";

function PhoneForm() {
  // Создаем ref для каждого input
  const phoneBrandRef = useRef(null);
  const phoneModelRef = useRef(null);
  const phoneScreenSizeRef = useRef(null);
  const phoneMatrixTypeRef = useRef(null);
  const phoneFrequencyRef = useRef(null);
  const phoneOSRef = useRef(null);
  const phoneCellularRef = useRef(null);
  const phoneProcessorRef = useRef(null);
  const phoneStorageRef = useRef(null);
  const phoneCameraRef = useRef(null);
  const phoneBatteryRef = useRef(null);
  const phoneChargingSpeedRef = useRef(null);
  const phoneMaterialRef = useRef(null);
  const phoneWeightRef = useRef(null);
  // --------------------------------------
  const btnPhoneGenerateClick = () => {
    const formData = {
      device: "phone",
      brand: phoneBrandRef.current?.value || "",
      model: phoneModelRef.current?.value || "",
      screenSize: phoneScreenSizeRef.current?.value || "",
      matrixType: phoneMatrixTypeRef.current?.value || "",
      frequency: phoneFrequencyRef.current?.value || "",
      os: phoneOSRef.current?.value || "",
      cellular: phoneCellularRef.current?.value || "",
      processor: phoneProcessorRef.current?.value || "",
      storage: phoneStorageRef.current?.value || "",
      camera: phoneCameraRef.current?.value || "",
      battery: phoneBatteryRef.current?.value || "",
      chargingSpeed: phoneChargingSpeedRef.current?.value || "",
      material: phoneMaterialRef.current?.value || "",
      weight: phoneWeightRef.current?.value || "",
    };
    console.log(formData);
    // TODO: connect to FastApi
    fetch('http://localhost:8000/phone_form', {
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
          Введите характеристки для генерации описания Телефона
        </h2>

        <div className="row">
          <div className="col">
            <div className="mb-3">
              <label className="form-label">Бренд</label>
              <input
                id="phoneBrand"
                className="form-control"
                placeholder="Apple, Samsung"
                ref={phoneBrandRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Модель</label>
              <input
                id="phoneModel"
                className="form-control"
                placeholder="Iphone Air, Pro"
                ref={phoneModelRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Диагональ (дюймы)</label>
              <input
                id="phoneScreen_size"
                className="form-control"
                placeholder="6.7"
                type="number"
                step="0.1"
                ref={phoneScreenSizeRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Тип матрицы</label>
              <input
                id="phoneDisplay_type"
                className="form-control"
                placeholder="AMOLED"
                ref={phoneMatrixTypeRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Частота обновления (Гц)</label>
              <input
                id="phoneScreen_refresh"
                className="form-control"
                placeholder="120"
                type="number"
                ref={phoneFrequencyRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Операционная система</label>
              <input
                id="phoneOS"
                className="form-control"
                placeholder="iOS 26"
                ref={phoneOSRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Сотовая связь</label>
              <input
                id="phoneCellular"
                className="form-control"
                placeholder="5G"
                ref={phoneCellularRef}
              />
            </div>
          </div>

          <div className="col">
            <div className="mb-3">
              <label className="form-label">Процессор</label>
              <input
                id="phoneProcessor"
                className="form-control"
                placeholder="A17 Bionic"
                ref={phoneProcessorRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Встроенная память (Гб)</label>
              <input
                id="phoneStorage"
                className="form-control"
                placeholder="512"
                type="number"
                ref={phoneStorageRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">
                Разрешение основной камеры (МП)
              </label>
              <input
                id="phoneCamera"
                className="form-control"
                placeholder="48"
                type="number"
                ref={phoneCameraRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Ёмкость батареи (мАч)</label>
              <input
                id="phoneBattery"
                className="form-control"
                placeholder="5000"
                type="number"
                ref={phoneBatteryRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">
                Скорость проводной зарядки (Вт)
              </label>
              <input
                id="phoneCharging_speed"
                className="form-control"
                placeholder="120"
                type="number"
                ref={phoneChargingSpeedRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Материал корпуса</label>
              <input
                id="phoneMaterial"
                className="form-control"
                placeholder="Титан"
                ref={phoneMaterialRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Вес (Гр)</label>
              <input
                id="phoneWeight"
                className="form-control"
                placeholder="210"
                type="number"
                ref={phoneWeightRef}
              />
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col"></div>
          <div className="col">
            <div
              id="generatePhoneBtn"
              className="generate-btn"
              onClick={btnPhoneGenerateClick}
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

export default PhoneForm;

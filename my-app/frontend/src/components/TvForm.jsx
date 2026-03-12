import { useRef } from "react";

function TvForm() {
  // Создаем ref для каждого input
  const tvBrandRef = useRef(null);
  const tvModelRef = useRef(null);
  const tvScreenSizeRef = useRef(null);
  const tvMatrixTypeRef = useRef(null);
  const tvFrequencyRef = useRef(null);
  const tvResolutionRef = useRef(null);
  const tvProcessorRef = useRef(null);
  const tvAudioPowerRef = useRef(null);
  const tvNumberOfSpeakersRef = useRef(null);
  const tvHDMICountRef = useRef(null);
  const tvHDMIVersionRef = useRef(null);
  const tvInstallationMethodRef = useRef(null);
  const tvMaterialRef = useRef(null);
  const tvWeightRef = useRef(null);
  // --------------------------------------
  const btnTvGenerateClick = () => {
    const formData = {
      device: "tv",
      brand: tvBrandRef.current?.value || "",
      model: tvModelRef.current?.value || "",
      screenSize: tvScreenSizeRef.current?.value || "",
      matrixType: tvMatrixTypeRef.current?.value || "",
      frequency: tvFrequencyRef.current?.value || "",
      resolution: tvResolutionRef.current?.value || "",
      processor: tvProcessorRef.current?.value || "",
      audioPower: tvAudioPowerRef.current?.value || "",
      numberOfSpeakers: tvNumberOfSpeakersRef.current?.value || "",
      hdmiCount: tvHDMICountRef.current?.value || "",
      hdmiVersion: tvHDMIVersionRef.current?.value || "",
      installationMethod: tvInstallationMethodRef.current?.value || "",
      material: tvMaterialRef.current?.value || "",
      weight: tvWeightRef.current?.value || "",
    };
    console.log(formData);
    // TODO: connect to FastApi
  };
  return (
    <>
      <div className="form-card">
        <h2 className="main-title">
          Введите характеристки для генерации описания Телевизора
        </h2>

        <div className="row">
          <div className="col">
            <div className="mb-3">
              <label className="form-label">Бренд</label>
              <input
                id="tvBrand"
                className="form-control"
                placeholder="Apple, Samsung"
                ref={tvBrandRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Модель</label>
              <input
                id="tvModel"
                className="form-control"
                placeholder="TV Pro, Ultra"
                ref={tvModelRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Диагональ (дюймы)</label>
              <input
                id="tvScreen_size"
                className="form-control"
                placeholder="65"
                type="number"
                step="0.1"
                ref={tvScreenSizeRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Тип матрицы</label>
              <input
                id="tvDisplay_type"
                className="form-control"
                placeholder="QLED"
                ref={tvMatrixTypeRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Частота обновления (Гц)</label>
              <input
                id="tvScreen_refresh"
                className="form-control"
                placeholder="120"
                type="number"
                ref={tvFrequencyRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Разрешение экрана</label>
              <input
                id="tvScreen_resolution"
                className="form-control"
                placeholder="4K Ultra HD"
                ref={tvResolutionRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Процессор</label>
              <input
                id="tvProcessor"
                className="form-control"
                placeholder="Neo Quantum Processor"
                ref={tvProcessorRef}
              />
            </div>
          </div>

          <div className="col">
            <div className="mb-3">
              <label className="form-label">Мощность звука (Вт)</label>
              <input
                id="tvAudio_power"
                className="form-control"
                placeholder="60"
                type="number"
                ref={tvAudioPowerRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">
                Количество динамиков (Каналов)
              </label>
              <input
                id="tvSpeakers_channels"
                className="form-control"
                placeholder="4.2"
                type="number"
                step="0.1"
                ref={tvNumberOfSpeakersRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Количество портов HDMI (Шт)</label>
              <input
                id="tvHDMI_count"
                className="form-control"
                placeholder="4"
                type="number"
                ref={tvHDMICountRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Версия HDMI</label>
              <input
                id="tvHDMI_version"
                className="form-control"
                placeholder="4.1"
                type="number"
                step="0.1"
                ref={tvHDMIVersionRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Способ установки</label>
              <input
                id="tvInstallation"
                className="form-control"
                placeholder="Крепление на стену"
                ref={tvInstallationMethodRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Материал корпуса</label>
              <input
                id="tvMaterial"
                className="form-control"
                placeholder="Пластик"
                ref={tvMaterialRef}
              />
            </div>

            <div className="mb-3">
              <label className="form-label">Вес (Кг)</label>
              <input
                id="tvWeight"
                className="form-control"
                placeholder="3"
                type="number"
                ref={tvWeightRef}
              />
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col"></div>
          <div className="col">
            <div
              id="generateTvBtn"
              className="generate-btn"
              onClick={btnTvGenerateClick}
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
// Что бы можно было использовать этот компонент в других файлах
export default TvForm;

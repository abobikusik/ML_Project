async function btnGoToMainPage(){
    window.location.href = "/";
};
async function btnGoToPhoneFormClick(){
    window.location.href = "/phone_form";
};
async function btnGoToLaptopFormClick(){
    window.location.href = "/laptop_form";
};
async function btnGoToTvFormClick(){
    window.location.href = "/tv_form";
};

//Функция отправки данных О ТЕЛЕФОНЕ на сервер 
async function postPhoneForm(phoneBrand, phoneModel, phoneScreen_size,
    phoneDisplay_type, phoneScreen_refresh, phoneOS, phoneCellular,
    phoneProcessor, phoneStorage, phoneCamera, phoneBattery,
    phoneCharging_speed, phoneMaterial, phoneWeight) {

    const response = await fetch("phone_form", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({ //Формирование словаря, который будет оправлен на сервер 
            brand: phoneBrand,
            model: phoneModel,
            screen_size: phoneScreen_size,
            display_type: phoneDisplay_type,
            screen_refresh: phoneScreen_refresh,
            OS: phoneOS,
            cellular: phoneCellular,
            processor: phoneProcessor,
            storage: phoneStorage,
            camera: phoneCamera,
            battery: phoneBattery,
            charging_speed: phoneCharging_speed,
            material: phoneMaterial,
            weight: phoneWeight
        })
    });
    if (response.ok === true) {
        console.log("generating...");
    }
    else {
        const error = await response.json();
        console.log(error.message);
    }
}
//Запуск процесса отправки ДАННЫХ О ТЕЛЕФОНЕ при нажатии на кнопку
async function btnPhoneGenerateClick() {
    //При нажании на кнопку, происходит сбор данных с формы на странице
    const brand = document.getElementById("phoneBrand").value;
    const model = document.getElementById("phoneModel").value;
    const screen_size = document.getElementById("phoneScreen_size").value;
    const display_type = document.getElementById("phoneDisplay_type").value;
    const screen_refresh = document.getElementById("phoneScreen_refresh").value;
    const OS = document.getElementById("phoneOS").value;
    const cellular = document.getElementById("phoneCellular").value;
    const processor = document.getElementById("phoneProcessor").value;
    const storage = document.getElementById("phoneStorage").value;
    const camera = document.getElementById("phoneCamera").value;
    const battery = document.getElementById("phoneBattery").value;
    const charging_speed = document.getElementById("phoneCharging_speed").value;
    const material = document.getElementById("phoneMaterial").value;
    const weight = document.getElementById("phoneWeight").value;

    //Эти данные передаются в функцию (postPhoneForm) для отправки данных на сервер
    postPhoneForm(brand, model, screen_size, display_type, screen_refresh, OS, cellular,
        processor, storage, camera, battery, charging_speed, material, weight);

};

//Функция отправки данных О НОУТБУКЕ на сервер 
async function postLaptopForm(laptopBrand, laptopModel, laptopScreen_size,
    laptopDisplay_type, laptopScreen_refresh, laptopScreen_resolution, laptopMaterial,
    laptopWeight, laptopProcessor, laptopRAM, laptopSSD,
    laptopGraphics_card, laptopVRAM, laptopBattery, laptopPower_adapter, laptopOS) {

    const response = await fetch("laptop_form", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({ //Формирование словаря, который будет оправлен на сервер 
            brand: laptopBrand,
            model: laptopModel,
            screen_size: laptopScreen_size,
            display_type: laptopDisplay_type,
            screen_refresh: laptopScreen_refresh,
            screen_resolution: laptopScreen_resolution,
            material: laptopMaterial,
            weight: laptopWeight,
            processor: laptopProcessor,
            RAM: laptopRAM,
            SSD: laptopSSD,
            graphics_card: laptopGraphics_card,
            VRAM: laptopVRAM,
            battery: laptopBattery,
            power_adapter: laptopPower_adapter,
            OS: laptopOS,

        })
    });
    if (response.ok === true) {
        console.log("generating...");
    }
    else {
        const error = await response.json();
        console.log("error.message");
    }
}
//Запуск процесса отправки ДАННЫХ О НОУТБУКЕ при нажатии на кнопку
async function btnLaptopGenerateClick() {
    //При нажании на кнопку, происходит сбор данных с формы на странице
    const brand = document.getElementById("laptopBrand").value;
    const model = document.getElementById("laptopModel").value;
    const screen_size = document.getElementById("laptopScreen_size").value;
    const display_type = document.getElementById("laptopDisplay_type").value;
    const screen_refresh = document.getElementById("laptopScreen_refresh").value;
    const screen_resolution = document.getElementById("laptopScreen_resolution").value;
    const material = document.getElementById("laptopMaterial").value;
    const weight = document.getElementById("laptopWeight").value;
    const processor = document.getElementById("laptopProcessor").value;
    const RAM = document.getElementById("laptopRAM").value;
    const SSD = document.getElementById("laptopSSD").value;
    const graphics_card = document.getElementById("laptopGraphics_card").value;
    const VRAM = document.getElementById("laptopVRAM").value;
    const battery = document.getElementById("laptopBattery").value;
    const power_adapter = document.getElementById("laptopPower_adapter").value;
    const OS = document.getElementById("laptopOS").value;

    //Эти данные передаются в функцию (postLaptopForm) для отправки данных на сервер
    postLaptopForm(brand, model, screen_size, display_type, screen_refresh, screen_resolution,
        material, weight, processor, RAM, SSD, graphics_card, VRAM, battery, power_adapter, OS);
};

//Функция отправки данных О ТЕЛЕВИЗОРЕ на сервер 
async function postTvForm(tvBrand, tvModel, tvScreen_size, tvDisplay_type, tvScreen_refresh, tvScreen_resolution, tvProcessor,
    tvAudio_power, tvSpeakers_channels, tvHDMI_count, tvHDMI_version, tvInstallation, tvMaterial, tvWeight) {

    const response = await fetch("tv_form", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({ //Формирование словаря, который будет оправлен на сервер 
            brand: tvBrand,
            model: tvModel,
            screen_size: tvScreen_size,
            display_type: tvDisplay_type,
            screen_refresh: tvScreen_refresh,
            screen_resolution: tvScreen_resolution,
            processor: tvProcessor,
            audio_power: tvAudio_power,
            speakers_channels: tvSpeakers_channels,
            HDMI_count: tvHDMI_count,
            HDMI_version: tvHDMI_version,
            installation: tvInstallation,
            material: tvMaterial,
            weight: tvWeight,
        })
    });
    if (response.ok === true) {
        console.log("generating...");
    }
    else {
        const error = await response.json();
        console.log(error.message);
    }
}
async function btnTvGenerateClick() {
    //При нажании на кнопку, происходит сбор данных с формы на странице
    const brand = document.getElementById("tvBrand").value;
    const model = document.getElementById("tvModel").value;
    const screen_size = document.getElementById("tvScreen_size").value;
    const display_type = document.getElementById("tvDisplay_type").value;
    const screen_refresh = document.getElementById("tvScreen_refresh").value;
    const screen_resolution = document.getElementById("tvScreen_resolution").value;
    const processor = document.getElementById("tvProcessor").value;
    const audio_power = document.getElementById("tvAudio_power").value;
    const speakers_channels = document.getElementById("tvSpeakers_channels").value;
    const HDMI_count = document.getElementById("tvHDMI_count").value;
    const HDMI_version = document.getElementById("tvHDMI_version").value;
    const installation = document.getElementById("tvInstallation").value;
    const material = document.getElementById("tvMaterial").value;
    const weight = document.getElementById("tvWeight").value;

    //Эти данные передаются в функцию (postTvForm) для отправки данных на сервер
    postTvForm(brand, model, screen_size, display_type, screen_refresh, screen_resolution, processor,
        audio_power, speakers_channels, HDMI_count, HDMI_version, installation, material, weight);
};
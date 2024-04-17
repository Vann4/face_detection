const container_popup_feedback = document.querySelector("#container_popup_feedback");

document.getElementById("close_button_popup_feedback").addEventListener("click", function() {
    container_popup_feedback.classList.remove("container_popup_feedback");
    container_popup_feedback.classList.add("display_none_container_popup_feedback");
});

const popup_feedback = document.querySelector("#popup_feedback");

if (popup_feedback) {
    popup_feedback.addEventListener("click", function() {
        document.getElementById("container_popup_feedback").classList.remove("display_none_container_popup_feedback");
        document.getElementById("container_popup_feedback").classList.add("container_popup_feedback");
    });
} else {
}

window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("container_popup_feedback").classList.remove("container_popup_feedback");
        document.getElementById("container_popup_feedback").classList.add("display_none_container_popup_feedback");
    }
});


const hamb = document.querySelector("#hamb");
const popup = document.querySelector("#popup");
const body = document.body;

// Клонируем меню, чтобы задать свои стили для мобильной версии
const menu = document.querySelector("#menu").cloneNode(1);
const auth = document.querySelector(".auth").cloneNode(1);

// При клике на иконку hamb вызываем ф-ию hambHandler
hamb.addEventListener("click", hambHandler);

// Выполняем действия при клике
function hambHandler(e) {
    e.preventDefault();
    // Переключаем стили элементов при клике
    popup.classList.toggle("open");
    hamb.classList.toggle("active");
    body.classList.toggle("noscroll");
    renderPopup();
}

// Здесь мы рендерим элементы в наш попап
function renderPopup() {
    popup.appendChild(menu);
    popup.appendChild(auth);
    buttons = document.querySelectorAll("#popup_feedback")
    buttons.forEach(function(button) {
    button.addEventListener('click', function() {
        document.getElementById("container_popup_feedback").classList.remove("display_none_container_popup_feedback");
        document.getElementById("container_popup_feedback").classList.add("container_popup_feedback");
        });
    });
}

// Код для закрытия меню при нажатии на ссылку
const links = Array.from(menu.children);

// Для каждого элемента меню при клике вызываем ф-ию
links.forEach((link) => {
    link.addEventListener("click", closeOnClick);
});

// Закрытие попапа при клике на меню
function closeOnClick() {
    popup.classList.remove("open");
    hamb.classList.remove("active");
    body.classList.remove("noscroll");
}

//Работа с камерой
const video_stream = document.querySelector("#video_stream");
const turn_on_camera = document.querySelector("#turn_on_camera");
const turn_off_the_camera = document.querySelector("#turn_off_the_camera");
const errorMessage = document.querySelector("#error_message");

// Открытие блока для распознавание лиц в прямом эфире
const form_delete_photo = document.getElementById("form_delete_photo");
// Получаем доступ к элементу input с именем "id"
let idInput = form_delete_photo.querySelector("input[name='id']");
// Получаем значение атрибута "value"
let idValue = idInput.value;

// Проверка, есть ли доступ к камере
async function checkCameraAvailability() {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const videoInputDevices = devices.filter(device => device.kind === 'videoinput');
    return videoInputDevices.length > 0;
  } catch (err) {
//    console.error('Ошибка при проверке доступности камеры:', err);
    return false;
  }
}

turn_on_camera.addEventListener("click", function() {
    video_stream.classList.remove("display_none");

    turn_on_camera.classList.add("display_none");
    turn_off_the_camera.classList.remove("display_none");
    let url = "/live_feed/" + idValue;
    video_stream.src = url;

    // вывод ошибки если камера не найдена
    checkCameraAvailability().then(isCameraAvailable => {
      if (isCameraAvailable) {
    //    console.log('Камера доступна');
      } else {
        errorMessage.style.display = 'block';
      }
    });
});

turn_off_the_camera.addEventListener("click", function() {
    video_stream.style.display = 'none';
    errorMessage.style.display = 'none';
    turn_on_camera.classList.remove("display_none");
    turn_off_the_camera.classList.add("display_none");
    video_stream.src = "";
});

//Формы для изменения данных распознанных лиц
const show_form_buttons = document.querySelectorAll(".button_edit_data_photo"); //Кнопка открытия формы

show_form_buttons.forEach(function(button) { //Открытие форм
    button.addEventListener("click", function() {
        let formId = this.getAttribute("data-form-id");
        let form_edit_popup_photo = document.querySelector("#edit_popup_photo" + formId);
        form_edit_popup_photo.classList.remove("display_none");
        form_edit_popup_photo.classList.add("edit_popup_photo");
    });
});

const closing_form_buttons = document.querySelectorAll(".close_button_popup_edit_data_photo"); //Кнопка закрытия формы

closing_form_buttons.forEach(function(button) { //Закрытие форм
    button.addEventListener("click", function() {
        let formId = this.getAttribute("id");
        let form_edit_popup_photo = document.querySelector("#edit_popup_photo" + formId);
        form_edit_popup_photo.classList.remove("edit_popup_photo");
        form_edit_popup_photo.classList.add("display_none");
    });
});

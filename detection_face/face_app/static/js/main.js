const container_popup_feedback = document.querySelector("#container_popup_feedback");

document.getElementById("close-button").addEventListener("click", function() {
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

// Выполняем действия при клике ..
function hambHandler(e) {
    e.preventDefault();
    // Переключаем стили элементов при кликеo
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

turn_on_camera.addEventListener("click", function() {
    video_stream.classList.toggle("display_none");
});
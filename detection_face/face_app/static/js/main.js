document.getElementById("close-button").addEventListener("click", function() {
  document.getElementById("popup_feedback_class").style.display = "none";
});

document.getElementById("popup_feedback").addEventListener("click", function() {
  document.getElementById("popup_feedback_class").style.display = "block";
});

window.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
        document.getElementById("popup_feedback_class").style.display = "none";
    }
});

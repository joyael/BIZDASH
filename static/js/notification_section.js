

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("notification-btn");
    const panel = document.getElementById("notification-panel");
    const close = document.getElementById("close-panel");

    btn.addEventListener("click", () => {
        panel.classList.toggle("open");
    });

    close.addEventListener("click", () => {
        panel.classList.remove("open");
    });
});
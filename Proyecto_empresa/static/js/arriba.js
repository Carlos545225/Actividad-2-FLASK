 // Mostrar el botón cuando se baja la página
 window.onscroll = function () {
    let btn = document.getElementById("btnTop");
    if (document.documentElement.scrollTop > 200) {
        btn.style.display = "block";
    } else {
        btn.style.display = "none";
    }
};

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}
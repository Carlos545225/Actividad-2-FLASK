// Script para calcular el IMC automáticamente
document.addEventListener("DOMContentLoaded", function() {
    const pesoInput = document.getElementById("peso");
    const alturaInput = document.getElementById("altura");
    const imcInput = document.getElementById("imc");

    function calculateIMC() {
        const peso = parseFloat(pesoInput.value);
        const altura = parseFloat(alturaInput.value) / 100; // Convertir cm a metros

        if (!isNaN(peso) && !isNaN(altura) && altura > 0) {
            const imc = peso / (altura * altura);
            imcInput.value = imc.toFixed(2); // Mostrar el IMC con 2 decimales
        } else {
            imcInput.value = ""; // Limpiar el campo IMC si los valores son inválidos
        }
    }

    pesoInput.addEventListener("input", calculateIMC);
    alturaInput.addEventListener("input", calculateIMC);
});

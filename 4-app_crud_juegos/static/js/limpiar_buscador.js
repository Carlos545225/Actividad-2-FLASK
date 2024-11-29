document.addEventListener('DOMContentLoaded', function() {
    const buscarInput = document.getElementById('buscarJuego');
    const tabla = document.getElementById('tablaJuegos');
    const filas = tabla.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

    buscarInput.addEventListener('input', function() {
        const termino = this.value.toLowerCase().trim();
        
        // Mostrar todas las filas si no hay texto en el input
        if (termino === '') {
            for (let fila of filas) {
                fila.style.display = '';
            }
            return;
        }

        for (let fila of filas) {
            const nombre = fila.getElementsByTagName('td')[0].textContent.toLowerCase();
            
            if (nombre.includes(termino)) {
                fila.style.display = '';
            } else {
                fila.style.display = 'none';
            }
        }
    });
});
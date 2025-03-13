// Función para confirmar cierre de sesión
function confirmarCerrarSesion(event) {
    event.preventDefault();
    Swal.fire({
        title: '¿Cerrar sesión?',
        text: "¿Estás seguro que deseas cerrar la sesión?",
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = "/logout";
        }
    });
}

function confirmarAccion(event, mensaje, url) {
    event.preventDefault(); // Evita que el enlace se siga por defecto
    Swal.fire({
        title: 'Confirmación',
        text: mensaje,
        icon: 'warning', // Cambiado a warning porque es una eliminación
        showCancelButton: true,
        confirmButtonColor: '#d33', // Rojo para eliminar
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url; // Redirige si se confirma
        }
    });
}

// Validación de formularios Bootstrap
(function () {
    'use strict'
    var forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })
})();

// Inicialización de toasts
document.addEventListener('DOMContentLoaded', function() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 10000
        });
    });
    
    // Mostrar todos los toasts
    toastList.forEach(toast => toast.show());
}); 

function confirmarPago() {
    Swal.fire({
      title: '¿Confirmar pago?',
      text: '¿Está seguro que desea proceder con el pago?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#ffc107',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Sí, pagar',
      cancelButtonText: 'Cancelar'
    }).then((result) => {
      if (result.isConfirmed) {
        document.getElementById('formPago').submit();
      }
    });
  }
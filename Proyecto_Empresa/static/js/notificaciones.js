console.log('Cargando script de notificaciones...');

// Función para actualizar el reloj en tiempo real
function actualizarReloj() {
    const ahora = new Date();
    const hora = ahora.getHours().toString().padStart(2, '0');
    const minutos = ahora.getMinutes().toString().padStart(2, '0');
    const segundos = ahora.getSeconds().toString().padStart(2, '0');
    const relojElement = document.getElementById('reloj');
    if (relojElement) {
        relojElement.textContent = `${hora}:${minutos}:${segundos}`;
    } else {
        console.error('Elemento reloj no encontrado');
    }
}

// Función para marcar una notificación como leída
async function marcarNotificacionLeida(notificacionId) {
    try {
        console.log('Marcando notificación como leída:', notificacionId);
        const response = await fetch(`/marcar_notificacion_leida/${notificacionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await response.json();
        console.log('Respuesta del servidor:', data);
        if (data.success) {
            obtenerNotificaciones(); // Actualizar la lista de notificaciones
        }
    } catch (error) {
        console.error('Error al marcar la notificación como leída:', error);
    }
}

// Función para obtener notificaciones del servidor
async function obtenerNotificaciones() {
    try {
        console.log('Obteniendo notificaciones...');
        const response = await fetch('/obtener_notificaciones');
        const data = await response.json();
        console.log('Notificaciones recibidas:', data);
        
        const contenedorNotificaciones = document.getElementById('notificaciones-dropdown');
        if (!contenedorNotificaciones) {
            console.error('No se encontró el contenedor de notificaciones');
            return;
        }

        const headerHTML = `
            <h6 class="dropdown-header bg-primary text-white">
                Centro de Notificaciones
            </h6>
        `;
        
        let notificacionesHTML = '';
        
        if (data.notificaciones.length === 0) {
            notificacionesHTML = '<p class="dropdown-item text-muted m-0">No hay notificaciones nuevas</p>';
        } else {
            data.notificaciones.forEach(notificacion => {
                notificacionesHTML += `
                    <a href="#" class="dropdown-item d-flex align-items-center ${notificacion.leida ? 'text-muted' : ''}" 
                       onclick="marcarNotificacionLeida(${notificacion.id}); return false;">
                        <div class="me-3">
                            <div class="icon-circle bg-${notificacion.tipo}">
                                <i class="bi bi-${notificacion.tipo === 'primary' ? 'info-circle' : 
                                                notificacion.tipo === 'success' ? 'check-circle' : 
                                                notificacion.tipo === 'warning' ? 'exclamation-circle' : 
                                                'bell'} text-white"></i>
                            </div>
                        </div>
                        <div>
                            <div class="small text-gray-500">${notificacion.fecha}</div>
                            <span>${notificacion.mensaje}</span>
                        </div>
                    </a>
                `;
            });
        }
        
        contenedorNotificaciones.innerHTML = headerHTML + notificacionesHTML;
        
        // Actualizar contador de notificaciones
        const contadorElemento = document.getElementById('contador-notificaciones');
        if (!contadorElemento) {
            console.error('No se encontró el elemento contador de notificaciones');
            return;
        }

        const noLeidas = data.notificaciones.filter(n => !n.leida).length;
        console.log('Notificaciones no leídas:', noLeidas);
        
        if (noLeidas > 0) {
            contadorElemento.textContent = noLeidas;
            contadorElemento.style.display = 'inline';
        } else {
            contadorElemento.style.display = 'none';
        }
    } catch (error) {
        console.error('Error al obtener notificaciones:', error);
    }
}

// Inicializar el reloj y las notificaciones
document.addEventListener('DOMContentLoaded', () => {
    console.log('Inicializando sistema de notificaciones...');
    
    // Iniciar el reloj
    actualizarReloj();
    setInterval(actualizarReloj, 1000);

    // Iniciar las notificaciones
    obtenerNotificaciones();
    setInterval(obtenerNotificaciones, 30000); // Actualizar cada 30 segundos
}); 
// static/js/calendario.js
document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
  
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth', // Vista inicial (mes, semana, día)
      locale: 'es', // Idioma (opcional)
      headerToolbar: { // Configuración de la barra de herramientas
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },
      events: [ // Lista de eventos (citas)
        {
          title: 'Cita con Juan',
          start: '2024-05-05T10:00:00',
          end: '2024-05-05T11:00:00',
          description: 'Consulta general'
        },
        {
          title: 'Cita con Maria',
          start: '2024-05-07T14:00:00',
          end: '2024-05-07T15:00:00',
          description: 'Control'
        }
        // ... más citas
      ],
      eventClick: function(info) { // Función que se ejecuta al hacer clic en un evento
        alert('Evento: ' + info.event.title + '\nDescripción: ' + info.event.extendedProps.description);
        // Puedes agregar aquí lógica para mostrar un modal con los detalles de la cita
      }
    });
  
    calendar.render(); // Renderiza el calendario
  });
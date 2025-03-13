// Variable global para rastrear la sección actual (médicos, pacientes, facturas, citas)
var currentSection = 'facturas'; // Valor por defecto: asume facturas al cargar la página

$(document).ready(function() {
    // Inicializar DataTable para las tablas
    if (!$.fn.DataTable.isDataTable('#tablaMedicos')) {
        $('#tablaMedicos').DataTable({
            paging: true,
            ordering: false,
            info: false,
            searching: false,
            language: {
                paginate: {
                    previous: "Anterior",
                    next: "Siguiente"
                }
            },
            pageLength: 8,
            lengthChange: false
        });
    }

    if (!$.fn.DataTable.isDataTable('#tablaPacientes')) {
        $('#tablaPacientes').DataTable({
            paging: true,
            ordering: false,
            info: false,
            searching: false,
            language: {
                paginate: {
                    previous: "Anterior",
                    next: "Siguiente"
                }
            },
            pageLength: 8,
            lengthChange: false
        });
    }

    if (!$.fn.DataTable.isDataTable('#tablaCitas')) {
        $('#tablaCitas').DataTable({
            paging: true,
            ordering: false,
            info: false,
            searching: false,
            language: {
                paginate: {
                    previous: "Anterior",
                    next: "Siguiente"
                }
            },
            pageLength: 8,
            lengthChange: false
        });
    }

    if (!$.fn.DataTable.isDataTable('#tablaFactura')) {
        $('#tablaFactura').DataTable({
            paging: true,
            ordering: false,
            info: false,
            searching: false,
            language: {
                paginate: {
                    previous: "Anterior",
                    next: "Siguiente"
                }
            },
            pageLength: 8,
            lengthChange: false
        });
    }

    if (!$.fn.DataTable.isDataTable('#tablaTratamientos')) {
        $('#tablaTratamientos').DataTable({
            paging: true,
            ordering: false,
            info: false,
            searching: false,
            language: {
                paginate: {
                    previous: "Anterior",
                    next: "Siguiente"
                }
            },
            pageLength: 8,
            lengthChange: false
        });
    }

    if (!$.fn.DataTable.isDataTable('#tablaHistoria')) {
        $('#tablaHistoria').DataTable({
            paging: true,
            ordering: false,
            info: false,
            searching: false,
            language: {
                paginate: {
                    previous: "Anterior",
                    next: "Siguiente"
                }
            },
            pageLength: 8,
            lengthChange: false
        });
    }

    // Detectar la sección actual al cargar la página
    if ($('#tablaMedicos').length > 0) {
        currentSection = 'medicos';
    } else if ($('#tablaPacientes').length > 0) {
        currentSection = 'pacientes';
    } else if ($('#tablaCitas').length > 0) {
        currentSection = 'citas';
    } else if ($('#tablaFactura').length > 0) {
        currentSection = 'facturas';
    } else if ($('#tablaTratamientos').length > 0) {
        currentSection = 'tratamientos';
    } else if ($('#tablaHistoria').length > 0) {
        currentSection = 'historia';
    } else {
        currentSection = 'facturas'; // Asumimos facturas por defecto
    }

    // Buscador
    $('#searchInput').on('keyup', function() {
        var searchText = $(this).val().toLowerCase();

        if (currentSection === 'medicos') {
            // Búsqueda en tabla médicos por número de documento
            $('#tablaMedicos tbody tr').each(function() {
                var documentNumber = $(this).find('td:eq(4)').text().toLowerCase();
                $(this).toggle(documentNumber.includes(searchText));
            });
        } else if (currentSection === 'pacientes') {
            // Búsqueda en tabla pacientes por número de documento
            $('#tablaPacientes tbody tr').each(function() {
                var documentNumber = $(this).find('td:eq(4)').text().toLowerCase();
                $(this).toggle(documentNumber.includes(searchText));
            });
        } else if (currentSection === 'citas') {
            // Búsqueda en tabla citas por nombre de paciente
            $('#tablaCitas tbody tr').each(function() {
                var nombrePaciente = $(this).find('td:eq(1)').text().toLowerCase(); // Segunda columna (índice 1)
                $(this).toggle(nombrePaciente.includes(searchText));
            });
        } else if (currentSection === 'facturas') {
            // Búsqueda en tabla facturas por nombre de paciente
            $('#tablaFactura tbody tr').each(function() {
                var nombrePaciente = $(this).find('td:eq(2)').text().toLowerCase(); // Tercera columna (índice 2)
                $(this).toggle(nombrePaciente.includes(searchText));
            });
        } else if (currentSection === 'tratamientos') {
            // Búsqueda en tabla tratamientos por nombre de paciente
            $('#tablaTratamientos tbody tr').each(function() {
                var nombrePaciente = $(this).find('td:eq(1)').text().toLowerCase(); // Segunda columna (índice 1)
                $(this).toggle(nombrePaciente.includes(searchText));
            });
        } else if (currentSection === 'historia') {
            // Búsqueda en tabla historia por nombre del médico
            $('#tablaHistoria tbody tr').each(function() {
                var nombreMedico = $(this).find('td:eq(2)').text().toLowerCase(); // Columna del médico
                $(this).toggle(nombreMedico.includes(searchText));
            });
        }
    });

    // Actualizar el placeholder del campo de búsqueda según la página
    if ($('#tablaMedicos').length > 0) {
        $('#searchInput').attr('placeholder', 'Buscar por número de documento...');
    } else if ($('#tablaPacientes').length > 0) {
        $('#searchInput').attr('placeholder', 'Buscar por número de documento...');
    } else if ($('#tablaCitas').length > 0) {
        $('#searchInput').attr('placeholder', 'Buscar por nombre de paciente...');
    } else if ($('#tablaFactura').length > 0) {
        $('#searchInput').attr('placeholder', 'Buscar por nombre de paciente...');
    } else if ($('#tablaTratamientos').length > 0) {
        $('#searchInput').attr('placeholder', 'Buscar por nombre de paciente...');
    } else if ($('#tablaHistoria').length > 0) {
        $('#searchInput').attr('placeholder', 'Buscar por nombre del médico...');
    }
});
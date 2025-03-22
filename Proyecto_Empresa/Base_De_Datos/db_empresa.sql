-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 22-03-2025 a las 00:53:48
-- Versión del servidor: 8.0.30
-- Versión de PHP: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `db_empresa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administradores`
--

CREATE TABLE `administradores` (
  `id` int NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` enum('Medico','Administrador','Paciente') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `administradores`
--

INSERT INTO `administradores` (`id`, `nombre`, `apellido`, `email`, `telefono`, `contraseña`, `rol`) VALUES
(1, 'Carlos', 'Admin', 'admin@gmail.com', '123-456-7890', 'admin123', 'Administrador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id` int NOT NULL,
  `paciente_id` int NOT NULL,
  `medico_id` int NOT NULL,
  `servicio` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `estado` enum('pendiente','confirmada','en_progreso','finalizada','cancelada') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `citas`
--

INSERT INTO `citas` (`id`, `paciente_id`, `medico_id`, `servicio`, `fecha`, `hora_inicio`, `hora_fin`, `motivo`, `estado`) VALUES
(6, 2, 1, 'Pediatría', '2025-03-20', '10:01:00', '11:01:00', 'Medicina General', 'finalizada'),
(7, 2, 1, 'Medicina General', '2025-03-20', '20:32:00', '22:31:00', 'Medicina General ', 'finalizada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `id` int NOT NULL,
  `numero_factura` varchar(50) NOT NULL,
  `id_cita` int NOT NULL,
  `fecha` date NOT NULL,
  `total` float NOT NULL,
  `tipo_pago` enum('Efectivo','Tarjeta','Transferencia') NOT NULL,
  `estado` enum('pendiente','pagada','cancelada') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `facturas`
--

INSERT INTO `facturas` (`id`, `numero_factura`, `id_cita`, `fecha`, `total`, `tipo_pago`, `estado`) VALUES
(5, 'F001', 6, '2025-03-20', 9000, 'Tarjeta', 'pagada'),
(6, 'F002', 7, '2025-03-20', 10000, 'Tarjeta', 'pagada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medicos`
--

CREATE TABLE `medicos` (
  `id` int NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `tipo_documento` enum('CC','CE') NOT NULL,
  `numero_documento` varchar(20) NOT NULL,
  `genero` enum('Masculino','Femenino','Otro') NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `especialidad` varchar(100) NOT NULL,
  `numero_registro` varchar(50) NOT NULL,
  `anios_experiencia` int NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` enum('Medico','Administrador','Paciente') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `medicos`
--

INSERT INTO `medicos` (`id`, `nombre`, `apellido`, `tipo_documento`, `numero_documento`, `genero`, `email`, `telefono`, `direccion`, `especialidad`, `numero_registro`, `anios_experiencia`, `contraseña`, `rol`) VALUES
(1, 'Carlos Eduardo', 'Correa Baloco', 'CC', '1102148630', 'Masculino', 'carlos@gmail.com', '3244016591', 'CR 7A CL 23D-78', 'endocrinologia', 'F3H452165455', 9, '123', 'Medico'),
(31, 'Valeria Ines', 'Perez Hernandez', 'CC', '5467890123', 'Femenino', 'valeria.perez@clinic.com', '3233334488', 'Calle 90 # 80-82', 'Genética Médica', 'D7D567890', 6, 'ValeGene6', 'Medico'),
(32, 'Juan Carlos', 'Rodriguez Lopez', 'CC', '1234567890', 'Masculino', 'juan.rodriguez@clinic.com', '3101234567', 'Carrera 15 # 45-67', 'Medicina General', 'M1234567', 10, 'JuanMed10', 'Medico'),
(33, 'Maria Fernanda', 'Gonzalez Diaz', 'CC', '9876543210', 'Femenino', 'maria.gonzalez@clinic.com', '3119876543', 'Avenida 68 # 78-90', 'Pediatría', 'P9876543', 5, 'MariaPed5', 'Medico'),
(34, 'Pedro Jose', 'Ruiz Martinez', 'CC', '4567890123', 'Masculino', 'pedro.ruiz@clinic.com', '3124567890', 'Calle 26 # 13-57', 'Ortopedia', 'O4567890', 12, 'PedroOrt12', 'Medico'),
(35, 'Laura Sofia', 'Ramirez Vargas', 'CC', '6543210987', 'Femenino', 'laura.ramirez@clinic.com', '3136543210', 'Diagonal 80 # 20-15', 'Cardiología', 'C6543210', 8, 'LauraCar8', 'Medico'),
(36, 'Andres Felipe', 'Torres Jimenez', 'CC', '7890123456', 'Masculino', 'andres.torres@clinic.com', '3147890123', 'Transversal 39 # 52-40', 'Dermatología', 'D7890123', 3, 'AndresDer3', 'Medico'),
(37, 'Sara Isabel', 'Castro Perez', 'CC', '3210987654', 'Femenino', 'sara.castro@clinic.com', '3153210987', 'Circunvalar # 1-23', 'Ginecología', 'G3210987', 7, 'SaraGin7', 'Medico'),
(38, 'Diego Armando', 'Soto Hernandez', 'CC', '8901234567', 'Masculino', 'diego.soto@clinic.com', '3168901234', 'Calle 100 # 10-10', 'Neurología', 'N8901234', 11, 'DiegoNeu11', 'Medico'),
(39, 'Valentina Sofia', 'Diaz Rodriguez', 'CC', '5678901234', 'Femenino', 'valentina.diaz@clinic.com', '3175678901', 'Carrera 7 # 77-77', 'Oftalmología', 'OF5678901', 4, 'ValentinaOft4', 'Medico'),
(40, 'Ricardo Andres', 'Gomez Sanchez', 'CC', '2345678901', 'Masculino', 'ricardo.gomez@clinic.com', '3182345678', 'Avenida 19 # 123-45', 'Psiquiatría', 'P2345678', 9, 'RicardoPsi9', 'Medico');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `notificaciones`
--

CREATE TABLE `notificaciones` (
  `id` int NOT NULL,
  `usuario_id` int NOT NULL,
  `mensaje` varchar(255) NOT NULL,
  `tipo` varchar(20) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `leida` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `notificaciones`
--

INSERT INTO `notificaciones` (`id`, `usuario_id`, `mensaje`, `tipo`, `fecha`, `leida`) VALUES
(1, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-11 14:38:39', 1),
(2, 1, 'Bienvenido/a Daniel Esteban! Has iniciado sesión como Paciente', 'success', '2025-03-11 14:42:46', 1),
(3, 1, 'Tu cita para Tomografía Computarizada ha sido solicitada para el 21/03/2025', 'success', '2025-03-11 14:43:28', 1),
(4, 38, 'Nueva cita solicitada para el 21/03/2025 - Tomografía Computarizada', 'primary', '2025-03-11 14:43:28', 0),
(5, 1, 'Pago procesado exitosamente para la factura F004', 'success', '2025-03-11 14:43:43', 1),
(6, 1, 'Bienvenido/a Dr(a). Carlos Eduardo! Has iniciado sesión como Médico', 'success', '2025-03-11 14:44:32', 1),
(7, 1, 'Tu cita del 19/03/2025 ha sido confirmada', 'warning', '2025-03-11 14:45:02', 1),
(8, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-11 14:56:14', 1),
(9, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-12 19:37:46', 1),
(10, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-12 19:50:44', 0),
(11, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-12 19:51:10', 1),
(12, 1, 'Bienvenido/a Dr(a). Carlos Eduardo! Has iniciado sesión como Médico', 'success', '2025-03-12 19:51:40', 1),
(13, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-12 19:52:26', 1),
(14, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-12 19:52:43', 0),
(15, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-12 19:53:03', 1),
(16, 1, 'Bienvenido/a Dr(a). Carlos Eduardo! Has iniciado sesión como Médico', 'success', '2025-03-12 19:58:58', 1),
(17, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-12 19:59:23', 0),
(18, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-12 20:00:11', 1),
(19, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-12 20:03:49', 0),
(20, 2, 'Pago procesado exitosamente para la factura F001', 'success', '2025-03-12 20:03:57', 0),
(21, 1, 'Bienvenido/a Dr(a). Carlos Eduardo! Has iniciado sesión como Médico', 'success', '2025-03-12 20:26:27', 1),
(22, 2, 'Tu cita del 20/03/2025 ha sido confirmada', 'warning', '2025-03-12 20:26:38', 0),
(23, 2, 'Tu cita del 20/03/2025 ha sido finalizada', 'warning', '2025-03-12 20:29:00', 0),
(24, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-12 20:29:15', 0),
(25, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-12 20:30:06', 1),
(26, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-12 20:32:23', 0),
(27, 2, 'Pago procesado exitosamente para la factura F002', 'success', '2025-03-12 20:32:30', 0),
(28, 1, 'Bienvenido/a Dr(a). Carlos Eduardo! Has iniciado sesión como Médico', 'success', '2025-03-12 20:33:35', 1),
(29, 2, 'Tu cita del 20/03/2025 ha sido finalizada', 'warning', '2025-03-12 20:33:47', 0),
(30, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-12 20:35:18', 0),
(31, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-12 20:47:38', 1),
(32, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-12 21:23:43', 1),
(33, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-12 21:24:38', 0),
(34, 1, 'Bienvenido/a Dr(a). Carlos Eduardo! Has iniciado sesión como Médico', 'success', '2025-03-12 21:25:22', 1),
(35, 1, 'Bienvenido/a Dr(a). Carlos Eduardo! Has iniciado sesión como Médico', 'success', '2025-03-12 21:28:29', 1),
(36, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-13 18:33:44', 1),
(37, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-13 18:57:21', 0),
(38, 2, 'Pago procesado exitosamente para la factura F001', 'success', '2025-03-13 18:57:36', 0),
(39, 2, 'Pago procesado exitosamente para la factura F002', 'success', '2025-03-13 18:57:39', 0),
(40, 1, 'Bienvenido/a Dr(a). Carlos Eduardo! Has iniciado sesión como Médico', 'success', '2025-03-13 18:58:41', 0),
(41, 2, 'Bienvenido/a David! Has iniciado sesión como Paciente', 'success', '2025-03-13 19:00:59', 0),
(42, 1, 'Bienvenido/a Dr(a). Carlos Eduardo! Has iniciado sesión como Médico', 'success', '2025-03-13 19:07:23', 0),
(43, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-13 19:54:07', 0),
(44, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-19 19:19:40', 0),
(45, 1, 'Bienvenido/a Carlos! Has iniciado sesión como Administrador', 'success', '2025-03-20 18:59:43', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pacientes`
--

CREATE TABLE `pacientes` (
  `id` int NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `tipo_documento` enum('CC','TI','CE','Pasaporte') NOT NULL,
  `numero_documento` varchar(20) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `genero` enum('Masculino','Femenino','Otro') NOT NULL,
  `grupo_sanguineo` enum('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `eps` varchar(100) NOT NULL,
  `contacto_emergencia` varchar(100) NOT NULL,
  `telefono_emergencia` varchar(20) NOT NULL,
  `contraseña` varchar(255) NOT NULL,
  `rol` enum('Paciente','Administrador','Medico') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `pacientes`
--

INSERT INTO `pacientes` (`id`, `nombre`, `apellido`, `tipo_documento`, `numero_documento`, `fecha_nacimiento`, `genero`, `grupo_sanguineo`, `email`, `telefono`, `direccion`, `eps`, `contacto_emergencia`, `telefono_emergencia`, `contraseña`, `rol`) VALUES
(2, 'David', 'Correa Baloco', 'CC', '1102148546', '2025-02-11', 'Masculino', 'B+', 'david@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'Famisanar', 'Carlos Correa', '3244016591', 'dav123', 'Paciente'),
(4, 'Maria', 'Correa Baloco', 'CC', '110231221', '2025-03-12', 'Masculino', 'A-', 'mari123@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'SaludTotal', 'Carlos Correa', '3244016591', 'mari123', 'Paciente'),
(5, 'Isabel', 'Correa Baloco', 'CC', '111245364', '2025-03-19', 'Masculino', 'O-', 'isa123@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'Sanitas', 'Maria Mendez', '3244016591', 'isa123', 'Paciente'),
(6, 'Fernado', 'Correa Baloco', 'CC', '1442111323', '2025-03-26', 'Masculino', 'O+', 'fer123@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'Sura', 'Maria Mendez', '3244016591', 'fer123', 'Paciente'),
(7, 'manuel', 'Correa Baloco', 'CC', '114321233', '2025-03-20', 'Masculino', 'AB+', 'manuel@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'Famisanar', 'Maria Mendez', '3244016591', 'mar123', 'Paciente'),
(8, 'Maria', 'Correa Baloco', 'TI', '1199836645', '2025-03-25', 'Masculino', 'O-', 'mar12@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'ComfenalcoValle', 'Carlos Correa', '3244016591', 'mar321', 'Paciente'),
(9, 'juan', 'Correa Baloco', 'CC', '12311124532', '2025-03-20', 'Masculino', 'B+', 'juan@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'CajacopiEps', 'Maria Mendez', '3244016591', 'iso123', 'Paciente'),
(10, 'gato', 'Correa Baloco', 'TI', '1102148523', '2025-03-12', 'Femenino', 'A+', 'gato@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'SaludTotal', 'Carlos Correa', '3244016591', 'gato123', 'Paciente'),
(11, 'perro', 'Correa Baloco', 'CC', '19999876553', '2025-03-27', 'Masculino', 'O-', 'perro@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'MutualSerEps', 'Maria Mendez', '3244016591', 'perro123', 'Paciente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tratamientos`
--

CREATE TABLE `tratamientos` (
  `id` int NOT NULL,
  `paciente_id` int NOT NULL,
  `medico_id` int NOT NULL,
  `fecha` date NOT NULL,
  `motivo` text NOT NULL,
  `diagnostico` text NOT NULL,
  `tratamiento` text NOT NULL,
  `receta` text,
  `notas` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `tratamientos`
--

INSERT INTO `tratamientos` (`id`, `paciente_id`, `medico_id`, `fecha`, `motivo`, `diagnostico`, `tratamiento`, `receta`, `notas`) VALUES
(2, 2, 1, '2025-03-12', 'Dolor de Cabeza', 'Friebre Y Gripa', 'Dolex Forte', '1 Caja de Dolex Cada 8horas', 'Que se mejore Señor Carlos'),
(3, 2, 1, '2025-03-12', 'Medicina General', 'Dolor intenso en la rodilla', 'Reposo y Descanso', 'Hibuprofeno de 100gr', 'Que se mejore');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `paciente_id` (`paciente_id`),
  ADD KEY `medico_id` (`medico_id`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_factura` (`numero_factura`),
  ADD KEY `id_cita` (`id_cita`);

--
-- Indices de la tabla `medicos`
--
ALTER TABLE `medicos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_documento` (`numero_documento`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `numero_registro` (`numero_registro`);

--
-- Indices de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_documento` (`numero_documento`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `paciente_id` (`paciente_id`),
  ADD KEY `medico_id` (`medico_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administradores`
--
ALTER TABLE `administradores`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `medicos`
--
ALTER TABLE `medicos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT de la tabla `notificaciones`
--
ALTER TABLE `notificaciones`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`),
  ADD CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`medico_id`) REFERENCES `medicos` (`id`);

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `facturas_ibfk_1` FOREIGN KEY (`id_cita`) REFERENCES `citas` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `tratamientos`
--
ALTER TABLE `tratamientos`
  ADD CONSTRAINT `tratamientos_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`),
  ADD CONSTRAINT `tratamientos_ibfk_2` FOREIGN KEY (`medico_id`) REFERENCES `medicos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

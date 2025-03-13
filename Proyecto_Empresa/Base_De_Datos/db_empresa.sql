-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 06-03-2025 a las 17:55:24
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
(5, 'Carlos Eduardo', 'Correa Baloco', 'CC', '1120148630', 'Masculino', 'carlosmedico@gmail.com', '3244016591', 'CR 7A CL 23D-75', 'Cardiologia', 'F3H452166', 12, 'Carsim32', 'Medico');

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
(4, 'Pedro', 'Paciente', 'CC', '987654321', '1990-01-01', 'Masculino', 'O+', 'paciente@gmail.com', '555-123-4567', 'Avenida Siempre Viva 456', 'SaludTotal', 'Maria Garcia', '555-987-6543', 'paciente123', 'Paciente');

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
-- Indices de la tabla `medicos`
--
ALTER TABLE `medicos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_documento` (`numero_documento`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `numero_registro` (`numero_registro`);

--
-- Indices de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_documento` (`numero_documento`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administradores`
--
ALTER TABLE `administradores`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `medicos`
--
ALTER TABLE `medicos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `pacientes`
--
ALTER TABLE `pacientes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

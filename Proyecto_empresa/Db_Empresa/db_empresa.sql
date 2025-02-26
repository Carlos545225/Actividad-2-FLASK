CREATE SCHEMA IF NOT EXISTS `db_empresa` DEFAULT CHARACTER SET utf8;
USE `db_empresa`;

-- Tabla Paciente
CREATE TABLE IF NOT EXISTS `Paciente` (
  `idPaciente` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NOT NULL,
  `Apellido` VARCHAR(100) NOT NULL,
  `Documento` ENUM("Cedula", "Tarjeta de identidad") NOT NULL,
  `NumeroDocumento` INT NOT NULL,
  `Telefono` VARCHAR(15) NOT NULL,
  `Correo` VARCHAR(100) NOT NULL,
  `Direccion` VARCHAR(100) NOT NULL,
  `FechaNacimiento` DATE NOT NULL,
  PRIMARY KEY (`idPaciente`)
) ENGINE = InnoDB;

-- Tabla Medico
CREATE TABLE IF NOT EXISTS `Medico` (
  `idMedico` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NOT NULL,
  `Apellido` VARCHAR(100) NOT NULL,
  `Especialidad` VARCHAR(50) NOT NULL,
  `Telefono` VARCHAR(15) NOT NULL,
  `Correo` VARCHAR(100) NOT NULL,
  `HorarioAtencion` VARCHAR(100) NOT NULL,
  `Disponibilidad` ENUM("Activo", "No activo") NOT NULL,
  PRIMARY KEY (`idMedico`)
) ENGINE = InnoDB;

-- Tabla CitaMedica
CREATE TABLE IF NOT EXISTS `CitaMedica` (
  `idCitaMedica` INT NOT NULL AUTO_INCREMENT,
  `idPaciente` INT NOT NULL,
  `idMedico` INT NOT NULL,
  `Fecha` DATE NOT NULL,
  `Hora` TIME NOT NULL,
  `Estado` ENUM("Pendiente", "Confirmada", "Cancelada", "Completada") NOT NULL,
  `Motivo` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`idCitaMedica`),
  INDEX `idx_Paciente` (`idPaciente` ASC),
  INDEX `idx_Medico` (`idMedico` ASC),
  CONSTRAINT `fk_CitaMedica_Paciente`
    FOREIGN KEY (`idPaciente`) REFERENCES `Paciente` (`idPaciente`),
  CONSTRAINT `fk_CitaMedica_Medico`
    FOREIGN KEY (`idMedico`) REFERENCES `Medico` (`idMedico`)
) ENGINE = InnoDB;

-- Tabla HistorialMedico
CREATE TABLE IF NOT EXISTS `HistorialMedico` (
  `idHistorialMedico` INT NOT NULL AUTO_INCREMENT,
  `idPaciente` INT NOT NULL,
  `Diagnostico` VARCHAR(200) NOT NULL,
  `Tratamiento` VARCHAR(200) NOT NULL,
  `Fecha` DATE NOT NULL,
  `idMedico` INT NOT NULL,
  PRIMARY KEY (`idHistorialMedico`),
  INDEX `idx_Paciente` (`idPaciente` ASC),
  INDEX `idx_Medico` (`idMedico` ASC),
  CONSTRAINT `fk_HistorialMedico_Paciente`
    FOREIGN KEY (`idPaciente`) REFERENCES `Paciente` (`idPaciente`),
  CONSTRAINT `fk_HistorialMedico_Medico`
    FOREIGN KEY (`idMedico`) REFERENCES `Medico` (`idMedico`)
) ENGINE = InnoDB;

-- Tabla Usuario
CREATE TABLE IF NOT EXISTS `Usuario` (
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `Nombre` VARCHAR(100) NOT NULL,
  `Contraseña` VARCHAR(100) NOT NULL,
  `Rol` ENUM("Paciente", "Medico", "Administrador") NOT NULL,
  PRIMARY KEY (`idUsuario`)
) ENGINE = InnoDB;

-- Tabla Recordatorio
CREATE TABLE IF NOT EXISTS `Recordatorio` (
  `idRecordatorio` INT NOT NULL AUTO_INCREMENT,
  `idPaciente` INT NOT NULL,
  `idCitaMedica` INT NOT NULL,
  `Fecha` DATE NOT NULL,
  `HoraEnvio` TIME NOT NULL,
  `MedioEnvio` ENUM("Correo", "SMS") NOT NULL,
  PRIMARY KEY (`idRecordatorio`),
  INDEX `idx_Paciente` (`idPaciente` ASC),
  INDEX `idx_CitaMedica` (`idCitaMedica` ASC),
  CONSTRAINT `fk_Recordatorio_Paciente`
    FOREIGN KEY (`idPaciente`) REFERENCES `Paciente` (`idPaciente`),
  CONSTRAINT `fk_Recordatorio_CitaMedica`
    FOREIGN KEY (`idCitaMedica`) REFERENCES `CitaMedica` (`idCitaMedica`)
) ENGINE = InnoDB;

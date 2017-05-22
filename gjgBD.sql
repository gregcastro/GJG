-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         5.5.24-log - MySQL Community Server (GPL)
-- SO del servidor:              Win64
-- HeidiSQL Versión:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Volcando estructura de base de datos para gjg
CREATE DATABASE IF NOT EXISTS `gjg` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `gjg`;

-- Volcando estructura para tabla gjg.administrador
CREATE TABLE IF NOT EXISTS `administrador` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `clave` varchar(255) NOT NULL COMMENT 'admin',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.administrador: ~1 rows (aproximadamente)
/*!40000 ALTER TABLE `administrador` DISABLE KEYS */;
INSERT INTO `administrador` (`id`, `usuario`, `correo`, `clave`) VALUES
	(1, 'admin', 'josegregorio994@gmail.com', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918');
/*!40000 ALTER TABLE `administrador` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.auditoria
CREATE TABLE IF NOT EXISTS `auditoria` (
  `idAuditoria` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(255) NOT NULL,
  `fecha` date NOT NULL,
  `usuario` varchar(50) NOT NULL,
  PRIMARY KEY (`idAuditoria`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.auditoria: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `auditoria` DISABLE KEYS */;
INSERT INTO `auditoria` (`idAuditoria`, `descripcion`, `fecha`, `usuario`) VALUES
	(2, 'Nuevo inicio de sesión', '2017-05-22', 'josegregorio994@gmail.com'),
	(3, 'Nuevo inicio de sesión', '2017-05-22', 'hsitechnologies@gmail.com'),
	(4, 'Realizó una búsqueda de solicitudes entre 2017/5/2 y 2017/5/19', '2017-05-22', 'hsitechnologies@gmail.com'),
	(5, 'Se solicitó un servicio de distribución con los siguientes datos: cédula: 6784585 nombre: Bernardo Fuentes teléfono: 04147856525 correo: berni@gmail.com peso: 6.1 costo: 2000.0 número de orden: 69288658', '2017-05-22', 'mercadolibre@gmail.com');
/*!40000 ALTER TABLE `auditoria` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.categoriapeso
CREATE TABLE IF NOT EXISTS `categoriapeso` (
  `idCategoriaPeso` int(11) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `pesoMinimo` double NOT NULL,
  `pesoMaximo` double NOT NULL,
  PRIMARY KEY (`idCategoriaPeso`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.categoriapeso: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `categoriapeso` DISABLE KEYS */;
INSERT INTO `categoriapeso` (`idCategoriaPeso`, `descripcion`, `pesoMinimo`, `pesoMaximo`) VALUES
	(1, 'BAJA', 0.1, 3),
	(2, 'MEDIA', 3.1, 7),
	(3, 'ALTA', 7.1, 10);
/*!40000 ALTER TABLE `categoriapeso` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.cliente
CREATE TABLE IF NOT EXISTS `cliente` (
  `idCliente` int(11) NOT NULL AUTO_INCREMENT,
  `correo` varchar(50) NOT NULL,
  `clave` varchar(255) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `rif` varchar(9) NOT NULL,
  `codPostal` int(4) NOT NULL,
  PRIMARY KEY (`idCliente`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.cliente: ~4 rows (aproximadamente)
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` (`idCliente`, `correo`, `clave`, `descripcion`, `rif`, `codPostal`) VALUES
	(1, 'ebay@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 'ebay C.A', '246359070', 1060),
	(3, 'mercadolibre@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 'Mercadolibre C.A', '112547540', 2014),
	(4, 'tutiendaonline@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 'Tu Tienda Online C.A', '085458742', 1025),
	(17, 'hsitechnologies@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 'HSI Tech', '12547854', 1060);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.direccion
CREATE TABLE IF NOT EXISTS `direccion` (
  `idDireccion` int(11) NOT NULL AUTO_INCREMENT,
  `codPostal` int(4) NOT NULL,
  `dirEnvio` varchar(255) NOT NULL,
  PRIMARY KEY (`idDireccion`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.direccion: ~69 rows (aproximadamente)
/*!40000 ALTER TABLE `direccion` DISABLE KEYS */;
INSERT INTO `direccion` (`idDireccion`, `codPostal`, `dirEnvio`) VALUES
	(7, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(8, 1060, 'Altamira Sur, Edf. cartagena'),
	(9, 1060, 'La castellana, tercera transversal, edf. juarez'),
	(10, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(11, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(12, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(13, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(14, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(15, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(16, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(17, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(18, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(19, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(20, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(21, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(22, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(23, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(24, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(25, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(26, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(27, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(28, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(29, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(30, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(31, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(32, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(33, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(34, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(35, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(36, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(37, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(38, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(39, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(40, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(41, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(42, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(43, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(44, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(45, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(46, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(47, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(48, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(49, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(50, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(51, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(52, 4060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(53, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(54, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(55, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(56, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(57, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(58, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(59, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(60, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(61, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(62, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(63, 5060, 'Estado Bolivar avenida paez edf miranda pso 4 apt 16'),
	(64, 1030, 'Av lecuna edf el marquito piso 2 apt 22'),
	(65, 1030, 'Av lecuna edf lecuna piso 8 apt 8-B'),
	(66, 1020, 'Chuao, esquina la margarita'),
	(67, 5014, 'Sotillo, Higuerote'),
	(68, 8014, 'Lecheria, Barcelona'),
	(69, 7041, 'Merida, edf. el gocho'),
	(70, 1050, 'Las mercedes, caracas'),
	(71, 1060, 'Chacao, Caracas'),
	(72, 1020, 'Parque Central, Caracas'),
	(73, 1020, 'Parque Central, Caracas'),
	(74, 1020, 'Parque Central, Caracas'),
	(75, 1090, 'Los Naranjos, Caracas'),
	(76, 1090, 'Los Naranjos, Caracas'),
	(77, 1090, 'Los Naranjos, Caracas'),
	(78, 1090, 'Los Naranjos, Caracas');
/*!40000 ALTER TABLE `direccion` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.encargo
CREATE TABLE IF NOT EXISTS `encargo` (
  `idEncargo` int(11) NOT NULL AUTO_INCREMENT,
  `cedula` varchar(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `peso` double NOT NULL,
  `fechaCompra` date NOT NULL,
  `fechaEstimada` date NOT NULL,
  `costo` double NOT NULL,
  `tracking` varchar(8) NOT NULL,
  `idDireccion` int(11) NOT NULL,
  `idEstatus` int(11) NOT NULL,
  `idCliente` int(11) NOT NULL,
  `idCategoriaPeso` int(11) NOT NULL,
  PRIMARY KEY (`idEncargo`),
  KEY `fk_encargo_direccion` (`idDireccion`),
  KEY `fk_encargo_estatus` (`idEstatus`),
  KEY `fk_encargo_cliente` (`idCliente`),
  KEY `fk_encargo_categoriaPeso` (`idCategoriaPeso`),
  CONSTRAINT `fk_encargo_categoriaPeso` FOREIGN KEY (`idCategoriaPeso`) REFERENCES `categoriapeso` (`idCategoriaPeso`),
  CONSTRAINT `fk_encargo_cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`),
  CONSTRAINT `fk_encargo_direccion` FOREIGN KEY (`idDireccion`) REFERENCES `direccion` (`idDireccion`),
  CONSTRAINT `fk_encargo_estatus` FOREIGN KEY (`idEstatus`) REFERENCES `estatusencargo` (`idEstatus`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.encargo: ~30 rows (aproximadamente)
/*!40000 ALTER TABLE `encargo` DISABLE KEYS */;
INSERT INTO `encargo` (`idEncargo`, `cedula`, `nombre`, `telefono`, `correo`, `peso`, `fechaCompra`, `fechaEstimada`, `costo`, `tracking`, `idDireccion`, `idEstatus`, `idCliente`, `idCategoriaPeso`) VALUES
	(11, '24635907', 'Jose Gregorio Castro', '04140179052', 'josegregorio994@gmail.com', 3.5, '2017-04-03', '2017-04-02', 3000, '06647903', 7, 1, 17, 2),
	(12, '24635907', 'Jose Gregorio Castro', '04140179052', 'juan@gmail.com', 2.2, '2017-04-04', '2017-04-02', 2000, '64576962', 8, 2, 17, 2),
	(13, '24635907', 'Jose Gregorio Castro', '04140179052', 'darkside@gmail.com', 7.5, '2017-04-02', '2017-04-02', 6000, '45692556', 9, 2, 17, 2),
	(14, '24635907', 'Jose Gregorio Castro', '04140179052', 'theteacher@gmail.com', 1.4, '2017-04-05', '2017-04-02', 1000, '28960237', 7, 3, 17, 2),
	(15, '24635907', 'Jose Gregorio Castro', '04140179052', 'alejandro@gmail.com', 5.6, '2017-04-07', '2017-04-02', 4000, '79096925', 8, 3, 17, 2),
	(16, '24635907', 'Jose Gregorio Castro', '04140179052', 'jesus@gmail.com', 3.3, '2017-04-09', '2017-04-02', 2000, '87397276', 8, 2, 17, 2),
	(17, '24635907', 'Jose Gregorio Castro', '04140179052', 'daniel@gmail.com', 1.4, '2017-04-12', '2017-04-02', 2000, '70995017', 7, 3, 17, 2),
	(18, '24635907', 'Jose Gregorio Castro', '04140179052', 'alexandra@gmail.com', 3.5, '2017-04-14', '2017-04-02', 2000, '97712095', 9, 2, 17, 2),
	(19, '24635907', 'Jose Gregorio Castro', '04140179052', 'karen@gmail.com', 3.5, '2017-04-14', '2017-04-03', 3000, '65733446', 52, 1, 17, 2),
	(20, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-14', '2017-04-04', 5000, '51124452', 53, 1, 17, 3),
	(21, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-14', '2017-04-04', 5000, '40164456', 53, 1, 17, 3),
	(22, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-14', '2017-04-04', 5000, '48219256', 53, 1, 17, 3),
	(23, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-14', '2017-04-05', 5000, '91157255', 53, 1, 17, 3),
	(24, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-14', '2017-04-06', 5000, '55608873', 53, 1, 17, 3),
	(25, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-14', '2017-04-04', 5000, '99910715', 53, 1, 17, 3),
	(26, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-14', '2017-04-06', 5000, '70625676', 53, 1, 17, 3),
	(27, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-14', '2017-04-04', 5000, '70458539', 53, 1, 17, 3),
	(28, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-14', '2017-04-05', 5000, '96597987', 53, 1, 17, 3),
	(29, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-20', '2017-04-05', 5000, '86747168', 53, 1, 17, 3),
	(30, '12545874', 'Petra Contreras', '04140179052', 'petra@gmail.com', 7.3, '2017-04-02', '2017-04-05', 5000, '88441907', 53, 2, 17, 3),
	(31, '25584564', 'Jose Alvarez', '04145687485', 'jesema@gmail.com', 2.4, '2017-05-08', '2017-05-09', 1000, '47772774', 64, 1, 17, 1),
	(32, '25584564', 'Jose Alvarez', '04145687485', 'jesema@gmail.com', 2.4, '2017-05-18', '2017-05-19', 1000, '25977748', 64, 3, 17, 1),
	(33, '12545874', 'Carlos Gonzalez', '0416854854', 'carlitos@gmail.com', 5, '2017-05-18', '2017-05-19', 2000, '80359229', 66, 2, 1, 2),
	(34, '14587454', 'Barbara Madrid', '0412568458', 'barbie@gmail.com', 1.2, '2017-05-18', '2017-05-21', 3000, '97051976', 67, 3, 1, 1),
	(35, '6454875', 'Karla Contreras', '0414587458', 'karla@gmail.com', 5.6, '2017-05-18', '2017-05-23', 5000, '70980108', 68, 3, 3, 2),
	(36, '6454875', 'Pedro Perez', '0412569856', 'pedrito@gmail.com', 7.4, '2017-05-18', '2017-05-22', 6000, '98638620', 69, 4, 3, 3),
	(37, '9874562', 'Aparicio Pena', '0414256985', 'aparicio@gmail.com', 2.5, '2017-05-18', '2017-05-19', 1000, '43232065', 70, 1, 3, 1),
	(38, '14568965', 'Miguel Silva', '0412545856', 'miguel@gmail.com', 9, '2017-05-18', '2017-05-19', 3000, '68266315', 71, 3, 3, 3),
	(41, '10808934', 'Jensy Lazo', '04166046105', 'jensy@gmail.com', 2, '2017-05-18', '2017-05-19', 1000, '06915886', 72, 3, 3, 1),
	(42, '6784585', 'Bernardo Fuentes', '04147856525', 'berni@gmail.com', 6.1, '2017-05-18', '2017-05-19', 2000, '54973197', 75, 3, 3, 2),
	(45, '6784585', 'Bernardo Fuentes', '04147856525', 'berni@gmail.com', 6.1, '2017-05-22', '2017-05-23', 2000, '69288658', 75, 1, 3, 2);
/*!40000 ALTER TABLE `encargo` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.estadofactura
CREATE TABLE IF NOT EXISTS `estadofactura` (
  `idEstadoFactura` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(50) NOT NULL,
  PRIMARY KEY (`idEstadoFactura`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.estadofactura: ~3 rows (aproximadamente)
/*!40000 ALTER TABLE `estadofactura` DISABLE KEYS */;
INSERT INTO `estadofactura` (`idEstadoFactura`, `descripcion`) VALUES
	(1, 'VIGENTE'),
	(2, 'VENCIDA'),
	(3, 'CANCELADA');
/*!40000 ALTER TABLE `estadofactura` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.estatusencargo
CREATE TABLE IF NOT EXISTS `estatusencargo` (
  `idEstatus` int(11) NOT NULL,
  `descripcion` varchar(30) NOT NULL,
  PRIMARY KEY (`idEstatus`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.estatusencargo: ~4 rows (aproximadamente)
/*!40000 ALTER TABLE `estatusencargo` DISABLE KEYS */;
INSERT INTO `estatusencargo` (`idEstatus`, `descripcion`) VALUES
	(1, 'POR PROCESAR'),
	(2, 'PROCESADO'),
	(3, 'EN RUTA'),
	(4, 'ENTREGADO');
/*!40000 ALTER TABLE `estatusencargo` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.factura
CREATE TABLE IF NOT EXISTS `factura` (
  `idFactura` int(11) NOT NULL AUTO_INCREMENT,
  `fechaCancelacion` date DEFAULT NULL,
  `fechaVencimiento` date NOT NULL,
  `monto` double NOT NULL,
  `idCliente` int(11) NOT NULL,
  `idEstadoFactura` int(11) NOT NULL,
  `idEncargo` int(11) NOT NULL,
  PRIMARY KEY (`idFactura`),
  KEY `fk_factura_cliente` (`idCliente`),
  KEY `fk_factura_estadoFactura` (`idEstadoFactura`),
  KEY `fk_factura_encargo` (`idEncargo`),
  CONSTRAINT `fk_factura_cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`),
  CONSTRAINT `fk_factura_encargo` FOREIGN KEY (`idEncargo`) REFERENCES `encargo` (`idEncargo`),
  CONSTRAINT `fk_factura_estadoFactura` FOREIGN KEY (`idEstadoFactura`) REFERENCES `estadofactura` (`idEstadoFactura`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.factura: ~5 rows (aproximadamente)
/*!40000 ALTER TABLE `factura` DISABLE KEYS */;
INSERT INTO `factura` (`idFactura`, `fechaCancelacion`, `fechaVencimiento`, `monto`, `idCliente`, `idEstadoFactura`, `idEncargo`) VALUES
	(1, '2017-05-16', '2017-05-29', 6000, 3, 3, 36),
	(2, '2017-05-16', '2017-05-31', 1000, 3, 3, 37),
	(3, '2017-05-17', '2017-06-02', 3000, 3, 3, 38),
	(4, NULL, '2017-06-02', 1000, 3, 1, 41),
	(5, NULL, '2017-05-17', 2000, 3, 2, 42),
	(8, NULL, '2017-06-06', 2000, 3, 1, 45);
/*!40000 ALTER TABLE `factura` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.historial
CREATE TABLE IF NOT EXISTS `historial` (
  `idHistorial` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `locacion` varchar(200) NOT NULL,
  `idEncargo` int(11) NOT NULL,
  PRIMARY KEY (`idHistorial`),
  KEY `fk_historial_encargo` (`idEncargo`),
  CONSTRAINT `fk_historial_encargo` FOREIGN KEY (`idEncargo`) REFERENCES `encargo` (`idEncargo`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.historial: ~19 rows (aproximadamente)
/*!40000 ALTER TABLE `historial` DISABLE KEYS */;
INSERT INTO `historial` (`idHistorial`, `fecha`, `locacion`, `idEncargo`) VALUES
	(2, '2017-05-19', 'oficina GJG la Urbina', 38),
	(6, '2017-05-19', 'entregado al mototaxista ', 38),
	(9, '2017-05-19', 'oficina GJC, paquete chequeado', 36),
	(10, '2017-05-20', 'aragua', 36),
	(11, '2017-05-21', 'barquisimeto', 36),
	(18, '2017-05-21', 'Producto Entregado', 36),
	(21, '2017-05-21', 'oficina GJG la Urbina', 41),
	(22, '2017-05-21', 'Producto Entregado', 41),
	(27, '2017-05-21', 'altamira', 41),
	(29, '2017-05-21', 'altamira', 41),
	(31, '2017-05-21', 'altamira', 41),
	(33, '2017-05-21', 'plaza venezuela', 41),
	(35, '2017-05-21', 'plaza venezuela', 41),
	(37, '2017-05-21', 'la urbina', 34),
	(39, '2017-05-21', 'la urbina', 34),
	(41, '2017-05-21', 'guarenas', 34),
	(47, '2017-05-21', 'la urbina', 42),
	(49, '2017-05-21', 'la urbina', 42),
	(51, '2017-05-21', 'estado bolivar, avenida intercomunal', 35);
/*!40000 ALTER TABLE `historial` ENABLE KEYS */;

-- Volcando estructura para vista gjg.view_clientes
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_clientes` (
	`descripcion` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`correo` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`rif` VARCHAR(9) NOT NULL COLLATE 'latin1_swedish_ci',
	`codPostal` INT(4) NOT NULL,
	`cantidad` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_destinos
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_destinos` (
	`codPostal` INT(4) NOT NULL,
	`dirEnvio` VARCHAR(255) NOT NULL COLLATE 'latin1_swedish_ci',
	`cantidad` BIGINT(21) NOT NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_estatus_cargo
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_estatus_cargo` (
	`idEstatus` INT(11) NOT NULL,
	`descripcion` VARCHAR(30) NOT NULL COLLATE 'latin1_swedish_ci'
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_facturas_cancelacion
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_facturas_cancelacion` (
	`fechaCancelacion` DATE NULL,
	`fechaVencimiento` DATE NOT NULL,
	`monto` DOUBLE NOT NULL,
	`comercio` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`estado` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci'
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_facturas_vencidas
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_facturas_vencidas` (
	`fechaVencimiento` DATE NOT NULL,
	`monto` DOUBLE NOT NULL,
	`comercio` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`estado` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci'
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_facturas_vigentes
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_facturas_vigentes` (
	`fechaVencimiento` DATE NOT NULL,
	`monto` DOUBLE NOT NULL,
	`comercio` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`estado` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci'
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_historial_paquete
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_historial_paquete` (
	`fecha` DATE NOT NULL,
	`locacion` VARCHAR(200) NOT NULL COLLATE 'latin1_swedish_ci',
	`idCliente` INT(11) NOT NULL,
	`idEncargo` INT(11) NOT NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_solicitudes
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_solicitudes` (
	`tracking` VARCHAR(8) NOT NULL COLLATE 'latin1_swedish_ci',
	`nombre` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`comercio` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`costo` DOUBLE NOT NULL,
	`fechaCompra` DATE NOT NULL,
	`fechaEstimada` DATE NOT NULL,
	`estatus` VARCHAR(30) NOT NULL COLLATE 'latin1_swedish_ci',
	`direccion` VARCHAR(255) NOT NULL COLLATE 'latin1_swedish_ci',
	`codPostal` INT(4) NOT NULL,
	`idCliente` INT(11) NOT NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_solicitudes_despachadas
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_solicitudes_despachadas` 
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_solicitudes_por_despachar
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_solicitudes_por_despachar` 
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_clientes
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_clientes`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_clientes` AS SELECT c.descripcion, c.correo, c.rif, c.codPostal, COUNT(e.idCliente) cantidad
FROM encargo e, cliente c
WHERE e.idCliente = c.idCliente
GROUP BY e.idCliente
ORDER BY COUNT(e.idCliente) DESC ;

-- Volcando estructura para vista gjg.view_destinos
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_destinos`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_destinos` AS SELECT d.codPostal, d.dirEnvio, COUNT(e.idDireccion) cantidad
FROM encargo e, direccion d
WHERE e.idDireccion = d.idDireccion
GROUP BY e.idDireccion
ORDER BY COUNT(e.idDireccion) DESC ;

-- Volcando estructura para vista gjg.view_estatus_cargo
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_estatus_cargo`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_estatus_cargo` AS SELECT * FROM estatusencargo ;

-- Volcando estructura para vista gjg.view_facturas_cancelacion
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_facturas_cancelacion`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_facturas_cancelacion` AS SELECT f.fechaCancelacion, f.fechaVencimiento, f.monto, c.descripcion comercio, e.descripcion estado
FROM factura f, cliente c, estadofactura e
WHERE f.idCliente = c.idCliente AND f.idEstadoFactura = e.idEstadoFactura AND f.idEstadoFactura = 3
ORDER BY f.fechaCancelacion ;

-- Volcando estructura para vista gjg.view_facturas_vencidas
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_facturas_vencidas`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_facturas_vencidas` AS SELECT f.fechaVencimiento, f.monto, c.descripcion comercio, e.descripcion estado
FROM factura f, cliente c, estadofactura e
WHERE f.idCliente = c.idCliente AND f.idEstadoFactura = e.idEstadoFactura AND f.idEstadoFactura = 2
ORDER BY f.fechaCancelacion ;

-- Volcando estructura para vista gjg.view_facturas_vigentes
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_facturas_vigentes`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_facturas_vigentes` AS SELECT f.fechaVencimiento, f.monto, c.descripcion comercio, e.descripcion estado
FROM factura f, cliente c, estadofactura e
WHERE f.idCliente = c.idCliente AND f.idEstadoFactura = e.idEstadoFactura AND f.idEstadoFactura = 1
ORDER BY f.fechaCancelacion ;

-- Volcando estructura para vista gjg.view_historial_paquete
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_historial_paquete`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_historial_paquete` AS SELECT h.fecha, h.locacion, e.idCliente, h.idEncargo
FROM historial h, encargo e
WHERE h.idEncargo = e.idEncargo


#SELECT * FROM view_historial_paquete WHERE idCliente = 3 AND idEncargo = 38 ;

-- Volcando estructura para vista gjg.view_solicitudes
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_solicitudes`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_solicitudes` AS SELECT DISTINCT e.tracking, e.nombre, c.descripcion comercio, e.costo, e.fechaCompra, e.fechaEstimada, est.descripcion estatus, d.dirEnvio direccion, d.codPostal, e.idCliente
FROM encargo e, cliente c, estatusencargo est, direccion d
WHERE e.idEstatus = est.idEstatus AND e.idCliente = c.idCliente AND e.idDireccion = d.idDireccion ;

-- Volcando estructura para vista gjg.view_solicitudes_despachadas
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_solicitudes_despachadas`;
CREATE DEFINER=`root`@`localhost` VIEW `view_solicitudes_despachadas` AS SELECT * FROM encargo WHERE idEstatus = 2 ;

-- Volcando estructura para vista gjg.view_solicitudes_por_despachar
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_solicitudes_por_despachar`;
CREATE DEFINER=`root`@`localhost` VIEW `view_solicitudes_por_despachar` AS SELECT * FROM encargo WHERE idEstatus = 1 ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

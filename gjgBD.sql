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

-- Volcando estructura para tabla gjg.auditoria
CREATE TABLE IF NOT EXISTS `auditoria` (
  `idAuditoria` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(255) NOT NULL,
  `fecha` datetime NOT NULL,
  PRIMARY KEY (`idAuditoria`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.auditoria: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `auditoria` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.cliente: ~4 rows (aproximadamente)
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` (`idCliente`, `correo`, `clave`, `descripcion`, `rif`, `codPostal`) VALUES
	(1, 'ebay@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 'ebay C.A', '246359070', 1060),
	(3, 'mercadolibre@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 'Mercado Libre C.A', '112547540', 2014),
	(4, 'mercadolibre2@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', '', '085458742', 1025),
	(16, 'hsitechnologies@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', 'HSI Tech', '12547854', 1060);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.direccion
CREATE TABLE IF NOT EXISTS `direccion` (
  `idDireccion` int(11) NOT NULL AUTO_INCREMENT,
  `codPostal` int(4) NOT NULL,
  `dirEnvio` varchar(255) NOT NULL,
  PRIMARY KEY (`idDireccion`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.direccion: ~15 rows (aproximadamente)
/*!40000 ALTER TABLE `direccion` DISABLE KEYS */;
INSERT INTO `direccion` (`idDireccion`, `codPostal`, `dirEnvio`) VALUES
	(7, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(8, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
	(9, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27'),
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
	(21, 1060, 'Los Palos Grandes, primera avenida, edf marialaya piso 6 apto. 27');
/*!40000 ALTER TABLE `direccion` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.encargo
CREATE TABLE IF NOT EXISTS `encargo` (
  `idEncargo` int(11) NOT NULL AUTO_INCREMENT,
  `cedula` varchar(50) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `telefono` varchar(50) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `peso` double NOT NULL,
  `fechaEnvio` date NOT NULL,
  `fechaEstimada` date NOT NULL,
  `dirFuente` varchar(255) DEFAULT NULL,
  `costo` double NOT NULL,
  `idDireccion` int(11) NOT NULL,
  `idEstatus` int(11) NOT NULL,
  `idCliente` int(11) NOT NULL,
  `idPrioridadEnvio` int(11) NOT NULL,
  `idCategoriaPeso` int(11) NOT NULL,
  PRIMARY KEY (`idEncargo`),
  KEY `fk_encargo_direccion` (`idDireccion`),
  KEY `fk_encargo_estatus` (`idEstatus`),
  KEY `fk_encargo_cliente` (`idCliente`),
  KEY `fk_encargo_prioridadEnvio` (`idPrioridadEnvio`),
  KEY `fk_encargo_categoriaPeso` (`idCategoriaPeso`),
  CONSTRAINT `fk_encargo_categoriaPeso` FOREIGN KEY (`idCategoriaPeso`) REFERENCES `categoriapeso` (`idCategoriaPeso`),
  CONSTRAINT `fk_encargo_cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`),
  CONSTRAINT `fk_encargo_direccion` FOREIGN KEY (`idDireccion`) REFERENCES `direccion` (`idDireccion`),
  CONSTRAINT `fk_encargo_estatus` FOREIGN KEY (`idEstatus`) REFERENCES `estatusencargo` (`idEstatus`),
  CONSTRAINT `fk_encargo_prioridadEnvio` FOREIGN KEY (`idPrioridadEnvio`) REFERENCES `prioridadenvio` (`idPrioridad`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.encargo: ~1 rows (aproximadamente)
/*!40000 ALTER TABLE `encargo` DISABLE KEYS */;
INSERT INTO `encargo` (`idEncargo`, `cedula`, `nombre`, `telefono`, `correo`, `peso`, `fechaEnvio`, `fechaEstimada`, `dirFuente`, `costo`, `idDireccion`, `idEstatus`, `idCliente`, `idPrioridadEnvio`, `idCategoriaPeso`) VALUES
	(2, '24635907', 'Jose Gregorio Castro', '04140179052', 'josegregorio994@gmail.com', 3.5, '2017-03-20', '2017-03-22', NULL, 5000.3, 7, 1, 1, 1, 2);
/*!40000 ALTER TABLE `encargo` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.encargoproducto
CREATE TABLE IF NOT EXISTS `encargoproducto` (
  `idEncargoProducto` int(11) NOT NULL AUTO_INCREMENT,
  `idProducto` int(11) NOT NULL,
  `idEncargo` int(11) NOT NULL,
  PRIMARY KEY (`idEncargoProducto`),
  KEY `fk_encargoProducto_producto` (`idProducto`),
  KEY `fk_encargoProducto_encargo` (`idEncargo`),
  CONSTRAINT `fk_encargoProducto_encargo` FOREIGN KEY (`idEncargo`) REFERENCES `encargo` (`idEncargo`),
  CONSTRAINT `fk_encargoProducto_producto` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.encargoproducto: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `encargoproducto` DISABLE KEYS */;
/*!40000 ALTER TABLE `encargoproducto` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.estadofactura
CREATE TABLE IF NOT EXISTS `estadofactura` (
  `idEstadoFactura` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(50) NOT NULL,
  PRIMARY KEY (`idEstadoFactura`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.estadofactura: ~2 rows (aproximadamente)
/*!40000 ALTER TABLE `estadofactura` DISABLE KEYS */;
INSERT INTO `estadofactura` (`idEstadoFactura`, `descripcion`) VALUES
	(1, 'VIGENTE'),
	(2, 'VENCIDA');
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
  `fechaCancelacion` date NOT NULL,
  `fechaVencimiento` date NOT NULL,
  `monto` double NOT NULL,
  `idCliente` int(11) NOT NULL,
  `idEstadoFactura` int(11) NOT NULL,
  PRIMARY KEY (`idFactura`),
  KEY `fk_factura_cliente` (`idCliente`),
  KEY `fk_factura_estadoFactura` (`idEstadoFactura`),
  CONSTRAINT `fk_factura_cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`),
  CONSTRAINT `fk_factura_estadoFactura` FOREIGN KEY (`idEstadoFactura`) REFERENCES `estadofactura` (`idEstadoFactura`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.factura: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `factura` DISABLE KEYS */;
/*!40000 ALTER TABLE `factura` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.prioridadenvio
CREATE TABLE IF NOT EXISTS `prioridadenvio` (
  `idPrioridad` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(50) NOT NULL,
  PRIMARY KEY (`idPrioridad`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.prioridadenvio: ~1 rows (aproximadamente)
/*!40000 ALTER TABLE `prioridadenvio` DISABLE KEYS */;
INSERT INTO `prioridadenvio` (`idPrioridad`, `descripcion`) VALUES
	(1, 'UNICA PRIORIDAD');
/*!40000 ALTER TABLE `prioridadenvio` ENABLE KEYS */;

-- Volcando estructura para tabla gjg.producto
CREATE TABLE IF NOT EXISTS `producto` (
  `idProducto` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(50) NOT NULL,
  `peso` double NOT NULL,
  PRIMARY KEY (`idProducto`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Volcando datos para la tabla gjg.producto: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;

-- Volcando estructura para vista gjg.view_estatus_cargo
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_estatus_cargo` (
	`idEstatus` INT(11) NOT NULL,
	`descripcion` VARCHAR(30) NOT NULL COLLATE 'latin1_swedish_ci'
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_solicitudes_despachadas
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_solicitudes_despachadas` (
	`idEncargo` INT(11) NOT NULL,
	`cedula` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`nombre` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`telefono` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`correo` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`peso` DOUBLE NOT NULL,
	`fechaEnvio` DATE NOT NULL,
	`fechaEstimada` DATE NOT NULL,
	`dirFuente` VARCHAR(255) NULL COLLATE 'latin1_swedish_ci',
	`costo` DOUBLE NOT NULL,
	`idDireccion` INT(11) NOT NULL,
	`idEstatus` INT(11) NOT NULL,
	`idCliente` INT(11) NOT NULL,
	`idPrioridadEnvio` INT(11) NOT NULL,
	`idCategoriaPeso` INT(11) NOT NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_solicitudes_por_despachar
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `view_solicitudes_por_despachar` (
	`idEncargo` INT(11) NOT NULL,
	`cedula` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`nombre` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`telefono` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`correo` VARCHAR(50) NOT NULL COLLATE 'latin1_swedish_ci',
	`peso` DOUBLE NOT NULL,
	`fechaEnvio` DATE NOT NULL,
	`fechaEstimada` DATE NOT NULL,
	`dirFuente` VARCHAR(255) NULL COLLATE 'latin1_swedish_ci',
	`costo` DOUBLE NOT NULL,
	`idDireccion` INT(11) NOT NULL,
	`idEstatus` INT(11) NOT NULL,
	`idCliente` INT(11) NOT NULL,
	`idPrioridadEnvio` INT(11) NOT NULL,
	`idCategoriaPeso` INT(11) NOT NULL
) ENGINE=MyISAM;

-- Volcando estructura para vista gjg.view_estatus_cargo
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_estatus_cargo`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_estatus_cargo` AS SELECT * FROM estatusencargo ;

-- Volcando estructura para vista gjg.view_solicitudes_despachadas
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_solicitudes_despachadas`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_solicitudes_despachadas` AS SELECT * FROM encargo WHERE idEstatus = 2 ;

-- Volcando estructura para vista gjg.view_solicitudes_por_despachar
-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `view_solicitudes_por_despachar`;
CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` VIEW `view_solicitudes_por_despachar` AS SELECT * FROM encargo WHERE idEstatus = 1 ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

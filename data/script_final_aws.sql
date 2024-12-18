-- MySQL Script generated by MySQL Workbench
-- Thu Dec  5 11:48:24 2024
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema keyfinder
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema keyfinder
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `keyfinder` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `keyfinder` ;

-- -----------------------------------------------------
-- Table `keyfinder`.`kb_input`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `keyfinder`.`kb_input` (
  `id_kb_input` INT NOT NULL AUTO_INCREMENT,
  `kb_usage` VARCHAR(45) NOT NULL,
  `budget` INT NOT NULL,
  `switch` VARCHAR(50) NOT NULL,
  `kb_size` VARCHAR(30) NOT NULL,
  `kb_connection` VARCHAR(20) NOT NULL,
  `mk_before` TINYINT(1) NOT NULL,
  `mk_input` VARCHAR(300) NOT NULL,
  `user_prompt` VARCHAR(500) NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_kb_input`))
ENGINE = InnoDB
AUTO_INCREMENT = 52
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `keyfinder`.`kb_output`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `keyfinder`.`kb_output` (
  `id_kb_output` INT NOT NULL AUTO_INCREMENT,
  `id_kb_input` INT NOT NULL,
  `kb_shown` INT NOT NULL,
  `price` INT NOT NULL,
  `switch` VARCHAR(50) NOT NULL,
  `kb_size` VARCHAR(50) NOT NULL,
  `mk_output` VARCHAR(300) NOT NULL,
  `sys_prompt` VARCHAR(500) NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `kb_name` VARCHAR(60) NULL DEFAULT NULL,
  `kb_link` VARCHAR(250) NULL DEFAULT NULL,
  PRIMARY KEY (`id_kb_output`),
  INDEX `id_kb_input` (`id_kb_input` ASC) VISIBLE,
  CONSTRAINT `kb_output_ibfk_1`
    FOREIGN KEY (`id_kb_input`)
    REFERENCES `keyfinder`.`kb_input` (`id_kb_input`))
ENGINE = InnoDB
AUTO_INCREMENT = 65
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
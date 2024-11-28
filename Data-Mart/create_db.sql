--Dimensionen

CREATE TABLE IF NOT EXISTS `District` (
    `districtCode` INT NOT NULL,
    `districtName` VARCHAR(100),
    PRIMARY KEY (`districtCode`)
);

CREATE TABLE IF NOT EXISTS `Date` (
    `date` TIMESTAMP NOT NULL,
    `year` INT,
    `month` INT,
    `day` INT,
    PRIMARY KEY (`date`)
);

--Fakten 

CREATE TABLE IF NOT EXISTS `PopulationFact` (
    `districtCode` INT NOT NULL,
    `date` TIMESTAMP NOT NULL,
    `austrianCitizens` INT,
    `foreignCitizens` INT,
    PRIMARY KEY (`districtCode`, `date`),
    FOREIGN KEY (`districtCode`) REFERENCES `District` (`districtCode`),
    FOREIGN KEY (`date`) REFERENCES `Date` (`date`)
);

CREATE TABLE IF NOT EXISTS `EducationFact` (
    `districtCode` INT NOT NULL,
    `date` TIMESTAMP NOT NULL,
    `academicEducation` FLOAT,
    `statutoryEducation` FLOAT,
    `highschoolEducation` FLOAT,
    `vocationalEducation` FLOAT,
    PRIMARY KEY (`districtCode`, `date`),
    FOREIGN KEY (`districtCode`) REFERENCES `District` (`districtCode`),
    FOREIGN KEY (`date`) REFERENCES `Date` (`date`)
);

CREATE TABLE IF NOT EXISTS `ElectionFact` (
    `districtCode` INT NOT NULL,
    `date` TIMESTAMP NOT NULL,
    `övpVotes` INT,
    `spöVotes` INT,
    `fpöVotes` INT,
    `grüneVotes` INT,
    `neosVotes` INT,
    `otherVotes` INT,
    PRIMARY KEY (`districtCode`, `date`),
    FOREIGN KEY (`districtCode`) REFERENCES `District` (`districtCode`),
    FOREIGN KEY (`date`) REFERENCES `Date` (`date`)
);

CREATE TABLE IF NOT EXISTS `WeatherFact` (
    `districtCode` INT NOT NULL,
    `date` TIMESTAMP NOT NULL,
    `airPressure` FLOAT,
    `temperature` FLOAT,
    `humidity` FLOAT,
    `wind` FLOAT,
    `rainfall` FLOAT,
    PRIMARY KEY (`districtCode`, `date`),
    FOREIGN KEY (`districtCode`) REFERENCES `District` (`districtCode`),
    FOREIGN KEY (`date`) REFERENCES `Date` (`date`)
);

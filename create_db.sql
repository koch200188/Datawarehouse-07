CREATE TABLE IF NOT EXISTS 'Location' (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    districtName VARCHAR(100),
    PRIMARY KEY (districtCode, date)
);

CREATE TABLE IF NOT EXISTS 'PopulationData' (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    austrianCitizens INT,
    foreignCitizens INT,
    PRIMARY KEY (districtCode, date),
);

CREATE TABLE IF NOT EXISTS 'EducationData' (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    academicEducation FLOAT,
    statutoryEducation FLOAT,
    highschoolEducation FLOAT,
    vocationalEducation FLOAT,
    PRIMARY KEY (districtCode, date),
);

CREATE TABLE IF NOT EXISTS 'ElectionData' (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    övpVotes INT NOT NULL,
    spöVotes INT NOT NULL,
    fpöVotes INT NOT NULL,
    grüneVotes INT NOT NULL,
    neosVotes INT NOT NULL,
    otherVotes INT NOT NULL,
    PRIMARY KEY (districtCode, date),
);

CREATE TABLE IF NOT EXISTS 'WeatherData' (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    airPressure FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    wind FLOAT,
    rainfaill FLOAT,
    PRIMARY KEY (districtCode, date),
);

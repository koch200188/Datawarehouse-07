CREATE DATABASE datawarehouse;
\c datawarehouse;

CREATE TABLE IF NOT EXISTS "Location" (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    districtName VARCHAR(100),
    PRIMARY KEY (districtCode, date)
);

CREATE TABLE IF NOT EXISTS "PopulationData" (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    austrianCitizens INT,
    foreignCitizens INT,
    PRIMARY KEY (districtCode, date)
);

CREATE TABLE IF NOT EXISTS "EducationData" (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    academicEducation FLOAT,
    statutoryEducation FLOAT,
    highschoolEducation FLOAT,
    vocationalEducation FLOAT,
    PRIMARY KEY (districtCode, date)
);

CREATE TABLE IF NOT EXISTS "ElectionData" (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    övpVotes INT NOT NULL,
    spöVotes INT NOT NULL,
    fpöVotes INT NOT NULL,
    grüneVotes INT NOT NULL,
    neosVotes INT NOT NULL,
    otherVotes INT NOT NULL,
    PRIMARY KEY (districtCode, date)
);

CREATE TABLE IF NOT EXISTS "WeatherData" (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    airPressure FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    wind FLOAT,
    rainfall FLOAT,
    PRIMARY KEY (districtCode, date)
);

CREATE OR REPLACE FUNCTION notify_weather_update()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('weather_data_updates', json_build_object(
        'districtCode', NEW.districtCode,
        'date', NEW.date,
        'airPressure', NEW.airPressure,
        'temperature', NEW.temperature,
        'humidity', NEW.humidity,
        'wind', NEW.wind,
        'rainfall', NEW.rainfall
    )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER weather_update_trigger
AFTER INSERT OR UPDATE ON "WeatherData"
FOR EACH ROW EXECUTE FUNCTION notify_weather_update();

CREATE TRIGGER population_update_trigger
AFTER INSERT OR UPDATE ON "PopulationData"
FOR EACH ROW EXECUTE FUNCTION notify_weather_update();

CREATE DATABASE ods;
\c ods;

CREATE TABLE IF NOT EXISTS "RealtimeWeatherData" (
    districtCode INT NOT NULL,
    date TIMESTAMP NOT NULL,
    temperature FLOAT,
    wind FLOAT,
    rainfall FLOAT,
    PRIMARY KEY (districtCode, date)
);
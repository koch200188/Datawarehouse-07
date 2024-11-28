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
    rainfaill FLOAT,
    PRIMARY KEY (districtCode, date)
);

-- Notify function to send updates via pg_notify
CREATE OR REPLACE FUNCTION notify_data_update()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM pg_notify('data_updates', json_build_object(
        'table', TG_TABLE_NAME,
        'districtCode', NEW.districtCode,
        'date', NEW.date
    )::text);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for PopulationData updates
CREATE TRIGGER population_update_trigger
AFTER INSERT OR UPDATE ON "PopulationData"
FOR EACH ROW EXECUTE FUNCTION notify_data_update();

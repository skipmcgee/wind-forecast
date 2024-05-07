
-- -----------------------------------------------------
-- Get Sensor + Location Information
-- -----------------------------------------------------
SELECT sensorID, sensorName, sensorAPIKEY, sensorNumber, locationLatitude, locationLongitude, locationAltitude FROM Sensors
JOIN Locations ON Sensors.sensorLocationID = Locations.locationID
ORDER BY sensorName DESC;"

- -----------------------------------------------------
-- Delete a Forecast
-- -----------------------------------------------------
DELETE FROM Forecasts WHERE forecastID=_forecastID;

-- -----------------------------------------------------
-- Get Forecast Information
-- -----------------------------------------------------
SELECT * FROM Forecasts;

-- -----------------------------------------------------
-- Insert Forecast Information
-- -----------------------------------------------------
INSERT INTO Forecasts (`forecastDateID`, `forecastTemperature2m`, `forecastPrecipitation`, `forecastWeatherCode`, `forecastPressureMSL`, `forecastWindSpeed10m`, `forecastWindDirection10m`, `forecastCape`, `forecastModelID`, `forecastLocationID`, `forecastWindGust`, `forecastForDateTime`,)
VALUES (_forecastDateID, _forecastTemperature2m, _forecastPrecipitation, _forecastWeatherCode, _forecastPressureMSL, _forecastWindSpeed10m, _forecastWindDirection10m, _forecastCape, _forecastModelID, _forecastLocationID, _forecastWindGust, _forecastForDateTime,);

-- -----------------------------------------------------
-- Update Forecast Information
-- -----------------------------------------------------
UPDATE Forecasts
SET column1 = value1, column2 = value2,
WHERE forecastID=_forecastID; 

- -----------------------------------------------------
-- Delete a Reading
-- -----------------------------------------------------
DELETE FROM Readings WHERE readingID=_readingID;

-- -----------------------------------------------------
-- Get Readings Information
-- -----------------------------------------------------
SELECT * FROM Readings;

-- -----------------------------------------------------
-- Insert Readings Information
-- -----------------------------------------------------
INSERT INTO Readings (`readingSensorID`, `readingWindSpeed`, `readingWindGust`, `readingWindMin`, `readingWindDirection`, `readingTemperature`, `readingDateID`,)
VALUES (_readingSensorID, _readingWindSpeed, _readingWindGust, _readingWindMin, _readingWindDirection, _readingTemperature, _readingDateID,);

-- -----------------------------------------------------
-- Update Reading Information
-- -----------------------------------------------------
UPDATE Readings
SET column1 = value1, column2 = value2,
WHERE readingID=_readingID; 

- -----------------------------------------------------
-- Delete a Model
-- -----------------------------------------------------
DELETE FROM Models WHERE modelID=_modelID;

-- -----------------------------------------------------
-- Get Models Information
-- -----------------------------------------------------
SELECT * FROM Models;

-- -----------------------------------------------------
-- Insert Models Information
-- -----------------------------------------------------
INSERT INTO Models (`modelName`)
VALUES (_modelName);

-- -----------------------------------------------------
-- Update Model Information
-- -----------------------------------------------------
UPDATE Models
SET column1 = value1, column2 = value2,
WHERE modelID=_modelID; 

- -----------------------------------------------------
-- Delete a Date
-- -----------------------------------------------------
DELETE FROM Dates WHERE dateID=_dateID;

-- -----------------------------------------------------
-- Get Dates Information
-- -----------------------------------------------------
SELECT * FROM Dates;

-- -----------------------------------------------------
-- Insert Dates Information
-- -----------------------------------------------------
INSERT INTO Dates (`dateDateTime`)
VALUES (_dateDateTime);

-- -----------------------------------------------------
-- Update Dates Information
-- -----------------------------------------------------
UPDATE Dates
SET column1 = value1, column2 = value2,
WHERE dateID=_dateID; 

- -----------------------------------------------------
-- Delete a Sensor
-- -----------------------------------------------------
DELETE FROM Sensors WHERE sensorID=_sensorID;

-- -----------------------------------------------------
-- Get Sensors Information
-- -----------------------------------------------------
SELECT * FROM Sensors;

-- -----------------------------------------------------
-- Insert Sensors Information
-- -----------------------------------------------------
INSERT INTO Sensors (`sensorName`, `sensorAPIKey`, `sensorNumber`, `sensorLocationID`,)
VALUES (_sensorName, _sensorAPIKey, _sensorNumber, _sensorLocationID,);

-- -----------------------------------------------------
-- Update Sensor Information
-- -----------------------------------------------------
UPDATE Sensors
SET column1 = value1, column2 = value2,
WHERE sensorID=_sensorID; 

- -----------------------------------------------------
-- Delete a Location
-- -----------------------------------------------------
DELETE FROM Locations WHERE locationID=_locationID;

-- -----------------------------------------------------
-- Get Locations Information
-- -----------------------------------------------------
SELECT * FROM Locations;

-- -----------------------------------------------------
-- Insert Locations Information
-- -----------------------------------------------------
INSERT INTO Locations (`locationName`, `locationLatitude`, `locationLongitude`, `locationAltitude`,)
VALUES (_locationName, _locationLatitude, _locationLongitude, _locationAltitude,);

-- -----------------------------------------------------
-- Update Location Information
-- -----------------------------------------------------
UPDATE Locations
SET column1 = value1, column2 = value2,
WHERE locationID=_locationID;

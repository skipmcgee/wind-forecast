
-- -----------------------------------------------------
-- Get Sensor + Location Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
SELECT sensorID, sensorName, sensorAPIKEY, sensorNumber, locationLatitude, locationLongitude, locationAltitude FROM Sensors
JOIN Locations ON Sensors.sensorLocationID = Locations.locationID
ORDER BY sensorName DESC;

- -----------------------------------------------------
-- Delete a Forecast
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
DELETE FROM Forecasts WHERE forecastID=_forecastID;

-- -----------------------------------------------------
-- Get Forecast Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
SELECT * FROM Forecasts;

-- -----------------------------------------------------
-- Insert Forecast Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
INSERT INTO Forecasts (`forecastDateID`, `forecastTemperature2m`, `forecastPrecipitation`, `forecastWeatherCode`, `forecastPressureMSL`, `forecastWindSpeed10m`, `forecastWindDirection10m`, `forecastCape`, `forecastModelID`, `forecastLocationID`, `forecastWindGust`, `forecastForDateTime`,)
VALUES (_forecastDateID, _forecastTemperature2m, _forecastPrecipitation, _forecastWeatherCode, _forecastPressureMSL, _forecastWindSpeed10m, _forecastWindDirection10m, _forecastCape, _forecastModelID, _forecastLocationID, _forecastWindGust, _forecastForDateTime,);

-- -----------------------------------------------------
-- Update Forecast Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
UPDATE Forecasts
SET column1 = value1, column2 = value2,
WHERE forecastID=_forecastID; 

- -----------------------------------------------------
-- Delete a Reading
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
DELETE FROM Readings WHERE readingID=_readingID;

-- -----------------------------------------------------
-- Get Readings Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
SELECT * FROM Readings;

-- -----------------------------------------------------
-- Insert Readings Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
INSERT INTO Readings (`readingSensorID`, `readingWindSpeed`, `readingWindGust`, `readingWindMin`, `readingWindDirection`, `readingTemperature`, `readingDateID`,)
VALUES (_readingSensorID, _readingWindSpeed, _readingWindGust, _readingWindMin, _readingWindDirection, _readingTemperature, _readingDateID,);

-- -----------------------------------------------------
-- Update Reading Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
UPDATE Readings
SET column1 = value1, column2 = value2,
WHERE readingID=_readingID; 

- -----------------------------------------------------
-- Delete a Model
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
DELETE FROM Models WHERE modelID=_modelID;

-- -----------------------------------------------------
-- Get Models Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
SELECT * FROM Models;

-- -----------------------------------------------------
-- Insert Models Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
INSERT INTO Models (`modelName`)
VALUES (_modelName);

-- -----------------------------------------------------
-- Update Model Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
UPDATE Models
SET column1 = value1, column2 = value2,
WHERE modelID=_modelID; 

- -----------------------------------------------------
-- Delete a Date
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
DELETE FROM Dates WHERE dateID=_dateID;

-- -----------------------------------------------------
-- Get Dates Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
SELECT * FROM Dates;

-- -----------------------------------------------------
-- Insert Dates Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
INSERT INTO Dates (`dateDateTime`)
VALUES (_dateDateTime);

-- -----------------------------------------------------
-- Update Dates Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
UPDATE Dates
SET column1 = value1, column2 = value2,
WHERE dateID=_dateID; 

- -----------------------------------------------------
-- Delete a Sensor
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
DELETE FROM Sensors WHERE sensorID=_sensorID;

-- -----------------------------------------------------
-- Get Sensors Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
SELECT * FROM Sensors;

-- -----------------------------------------------------
-- Insert Sensors Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
INSERT INTO Sensors (`sensorName`, `sensorAPIKey`, `sensorNumber`, `sensorLocationID`,)
VALUES (_sensorName, _sensorAPIKey, _sensorNumber, _sensorLocationID,);

-- -----------------------------------------------------
-- Update Sensor Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
UPDATE Sensors
SET column1 = value1, column2 = value2,
WHERE sensorID=_sensorID; 

- -----------------------------------------------------
-- Delete a Location
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
DELETE FROM Locations WHERE locationID=_locationID;

-- -----------------------------------------------------
-- Get Locations Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
SELECT * FROM Locations;

-- -----------------------------------------------------
-- Insert Locations Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
INSERT INTO Locations (`locationName`, `locationLatitude`, `locationLongitude`, `locationAltitude`,)
VALUES (_locationName, _locationLatitude, _locationLongitude, _locationAltitude,);

-- -----------------------------------------------------
-- Update Location Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
UPDATE Locations
SET column1 = value1, column2 = value2,
WHERE locationID=_locationID;

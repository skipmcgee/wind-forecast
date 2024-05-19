-- MySQL Script created by David McGee and Theodore Norred
-- CS-340 Group 10 Project


-- --------------------
-- Create
-- --------------------

-- Forecasts

INSERT INTO 
	`Forecasts` (
		forecastForDateTime, 
		forecastDateID, 
		forecastTemperature2m, 
		forecastPrecipitation, 
		forecastWeatherCode, 
		forecastPressureMSL, 
		forecastWindSpeed10m, 
		forecastWindDirection10m, 
		forecastCape, 
		forecastLocationID,
        forecastModelID
	)
VALUES 
	(
		%(forecastForDateTime)s, 
		%(forecastDateID)s, 
		%(forecastTemperature2m)s, 
		%(forecastPrecipitation)s, 
		%(forecastWeatherCode)s, 
		%(forecastPressureMSL)s, 
		%(forecastWindSpeed10m)s, 
		%(forecastWindDirection10m)s, 
		%(forecastCape)s, 
		%(forecastLocationID)s,
        %(forecastModelID)s
);
                    
-- Locations
-- Sensors
-- Models
-- Dates
-- Readings

-- --------------------
-- Read
-- --------------------

-- Forecasts

SELECT 
	Forecasts.forecastID,
	Dates.dateDateTime,
	Forecasts.forecastTemperature2m,
	Forecasts.forecastPrecipitation,
	Forecasts.forecastWeatherCode,
	Forecasts.forecastPressureMSL,
	Forecasts.forecastWindSpeed10m,
	Forecasts.forecastWindDirection10m,
	Forecasts.forecastCape,
	Models.modelName,
	Locations.locationName,
	Forecasts.forecastForDateTime
FROM 
	Forecasts
LEFT JOIN 
	Models ON Forecasts.forecastModelID = Models.modelID
JOIN 
	Locations ON Forecasts.forecastLocationID = Locations.locationID
JOIN 
	Dates ON Forecasts.forecastDateID = Dates.dateID;
    
-- Locations

SELECT 
    locationID,
    locationName,
    locationLatitude,
    locationLongitude,
    locationAltitude
FROM
    Locations;
        
-- Sensors

SELECT 
    Sensors.sensorID,
    Sensors.sensorName,
    Sensors.sensorAPIKEY,
    Sensors.sensorNumber,
    Locations.locationLatitude,
    Locations.locationLongitude,
    Locations.locationAltitude
FROM
    Sensors
JOIN
    Locations ON Sensors.sensorLocationID = Locations.locationID;

-- Models

SELECT 
    modelID, 
    modelName
FROM
    Models;
        
-- Dates

SELECT 
    dateID, 
    dateDateTime
FROM
    Dates;

-- Readings

SELECT 
    Readings.readingID,
    Sensors.sensorName,
    Sensors.sensorNumber,
    Readings.readingWindSpeed,
    Readings.readingWindGust,
    Readings.readingWindMin,
    Readings.readingWindDirection,
    Readings.readingTemperature,
    Dates.dateDateTime
FROM
    Readings
JOIN 
	Sensors ON Readings.readingSensorID = Sensors.sensorID
JOIN 
	Dates ON Readings.readingDateID = Dates.dateID;

-- --------------------
-- Update
-- --------------------

-- Forecasts

SELECT 
	forecastID,
	forecastDateID,
	forecastTemperature2m,
	forecastPrecipitation,
	forecastWeatherCode,
	forecastPressureMSL,
	forecastWindSpeed10m,
	forecastWindDirection10m,
	forecastCape,
	forecastModelID,
	forecastLocationID,
	forecastForDateTime
FROM 
	Forecasts
WHERE
	forecastID = %(forecastID)s;
            
-- Locations
-- Sensors

SELECT 
	* 
FROM 
	Sensors
JOIN 
	Locations ON Sensors.sensorLocationID = Locations.locationID;
-- WHERE Sensors.sensorID = %(sensorID)s;
            
-- Models
-- Dates
-- Readings

-- --------------------
-- Delete
-- --------------------

-- Forecasts

DELETE FROM 
	Forecasts
WHERE
	forecastID = %(forecastID)s;
        
-- Locations
-- Sensors
-- Models
-- Dates
-- Readings

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


-- OR get Forecasts from a date range

SELECT * 
FROM Forecasts
JOIN Models ON Forecasts.forecastModelID = Models.modelID
JOIN Locations ON Forecasts.forecastLocationID = Locations.locationID
WHERE 
    forecastForDateTime BETWEEN _toDate AND _fromDate
    AND
    Locations.locationID = _locationID;
-- -----------------------------------------------------
-- Insert Forecast Information
-- '_' is used to denote backend language variables
-- -----------------------------------------------------
INSERT INTO Forecasts (`forecastDateID`, `forecastTemperature2m`, `forecastPrecipitation`, `forecastWeatherCode`, `forecastPressureMSL`, `forecastWindSpeed10m`, `forecastWindDirection10m`, `forecastCape`, `forecastModelID`, `forecastLocationID`, `forecastForDateTime`,)
VALUES (_forecastDateID, _forecastTemperature2m, _forecastPrecipitation, _forecastWeatherCode, _forecastPressureMSL, _forecastWindSpeed10m, _forecastWindDirection10m, _forecastCape, _forecastModelID, _forecastLocationID, _forecastForDateTime,);

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

-- OR get Readings from a date range

SELECT * FROM Readings
JOIN Sensors ON Readings.readingSensorID = Sensors.sensorID
JOIN Dates ON Readings.readingDateID = Dates.dateID
WHERE 
    dateDateTime BETWEEN _toDate AND _fromDate
    AND
    sensorLocationID =_locationID;
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

-- OR get Dates from a date range

SELECT * 
FROM Dates
WHERE dateDateTime BETWEEN _toDate AND _fromDate;

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

-- OR

SELECT * FROM Sensors
JOIN Locations ON Sensors.sensorLocationID = Locations.locationID
WHERE Sensors.sensorID = _sensorID;

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
SET `sensorName` = _sensorName, `sensorAPIKey` = _sensorAPIKey, `sensorNumber` = _sensorNumber, `sensorLocationID` = _sensorLocationID,
WHERE `sensorID` = _sensorID; 

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
SET `locationName`={editsensor['locationName']}, `locationLatitude`={editsensor['locationLatitude']}, `locationLongitude`={editsensor['locationLongitude']}, `locationAltitude`={editsensor['locationAltitude']},
WHERE `locationID`=_locationID;

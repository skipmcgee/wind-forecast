-- Data Manipulation Language
-- 4/28/2024
-- MySQL Script created by David McGee and Theodore Norred
-- CS-340 Group 10 Project


-- ------------
-- Forecasts --
-- ------------

-- Create

INSERT INTO 
	Forecasts (
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

-- Read

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
    
-- Update

UPDATE 
	Forecasts
SET 
	forecastForDateTime = %(forecastForDateTime)s,
	forecastDateID = %(forecastDateID)s,
	forecastTemperature2m = %(forecastTemperature2m)s,
	forecastPrecipitation = %(forecastPrecipitation)s,
	forecastWeatherCode = %(forecastWeatherCode)s,
	forecastPressureMSL = %(forecastPressureMSL)s,
	forecastWindSpeed10m = %(forecastWindSpeed10m)s,
	forecastWindDirection10m = %(forecastWindDirection10m)s,
	forecastCape = %(forecastCape)s,
	forecastLocationID = %(forecastLocationID)s,
	forecastModelID = %(forecastModelID)s
WHERE 
	forecastID = %(forecastID)s;
    
-- Delete

DELETE FROM 
	Forecasts
WHERE
	forecastID = %(forecastID)s;
	

-- ------------
-- Locations --
-- ------------

-- Create

INSERT INTO
	Locations (locationName, locationLatitude, locationLongitude, locationAltitude)
VALUES
	(%(locationName)s, %(locationLatitude)s, %(locationLongitude)s, %(locationAltitude)s);
            
-- Read

SELECT 
    locationID,
    locationName,
    locationLatitude,
    locationLongitude,
    locationAltitude
FROM
    Locations;
    
-- Update

UPDATE 
	Locations
SET 
	locationName= %(locationName)s, 
    locationLatitude= %(locationLatitude)s, 
    locationLongitude= %(locationLongitude)s, 
    locationAltitude= %(locationAltitude)s
WHERE 
	Locations.locationID = %(locationID)s;
    
-- Delete

DELETE FROM 
	Locations
WHERE 
	locationID = %(locationID)s;
	
	
-- ----------
-- Sensors --
-- ----------

-- Create

INSERT INTO 
	Sensors (sensorName, sensorAPIKey, sensorNumber, sensorLocationID)
VALUES 
	(%(sensorName)s, %(sensorAPIKey)s, %(sensorNumber)s, %(location)s);

-- Read

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
    
-- Update

UPDATE 
	Sensors 
SET 
	sensorName= %(sensorName)s, sensorAPIKey= %(sensorAPIKey)s, sensorNumber= %(sensorNumber)s, sensorLocationID= %(locationID)s
WHERE 
	sensorID= %(sensorID)s;

-- Delete

DELETE FROM
	Sensors
WHERE
	sensorID = %(sensorID)s;
	

-- ---------
-- Models --
-- ---------

-- Create

INSERT INTO 
	Models (
		modelID, 
        modelName
        )
VALUES 
	(%(modelID)s, %(modelName)s);

-- Read

SELECT 
    modelID, 
    modelName
FROM
    Models;
    
-- Update

UPDATE 
	Models
SET 
	modelName = %(modelName)s
WHERE 
	Models.modelID = %(modelID)s;
    
-- Delete

DELETE FROM 
	Models
WHERE 
	modelID = %(modelID)s;
	
    
-- --------
-- Dates --
-- --------

-- Create

INSERT INTO 
	Dates (dateDateTime)
VALUES 
	(%(dateDateTime)s);
    
-- Read

SELECT 
    dateID, 
    dateDateTime
FROM
    Dates;
    
-- Update

UPDATE 
	Dates
SET 
	dateDateTime = %(dateDateTime)s
WHERE 
	Dates.dateID = %(dateID)s;
        
-- Delete

DELETE FROM 
	Dates
WHERE 
	dateID = %(dateID)s;
        
-- -----------
-- Readings --
-- -----------

-- Create

INSERT INTO 
	Readings (
    readingSensorID, 
    readingWindSpeed, 
    readingWindGust, 
    readingWindMin, 
    readingWindDirection, 
    readingTemperature, 
    readingDateID)
VALUES (
	%(readingSensorID)s, 
	%(readingWindSpeed)s, 
	%(readingWindGust)s, 
	%(readingWindMin)s, 
	%(readingWindDirection)s, 
	%(readingTemperature)s, 
	%(readingDateID)s);
        
-- Read

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
    
-- Update

UPDATE 
	Readings
SET 
	readingSensorID= %(readingSensorID)s,
    readingWindSpeed= %(readingWindSpeed)s,
    readingWindGust= %(readingWindGust)s,
    readingWindMin= %(readingWindMin)s,
    readingWindDirection= %(readingWindDirection)s,
    readingTemperature= %(readingTemperature)s,
    readingDateID= %(readingDateID)s
WHERE 
	Readings.readingID = %(readingID)s
    
-- Delete

DELETE FROM
	Readings
WHERE
	readingID = %(readingID)s;

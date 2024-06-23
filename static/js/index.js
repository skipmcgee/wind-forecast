// Citation for the following function: convertDateTime()
// Date: 05/30/2024
// Based on the StackOverflow solution #3 by Kevin Ternet
// Adapted the code to convert JavaScript Date() into a format suitable for datetime-local
// Source URL: https://stackoverflow.com/questions/38816337/convert-javascript-date-format-to-yyyy-mm-ddthhmmss
// Source URL: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now


// Set the current sensor in the form to the 1st in the list
const currentSensors = [1, 2,];

function convertDateTime() {
  // Fetch the current date & time
  const today = new Date();

  // Extract the year, month, day, hours, and minutes from the date/time
  let year = today.getFullYear();
  let month = String(today.getMonth()+1).padStart(2, '0');
  let day = String(today.getDate()).padStart(2, '0');
  let hours = String(today.getHours()).padStart(2, '0');
  let minutes = String(today.getMinutes()).padStart(2, '0');

  // Return datetime-local format
  return (`${year}-${month}-${day}T${hours}:${minutes}`);
};

// Select document elements
const toDate = document.getElementById('toDate');
const fromDate = document.getElementById('fromDate');
const submitButton = document.getElementById('submitButton');
const sensor = document.getElementById('sensorlist');

// Update max and value with the date
let dateTimeLocalFormat = convertDateTime();
fromDate.max = dateTimeLocalFormat;
toDate.max = dateTimeLocalFormat;
toDate.value = dateTimeLocalFormat;

function checkDates() {
  // Function to validate date criteria in the form
  const fromDateValue = fromDate.value;
  const toDateValue = toDate.value;
  
  // Check to make sure a valid date has been given
  if (fromDateValue && toDateValue) {
    const fromDateSelection = new Date(fromDateValue);
    const toDateSelection = new Date(toDateValue);
    if (fromDateSelection < toDateSelection) {
      submitButton.disabled = false;
    } else {
      // Clear the from date field and disable the submit button
      fromDate.value = '';
      submitButton.disabled = true;
      alert('The "From" date cannot be after the "To" date.');
    }
  } else {
    // Disable the submit button by default
    submitButton.disabled = true;
  }
}

function checkSensor() {
  // Function to validate the sensor selection in the form.
  let checkSensorValue = sensor.value;
  if (currentSensor == checkSensorValue) {
    submitButton.disabled = false;
  } else {
    submitButton.disabled = true;
    alert('The selected sensor must be one supported for MVP');
  }
}

fromDate.addEventListener('change', checkDates);
toDate.addEventListener('change', checkDates);
//sensor.addEventListener('change', checkSensor);
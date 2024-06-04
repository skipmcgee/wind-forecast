    // Fetch current Date / Time
    // Referenced https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now
    const today = new Date();
    const currentSensor = 1;

    // Need to convert Date/Time to YYYY-MM-DDThh:mm for datetime-local
    // Referenced Solution 3 (Kevin Ternet) https://stackoverflow.com/questions/38816337/convert-javascript-date-format-to-yyyy-mm-ddthhmmss
    let year = today.getFullYear();
    let month = String(today.getMonth()+1).padStart(2, '0');
    let day = String(today.getDate()).padStart(2, '0');
    let hours = String(today.getHours()).padStart(2, '0');
    let minutes = String(today.getMinutes()).padStart(2, '0');
    let dateTimeLocalFormat = (`${year}-${month}-${day}T${hours}:${minutes}`);

    // Select document elements
    const toDate = document.getElementById('toDate');
    const fromDate = document.getElementById('fromDate');
    const submitButton = document.getElementById('submitButton');
    const sensor = document.getElementById('sensorlist');

    // Update max and value with the date
    fromDate.max = dateTimeLocalFormat;
    toDate.max = dateTimeLocalFormat;
    toDate.value = dateTimeLocalFormat;

    function checkDates() {
      const fromDateValue = fromDate.value;
      const toDateValue = toDate.value;
      
      if (fromDateValue && toDateValue) {
        const fromDateSelection = new Date(fromDateValue);
        const toDateSelection = new Date(toDateValue);
        if (fromDateSelection < toDateSelection) {
          submitButton.disabled = false;
        } else {
          fromDate.value = '';
          submitButton.disabled = true;
          alert('The "From" date cannot be after the "To" date.');
        }
      } else {
        submitButton.disabled = true;
      }
    }

    function checkSensor() {
      const checkSensorValue = sensor.value;
      if (currentSensor == checkSensorValue) {
        submitButton.disabled = false;
      } else {
        submitButton.disabled = true;
        alert('The selected sensor must be one supported for MVP');
      }
    }

    fromDate.addEventListener('change', checkDates);
    toDate.addEventListener('change', checkDates);
    sensor.addEventListener('change', checkSensor);
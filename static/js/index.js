    // Fetch current Date / Time
    // Referenced https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/now
    const today = new Date();

    // Need to convert Date/Time to YYYY-MM-DDThh:mm for datetime-local
    // Referenced Solution 3 (Kevin Ternet) https://stackoverflow.com/questions/38816337/convert-javascript-date-format-to-yyyy-mm-ddthhmmss
    let year = today.getFullYear();
    let month = String(today.getMonth()+1).padStart(2, '0');
    let day = String(today.getDate()).padStart(2, '0');
    let hours = String(today.getHours()).padStart(2, '0');
    let minutes = String(today.getMinutes()).padStart(2, '0');
    let dateTimeLocalFormat = (`${year}-${month}-${day}T${hours}:${minutes}`);

    // Select toDate element
    const toDate = document.getElementById('toDate');

    // Update max and value with the date
    toDate.max = dateTimeLocalFormat;
    toDate.value = dateTimeLocalFormat;

    // If we want a minimum date then we need to subtract from date and add to the fromDate
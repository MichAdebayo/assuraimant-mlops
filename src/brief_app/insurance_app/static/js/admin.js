document.addEventListener("DOMContentLoaded", function () {
    flatpickr("#id_date", {
        enableTime: false,
        dateFormat: "Y-m-d",
    });

    // When a date is selected, update the available times dropdown
    const availabilityField = document.getElementById('id_availability');
    const timeField = document.getElementById('id_time');
    
    availabilityField.addEventListener('change', function () {
        const availabilityId = availabilityField.value;
        
        fetch(`/get_available_times/${availabilityId}/`)
            .then(response => response.json())
            .then(data => {
                timeField.innerHTML = ''; // Clear existing time options
                data.available_times.forEach(function (time) {
                    const option = document.createElement('option');
                    option.value = time;
                    option.textContent = time;
                    timeField.appendChild(option);
                });
            });
    });
});

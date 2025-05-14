import flatpickr from 'flatpickr';
import 'flatpickr/dist/flatpickr.min.css';
document.addEventListener('DOMContentLoaded', function() {
    flatpickr("#calendar", {
        dateFormat: "Y-m-d", // Set the date format
        disable: [
            function(date) {
                // Disable past dates
                return date < new Date();
            }
        ],
        minDate: "today" // Disable past dates automatically
    });
});

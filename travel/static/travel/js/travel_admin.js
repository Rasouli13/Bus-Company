document.addEventListener('DOMContentLoaded', function() {
    const driverSelect = document.getElementById('id_driver'); // فیلد راننده
    const vehicleNameField = document.getElementById('id_vehicle_name');
    const vehicleCapacityField = document.getElementById('id_vehicle_capacity');

    if (!driverSelect) return;

    driverSelect.addEventListener('change', function() {
        const driverId = this.value;

        if (!driverId) {
            vehicleNameField.value = '';
            vehicleCapacityField.value = '';
            return;
        }

        fetch(`/travel/get_driver_vehicle/${driverId}/`)
            .then(response => response.json())
            .then(data => {
                vehicleNameField.value = data.vehicle_name;
                vehicleCapacityField.value = data.capacity;
            })
            .catch(err => console.error(err));
    });
});

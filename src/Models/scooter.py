class Scooter:
    def __init__(
        self, id, brand, model, serial_number, top_speed, battery_capacity,
        state_of_charge, target_range_state_of_charge, location, out_of_service,
        mileage, last_maintenance, in_service_date
    ):
        self.id = id
        self.brand = brand
        self.model = model
        self.serial_number = serial_number
        self.top_speed = top_speed
        self.battery_capacity = battery_capacity
        self.state_of_charge = state_of_charge
        self.target_range_state_of_charge = target_range_state_of_charge
        self.location = location
        self.out_of_service = out_of_service
        self.mileage = mileage
        self.last_maintenance = last_maintenance
        self.in_service_date = in_service_date

    def __repr__(self):
        return f"<Scooter {self.id}: {self.brand} {self.model}>"

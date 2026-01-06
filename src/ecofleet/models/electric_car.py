from .vehicle import Vehicle

class ElectricCar(Vehicle):
    def __init__(self, vehicle_id, model, battery_percentage,
                 maintenance_status, rental_price, seating_capacity):

        # calling parent constructor
        super().__init__(vehicle_id, model, battery_percentage,
                         maintenance_status, rental_price)

        self.seating_capacity = seating_capacity

        # UC-5: Polymorphic behavior
        def calculate_trip_cost(self, distance):
            # $5 base + $0.50 per km
            return 5.0 + (0.5 * distance)
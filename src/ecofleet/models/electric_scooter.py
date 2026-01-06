from .vehicle import Vehicle


class ElectricScooter(Vehicle):
    def __init__(self, vehicle_id, model, battery_percentage,
                 maintenance_status, rental_price, max_speed_limit):

        # calling parent constructor
        super().__init__(vehicle_id, model, battery_percentage,
                         maintenance_status, rental_price)

        self.max_speed_limit = max_speed_limit
class FleetManager:
    def __init__(self):

        self.hubs={}    # Dictionary :HUb Name -> List of vehicles

    def add_hub(self, hub_name):
        if hub_name in self.hubs:
            print("Hub already exists.")
        else:
            self.hubs[hub_name] = []
            print(f"Hub '{hub_name}' added successfully.")

    def add_vehicle_to_hub(self, hub_name, vehicle):
        if hub_name not in self.hubs:
            print("Hub does not exist.")
            return

        self.hubs[hub_name].append(vehicle)
        print(f"Vehicle added to '{hub_name}' hub.")


    def display_hubs(self):
        for hub, vehicles in self.hubs.items():
            print(f"{hub} -> {len(vehicles)} vehicles")

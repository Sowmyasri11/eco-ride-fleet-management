class FleetManager:
    def __init__(self):
        # Dictionary: Hub Name -> List of Vehicle objects
        self.hubs = {}

    def add_hub(self, hub_name):
        # checking if hub already exists
        if hub_name in self.hubs:
            print("Hub already exists.")
        else:
            # creating a new hub with empty vehicle list
            self.hubs[hub_name] = []
            print(f"Hub '{hub_name}' added successfully.")

    def add_vehicle_to_hub(self, hub_name, vehicle):
        # checking if hub exists
        if hub_name not in self.hubs:
            print("Hub does not exist.")
            return

        ''' prevent duplicate Vehicle IDs in the same hub
        Extract existing vehicle IDs using list comprehension '''

        existing_ids = [v.vehicle_id for v in self.hubs[hub_name]]

        # Check for duplicate ID
        if vehicle.vehicle_id in existing_ids:
            print(
                f"Duplicate Vehicle ID '{vehicle.vehicle_id}' not allowed in '{hub_name}' hub."
            )
            return

        # if no duplicate then  add vehicle
        self.hubs[hub_name].append(vehicle)
        print(f"Vehicle added to '{hub_name}' hub successfully.")

    def display_hubs(self):
        # Display each hub
        for hub, vehicles in self.hubs.items():
            print(f"{hub} -> {len(vehicles)} vehicles")

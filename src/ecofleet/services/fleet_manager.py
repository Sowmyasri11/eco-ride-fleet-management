from src.ecofleet.models.electric_car import ElectricCar
from src.ecofleet.models.electric_scooter import ElectricScooter


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

    # search & return all vehicles present in  particular hub
    def search_vehicles_by_hub(self, hub_name):
        if hub_name not in self.hubs:
            print("Hub does not exist.")
            return []

        return self.hubs[hub_name]

    # searching  vehicles across all hubs with battery percentage greater than 80%
    def search_high_battery_vehicles(self):
        # flatten all  lists and filter using lambda
        return list(
            filter(
                lambda v: v.get_battery_percentage() > 80,
                [vehicle for vehicles in self.hubs.values() for vehicle in vehicles]
            )
        )

    def categorized_view(self):

        '''
        Displaying vehicles grouped by their type (Car/Scooter)
        it return a dictionary : type -> list of vehicles
        '''

        categorized = {"ElectricCar": [], "ElectricScooter": []}

        # traverse through all hubs and vehicles
        for vehicles in self.hubs.values():
            for v in vehicles:
                if isinstance(v, ElectricCar):
                    categorized["ElectricCar"].append(v)
                elif isinstance(v, ElectricScooter):
                    categorized["ElectricScooter"].append(v)

            # display the vehicles
            print("Categorized view")
            for v_type, v_list in categorized.items():
                print(f"\n{v_type}s ({len(v_list)}):")
                for v in v_list:
                    print(f"- {v.vehicle_id} | {v.model} | Battery: {v.get_battery_percentage()}%")

        return categorized

    # provides info about vehicle status across all hubs
    def get_vehicle_status_count(self):

        status_count={
            "Available":0,
            "On Trip":0,
            "Under Maintenance":0
        }

        for vehicles in self.hubs.values():
            for vehicle in vehicles:
                status=vehicle.get_maintenance_status()
                if status in status_count:
                    status_count[status]+=1

        return status_count

     # to display the fleet status summary
    def display_status_summary(self):

        status_count = self.get_vehicle_status_count()

        print("\n Fleet Status Summary:")

        for status, count in status_count.items():
            print(f"{status} : {count} vehicles\n")    #print(f"{status:<20}: {count}")

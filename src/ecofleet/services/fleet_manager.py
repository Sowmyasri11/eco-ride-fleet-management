import csv
import json
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

        status_count = {
            "Available": 0,
            "On Trip": 0,
            "Under Maintenance": 0
        }

        for vehicles in self.hubs.values():
            for vehicle in vehicles:
                status = vehicle.get_maintenance_status()
                if status in status_count:
                    status_count[status] += 1

        return status_count

    # to display the fleet status summary
    def display_status_summary(self):

        status_count = self.get_vehicle_status_count()

        print("\n Fleet Status Summary:")

        for status, count in status_count.items():
            print(f"{status} : {count} vehicles\n")  # print(f"{status:<20}: {count}")

    # sorting vehicles in a hub based on model name
    def sort_vehicles_by_model(self, hub_name):
        if hub_name not in self.hubs:
            print("Hub does not exist.")
            return

        vehicles = self.hubs[hub_name]

        if not vehicles:
            print("No vehicles available in this hub. ")
            return

        vehicles.sort(key=lambda vehicle: vehicle.model)

        print(f"Vehicles in '{hub_name}' hub sorted by model:\n")
        for vehicle in vehicles:
            print(vehicle)

    # collects all vehicles from all hubs into a single list
    def get_all_vehicles(self):
        return [
            vehicle for vehicles in self.hubs.values() for vehicle in vehicles
        ]

    # sort vehicles based on battery percentage (descending order)
    def sort_vehicles_by_battery(self):
        all_vehicles = self.get_all_vehicles()

        return sorted(
            all_vehicles,
            key=lambda vehicle: vehicle.get_battery_percentage(),
            reverse=True
        )

    # sorting vehicle based on rental price
    def sort_vehicles_by_rental_price(self):
        all_vehicles = self.get_all_vehicles()
        return sorted(
            all_vehicles,
            key=lambda vehicle: vehicle.get_rental_price(),
            reverse=True
        )

    # exporting all fleet data in to a csv file
    def export_fleet_to_csv(self, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow([
                "hub_name",
                "vehicle_type",
                "vehicle_id",
                "model",
                "battery_percentage",
                "maintenance_status",
                "rental_price",
                "extra_attribute"
            ])

            for hub_name, vehicles in self.hubs.items():
                for vehicle in vehicles:
                    if isinstance(vehicle, ElectricCar):
                        vehicle_type = "ElectricCar"
                        extra_value = vehicle.seating_capacity
                    elif isinstance(vehicle, ElectricScooter):
                        vehicle_type = "ElectricScooter"
                        extra_value = vehicle.max_speed_limit
                    else:
                        continue

                    writer.writerow([
                        hub_name,
                        vehicle_type,
                        vehicle.vehicle_id,
                        vehicle.model,
                        vehicle.get_battery_percentage(),
                        vehicle.get_maintenance_status(),
                        vehicle.get_rental_price(),
                        extra_value
                    ])

            print("Fleet data exported successfully")

    # Importing fleet data from CSV file into the system
    def import_fleet_from_csv(self, file_path):

        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                hub_name = row["hub_name"]

                if hub_name not in self.hubs:
                    self.hubs[hub_name] = []

                if row["vehicle_type"] == "ElectricCar":
                    vehicle = ElectricCar(
                        row["vehicle_id"],
                        row["model"],
                        int(row["battery_percentage"]),
                        row["maintenance_status"],
                        float(row["rental_price"]),
                        int(row["extra_attribute"])
                    )

                elif row["vehicle_type"] == "ElectricScooter":
                    vehicle = ElectricScooter(
                        row["vehicle_id"],
                        row["model"],
                        int(row["battery_percentage"]),
                        row["maintenance_status"],
                        float(row["rental_price"]),
                        int(row["extra_attribute"])
                    )
                else:
                    continue

                self.hubs[hub_name].append(vehicle)

        print("Fleet data imported successfully from CSV.")

    def export_fleet_to_json(self, file_path):

        fleet_data = {}

        for hub_name, vehicles in self.hubs.items():
            fleet_data[hub_name] = []

            for vehicle in vehicles:
                vehicle_dict = {
                    "vehicle_id": vehicle.vehicle_id,
                    "model": vehicle.model,
                    "battery_percentage": vehicle.get_battery_percentage(),
                    "maintenance_status": vehicle.get_maintenance_status(),
                    "rental_price": vehicle.get_rental_price(),
                }

                if isinstance(vehicle, ElectricCar):
                    vehicle_dict["vehicle_type"] = "ElectricCar"
                    vehicle_dict["seating_capacity"] = vehicle.seating_capacity
                elif isinstance(vehicle, ElectricScooter):
                    vehicle_dict["vehicle_type"] = "ElectricScooter"
                    vehicle_dict["max_speed_limit"] = vehicle.max_speed_limit

                fleet_data[hub_name].append(vehicle_dict)

        with open(file_path, 'w') as file:
            json.dump(fleet_data, file, indent=4)

        print("fleet data exported successfully to JSON")

    #Import fleet data from JSON file into the system
    def import_fleet_from_json(self, file_path):
        with open(file_path, mode="r") as file:
            fleet_data = json.load(file)

        self.hubs.clear()

        for hub_name, vehicles in fleet_data.items():
            self.hubs[hub_name] = []

            for v in vehicles:
                if v["vehicle_type"] == "ElectricCar":
                    vehicle = ElectricCar(
                        v["vehicle_id"],
                        v["model"],
                        v["battery_percentage"],
                        v["maintenance_status"],
                        v["rental_price"],
                        v["seating_capacity"]
                    )

                elif v["vehicle_type"] == "ElectricScooter":
                    vehicle = ElectricScooter(
                        v["vehicle_id"],
                        v["model"],
                        v["battery_percentage"],
                        v["maintenance_status"],
                        v["rental_price"],
                        v["max_speed_limit"]
                    )
                else:
                    continue

                self.hubs[hub_name].append(vehicle)

        print("Fleet data imported successfully from JSON.")

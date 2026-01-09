from src.ecofleet.models.electric_car import ElectricCar
from src.ecofleet.models.electric_scooter import ElectricScooter
from src.ecofleet.services.fleet_manager import FleetManager


def display_menu():
    print("\n========= Eco-Ride Fleet Management =========")
    print("1. Add Hub")
    print("2. Add Vehicle")
    print("3. Display Hubs")
    print("4. Search Vehicles by Hub")
    print("5. Search High Battery Vehicles (>80%)")
    print("6. Categorized View")
    print("7. Vehicle Status Summary")
    print("8. Sort Vehicles by Model")
    print("9. Sort Vehicles by Battery")
    print("10. Sort Vehicles by Rental Price")
    print("11. Export Fleet to CSV")
    print("12. Import Fleet from CSV")
    print("13. Export Fleet to JSON")
    print("14. Import Fleet from JSON")
    print("0. Exit")


def main():
    print("\nWelcome to Eco-Ride Urban Mobility System")
    fleet_manager = FleetManager()

    while True:
        display_menu()
        choice = input("\nEnter your choice: ")

        try:
            if choice == "1":
                hub_name = input("Enter hub name: ")
                fleet_manager.add_hub(hub_name)

            elif choice == "2":
                hub_name = input("Enter hub name: ")
                vehicle_type = input("Enter vehicle type (car/scooter): ").lower()

                vehicle_id = input("Vehicle ID: ")
                model = input("Model Name: ")
                battery = int(input("Battery Percentage: "))
                status = input("Status (Available/On Trip/Under Maintenance): ")
                price = float(input("Rental Price: "))

                if vehicle_type == "car":
                    seating = int(input("Seating Capacity: "))
                    vehicle = ElectricCar(
                        vehicle_id, model, battery, status, price, seating
                    )

                elif vehicle_type == "scooter":
                    speed = int(input("Max Speed Limit: "))
                    vehicle = ElectricScooter(
                        vehicle_id, model, battery, status, price, speed
                    )
                else:
                    print("Invalid vehicle type")
                    continue

                fleet_manager.add_vehicle_to_hub(hub_name, vehicle)

            elif choice == "3":
                fleet_manager.display_hubs()

            elif choice == "4":
                hub = input("Enter hub name: ")
                vehicles = fleet_manager.search_vehicles_by_hub(hub)
                for v in vehicles:
                    print(v)

            elif choice == "5":
                vehicles = fleet_manager.search_high_battery_vehicles()
                for v in vehicles:
                    print(v)

            elif choice == "6":
                fleet_manager.categorized_view()

            elif choice == "7":
                fleet_manager.display_status_summary()

            elif choice == "8":
                hub = input("Enter hub name: ")
                fleet_manager.sort_vehicles_by_model(hub)

            elif choice == "9":
                vehicles = fleet_manager.sort_vehicles_by_battery()
                fleet_manager.display_sorted_vehicles(
                    vehicles, "Sorted by Battery Level"
                )

            elif choice == "10":
                vehicles = fleet_manager.sort_vehicles_by_rental_price()
                fleet_manager.display_sorted_vehicles(
                    vehicles, "Sorted by Rental Price"
                )

            elif choice == "11":
                fleet_manager.export_fleet_to_csv("fleet_data.csv")

            elif choice == "12":
                fleet_manager.import_fleet_from_csv("fleet_data.csv")

            elif choice == "13":
                fleet_manager.export_fleet_to_json("fleet_data.json")

            elif choice == "14":
                fleet_manager.import_fleet_from_json("fleet_data.json")

            elif choice == "0":
                print("Exiting system. Thank you!")
                break

            else:
                print("Invalid choice. Try again.")

        except ValueError as ve:
            print(f"Input error: {ve}")

        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()

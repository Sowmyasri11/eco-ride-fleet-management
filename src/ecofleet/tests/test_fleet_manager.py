import pytest
import os
from src.ecofleet.services.fleet_manager import FleetManager
from src.ecofleet.models.electric_car import ElectricCar
from src.ecofleet.models.electric_scooter import ElectricScooter


@pytest.fixture
def fleet():
    """
        Fixture to set up a FleetManager instance with:
        - Multiple hubs
        - Electric cars and scooters
        - Preloaded vehicles for reuse across test cases
        """
    fm = FleetManager()
    # Create initial hubs
    hubs = ["Hyderabad", "Delhi", "Bangalore", "Mumbai", "Chennai"]
    for hub in hubs:
        fm.add_hub(hub)

    # Create vehicle objects
    car1 = ElectricCar("EC101", "Tesla", 90, "Available", 500, 5)
    car2 = ElectricCar("EC102", "Nexon", 70, "Available", 400, 5)
    scooter1 = ElectricScooter("ES201", "Ather", 85, "Available", 200, 90)
    scooter2 = ElectricScooter("ES202", "Ola", 60, "Available", 180, 85)

    # Add vehicles to hubs
    fm.add_vehicle_to_hub("Hyderabad", car1)
    fm.add_vehicle_to_hub("Hyderabad", scooter1)
    fm.add_vehicle_to_hub("Delhi", car2)
    fm.add_vehicle_to_hub("Bangalore", scooter2)

    return fm, car1, car2, scooter1, scooter2

def test_add_hub(fleet):
    """
       Verify that a new hub can be added successfully
       and is present in the FleetManager hubs dictionary.
    """
    fm, *_ = fleet
    fm.add_hub("Pune")
    assert "Pune" in fm.hubs

#testing duplicate prevention
def test_duplicate_vehicle_not_allowed(fleet):
    """
        Ensure that duplicate vehicles (same vehicle_id)
        are not added to the same hub.
    """
    fm, car1, *_ = fleet
    fm.add_vehicle_to_hub("Hyderabad", car1)
    assert fm.hubs["Hyderabad"].count(car1) == 1

def test_search_vehicles_by_hub(fleet):
    """
        Validate that vehicles can be retrieved
        correctly based on hub name.
    """
    fm, *_ = fleet
    vehicles = fm.search_vehicles_by_hub("Hyderabad")
    assert len(vehicles) == 2

def test_search_high_battery_vehicles(fleet):
    """
    Confirm that vehicles with battery percentage
    greater than 80% are correctly filtered.
    """
    fm, car1, *_ = fleet
    result = fm.search_high_battery_vehicles()

    assert car1 in result
    for v in result:
        assert v.get_battery_percentage() > 80



#testing categorized view
def test_categorized_view(fleet):
    fm, car1, _, scooter1, _ = fleet
    categories = fm.categorized_view()

    assert car1 in categories["ElectricCar"]
    assert scooter1 in categories["ElectricScooter"]


#testing vehicle status count
def test_vehicle_status_count(fleet):
    """
       Verify accurate counting of vehicle maintenance
       status across all hubs.
    """
    fm, car1, _, scooter1, _ = fleet
    car1.set_maintenance_status("On Trip")
    scooter1.set_maintenance_status("Under Maintenance")

    status = fm.get_vehicle_status_count()
    assert status["On Trip"] == 1
    assert status["Under Maintenance"] == 1

def test_sort_vehicles_by_model(fleet):
    """
    Ensure vehicles inside a hub are sorted
    alphabetically by model name.
    """
    fm, *_ = fleet
    fm.sort_vehicles_by_model("Hyderabad")

    models = [v.model for v in fm.hubs["Hyderabad"]]
    assert models == sorted(models)

def test_get_all_vehicles(fleet):
    """
    Validate that all vehicles from all hubs
    are collected into a single list.
    """
    fm, *_ = fleet
    all_vehicles = fm.get_all_vehicles()
    assert len(all_vehicles) == 4

def test_sort_vehicles_by_battery(fleet):
    """
    Confirm vehicles are sorted in descending
    order based on battery percentage.
    """
    fm, *_ = fleet
    sorted_list = fm.sort_vehicles_by_battery()

    batteries = [v.get_battery_percentage() for v in sorted_list]
    assert batteries == sorted(batteries, reverse=True)

def test_sort_vehicles_by_rental_price(fleet):
    """
    Ensure vehicles are sorted by rental price
    from highest to lowest.
    """
    fm, *_ = fleet
    sorted_list = fm.sort_vehicles_by_rental_price()

    prices = [v.get_rental_price() for v in sorted_list]
    assert prices == sorted(prices, reverse=True)

def test_export_import_csv(fleet):
    """
    Test exporting fleet data to CSV and
    importing it back without data loss.
    """
    fm, *_ = fleet
    file = "fleet_test.csv"

    fm.export_fleet_to_csv(file)

    new_fm = FleetManager()
    new_fm.import_fleet_from_csv(file)

    assert len(new_fm.get_all_vehicles()) == 4
    os.remove(file)

def test_export_import_json(fleet):
    """
    Test exporting fleet data to JSON and
    importing it back successfully.
    """
    fm, *_ = fleet
    file = "fleet_test.json"

    fm.export_fleet_to_json(file)

    new_fm = FleetManager()
    new_fm.import_fleet_from_json(file)

    assert len(new_fm.get_all_vehicles()) == 4
    os.remove(file)

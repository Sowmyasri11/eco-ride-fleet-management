import pytest
import os
from src.ecofleet.services.fleet_manager import FleetManager
from src.ecofleet.models.electric_car import ElectricCar
from src.ecofleet.models.electric_scooter import ElectricScooter


@pytest.fixture
def fleet():
    fm = FleetManager()

    hubs = ["Hyderabad", "Delhi", "Bangalore", "Mumbai", "Chennai"]
    for hub in hubs:
        fm.add_hub(hub)

    car1 = ElectricCar("EC101", "Tesla", 90, "Available", 500, 5)
    car2 = ElectricCar("EC102", "Nexon", 70, "Available", 400, 5)
    scooter1 = ElectricScooter("ES201", "Ather", 85, "Available", 200, 90)
    scooter2 = ElectricScooter("ES202", "Ola", 60, "Available", 180, 85)

    fm.add_vehicle_to_hub("Hyderabad", car1)
    fm.add_vehicle_to_hub("Hyderabad", scooter1)
    fm.add_vehicle_to_hub("Delhi", car2)
    fm.add_vehicle_to_hub("Bangalore", scooter2)

    return fm, car1, car2, scooter1, scooter2

def test_add_hub(fleet):
    fm, *_ = fleet
    fm.add_hub("Pune")
    assert "Pune" in fm.hubs

#testing duplicate prevention
def test_duplicate_vehicle_not_allowed(fleet):
    fm, car1, *_ = fleet
    fm.add_vehicle_to_hub("Hyderabad", car1)
    assert fm.hubs["Hyderabad"].count(car1) == 1

def test_search_vehicles_by_hub(fleet):
    fm, *_ = fleet
    vehicles = fm.search_vehicles_by_hub("Hyderabad")
    assert len(vehicles) == 2


#testing categorized view
def test_categorized_view(fleet):
    fm, car1, _, scooter1, _ = fleet
    categories = fm.categorized_view()

    assert car1 in categories["ElectricCar"]
    assert scooter1 in categories["ElectricScooter"]

#testing vehicle status count
def test_vehicle_status_count(fleet):
    fm, car1, _, scooter1, _ = fleet
    car1.set_maintenance_status("On Trip")
    scooter1.set_maintenance_status("Under Maintenance")

    status = fm.get_vehicle_status_count()
    assert status["On Trip"] == 1
    assert status["Under Maintenance"] == 1


from src.ecofleet.services.fleet_manager import FleetManager
import pytest


@pytest.fixture(scope="module")
def fleet():
    return FleetManager()


# add_hub using parameterize
@pytest.mark.parametrize("hub_name", [
    "Hyderabad",
    "Delhi",
    "Bangalore",
    "Mumbai",
    "Chennai"
])
def test_add_hub(fleet, hub_name):
    fleet.add_hub(hub_name)
    assert hub_name in fleet.hubs
    assert fleet.hubs[hub_name] == []


@pytest.mark.parametrize("hub, vehicle", [
    ("Hyderabad", "Car-101"),
    ("Hyderabad", "Bike-102"),
    ("Delhi", "Car-201"),
    ("Delhi", "Bike-202"),
    ("Bangalore", "Car-301"),
    ("Mumbai", "Car-401"),
    ("Chennai", "Bike-501")
])
def test_add_vehicle_to_hub(fleet, hub, vehicle):
    fleet.add_vehicle_to_hub(hub, vehicle)
    assert vehicle in fleet.hubs[hub]

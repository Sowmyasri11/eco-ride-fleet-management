import pytest
from src.ecofleet.models.electric_car import ElectricCar
from src.ecofleet.models.electric_scooter import ElectricScooter


def test_electric_car_trip_cost():
    car = ElectricCar("EC101", "Tesla", 90, "Available", 500, 5)
    cost = car.calculate_trip_cost(10)
    assert cost == 5.0 + (0.5 * 10)


def test_electric_scooter_trip_cost():
    scooter = ElectricScooter("ES201", "Ather", 80, "Available", 200, 90)
    cost = scooter.calculate_trip_cost(20)
    assert cost == 1.0 + (0.15 * 20)


def test_vehicle_battery_validation():
    with pytest.raises(ValueError):
        ElectricCar("EC999", "Invalid", 120, "Available", 500, 5)


def test_vehicle_rental_price():
    car = ElectricCar("EC102", "Nexon", 70, "Available", 400, 5)
    assert car.get_rental_price() == 400

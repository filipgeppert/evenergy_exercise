from main import create_charging_schedule, create_low_tariff_connection_schedule
import numpy as np
from datetime import datetime


class TestCreateLowTariffConnectionSchedule:
    def test_create_low_tariff_schedule_same_day(self):
        low_price_tariff = np.array(
            [0] * 30
            + [1] * 7 * 60
            + [0] * (16 * 60 + 30)
        )
        schedule = create_low_tariff_connection_schedule(
            low_price_daily_tariff=low_price_tariff,
            plug_in_time=datetime.fromisoformat("2019-10-04T00:00:00"),
            ready_by=datetime.fromisoformat("2019-10-04T10:00:00")
        )

        correct_schedule = np.array(
            [0] * 30 + [1] * 7 * 60 + [0] * (2 * 60 + 30)
        )
        assert np.array_equal(schedule, correct_schedule)

    def test_create_low_tariff_schedule_overnight(self):
        low_price_tariff = np.array(
            [0] * 30
            + [1] * 7 * 60
            + [0] * (16 * 60 + 30)
        )
        schedule = create_low_tariff_connection_schedule(
            low_price_daily_tariff=low_price_tariff,
            plug_in_time=datetime.fromisoformat("2019-10-04T23:30:00"),
            ready_by=datetime.fromisoformat("2019-10-05T08:00:00")
        )

        correct_schedule = np.array(
            [0] * 60 + [1] * 7 * 60 + [0] * 30
        )
        assert np.array_equal(schedule, correct_schedule)


class TestCreateChargingSchedule:
    def test_charging_overnight(self):
        schedule = create_charging_schedule(
            plug_in_time="2019-10-04T18:00:00",
            charge_time=300,
            ready_by="2019-10-05T07:00:00"
        )

        assert schedule.sum() == 300
        assert schedule.size == 60 * 13

    def test_charging_overnight_not_enough_time(self):
        schedule = create_charging_schedule(
            plug_in_time="2019-10-04T23:00:00",
            charge_time=300,
            ready_by="2019-10-05T01:00:00"
        )

        assert schedule.sum() == 60 * 2
        assert schedule.size == 60 * 2

    def test_charging_same_day(self):
        schedule = create_charging_schedule(
            plug_in_time="2019-10-05T07:00:00",
            charge_time=300,
            ready_by="2019-10-05T15:00:00"
        )

        assert schedule.sum() == 300
        assert schedule.size == 60 * 8

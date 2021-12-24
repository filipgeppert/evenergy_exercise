from datetime import datetime, timedelta, time

import numpy as np

ConnectionSchedule = np.ndarray


class InvalidInputError(Exception):
    pass


def is_the_same_day(date_one: datetime, date_two: datetime) -> bool:
    return date_one.date() == date_two.date()


def minutes_until_end_of_day(dt: datetime) -> int:
    day_after = dt + timedelta(days=1)
    return int((datetime.combine(date=day_after, time=time.min, tzinfo=day_after.tzinfo) - dt).seconds / 60)


def minutes_from_day_start(dt: datetime) -> int:
    day_before = dt - timedelta(days=1)
    return int((dt - datetime.combine(date=day_before, time=time.max, tzinfo=day_before.tzinfo)).seconds / 60)


def create_low_tariff_connection_schedule(
        low_price_daily_tariff: np.ndarray, plug_in_time: datetime, ready_by: datetime
) -> np.ndarray:
    minute_of_a_day = minutes_from_day_start(plug_in_time)
    if is_the_same_day(plug_in_time, ready_by):
        minutes_from_midnight = minutes_from_day_start(ready_by)
        connection_schedule_low_tariff = low_price_daily_tariff[minute_of_a_day:minutes_from_midnight]
    else:
        minutes_from_midnight = minutes_from_day_start(ready_by)
        connection_schedule_low_tariff = np.concatenate(
            (low_price_daily_tariff[minute_of_a_day:], low_price_daily_tariff[:minutes_from_midnight])
        )
    return connection_schedule_low_tariff


def create_charging_schedule(ready_by: str, charge_time: int, plug_in_time: str) -> ConnectionSchedule:
    connection_time = datetime.fromisoformat(plug_in_time)
    ready_time = datetime.fromisoformat(ready_by)

    if connection_time.tzinfo != ready_time.tzinfo:
        raise InvalidInputError("Plug in and ready time timezones are different.")
    if (ready_time - connection_time).total_seconds() / 3600 > 24:
        raise InvalidInputError("Max duration exceeded 24 hours limit.")

    low_price_tariff = np.array(
        [0] * 30
        + [1] * 7 * 60
        + [0] * (16 * 60 + 30)
    )

    connection_schedule_low_tariff = create_low_tariff_connection_schedule(
        low_price_daily_tariff=low_price_tariff,
        plug_in_time=connection_time,
        ready_by=ready_time
    )

    # Check if there's enough time to charge with low rate
    if connection_schedule_low_tariff.size < charge_time:
        # Connection time is lower than charging time. Full charge impossible.
        # Return charge start -> right away
        connection_schedule = np.ones(connection_schedule_low_tariff.size)
        return connection_schedule

    available_minutes_in_low_tariff = connection_schedule_low_tariff.sum()
    # Array containing elements: 1 - charging, 0 - not charging
    connection_schedule = connection_schedule_low_tariff.copy()

    if available_minutes_in_low_tariff == charge_time:
        return connection_schedule

    if available_minutes_in_low_tariff < charge_time:
        # Connection time in low tariff lower than charging time. Charging from high tariff.
        remaining_charging_minutes = charge_time - available_minutes_in_low_tariff
        # Prioritize charging close to unplug time
        indexes = np.nonzero(connection_schedule == 0)[0][-remaining_charging_minutes:]
        connection_schedule[indexes] = 1
        return connection_schedule

    if available_minutes_in_low_tariff > charge_time:
        # Charge as long as it's necessary
        minute_surplus = available_minutes_in_low_tariff - charge_time
        # Prioritize charging close to unplug time
        indexes = np.nonzero(connection_schedule)[0][:minute_surplus]
        connection_schedule[indexes] = 0
        return connection_schedule


if __name__ == "__main__":
    schedule = create_charging_schedule(
        plug_in_time="2019-10-04T18:42:00+00:00",
        charge_time=300,
        ready_by="2019-10-05T07:00:00+00:00"
    )
    print(f"Connection schedule:\n{schedule}")
    print(f"Total charging minutes: {schedule.sum()}")
    print(f"Total schedule duration (minutes): {schedule.size}")

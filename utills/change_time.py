from datetime import timedelta, date, datetime
import pytz


class ChangeTime:
    def __init__(self, base_datetime, time_speed_factor=144):
        self._base_datetime = base_datetime
        self._time_speed_factor = time_speed_factor

    def get_base_date(self):
        return self._base_datetime

    def get_time_speed_factor(self):
        return self._time_speed_factor

    def changed_today(self):
        real_datetime = datetime.now()
        base_datetime = self.get_base_date()
        time_diff = (real_datetime - base_datetime)
        time_diff_changed = time_diff * self.get_time_speed_factor()
        new_datetime = base_datetime + time_diff_changed

        print(f"Changed today info:")
        print(f"        real_datetime: {real_datetime}")
        print(f"    base_datetime: {base_datetime}")
        print(f"    time_diff: {time_diff}")
        print(f"    time_diff_changed: {time_diff_changed}")
        print(f"    new_datetime: {new_datetime}")

        return new_datetime.date()

    @classmethod
    def constant_today(cls, constant_date):
        try:
            # In case datetime input
            return constant_date.date()
        except:
            # In case date input
            return constant_date

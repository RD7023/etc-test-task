from datetime import timedelta, date, datetime
import pytz
timezone = pytz.timezone("Europe/Kiev")


class ChangeTime:
    def __init__(self, base_datetime, time_speed_factor=144):
        self._base_datetime = base_datetime
        self._time_speed_factor = time_speed_factor

    def get_base_date(self):
        return self._base_datetime

    def get_time_speed_factor(self):
        return self._time_speed_factor

    def changed_today(self):
        real_datetime = timezone.localize(datetime.now())
        base_datetime = self.get_base_date()
        seconds_diff = (real_datetime - base_datetime).seconds
        new_datetime = base_datetime + timedelta(seconds=seconds_diff*self.get_time_speed_factor())

        print(f"Changed today info:")
        print(f"    real_datetime: {real_datetime}")
        print(f"    base_datetime: {base_datetime}")
        print(f"    seconds_diff: {seconds_diff}")
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

from datetime import timedelta, date

import pytz
timezone = pytz.timezone("Europe/Kiev")
class DateUtils:
    possible_days = ['Mo', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    @staticmethod
    def get_next_days(n_days, start_date):
        next_days = []
        for i in range(n_days):
            next_days.append(start_date + timedelta(days=i+1))

        return next_days

    @staticmethod
    def get_next_valid_day(current_due_date, period_days, current_day, to_reverse, n_days):

        if len(period_days) > 0:

            next_days = DateUtils.get_next_days(n_days, current_due_date)
            if to_reverse:
                next_days = next_days[::-1]

            for next_day in next_days:
                if (next_day > current_day) and (DateUtils.possible_days[next_day.weekday()] in period_days):
                    return next_day

            next_days = DateUtils.get_next_days(n_days, current_day)
            if to_reverse:
                next_days = next_days[::-1]

            for next_day in next_days:
                if DateUtils.possible_days[next_day.weekday()] in period_days:
                    return next_day
        else:
            next_days = DateUtils.get_next_days(n_days, current_due_date)
            if to_reverse:
                next_days = next_days[::-1]

            for next_day in next_days[:1]:
                if next_day > current_day:
                    return next_day

            next_days = DateUtils.get_next_days(n_days, current_day)
            if to_reverse:
                next_days = next_days[::-1]
            return next_days[0]

    @classmethod
    def eval_new_due_date(cls, current_due_date, period_freq, period_days, current_day):

        if period_freq == "Daily":
            return current_day

        if period_freq[1:] == "t/w":
            return cls.get_next_valid_day(current_due_date, period_days, current_day, to_reverse=False, n_days=7)

        if period_freq[1:] == "t/2w":
            return cls.get_next_valid_day(current_due_date, period_days, current_day, to_reverse=True, n_days=14)

        if period_freq == "2t/m":
            return cls.get_next_valid_day(current_due_date, period_days, current_day, to_reverse=True, n_days=16)

        if period_freq == "1t/m":
            return cls.get_next_valid_day(current_due_date, period_days, current_day, to_reverse=True, n_days=31)

        if period_freq == "1t/2m":
            return cls.get_next_valid_day(current_due_date, period_days, current_day, to_reverse=True, n_days=62)

        if period_freq == "1t/3m":
            return cls.get_next_valid_day(current_due_date, period_days, current_day, to_reverse=True, n_days=93)

    @classmethod
    def eval_new_set_date(cls, due_date, period_freq):
        if period_freq == "Daily":
            return due_date

        if period_freq[1:] == "t/w":
            return due_date - timedelta(days=1)

        if period_freq[1:] == "t/2w":
            return due_date - timedelta(days=3)

        if period_freq[1:] == "t/m":
            return due_date - timedelta(days=7)

        if (period_freq[1:] == "t/2m") or (period_freq[1:] == "t/3m"):
            return due_date - timedelta(days=14)


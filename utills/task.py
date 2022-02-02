import notion
timezone = "Europe/Kiev"


class Task:

    possible_status_values = ["TO DO", "DONE"]
    periodicity_freq_options = ["Daily", "3t/w", "2t/w", "1t/w",
                                "1t/2w", "2t/m", "1t/m", "1t/2m",
                                "1t/3m"]

    def __init__(self, notion_obj):
        self._notion_obj = notion_obj

    def get_task_text(self):
        try:
            return self._notion_obj.title
        except:
            return None

    def get_status(self):
        try:
            return self._notion_obj.status
        except:
            return None

    def get_periodicity(self):
        try:
            return self._notion_obj.periodicity
        except:
            return None

    def get_periodicity_freq(self):
        try:
            for val in self.get_periodicity():
                if val in self.periodicity_freq_options:
                    return val
        except:
            return None

    def get_periodicity_days(self):
        try:
            return [val for val in self.get_periodicity() if val not in self.periodicity_freq_options]
        except:
            return None

    def get_set_date(self):
        try:
            return self._notion_obj.set_date.start
        except:
            return None

    def get_due_date(self):
        try:
            return self._notion_obj.due_date.start
        except:
            return None

    def set_status(self, status):
        try:
            if status in self.possible_status_values:
                self._notion_obj.status = status
            else:
                print(f"Not valid status: {status}")
        except:
            pass

    def set_due_date(self, date_value):
        try:
            self._notion_obj.due_date = notion.collection.NotionDate(date_value, timezone=timezone)
        except:
            pass

    def set_set_date(self, date_value):
        try:
            self._notion_obj.set_date = notion.collection.NotionDate(date_value, timezone=timezone)
        except:
            pass

    @staticmethod
    def filter_done_tasks(tasks):
        return [task for task in tasks if task.get_status() == "DONE"]

    @staticmethod
    def filter_periodic_tasks(tasks):
        return [task for task in tasks if not task.get_periodicity_freq() is None]


import os
from flask import Flask
from datetime import datetime, date
import pytz

from notion.client import NotionClient
from utills.task import Task
from utills.date_utils import DateUtils
from utills.change_time import ChangeTime


timezone = pytz.timezone("Europe/Kiev")

token_v2 = os.environ.get("TOKEN")
table_url = os.environ.get("URL")


# Obtain the `token_v2` value by inspecting your browser cookies on a logged-in (non-guest) session on Notion.so
client = NotionClient(token_v2=token_v2)
change_time = ChangeTime(base_datetime=timezone.localize(datetime(2022, 2, 2, 10, 0, 0)))


app = Flask(__name__)


@app.route("/updateTasks", methods=["GET"])
def update_tasks():
    # Last Update
    page = client.get_block(table_url)
    cv = client.get_collection_view(table_url)
    collection_elements = cv.collection.get_rows()

    tasks = [Task(col_el) for col_el in collection_elements]

    filtred_tasks = Task.filter_periodic_tasks(Task.filter_done_tasks(tasks))

    # regular_today = date.today()
    changed_today = change_time.changed_today()
    # constant_today = change_time.constant_today(date(2022, 2, 25))

    today = changed_today

    # Update Page info
    page.title = f"Task board (Last update: {today})"
    for task in filtred_tasks:
        try:
            # print("Changed today:", changed_today)
            # print("Constant today:", constant_today)
            print("Today's date:", today)
            print("Set date:", task.get_set_date())

            if task.get_set_date() > today:
                print("-" * 20)
                continue

            if task.get_set_date() < today:
                due_date = task.get_due_date()
                period_freq = task.get_periodicity_freq()
                period_days = task.get_periodicity_days()

                print("Due date: ", due_date)
                print("Freq: ", period_freq)
                print("Days: ", period_days)

                new_due_date = DateUtils.eval_new_due_date(due_date, period_freq, period_days, today)
                new_set_date = DateUtils.eval_new_set_date(new_due_date, period_freq)

                task.set_due_date(new_due_date)
                task.set_set_date(new_set_date)

            if task.get_set_date() == today:
                task.set_status("TO DO")

            print("After Update:")
            print("New Due:", task.get_due_date())
            print("New Set:", task.get_set_date())
            print("New Status: ", task.get_status())
            print("-" * 20)

        except:
            pass

    return "Updated Tasks"


if __name__ == "__main__":

    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
from flask_table import Table, Col
from markupsafe import Markup


# Declare your table
class ShiftTable(Table):
    time = Col('Time')
    description = Col('Description')
    command = Col('Command')

class Task(object):
    def __init__(self, time, description, command):
        self.time = time
        self.description = description
        self.command = command


if  __name__ == "__main__":
    # Get some objects
    tasks = [Task('Name1', 'Description1', 'Command1'),
             Task('Name2', 'Description2', 'Command2'),
             Task('Name3', 'Description3', "Command3")]

    # Populate the table
    table = ShiftTable(tasks)

    print(table.__html__())

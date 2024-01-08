from zipfile import ZipFile
import json
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


class Shifts:
    def __init__(self, filename):
        self.filename = filename
        logging.debug(f'Reading {self.filename} as shifts file.')
        try:
            self.zipfile = ZipFile(self.filename, 'r')
        except:
            logging.critical(f'Unable to read {self.filename}!')

        # list of shifts without .json at the end
        self.shiftlist = []
        for shift in self.zipfile.namelist():
            self.shiftlist.append(shift[:-5])

        # task list for each shift
        self.tasklist = {}
        for shift in self.shiftlist:
            #print(shift)
            with self.zipfile.open(f'{shift}.json') as shift_json:
                self.tasklist[shift] = json.load(shift_json)
        print(self.tasklist.keys())


    def shift_list(self):
        return(self.shiftlist)
    
    def task_list(self, shift):
        print(shift)
        return self.tasklist[shift]



if __name__ == "__main__":
    shifts = Shifts('tmp/shift-definitions_04-01-2024_12-17-06.zip')
    shifts = shifts.shift_list()
    print(shifts)
    tasklist_G1 = shifts.task_list('G1_GVE_22-12-2023_08-29-53')
    print(tasklist_G1)


#@app.get("/v2/tasks4shift/")
#async def tasks4shift(filename, shiftname):
#    logging.debug(f"In tasks4shift with {filename} and {shiftname}")
#    # open zipfile and extract the json file corresponding to shiftname
#    with ZipFile(f'tmp/{filename}', 'r') as zipfile:
#        with zipfile.open(shiftname) as shift:
#            shift_task_list = json.load(shift)
#
#    # convert the json value to pandas dataframe
#    tasks = pd.json_normalize(shift_task_list['taskDefinitions'])
#    # set index to the id which is defined in LAMA ans is unique
#    tasks.set_index('id', inplace=True)
#    # remove unnecessary column in the pandas dataframe
#    tasks_cleaned = tasks.drop(['version',\
#                                'name',\
#                                'unit',\
#                                'commands',\
#                                'onDemand',\
#                                'allowedStartTime',\
#                                'duration',\
#                                'schedule.startDate',\
#                                'schedule.endDate',\
#                                'schedule.expression',\
#                                'auditData.createdBy',\
#                                'auditData.createdTime',\
#                                'auditData.lastModifiedBy',\
#                                'auditData.lastModifiedTime'],\
#                                axis=1)
#    # reorder the columns
#    tasks_ordered = tasks_cleaned.loc[:,['intendedStartTime','zoneId','description']]
#    # convert the pandas dataframe to a list
#    task_list = np.array(tasks_ordered).tolist()
#    # insert the header for the columns
#    task_list.insert(0,['Start time', 'Locale', 'Description'])
#
#    t1 = pdf(task_list)
#
#    return t1

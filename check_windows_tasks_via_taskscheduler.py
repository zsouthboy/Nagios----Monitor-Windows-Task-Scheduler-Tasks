import os
import csv
import datetime

VERSION = "1.01 2010-09-27" #CAF

#this dictionary is the name of the task registered in task scheduler
#and the number of minutes before calling that task stuck
DICT_OF_TASKS = {"some named task" : 30, 
                 "another task that runs once a day" : 1500,                  
                 "task that had better complete quickly" : 5 
                 }

def is_currently_out_of_date(data, max_minutes):
    #returns the time in minutes since the given time
    #example data: 12:08:00 AM, 9/27/2010
    that_date = datetime.datetime.strptime(data, "%I:%M:%S %p, %m/%d/%Y")
    
    difference = datetime.timedelta(minutes=max_minutes)
    if datetime.datetime.today() - difference > that_date:
        return True
    
    return False

def main():
    global DICT_OF_TASKS
    #dump task sched tasks to a csv
    result = os.system('schtasks /query /v /fo csv > C:\\temp\\tasks.csv')
    #bomb out now if result code isn't 0    
    if result != 0:
        print "Failed getting csv from task scheduler."
        exit(3)

    try:
        tasks = csv.reader(open("C:\\temp\\tasks.csv"), delimiter=',', quotechar='"')
    except IOError:
        #failed to open the file for some reason. bomb out
        print "Failed opening csv file, check permissions"
        exit(3)
        
    for i in tasks:
        #we care about two columns in the csv:
        #last run time, which is column 5 (the data of our DICT_OF_TASKS)
        #task name, column 1 (and the key)
        if i[1] in DICT_OF_TASKS:
            #
            if is_currently_out_of_date(i[5], DICT_OF_TASKS[i[1]]):
                #WEEEOOOOOWEEEOOOOO alarm, etc
                print "CRITICAL: %s last ran at %s" % (i[1], i[5])
                exit(2) #2 is critical from Nagios point of view

    print "OK: Checked %i tasks." % len(DICT_OF_TASKS)
    exit(0)

if __name__ == "__main__":
    main()


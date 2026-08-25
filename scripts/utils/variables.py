"""
In this module, global variables are declared. 
The CAUSE_ORDER is used for visualisation and some data organisation to ensure consistency rather than the automatic sorting by pandas or alt library 
"""
CAUSE_ORDER = ['Injured & Medical',
               'Lost',
               'Overdue',
               'Cragfast',
               'Other']

# for data between 2015 - 2025
PATH = "../../data/all_incidents.json"
# TODO find out where the data is from
# file used to identify bankholidays
HOLIDAY_PATH = "../../data/ukbankholidays-jul19.csv"


# for data before 2015 but not complete 2025
PATH_archive = "../../data_archive/all_incidents.json"
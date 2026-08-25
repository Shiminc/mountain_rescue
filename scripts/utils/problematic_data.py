"""
# This module consisted of one function that replace problematic data.
# It also acted as a documentation of what has been changed. 
"""

def handling_problematic_data(data):
    # empty cell in incident cause to be recoded to another original value Other
    # other could include help sweeping snow or flood or dog https://www.wmrt.org.uk/incidents/corney-fell-sat-11th-mar-2023/, https://www.wmrt.org.uk/incidents/brown-tongue-scafell-pike-thu-1st-jan-1970/
    data.loc[data['Incident_Cause']=='','Incident_Cause']='Other' 

    # 6 Callout - based on the mean number of staff of the full callout and limited callout - 15 vs 7, current data only 6 count of callout which is quite seperate, 2, 4, then 11 , so use 10 as cut off
    data.loc[(data['Incident_Type']=='Callout') & (data['staff'] >=10),'Incident_Type']='Full Callout'
    data.loc[(data['Incident_Type']=='Callout') & (data['staff'] <10),'Incident_Type']='Limited Callout'

    # missing data on Incident_Type, I read through and assign based on my judgement
    data.loc[data["Incident"]=='106 in 2025', 'Incident_Type']='Alert'
    data.loc[data["Incident"]=='38 in 2025', 'Incident_Type']='Full Callout'
    data.loc[data["Incident"]=='87 in 2025', 'Incident_Type']='Full Callout'
    data.loc[data["Incident"]=='133 in 2023', 'Incident_Type']='Alert'
    data.loc[data["Incident"]=='95 in 2023', 'Incident_Type']='Full Callout'
    data.loc[data["Incident"]=='55 in 2023', 'Incident_Type']='Limited Callout'

    # odd number of staff for small alerts due to the big number of staff around for other incidents or training, change the number to reflect based on reading of incident reports
    # to avoid inflation of total_hrs 
    data.loc[data["Incident"]=='117 in 2025', 'staff'] = 1
    data.loc[data["Incident"]=='117 in 2025', 'total_hrs'] = 2.6
    data.loc[data["Incident"]=='2 in 2023', 'staff'] = 1
    data.loc[data["Incident"]=='2 in 2023', 'total_hrs'] = 0.6
    data.loc[data["Incident"]=='121 in 2021', 'staff'] = 1
    data.loc[data["Incident"]=='121 in 2021', 'total_hrs'] = 4.3


    # replace with mean number of staff as again training nearby with 22 members, as no clear mentions of staff
    data.loc[data["Incident"]=='57 in 2017', 'staff'] = 7
    data.loc[data["Incident"]=='57 in 2017', 'total_hrs'] = 20.3

    # drop rows with hrs or staff as NaN, most are either short alert or flood responding rather than mountain rescue
    data = data.dropna(subset=['hrs','staff','date'])

    return data
    
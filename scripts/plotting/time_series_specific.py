from statsmodels.graphics.tsaplots import plot_acf, plot_pacf, month_plot, quarter_plot
from utils import set_up_altair, moving_averages, read_json_to_df, format_time_columns,aggregate_by_year_month, filter_by_year
import pandas as pd

PATH = "../../data/all_incidents.json"




def main():
    data = read_json_to_df(PATH)
    data = format_time_columns(data)
    incident_count = aggregate_by_year_month(data)

    plot_acf(incident_count['Incident']).show()
    plot_pacf(incident_count['Incident']).show()
    # month_plot(incident_count['Incident']).show()


    print('finish')

main()
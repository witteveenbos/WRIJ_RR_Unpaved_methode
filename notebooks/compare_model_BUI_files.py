# %% imports

import sys
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
%matplotlib inline

# sys.path.append(r"C:\Users\ROMN\git_projects\pysobek")

# from pysobek.sobekfunc import parse_buifile

# %% 

bui_file1 = r"D:\153961_Oude_IJssel\WRIJ_RR_Unpaved_methode_03_modellen\OY_5_kD20_L4_W_InfMax_InitGWS_20120401_20160930\gebied_1\REF\OY_5_gebied1_REF_rr_20150401_20150701\rr\DEFAULT.BUI"

bui_file2 = r"D:\153961_Oude_IJssel\WRIJ_RR_Unpaved_methode_03_modellen\OY_5_kD20_L4_W_InfMax_InitGWS_20140101_20160930\gebied_1\REF\OY_5_gebied1_REF_rr_20150401_20150701\rr\DEFAULT.BUI"

outputdir = r"D:\153961_Oude_IJssel\vergelijking_modelschematisatie"

# %% 

def parse_buifile(bui_file):

    with open(bui_file) as textfile:
            textfile_list = textfile.readlines()
            textfile_list_filtered = [x for x in textfile_list if '*' not in x]
            no_stations = int(textfile_list_filtered[1])
            stations_list = textfile_list_filtered[2:no_stations+2]
            stations_list = [x.strip().strip("'") for x in stations_list]
            index_datetimesettings = int(str([i for i, s in enumerate(textfile_list_filtered) if stations_list[-1]  in s][0])) + 2
            datetimesetting = textfile_list_filtered[index_datetimesettings]
            timestep = int(textfile_list_filtered[index_datetimesettings-1].split()[-1])
            index_data = int(str([i for i, s in enumerate(textfile_list) if datetimesetting  in s][0])) + 1
            df_bui_file = pd.read_csv(bui_file, sep='[\s]{1,}', skiprows=index_data, header=None, engine='python') # addition 20190925 seperator can be 1 or more whitespaces
            df_bui_file.columns = stations_list

            start_year= int(datetimesetting.split(' ')[0])
            start_month = int(datetimesetting.split(' ')[1])
            start_day = int(datetimesetting.split(' ')[2])
            start_hour = int(datetimesetting.split(' ')[3])
            start_minute = int(datetimesetting.split(' ')[4])
            start_second = int(datetimesetting.split(' ')[5])
            
            datetime_start = dt.datetime(start_year, start_month, start_day, start_hour, start_minute, start_second)
            df_bui_file.index = pd.date_range(start=datetime_start, periods=len(df_bui_file), freq=str(timestep)+'s')

    return df_bui_file

# %% 

df_bui_file1 = parse_buifile(bui_file1)
df_bui_file2 = parse_buifile(bui_file2)


# %%

for column in df_bui_file1.columns:
    fig, ax = plt.subplots()
    df_bui_file2[[column]].plot(ax=ax)
    df_bui_file1[[column]].plot(ax=ax, linestyle='--')
    ax.set_title(column)
    plt.show()
    fig.savefig(f"{outputdir}\\{column}.png")

# %% 



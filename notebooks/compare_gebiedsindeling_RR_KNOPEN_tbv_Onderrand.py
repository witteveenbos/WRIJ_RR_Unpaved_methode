# %% imports

import pandas as pd
import geopandas as gpd
%matplotlib inline

# %% directories

file1 = r"D:\153961_Oude_IJssel\WRIJ_RR_Unpaved_methode_02_input\rr_data_scenarios\OY_5_kD20_L4_W_InfMax_InitGWS_20120401_20160930_IMPROVED\REF\REF_gebiedsindeling_RR_KNOPEN_tbv_Onderrand.csv"
file2 = r"D:\153961_Oude_IJssel\WRIJ_RR_Unpaved_methode_02_input\rr_data_scenarios\OY_5_kD20_L4_W_InfMax_InitGWS_20130101_20160930_IMPROVED\REF\REF_gebiedsindeling_RR_KNOPEN_tbv_Onderrand.csv"
file3 = r"D:\153961_Oude_IJssel\WRIJ_RR_Unpaved_methode_02_input\rr_data_scenarios\OY_5_kD20_L4_W_InfMax_InitGWS_20140101_20160930_IMPROVED\REF\REF_gebiedsindeling_RR_KNOPEN_tbv_Onderrand.csv"

list_files = [file1, file2, file3]

# %% read and process files

for file in list_files:

    df = pd.read_csv(file)

    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.xcoor, df.ycoor))
    gdf = gdf.set_crs(epsg=28992)

    gdf.to_file(file.replace(".csv", ".gpkg"), driver="GPKG")

# %%

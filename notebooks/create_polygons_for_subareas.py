# %% imports

import geopandas as gpd
import pandas as pd
from shapely import Polygon, Point
from shapely.geometry import MultiPolygon
import os
from pathlib import Path
import numpy as np
import shutil
from rasterstats import zonal_stats
from tqdm import tqdm
%matplotlib inline

from hydrolib.dhydamo.core.drr import DRRModel

# %% directories and settings

input_gpkg = r"D:\153961_Oude_IJssel\vergelijking_modelschematisatie\inspect_df_RR_00.gpkg"
subcatchments_gpkg = r"D:\153961_Oude_IJssel\WRIJ_RR_Unpaved_methode_02_input\basisdata\afwateringseenheden.gpkg"

cellsize = 25 # m

# %% read files

gdf = gpd.read_file(input_gpkg)
gdf.head()

gdf_subcatchments = gpd.read_file(subcatchments_gpkg)
gdf_subcatchments.head()

# %% define function create_polygon_for_cell

def create_polygon_for_cell(x_midpoint, y_midpoint, cellsize):

    upper_left_x = x_midpoint - cellsize / 2
    upper_left_y = y_midpoint + cellsize / 2
    upper_right_x = x_midpoint + cellsize / 2
    upper_right_y = y_midpoint + cellsize / 2
    lower_left_x = x_midpoint - cellsize / 2
    lower_left_y = y_midpoint - cellsize / 2
    lower_right_x = x_midpoint + cellsize / 2
    lower_right_y = y_midpoint - cellsize / 2

    return Polygon([
        Point(upper_left_x, upper_left_y),
        Point(upper_right_x, upper_right_y),
        Point(lower_right_x, lower_right_y),
        Point(lower_left_x, lower_left_y),
        Point(upper_left_x, upper_left_y)
    ])

# %% define function seepage_from_input (based on HYDROLIB)

def seepage_from_input(catchments: gpd.GeoDataFrame, seepage_folder : str):

    file_list = os.listdir(seepage_folder)
    file_list = [file for file in file_list if file.endswith(".ASC")]
    times = []
    arr = np.zeros((len(file_list[0:4]), len(catchments.code)))
    for ifile, file in tqdm(enumerate(file_list[0:4]), total=len(file_list[0:4]), desc="Reading seepage files"):
        if file.endswith(".ASC"):
            file_renamed = file[:10].replace("_", "") + file[10:-8] + "01_MMD.ASC"
            seepage_folder_renamed = Path(seepage_folder).parent / (Path(seepage_folder).name + "_renamed")
            if not os.path.exists(seepage_folder_renamed):
                os.makedirs(seepage_folder_renamed, exist_ok=True)
                shutil.copy2(os.path.join(seepage_folder, file), os.path.join(seepage_folder_renamed, file_renamed))
            drrmodel = DRRModel()
            array, affine, time = drrmodel.read_raster(os.path.join(seepage_folder_renamed, file_renamed))
            times.append(time)
            stats = zonal_stats(catchments, array, affine=affine, stats="mean", all_touched=True)
            arr[ifile, :] = [stat["mean"] for stat in stats]
    result = pd.DataFrame(arr, columns=["sep_" + str(cat) for cat in catchments.code])
    result.index = times

    return result

# %% create polygons for all cells in the GeoDataFrame

gdf['geometry'] = gdf.apply(lambda row: create_polygon_for_cell(row.geometry.x, row.geometry.y, cellsize), axis=1)

# %% 

pd.to_datetime("2016-02-03").year

# %% inspect the updated GeoDataFrame

gdf.head()

# %% merge the polygons for each subarea

gdf["GFEIDENT_id"] = gdf.apply(lambda row: f"{row.GFEIDENT_id}_{row.hoog_middel_laag}", axis=1)
gdf_merged = gdf.dissolve(by='GFEIDENT_id')
gdf_merged["ligging"] = gdf_merged.apply(lambda row: "laag" if row.hoog_middel_laag == 1 else ("middel" if row.hoog_middel_laag == 2 else "hoog"), axis=1)

# %%

gdf_merged

# %%

gdf_merged = gdf_merged.set_crs("EPSG:28992")
gdf_subcatchments = gdf_subcatchments.set_crs("EPSG:28992")

gdf_subcatchments["_right_geometry"] = gdf_subcatchments["geometry"]

gdf_merged_joined = gdf_merged.sjoin(gdf_subcatchments[["GFEIDENT", "_right_geometry", "geometry"]], how="inner", predicate="intersects", rsuffix="_right")

gdf_merged_joined.head()

# %% calculate intersection area

gdf_merged_joined["intersection_area"] = gdf_merged_joined.geometry.intersection(gdf_merged_joined["_right_geometry"]).area

# %%

gdf_merged_joined
# gdf_merged_joined = gdf_merged_joined.reset_index(drop=True)

# %%

gdf_merged_joined["GFEIDENT_id"] = gdf_merged_joined.index
gdf_merged_joined = gdf_merged_joined.reset_index(drop=True)

# %% 

gdf_merged_joined

# %%

idx = gdf_merged_joined.groupby("GFEIDENT_id")["intersection_area"].idxmax()
gdf_merged_joined_selected = gdf_merged_joined.loc[idx]

# %%

gdf_merged_joined_selected

# %%

gdf_merged_joined_selected["subarea"] = gdf_merged_joined_selected.apply(lambda row: row["GFEIDENT"] + "_" + row["ligging"], axis=1)
gdf_merged_joined_selected = gdf_merged_joined_selected[["geometry", "subarea"]]
gdf_merged_joined_selected.to_file("test.gpkg")


# %%

gdf_merged_joined_selected.geometry = gdf_merged_joined_selected.apply(lambda row: MultiPolygon([row.geometry]) if not isinstance(row.geometry, MultiPolygon) else row.geometry, axis=1)

# %%

gdf_merged_joined_selected["code"] = gdf_merged_joined_selected["subarea"]

# op alfabetische volgorde sorteren

# %% 

# drr = DRRModel()
df_seepage = seepage_from_input(gdf_merged_joined_selected, r"D:\153961_Oude_IJssel\WRIJ_RR_Unpaved_methode_02_input\rr_data_scenarios\seepage\REF")

# %% 

# df_seepage.min().idxmin()"
df_seepage['sep_AE54670024_laag']

# %%




# %%

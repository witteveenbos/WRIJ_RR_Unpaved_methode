# %% imports

from pathlib import Path

# %% 

dir1 = r"D:\153961_Oude_IJssel\WRIJ_RR_Unpaved_methode_03_modellen\OY_5_kD20_L4_W_InfMax_InitGWS_20120401_20160930\gebied_1\REF\OY_5_gebied1_REF_rr_20150401_20150701\rr"
dir2 = r"D:\153961_Oude_IJssel\WRIJ_RR_Unpaved_methode_03_modellen\OY_5_kD20_L4_W_InfMax_InitGWS_20140101_20160930\gebied_1\REF\OY_5_gebied1_REF_rr_20150401_20150701\rr"

# %% 

# file = '3B_LINK.TP'
# location = 13

file = "3B_NOD.TP"
location = 2

with open(Path(dir1) / file, "r") as f1, open(Path(dir2) / file, "r") as f2:
    
    content1 = f1.read()
    content2 = f2.read()
    content1_split = content1.split(" ")
    content2_split = content2.split(" ")

    print("dir1 missing in dir2")
    for line in content1.splitlines():
        line_split = line.split(" ")
        # if line_split[location] in content2_split:
            # print(True)
        if line_split[location] not in content2_split:
            print(line_split[location])

    print("dir2 missing in dir1")
    for line in content2.splitlines():
        line_split = line.split(" ")
        # if line_split[location] in content1_split:
        #     print(True)
        if line_split[location] not in content1_split:
            print(line_split[location])

# %% 

print(line_split[location])
content1_split.index(line_split[location])
print(content1_split[content1_split.index(line_split[location])])

# %%

print(len(content1_split))
print(len(content2_split))

# %%

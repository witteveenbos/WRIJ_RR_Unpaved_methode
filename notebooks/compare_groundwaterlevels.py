# %% 

import sys
import shutil
import os
import subprocess
import matplotlib.pyplot as plt
%matplotlib inline

sys.path.append(r"C:\Users\ROMN\git_projects\pysobek")

from pysobek.sobekfunc import get_data

# %%

hisfile1 = r"D:\153961_Oude_IJssel\vergelijking_modelschematisatie\OY_5_gebied1_REF_rr_20150401_20150701_1jaar_inlooptijd\rr\upflowdt.his"
hisfile2 = r"D:\153961_Oude_IJssel\vergelijking_modelschematisatie\OY_5_gebied1_REF_rr_20150401_20150701_2jaar_9maanden_inlooptijd\rr\upflowdt.his"
hisfile3 = r"D:\153961_Oude_IJssel\vergelijking_modelschematisatie\OY_5_gebied1_REF_rr_20150401_20150701_2jaar_9maanden_inlooptijd_originele_kwelflux\rr\upflowdt.his"
parameter = "GWLevel-Surface"
outputdir = r"D:\153961_Oude_IJssel\vergelijking_modelschematisatie\vergelijking_grondwaterstand_na_correctie_kwel"

# %% convert his to txt

def his2txt(hisfile, outputdir):

    his_type = "upflowdt"
    hia_file = hisfile.replace(".his", ".hia")

    temp_hisfile = os.path.join(outputdir, hisfile.split('\\')[-1])
    shutil.copyfile(hisfile, temp_hisfile)

    if os.path.exists(hia_file):
        temp_hiafile = os.path.join(outputdir, hia_file.split('\\')[-1])
        shutil.copyfile(hia_file, temp_hiafile)

        pkdir = os.path.dirname(os.path.realpath(__file__))
        reahis = os.path.join(pkdir, "ReaHis.exe")

        txtfile = os.path.join(outputdir, his_type + ".txt")

        output_file = open(txtfile, "w")

        if not os.path.exists(temp_hiafile):
            cmd_command = [reahis, temp_hisfile]
        else:
            cmd_command = [reahis, temp_hisfile, temp_hiafile]

        subprocess.Popen(cmd_command, stdout=output_file).wait()

        os.remove(temp_hisfile)
        if os.path.exists(temp_hiafile):
            os.remove(temp_hiafile)

# %% 

his2txt(hisfile1, outputdir)
txtfile1 = hisfile1.replace(".his", ".txt")
df1 = get_data(outputdir, os.path.basename(txtfile1), parameter)

# %% 

his2txt(hisfile2, outputdir)
txtfile2 = hisfile2.replace(".his", ".txt")
df2 = get_data(outputdir, os.path.basename(txtfile2), parameter)

# %%

his2txt(hisfile3, outputdir)
txtfile3 = hisfile3.replace(".his", ".txt")
df3 = get_data(outputdir, os.path.basename(txtfile3), parameter)

# %% plot comparison

for col in df1.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df1.index, df1[col], label="1 jaar inlooptijd")
    ax.plot(df2.index, df2[col], label="2 jaar en 9 maanden inlooptijd - kwelflux gelijk aan 1 jaar inlooptijd", linestyle="--")
    ax.plot(df3.index, df3[col], label="2 jaar en 9 maanden inlooptijd - originele kwelflux", linestyle="--")
    ax.set_xlabel("Time")
    ax.set_ylabel("Groundwater Level [w.r.t. surface level]")
    ax.set_title(f"Comparison of groundwater levels {col}")
    ax.legend()
    ax.grid()
    plt.show()
    fig.savefig(os.path.join(outputdir, f"comparison_groundwater_levels_{col}.png"))

# %% 

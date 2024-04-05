import os
import shutil as sht
import subprocess
import pandas as pd
import matplotlib.pyplot as plt


def write_flight_log(output_dir):
    subprocess.check_output(["sbcl", "--noinform", "--load",
                             "src/utils.lisp", "--eval",
                             "(write-flight-log \"{}\")".format(output_dir),
                             "--quit"])


def make_plot(data_dir, out_dir):
    df = pd.read_csv(data_dir)

    plt.style.use("ggplot")

    ax = df.plot(figsize=(6, 5),
                 x="Time",
                 subplots=[("ax", "ay"),
                           ("vx", "vy"),
                           ("Height", "Mass")])

    plt.show()

    fig = ax.ravel()[0].get_figure()
    fig.savefig(out_dir)


def clean_dir(dir_to_clean):
    if os.path.isdir(dir_to_clean):
        sht.rmtree(dir_to_clean)

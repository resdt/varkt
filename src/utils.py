import os
import shutil as sht
import csv
import math
import pandas as pd
import matplotlib.pyplot as plt

import src.PATH as path
import src.constants as cst


TMP_FOLD = path.TMP_FOLD
OUT_FOLD = path.OUT_FOLD

PLOT_TABLE_PATH = path.PLOT_TABLE_PATH
OUT_TABLE_PATH = path.OUT_TABLE_PATH
OUT_PICT_PATH = path.OUT_PICT_PATH

M0_ROCKET = cst.M0_ROCKET
RHO0 = cst.RHO0
THAU = cst.THAU
G = cst.G
M_EARTH = cst.M_EARTH
R_EARTH = cst.R_EARTH
PI = cst.PI
THRUST = cst.THRUST
ENV_RES = cst.ENV_RES
S_ROCKET = cst.S_ROCKET
M_MASS_AIR = cst.M_MASS_AIR
R = cst.R
T0_AIR = cst.T0_AIR
M0_FUEL = cst.M0_FUEL
T_FUEL = cst.T_FUEL


def write_flight_log(output_dir=OUT_TABLE_PATH):
    os.makedirs(TMP_FOLD, exist_ok=True)
    plot_table = open(PLOT_TABLE_PATH, "w", newline="")
    plot_writer = csv.writer(plot_table)
    plot_writer.writerow(["Time", "ax", "ay",
                         "vx", "vy", "Height",
                         "Mass", "Density"])

    os.makedirs(OUT_FOLD, exist_ok=True)
    out_table = open(output_dir, "w", newline="")
    out_writer = csv.writer(out_table)
    out_writer.writerow(["Time", "Velocity", "Acceleration",
                         "Mass", "Density"])

    m = M0_ROCKET
    h = 0
    a = ax = ay = 0
    v = vx = vy = 0
    density = RHO0

    for t in range(THAU + 1):
        plot_writer.writerow([t, ax, ay, vx, vy, h, m, density])
        out_writer.writerow([t, v, a, m, h])

        g = G * M_EARTH / (R_EARTH+h)**2
        alpha = PI/2 - PI*t/300
        ax = (THRUST * math.cos(alpha) -
              ENV_RES * density * vx**2 * S_ROCKET / 2) / m
        ay = (THRUST * math.sin(alpha) -
              ENV_RES * density * vy**2 * S_ROCKET / 2 -
              G * m * M_EARTH / (R_EARTH+h)**2) / m
        density = RHO0 * math.exp(-M_MASS_AIR * g * h / (R*T0_AIR))
        vx += ax
        vy += ay
        v = (vx**2 + vy**2) ** 0.5
        a = (ax**2 + ay**2) ** 0.5
        m = M0_ROCKET - M0_FUEL*t/T_FUEL
        h += vy

    plot_table.close()
    out_table.close()


def make_plot(data_dir, out_dir=OUT_PICT_PATH):
    df = pd.read_csv(data_dir)

    plt.style.use("ggplot")

    ax = df.plot(figsize=(6, 5),
                 x="Time",
                 subplots=[("ax", "ay"),
                           ("vx", "vy"),
                           ("Height", "Mass")])

    plt.show()

    os.makedirs(OUT_FOLD, exist_ok=True)
    fig = ax.ravel()[0].get_figure()
    fig.savefig(OUT_PICT_PATH)


def clean_dir(dir_to_clean=TMP_FOLD):
    if os.path.isdir(dir_to_clean):
        sht.rmtree(dir_to_clean)

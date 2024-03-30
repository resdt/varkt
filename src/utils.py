import os
import shutil as sht
import csv
import math
import pandas as pd
import matplotlib.pyplot as plt

import src.PATH as path


TMP_FOLD = path.TMP_FOLD
OUT_FOLD = path.OUT_FOLD

PLOT_TABLE_PATH = f"{TMP_FOLD}/plot-data.csv"

# Глобальные константы
G = 6.6743 * 10**-11  # Гравитационная постоянная
R_EARTH = 6378100  # Радиус Земли
M_EARTH = 5.9742 * 10**24  # Масса Земли
ENV_RES = 0.4  # Коэффициент сопротивления среды
M_MASS_AIR = 0.029  # Молярная масса воздуха
R = 8.314  # Универсальная газовая постоянная
PI = math.pi

# Начальные значения
M0_ROCKET = 344040  # Масса ракеты
M0_FUEL = 284000  # Масса топлива
T_FUEL = 253  # Время, на которое хватит топлива
S_ROCKET = 13.28  # Площадь поверхности ракеты, на которую действует среда
THAU = 104  # Время полета
RHO0 = 1.225  # Плотность
THRUST = 41520000  # Тяга двигателя
T0_AIR = 288  # Температура воздуха (считаем постоянной)


def write_flight_log(output_dir):
    os.makedirs(TMP_FOLD, exist_ok=True)
    plot_table = open(PLOT_TABLE_PATH, "w", newline="")
    plot_writer = csv.writer(plot_table)
    plot_writer.writerow(["Time", "ax", "ay",
                          "vx", "vy", "Height",
                          "Mass", "Density"])

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


def make_plot(out_dir, data_dir=PLOT_TABLE_PATH):
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

import math
import pandas as pd
import matplotlib.pyplot as plt

from src.constants import *


def flight_process(data_dir, output_dir):
    data_file = open(data_dir, "w")
    output_file = open(output_dir, "w")

    m = M0_ROCKET
    h = 0
    a = ax = ay = 0
    v = vx = vy = 0
    density = RHO0

    for t in range(THAU + 2):
        if t == 0:
            output_file.write("Time\tVelocity\tAcceleration\tMass\tHeight\n")
            data_file.write("Time;ax;ay;vx;vy;Height;Mass;Density\n")

        output_file.write("\t".join(map(str, [t, v, a, m, h])) + "\n")
        data_file.write(";".join(map(str, [t, ax, ay, vx, vy, h, m, density])) + "\n")

        g = G * M_EARTH / (R_EARTH+h)**2
        alpha = PI/2 - PI*t/300
        ax = (THRUST*math.cos(alpha) - ENV_RES * density * vx**2 * S_ROCKET / 2) / m
        ay = (THRUST*math.sin(alpha) - ENV_RES * density * vy**2 * S_ROCKET / 2 - G * m * M_EARTH / (R_EARTH+h)**2) / m
        density = RHO0 * math.exp(-M_MASS_AIR * g * h / (R*T0_AIR))
        vx += ax
        vy += ay
        v = (vx**2 + vy**2) ** 0.5
        a = (ax**2 + ay**2) ** 0.5
        m = M0_ROCKET - M0_FUEL*t/T_FUEL
        h += vy

    data_file.close()
    output_file.close()


def plot(data_dir):
    df = pd.read_csv(data_dir, sep=";")
    plt.style.use("ggplot")
    df.plot(figsize=(6, 5),
            x="Time",
            subplots=[("ax", "ay"),
                      ("vx", "vy"),
                      ("Height", "Mass")])

    plt.show()

import math
import numpy as np
import matplotlib.pyplot as plt
import csv

from include.constants import *


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
            data_file.write("Time\tax\tay\tvx\tvy\tHeight\tMass\tDensity\n")

        output_file.write("\t".join(map(str, [t, v, a, m, h])) + "\n")
        data_file.write("\t".join(map(str, [t, ax, ay, vx, vy, h, m, density])) + "\n")

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
    flag = True

    time = []
    ax = []
    ay = []
    vx = []
    vy = []
    height = []
    mass = []
    density = []

    with open(data_dir, "r") as data_file:
        plotting = csv.reader(data_file, delimiter="\t")

        for line in plotting:
            if flag:
                time_label = line[0]
                ax_label = line[1]
                ay_label = line[2]
                vx_label = line[3]
                vy_label = line[4]
                height_label = line[5]
                mass_label = line[6]
                density_label = line[7]

                flag = False
            else:
                time.append(float(line[0]))
                ax.append(float(line[1]))
                ay.append(float(line[2]))
                vx.append(float(line[3]))
                vy.append(float(line[4]))
                height.append(float(line[5]))
                mass.append(float(line[6]))
                density.append(float(line[7]))

    # ax
    plt.subplot(421)
    plt.xlabel(time_label)
    plt.ylabel(ax_label)
    plt.grid(True)
    plt.plot(time, ax, "b")

    # ay
    plt.subplot(422)
    plt.xlabel(time_label)
    plt.ylabel(ay_label)
    plt.grid(True)
    plt.plot(time, ay, "b")

    # vx
    plt.subplot(423)
    plt.xlabel(time_label)
    plt.ylabel(vx_label)
    plt.grid(True)
    plt.plot(time, vx, "b")

    # vy
    plt.subplot(424)
    plt.xlabel(time_label)
    plt.ylabel(vy_label)
    plt.grid(True)
    plt.plot(time, vy, "b")

    # Height
    plt.subplot(425)
    plt.xlabel(time_label)
    plt.ylabel(height_label)
    plt.grid(True)
    plt.plot(time, height, "b")

    # Mass
    plt.subplot(426)
    plt.xlabel(time_label)
    plt.ylabel(mass_label)
    plt.grid(True)
    plt.plot(time, mass, "b")

    # Density
    plt.subplot(427)
    plt.xlabel(time_label)
    plt.ylabel(density_label)
    plt.grid(True)
    plt.plot(time, density, "b")

    plt.show()

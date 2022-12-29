import math
import numpy as np
import matplotlib.pyplot as plt
import csv


# Глобальные константы.
G = 6.6743 * 10**-11 # Гравитационная постоянная.
RE = 6378100 # Радиус Земли.
ME = 5.9742 * 10**24 # Масса Земли.
Coef = 0.4 # Коэффициент сопротивления среды.
Mmol = 0.029 # Молярная масса воздуха.
Rgas = 8.314 # Универсальная газовая постоянная.

# Начальные значения.
M = 344040 # Масса ракеты.
Mf = 284000 # Масса топлива.
Tfuel = 253 # Время, на которое хватит топлива.
S = 13.28 # Площадь поверхности ракеты, на которую действует среда.
THAU = 104 # Время полета.
Density0 = 1.225 # Плотность.
Thrust = 41520000 # Тяга двигателя.
Temp = 288 # Температура воздуха (считаем постоянной).


def flight_process(file_, data_file, t, v, vx, vy, a, ax, ay, m, h, Density, pi=math.pi):
    if t == THAU + 1:
        return 0

    if not t:
        file_.write("Time\tVelocity\tAcceleration\tMass\tHeight\n")
        data_file.write("Time\tax\tay\tvx\tvy\tHeight\tMass\tDensity\n")

    file_.write("\t".join(map(str, [t, v, a, m, h])) + "\n")
    data_file.write("\t".join(map(str, [t, ax, ay, vx, vy, h, m, Density])) + "\n")

    g = G * ME / (RE+h)**2
    Alpha = pi/2 - pi*t/300
    ax = (Thrust*math.cos(Alpha) - Coef * Density * vx**2 * S / 2) / m
    ay = (Thrust*math.sin(Alpha) - Coef * Density * vy**2 * S / 2 - G * m * ME / (RE+h)**2) / m
    Density = Density0 * math.exp(-Mmol * g * h / (Rgas*Temp))
    vx += ax
    vy += ay
    v = (vx**2 + vy**2) ** 0.5
    a = (ax**2 + ay**2) ** 0.5
    m = M - Mf*t/Tfuel
    h += vy

    return flight_process(file_, data_file, t + 1, v, vx, vy, a, ax, ay, m, h, Density)

def plot():
    flag = True

    time = []
    ax = []
    ay = []
    vx = []
    vy = []
    height = []
    mass = []
    density = []

    with open("Plot_data.txt", "r") as data_file:
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

    # ax.
    plt.subplot(421)
    plt.xlabel(time_label)
    plt.ylabel(ax_label)
    plt.grid(True)
    plt.plot(time, ax, "b")

    # ay.
    plt.subplot(422)
    plt.xlabel(time_label)
    plt.ylabel(ay_label)
    plt.grid(True)
    plt.plot(time, ay, "b")

    # vx.
    plt.subplot(423)
    plt.xlabel(time_label)
    plt.ylabel(vx_label)
    plt.grid(True)
    plt.plot(time, vx, "b")

    # vy.
    plt.subplot(424)
    plt.xlabel(time_label)
    plt.ylabel(vy_label)
    plt.grid(True)
    plt.plot(time, vy, "b")

    # Height.
    plt.subplot(425)
    plt.xlabel(time_label)
    plt.ylabel(height_label)
    plt.grid(True)
    plt.plot(time, height, "b")

    # Mass.
    plt.subplot(426)
    plt.xlabel(time_label)
    plt.ylabel(mass_label)
    plt.grid(True)
    plt.plot(time, mass, "b")

    # Density.
    plt.subplot(427)
    plt.xlabel(time_label)
    plt.ylabel(density_label)
    plt.grid(True)
    plt.plot(time, density, "b")

    plt.show()


def main():
    t = 0
    m = M
    h = 0
    a = ax = ay = 0
    v = vx = vy = 0
    Density = Density0
    output_file = open("Output.txt", "w")
    data_file = open("Plot_data.txt", "w")

    flight_process(output_file, data_file, t, v, vx, vy, a, ax, ay, m, h, Density)

    output_file.close()
    data_file.close()

    plot()


main()

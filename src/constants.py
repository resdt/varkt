import math


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

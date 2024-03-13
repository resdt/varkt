from src.functions import *


def main():
    data_dir = "lib/plot-data.txt"
    output_dir = "out/output.txt"

    flight_process(data_dir, output_dir)

    plot(data_dir)

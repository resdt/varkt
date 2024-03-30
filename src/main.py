import os

import src.PATH as path
import src.utils as utl


TMP_FOLD = path.TMP_FOLD
OUT_FOLD = path.OUT_FOLD

OUT_TABLE_PATH = f"{OUT_FOLD}/flight-log.csv"
OUT_PICT_PATH = f"{OUT_FOLD}/plot.png"

write_flight_log = utl.write_flight_log
make_plot = utl.make_plot
clean_dir = utl.clean_dir


def main():
    os.makedirs(OUT_FOLD, exist_ok=True)
    write_flight_log(OUT_TABLE_PATH)
    make_plot(OUT_PICT_PATH)
    clean_dir(TMP_FOLD)

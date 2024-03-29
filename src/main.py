import src.PATH as path
import src.utils as utl


TMP_FOLD = path.TMP_FOLD

OUT_TABLE_PATH = path.OUT_TABLE_PATH
PLOT_TABLE_PATH = path.PLOT_TABLE_PATH

write_flight_log = utl.write_flight_log
make_plot = utl.make_plot
clean_dir = utl.clean_dir


def main():
    write_flight_log(OUT_TABLE_PATH)
    make_plot(PLOT_TABLE_PATH)
    clean_dir(TMP_FOLD)

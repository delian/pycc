import readline
import atexit


histfile = ".pycc_history"
try:
    readline.read_history_file(histfile)
    h_len = readline.get_current_history_length()
except FileNotFoundError:
    open(histfile, "wb").close()
    h_len = 0


def save_history(h_len, histfile):
    new_h_len = readline.get_current_history_length()
    readline.set_history_length(1000)
    readline.append_history_file(new_h_len - h_len, histfile)


atexit.register(save_history, h_len, histfile)

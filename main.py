import os
import sys

import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

from functools import partial
from pathlib import Path

from vlc import MediaPlayer


APPLICATION_PATH = Path(os.path.dirname(__file__) if getattr(sys, 'frozen', True) else os.path.dirname(sys.executable))
ALARM_PATH = APPLICATION_PATH / "resources/alarm.mp3"
ICON_PATH = APPLICATION_PATH / "resources/good-head-wink.ico"
ALARM_VOLUME = 50


def fancy_time_to_seconds(fancy_time):
    total_seconds = 0

    for pos, digit in enumerate(reversed(f'{fancy_time}')):
        total_seconds += int(digit) * 6 ** (pos // 2) * 10 ** ((pos + 1) // 2)

    return total_seconds


def split_up_seconds(seconds):
    total_minutes, seconds = divmod(seconds, 60)
    total_hours, minutes = divmod(total_minutes, 60)
    days, hours = divmod(total_hours, 24)

    return days, hours, minutes, seconds


def seconds_to_time_string(seconds):
    days, hours, minutes, seconds = split_up_seconds(seconds)

    time_string = ''
    if days:
        time_string = f'{days}d '
    if hours or days:
        time_string += f'{hours}h '
    if minutes or hours or days:
        time_string += f'{minutes}m '
    time_string += f'{seconds}s'

    return time_string


def seconds_to_compact_time_string(seconds):
    days, hours, minutes, seconds = split_up_seconds(seconds)

    time_string = ''
    if days:
        time_string = f'{days}d'
    if hours:
        time_string += f'{hours}h'
    if minutes:
        time_string += f'{minutes}m'
    if seconds or not time_string:
        time_string += f'{seconds}s'

    return time_string


def close_window(window, event):
    # event has to be accepted for tkinter to be happy
    window.destroy()


def centralize_window(window):
    window.update_idletasks()

    width = window.winfo_width()
    height = window.winfo_height()

    border_width = window.winfo_rootx() - window.winfo_x()
    titlebar_height = window.winfo_rooty() - window.winfo_y()

    window_width = width + 2 * border_width
    window_height = height + titlebar_height + border_width

    x = (window.winfo_screenwidth() - window_width) // 2
    y = (window.winfo_screenheight() - window_height) // 2

    window.geometry(f'{width}x{height}+{x}+{y}')


def get_time():
    while True:
        try:
            fancy_time = tk.simpledialog.askstring("Timerrhymer", "Please enter a time:").replace(" ", "")

            if fancy_time is None:
                exit()
            elif fancy_time == "":
                return "0"
            elif 1000000 > int(fancy_time) >= 0:
                return fancy_time
            else:
                raise ValueError
        except ValueError:
            tk.messagebox.showinfo("Timerrhymer",
                                   "Improper formatting.\n\nPlease enter up to six digits.")
        except AttributeError:
            exit()


def update_timer(window, text, seconds):
    if seconds > 0:
        seconds -= 1
        time_string = seconds_to_time_string(seconds)

        text.config(text=f'{time_string}')
        window.title(f'{time_string} - Timerrhymer')
        window.update()

        window.after(1000, partial(update_timer, window, text, seconds))
    else:
        completion_string = 'WE DONE HERE!!!'
        text.config(text=completion_string)
        window.title(f'==> {completion_string} <==')
        window.attributes('-topmost', 1)
        window.attributes('-topmost', 0)
        window.update()
        window.focus()

        window.bind('<Return>', partial(close_window, window) )
        window.bind('<space>', partial(close_window, window))

        alarm = MediaPlayer(ALARM_PATH)
        alarm.audio_set_volume(ALARM_VOLUME)
        alarm.play()


def start_timer(seconds):
    time_string = seconds_to_time_string(seconds)

    window = tk.Tk()
    window.iconbitmap(ICON_PATH)
    window.geometry("500x150")
    # window.attributes("-topmost", True)
    # window.lift()
    # window.focus_force()
    window.attributes('-topmost', True)
    window.attributes('-topmost', False)
    window.lift()
    window.focus_force()
    centralize_window(window)

    text = tk.Label(text=f'{time_string}', padx=50, pady=50, font=('arial black', 35))
    text.pack()

    window.title(f'{seconds_to_compact_time_string(seconds)} - Timerrhymer')
    window.after(1000, partial(update_timer, window, text, seconds))

    window.bind('<Escape>', partial(close_window, window))

    window.mainloop()


def main():
    fancy_time = get_time()
    seconds = fancy_time_to_seconds(fancy_time)
    compact_time_string = seconds_to_compact_time_string(seconds)

    if tk.messagebox.askyesno("Timerrhymer",
                              f"Confirm timer for {f'{compact_time_string} aka ' if seconds >= 60 else ''}{seconds}s."):
        start_timer(seconds)
    else:
        tk.messagebox.showerror("Timerrhymer", "Well then maybe don't or whatever...")
        exit()


if __name__ == '__main__':
    main()


# tests
def run_tests():
    result_fancy_time_to_seconds = [fancy_time_to_seconds(x) for x in [0, 1, 5, 10, 60, 90, 130, 360, 13000]]
    assert result_fancy_time_to_seconds == [0, 1, 5, 10, 60, 90, 90, 240, 5400], \
        result_fancy_time_to_seconds

    result_seconds_to_time_string = [seconds_to_time_string(x) for x in [0, 5, 60, 90, 3600, 3600 * 49]]
    assert result_seconds_to_time_string == ['0s', '5s', '1m 0s', '1m 30s', '1h 0m 0s', '2d 1h 0m 0s'], \
        result_seconds_to_time_string

    result_seconds_to_compact_time_string = [seconds_to_compact_time_string(x) for x in [0, 5, 60, 90, 3600, 3600 * 49]]
    assert result_seconds_to_compact_time_string == ['0s', '5s', '1m', '1m30s', '1h', '2d1h'], \
        result_seconds_to_compact_time_string


# run_tests()

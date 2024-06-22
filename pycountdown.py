#!/bin/python3
import datetime
import time
import tkinter as tk
import tkinter.font as tkfont
import threading
import sys
import getopt

help_string = """Pycountdown: a simple countdown script using Tkinter
Required arguments:
  -y <YEAR>: set the year to count down to
  -m <MONTH>: set the month to count down to
  -d <DAY>: set the day to count down to

Optional arguments:
  -H [HOUR]: set the hour to count down to
  -M [MINUTE]: set the minute to count down to
  -n [NAME]: display text of the event
  -f [SIZE]: set the default font size

You can press + or - in the window to change font size as well."""

year = False
month = False
day = False
hour = False
minute = False
name = False
font_size = 9

opts, args = getopt.getopt(sys.argv[1:], "hf:n:y:m:d:H:M:")

for opt, arg in opts:
    if opt == "-h":
        print(help_string)
        sys.exit(0)
    elif opt == "-y":
        year = int(arg)
    elif opt == "-m":
        month = int(arg)
    elif opt == "-d":
        day = int(arg)
    elif opt == "-H":
        hour = int(arg)
    elif opt == "-M":
        minute = int(arg)
    elif opt == "-n":
        name = arg
    elif opt == "-f":
        font_size = int(arg)

if not year or not month or not day:
    print("Error! Must provide ", end="")
    if not year: print("Year ")
    if not month: print("Month ")
    if not day: print("Day")

if hour:
    if minute:
        date_tuple = (year, month, day, hour, minute)
    else:
        date_tuple = (year, month, day, hour)
else:
    date_tuple = (year, month, day)

countdown_date = datetime.datetime(*date_tuple)


main_window = tk.Tk()
main_window.title("Countdown")
main_window.resizable(False, False)
countdown_stringvar = tk.StringVar()

default_font = tkfont.nametofont("TkDefaultFont")


def pluralize(word, number):
    return f"{number} {word}" if number == 1 else f"{number} {word}s"


def countdown():
    while True:
        try:
            now = datetime.datetime.now()
            delta = countdown_date - now
            days = delta.days
            hours = delta.seconds // 3600
            minutes = (delta.seconds // 60) % 60
            seconds = delta.seconds % 60

            countdown_string = ""
            if days != 0:
                countdown_string += f"{pluralize('day', days)}, "
            countdown_string += f"{pluralize('hour', hours)}, {pluralize('minute', minutes)}, {pluralize('second', seconds)}"
            countdown_stringvar.set(countdown_string)
            time.sleep(1)
        except:
            sys.exit(0)


def scale(px):
    global font_size
    font_size += px
    font_size = min(font_size, 200)
    default_font.configure(size=font_size)


def key_pressed(event):
    if event.char == "+":
        scale(max(font_size // 4, 1))
    elif event.char == "-":
        if not font_size // 4 < 1:
            scale(font_size // -4)


countdown_thread = threading.Thread(target=countdown)
countdown_label = tk.Label(main_window, textvariable=countdown_stringvar)
countdown_label.pack()
on_word = "until"
if name:
    name_label = tk.Label(main_window, text=f"until {name}")
    name_label.pack()
    on_word = "on"
on_label = tk.Label(main_window, text=f"{on_word} {countdown_date.strftime('%A %d %B %Y, %H:%M')}")
on_label.pack()
main_window.bind("<KeyPress>", key_pressed)

if __name__ == '__main__':
    countdown_thread.start()
    scale(0)
    main_window.mainloop()
    countdown_thread.join()
import tkinter as tk
import tkcalendar as tkc
import datetime
import pathlib
import os

root = tk.Tk()
root.title("cal.py")

cal_frame = tk.Frame(root)
event_frame = tk.Frame(root)
button_frame = tk.Frame(event_frame)
text_frame = tk.Frame(event_frame)
color_frame = tk.Frame(event_frame, bd="3", bg="grey")
appdata_dir = str(os.getenv('APPDATA')) + "/Calendar/"
try:
    open(os.path.abspath(appdata_dir + "events.txt"), "a+").close()
except :
    os.mkdir(os.path.abspath(appdata_dir))
    open(os.path.abspath(appdata_dir + "events.txt"), "a+").close()

"""Configuration section WIP
config_file = open(appdata_dir+"config.txt","r")
config = config_file.readlines()
config_file.close()
"""
"""Icons must be in Calendar/icons at AppData"""
icon_loaded=True
try:
    root.wm_iconbitmap(os.path.abspath(appdata_dir + "/icons/" + datetime.datetime.now().strftime("%d") + ".ico"))
except:
    icon_loaded=False
current_date = datetime.datetime.now()
if icon_loaded:
    root.title(current_date.strftime("%B")+" "+current_date.strftime("%Y"))
else:
    root.title(current_date.strftime("%d")+" "+current_date.strftime("%B")+" "+current_date.strftime("%Y"))

def display_event(eventObject="cal"):
    text.config(state=tk.NORMAL)
    text.delete(1.0, tk.END)
    text.insert(1.0, str(event_read(cal.selection_get())[0]))
    text.config(state=tk.DISABLED)

    event_create()



text = tk.Text(text_frame, wrap=tk.WORD, state=tk.DISABLED)


color_list = ["blue", "red", "green", "yellow", "magenta"]
color_listbox = tk.Listbox(color_frame,selectmode=tk.SINGLE)
for i in color_list:
    color_listbox.insert(tk.END,i)
cal = tkc.Calendar(cal_frame, locale="en_UK")
cal.bind("<<CalendarSelected>>", display_event)
edit_button = tk.Button(button_frame, text="Edit")
save_button = tk.Button(button_frame, text="Save", state=tk.DISABLED)
color_listbox.select_set(0)
pathlib.Path(appdata_dir).mkdir(parents=True, exist_ok=True)

color_listbox.configure(state=tk.DISABLED)

"""
WIP
"""

"""Event section."""


def configuration():
    pass


def newline_remover(string):
    length = len(string)
    if string[length - 2:length - 1] == "\n":
        string = string[length - 2:length - 1]
    return string


"""Event file format:
"%Y-%m-%d":text:color|
Example:


"""

"""Returns dictionary of events, where date is key and text is value."""


def event_read_file():
    events = open(os.path.abspath(appdata_dir + "events.txt"), "r", encoding="utf8", errors='ignore')
    events_list = events.read().split("|")
    events.close()
    try:
        events_list.remove('')
    except ValueError:
        pass
    # Removes newlines
    events = {}
    # Splits string and updates dictionary
    for i in events_list:
        event_tuple = i.split(":")
        events.update({event_tuple[0]: {"text" : newline_remover(event_tuple[1]),
                                        "color" : newline_remover(event_tuple[2])
                                        }
                       })
    return events

previous_color = "blue"

"""Returns event`s text from date."""


def event_read(date):
    events = event_read_file()
    return dict_separation(events,date)


"""Writes event file from event_read_file and new date-text pair."""



def event_write_file(date, _text,_color):
    events = event_read_file()
    events.update({str(date.strftime("%Y-%m-%d")): {"text":_text,"color":_color}})
    event_string = ""
    # Creates list of write-ready lines
    for i in events.keys():
        if events.get(i) != "\n":
            text,color = dict_separation(events,i)
            event_string += (str(i) + ":" + str(newline_remover(text)) + ":" + str(newline_remover(color)) + "|")
    file = open(os.path.abspath(appdata_dir + "events.txt"), "w", encoding="utf8", errors='ignore')
    file.write(event_string)
    file.close()

def dict_separation(dict,date):
    if not isinstance(date,str):
        date = date.strftime("%Y-%m-%d")
    dict = dict.get(date)
    try:
        text = dict.get("text")
    except AttributeError:
        text = None
    try:
        color = dict.get("color")
    except AttributeError:
        color = previous_color
    return(text,color)

def edit_click():
    display_event()
    text.config(state=tk.NORMAL)
    edit_button.config(state=tk.DISABLED)
    color_listbox.configure(state=tk.NORMAL)
    save_button.config(state=tk.NORMAL)
    cal.config(selectmode="none")


def save_click():
    edit_button.config(state=tk.NORMAL)
    save_button.config(state=tk.DISABLED)
    cal.config(selectmode="day")
    color_listbox.configure(state=tk.DISABLED)
    #color_listbox.select_set(previous_color)
    print(text.get(1.0,tk.END))
    event_write_file(cal.selection_get(), text.get(1.0, tk.END), color_listbox.get(tk.ACTIVE))
    display_event()



event_ids = []


def event_create(eventObject=cal):
    date = cal.get_displayed_month()
    events = event_read_file()
    cal.calevent_remove("all")
    keys = events.keys()
    for i in keys:
        key_date = datetime.datetime.strptime(i, "%Y-%m-%d")
        if key_date.year == date[1] and key_date.month == date[0]:
            text, color = dict_separation(events,key_date)
            cal.calevent_raise(
                cal.calevent_create(datetime.datetime.strptime(i, "%Y-%m-%d"),
                                                   str(text),
                                                   str(color)
                                    )
                               )
            cal.tag_config(color, background=color)
            cal.tag_config("yellow", foreground="black")

cal.bind("<<CalendarMonthChanged>>", event_create)
event_create()
edit_button.config(command=edit_click)
save_button.config(command=save_click)

text_frame.pack(side="left")
cal_frame.pack(side="top", fill="both", expand=True)
button_frame.pack(side="bottom", fill="x")
event_frame.pack(side="bottom", fill="both")
color_frame.pack(side="right", fill="y")


color_listbox.pack(side="right", fill="y")

edit_button.pack(side="left", fill="x", expand=True)
save_button.pack(side="right", fill="x", expand=True)
text.pack(side="left", fill="x")
cal.pack(fill="both", expand=True)
root.mainloop()

# Todo next session: 
# - figure a way to incorporate the boss checklist for each character
# - - maybe add all the bosses as vars in the charInfo and update add_char popup to reflect ability to select bosses
# - - maybe just have a new popup display the bosses, with relevant stuff (bosses killed, party size, mesos gained) that gets saved as a separate obj? (cont.)
# - - (cont. ^) maybe second boss obj can be added in a list form for characters i.e. {char_name : [charinfo obj, bossing obj]} ? main thing - find a way to retain player's character progression (cont.)
# - - (cont. ^) maybe forget about the mesos accumulated (party size identification/calculations) for the time being and have it as a simple boss checklist

import tkinter as tk
from tkinter import messagebox
from datetime import timezone, timedelta
import datetime as dt
import webbrowser
from charinfo import CharInfo, BossList
import json
import os # note to self: needed to find json file from prev experience

# list of charinfo (characters) objs
characters = {}

# json save file
storage_filename = 'chars_save.json'

# custom json serializer
def custom_serializer(obj):
    if isinstance(obj, CharInfo):
        return {
            'ign': obj.ign,
            'job': obj.job,
            'level': obj.level,
            'capped': obj.capped
        }
    elif isinstance(obj, BossList):
        return {
           'Chaos Pink Bean': obj.cpb,
           'Hard Hilla': obj.hh,
           'Cygnus': obj.cyg,
           'Chaos Zakum': obj.czak,
           'Princess No': obj.pno,
           'Chaos Queen': obj.cqueen,
           'Chaos Pierre': obj.cpierre,
           'Chaos VonBon': obj.cvonbon,
           'Chaos Vellum': obj.cvell,
           'Akechi Mitsuhide': obj.akechi,
           'Hard Magnus': obj.hmag,
           'Chaos Papulatus': obj.cpap,
           'Lotus': obj.lotus,
           'Damien': obj.damien,
           'Guardian Slime': obj.gslime,
           'Lucid': obj.lucid,
           'Will': obj.will,
           'Gloom': obj.gloom,
           'Darknell': obj.darknell,
           'Versus Hilla': obj.vhilla,
           'Seren': obj.seren,
           'Kaling': obj.kaling 
        }
    return obj

# create a new character entry
def create_char(ign, job, level):    

    # character entry validation
    # checks to see if the character already exists in the characters dictionary, if so do not process given character entry and output error message
    # ** Self Note ** Find a way to pass the error to the pop-up window and prevent ability to submit
    if ign in characters.keys():
        print('Already Exists!')
    else:

        # create a new character obj
        new_char = CharInfo(ign, job, level, False)
        
        # add new character obj to the characters dictionary
        characters[new_char.ign] = new_char
        
        # set serialization for characters dictionary for json save file / serialize the characters dictionary to json string
        json_data = json.dumps(characters, default=custom_serializer, indent=4)
        
        # save latest version of characters dictionary to the json save file / updates the json save file with latest data
        with open(storage_filename, 'w') as outfile:
            outfile.write(json_data)

        chars_lb.delete(0, 'end')
        populate_entries()

# read and add existing character entries found in the json save file to the characters dictionary
def load_characters():

    # check if file exists
    if os.path.exists(storage_filename):

        # read the file
        with open(storage_filename, 'r') as file:

            # load the json file data
            characters_data = json.load(file)

            # update the characters dictionary with existing character entries in the selected json save file
            for char_ign, char_info in characters_data.items():
                characters[char_ign] = CharInfo(char_ign, char_info['job'], char_info['level'], char_info['capped'])

# delete an existing character entry
def delete_char():

    # store selected character key
    selected_ign = ''

    # retrieve the selected character ign which is also the key
    for i in chars_lb.curselection():
        selected_ign = chars_lb.get(i)

    if selected_ign == '':
        messagebox.showerror('No Selection Error', 
                             'No character has been selected in the list.')
    else:

        # load and delete the selected character key from the json save file
        with open(storage_filename, 'r') as file:
            json_data = json.load(file)
            del json_data[selected_ign]

        # update the json save file
        with open(storage_filename, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)

        # delete the key from the characters dictionary
        del characters[selected_ign]

        # delete all character entries in the current listbox
        chars_lb.delete(0, 'end')

        # update the listbox with latest characters data
        populate_entries()

        # logger to check if character dictionary reflects action change
        # print(characters.keys())

# check if characters dictionary is storing data correctly
def check_characters():
    load_characters()
    for k, v in characters.items():
        v.charinfo_str()

# check_characters()

root = tk.Tk()
# root.resizable(False, False)

# frames setup
yellow_frame = tk.Frame(root, width=600, height=80, bg='yellow', highlightbackground='black', highlightthickness=2, borderwidth=1, padx=5, pady=5)
red_frame = tk.Frame(root, width=200, height=500, bg='red', highlightbackground='black', highlightthickness=1)
blue_frame = tk.Frame(root, width=400, height=125, bg='blue', highlightbackground='black', highlightthickness=1)
magenta_frame = tk.Frame(root, width=400, height=125, bg='magenta', highlightbackground='black', highlightthickness=1)
orange_frame = tk.Frame(root, width=400, height=125, bg='orange', highlightbackground='black', highlightthickness=1)
green_frame = tk.Frame(root, width=400, height=125, bg='green', highlightbackground='black', highlightthickness=1)

yellow_frame.grid(row=0, columnspan=2, sticky='nwse')
red_frame.grid(rowspan=4, column=0, sticky='nwse')
blue_frame.grid(row=1, column=1, sticky='nwse')
magenta_frame.grid(row=2, column=1, sticky='nwse')
orange_frame.grid(row=3, column=1, sticky='nwse')
green_frame.grid(row=4, column=1, sticky='nwse')

# to not ignore frame attributes when widgets are introduced
yellow_frame.grid_propagate(False)
red_frame.grid_propagate(False)

# yellow frame
co_lbl = tk.Label(yellow_frame, text='Characters Overview', font=('Kozuka Gothic Pro B', 18), bg='yellow')
co_lbl.place(relx=0.5, rely=0.5, anchor='center')

# red frame

# fill listbox 'chars_lb' with all characters found in characters dictionary
def populate_entries():

    # loop through the characters dictionary and insert their character ign
    for char_ign in characters:
        chars_lb.insert('end', char_ign)

chars_lb = tk.Listbox(red_frame, height=30)
chars_lb.place(relx=0.5, rely=0.5, anchor='center')

# blue frame

# add a new character pop-up window
def add_character_popup():

    ac_ign = tk.StringVar()
    ac_job = tk.StringVar()
    ac_level = tk.StringVar()

    aesthetic_params = {'font': ('Kozuka Gothic Pro B', 12)}

    # check to see if character already exists
    def validate_character_entry(check_ign):
        # if character already exists in characters dictionary, give error message and close pop-up
        if check_ign in characters.keys():
            messagebox.showerror('Invalid IGN (Player Name)',
                                 'The IGN (Character Name) has already been registered.')
            ac_win.destroy()
        else:
            # otherwise, update characters dictionary with new entry and close pop-up
            create_char(ac_ign.get(), ac_job.get(), ac_level.get())
            ac_win.destroy()

    # ac short for add_character
    ac_win = tk.Toplevel(blue_frame)
    ac_win.title('Add New Character')
    ac_win.geometry('300x200+650+150')
    
    ac_title_lbl = tk.Label(ac_win, text='Add New Character', **aesthetic_params)
    ac_ign_lbl = tk.Label(ac_win, text='In-Game Name:', **aesthetic_params)
    ac_ign_entry = tk.Entry(ac_win, textvariable=ac_ign)
    ac_job_lbl = tk.Label(ac_win, text='Job (Class):', **aesthetic_params)
    ac_job_entry = tk.Entry(ac_win, textvariable=ac_job)
    ac_level_lbl = tk.Label(ac_win, text='Level:', **aesthetic_params)
    ac_level_entry = tk.Entry(ac_win, textvariable=ac_level)
    ac_submit_btn = tk.Button(ac_win, text='Add to Roster', command=lambda:validate_character_entry(ac_ign.get()), **aesthetic_params)
    ac_cancel_btn = tk.Button(ac_win, text='Cancel', command=ac_win.destroy, **aesthetic_params)

    ac_title_lbl.grid(row=0, columnspan=2)
    ac_ign_lbl.grid(row=1, column=0)
    ac_ign_entry.grid(row=1, column=1)
    ac_job_lbl.grid(row=2, column=0)
    ac_job_entry.grid(row=2, column=1)
    ac_level_lbl.grid(row=3, column=0)
    ac_level_entry.grid(row=3, column=1)
    ac_submit_btn.grid(row=4, column=0)
    ac_cancel_btn.grid(row=4, column=1)

    ac_win.rowconfigure(0, weight=1)
    ac_win.rowconfigure(1, weight=1)
    ac_win.rowconfigure(2, weight=1)
    ac_win.rowconfigure(3, weight=1)
    ac_win.rowconfigure(4, weight=1)
    ac_win.columnconfigure(0, weight=1)
    ac_win.columnconfigure(1, weight=1)

def update_character_popup():

    uc_ign = tk.StringVar()
    uc_job = tk.StringVar()
    uc_level = tk.StringVar()

    aesthetic_params = {'font': ('Kozuka Gothic Pro B', 12)}

    selected_ign = ''

    # selected a character from listbox and store in selected_ign
    for i in chars_lb.curselection():
        selected_ign = chars_lb.get(i)

    # validation check to see if a character has been selected from the listbox
    # if none selected, show error prompt 
    if selected_ign == '':
        messagebox.showerror('Character Selection Error', 
                             'A character has not been selected from the list.')
        
    # check if the updated ign is already registered for another character
    def validate_updated_entry():

        # temp dictionary to manipulate the characters dictionary, purely for validation checking
        temp = {}

        # copying data from characters dictionary to temp
        for key, val in characters.items():
            temp[key] = val

        # deleting the selected character obj in temp
        del temp[selected_ign]

        # checking if the newly proposed ign update is already registered for another character in the established list
        if uc_ign.get() in temp.keys():
            uc_win.destroy()
            # error message prompt if that is the case
            messagebox.showerror('IGN Error',
                                 'The new IGN already exists for another character in the registered list.')
        else:

            # ** Maybe find put this in its own function called 'update_character()' ? **
            # updates the existing character entry 

            # deletes the old character entry in characters dictionary
            del characters[selected_ign]
            
            # create a new character entry with updated details into the characters dictionary
            create_char(uc_ign.get(), uc_job.get(), uc_level.get())

            # closes the popup window
            uc_win.destroy()

    # set the input fields with existing character data
    uc_ign.set(characters[selected_ign].ign)
    uc_job.set(characters[selected_ign].job)
    uc_level.set(characters[selected_ign].level)

    uc_win = tk.Toplevel(blue_frame)
    uc_win.title('Update Character')
    uc_win.geometry('300x200+650+150')

    uc_title_lbl = tk.Label(uc_win, text='Update Character', **aesthetic_params)
    uc_ign_lbl = tk.Label(uc_win, text='In-Game Name:', **aesthetic_params)
    uc_ign_entry = tk.Entry(uc_win, textvariable=uc_ign)
    uc_job_lbl = tk.Label(uc_win, text='Job (Class):', **aesthetic_params)
    uc_job_entry = tk.Entry(uc_win, textvariable=uc_job)
    uc_level_lbl = tk.Label(uc_win, text='Level:', **aesthetic_params)
    uc_level_entry = tk.Entry(uc_win, textvariable=uc_level)
    uc_submit_btn = tk.Button(uc_win, text='Update Roster', **aesthetic_params, command=validate_updated_entry)
    uc_cancel_btn = tk.Button(uc_win, text='Cancel', **aesthetic_params, command=uc_win.destroy)

    uc_title_lbl.grid(row=0, columnspan=2)
    uc_ign_lbl.grid(row=1, column=0)
    uc_ign_entry.grid(row=1, column=1)
    uc_job_lbl.grid(row=2, column=0)
    uc_job_entry.grid(row=2, column=1)
    uc_level_lbl.grid(row=3, column=0)
    uc_level_entry.grid(row=3, column=1)
    uc_submit_btn.grid(row=4, column=0)
    uc_cancel_btn.grid(row=4, column=1)

    uc_win.grid_rowconfigure(0, weight=1)
    uc_win.grid_rowconfigure(1, weight=1)
    uc_win.grid_rowconfigure(2, weight=1)
    uc_win.grid_rowconfigure(3, weight=1)
    uc_win.grid_rowconfigure(4, weight=1)
    uc_win.grid_columnconfigure(0, weight=1)
    uc_win.grid_columnconfigure(1, weight=1)

btn_params = {'font':('Kozuka Gothic Pro B', 12), 'relief': 'raised'}

addchar_btn = tk.Button(blue_frame, text='Add Char', **btn_params, command=add_character_popup)
updchar_btn = tk.Button(blue_frame, text='Update Char', **btn_params, command=update_character_popup)
delchar_btn = tk.Button(blue_frame, text='Delete Char', **btn_params, command=delete_char)

blue_frame.grid_rowconfigure(0, weight=1)
blue_frame.grid_columnconfigure(0, weight=1)
blue_frame.grid_columnconfigure(1, weight=1)
blue_frame.grid_columnconfigure(2, weight=1)

addchar_btn.grid(row=0, column=0)
updchar_btn.grid(row=0, column=1)
delchar_btn.grid(row=0, column=2)

# magenta frame

# updates the utc time clock aka server time
def update_utc():
    # finds the utc timezone's time
    utc_time = dt.datetime.now(timezone.utc)
    # reformats the time to string 
    string_time = utc_time.strftime('%H:%M:%S %p')
    # updates the display label that showcases the utc time
    utc_livetime_lbl.config(text=f"Current Server Time: {string_time}")
    # executes the update_utc function after time elapse (in ms)
    utc_livetime_lbl.after(1000, update_utc)

# ursus time countdown and tracker algorithm (sidenote: bonus as in 2x rewards)
def bonus_ursus_tracker():

    # ursus time ranges
    uto_start_str = '01:00:00'
    uto_end_str = '05:00:00'

    utt_start_str = '18:00:00'
    utt_end_str = '22:00:00'

    # get the current utc time aka server time
    utc_time = dt.datetime.now(timezone.utc)

    # get today's day
    today = utc_time.date()

    # create datetime objects for the ursus times (aka the triggers)
    uto_start = dt.datetime.combine(today, dt.datetime.strptime(uto_start_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    uto_end = dt.datetime.combine(today, dt.datetime.strptime(uto_end_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    utt_start = dt.datetime.combine(today, dt.datetime.strptime(utt_start_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    utt_end = dt.datetime.combine(today, dt.datetime.strptime(utt_end_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # check if server time is currently within the bonus ursus time period
    if utc_time >= uto_start and utc_time <= uto_end:
        ursus_time_lbl.config(text="It's Ursus 2x Now! (Round 1)")
        ursus_time_lbl.after(1000, bonus_ursus_tracker)
    elif utc_time >= utt_start and utc_time <= utt_end:
        ursus_time_lbl.config(text="It's Ursus 2x Now! (Round 2)")
        ursus_time_lbl.after(1000, bonus_ursus_tracker)
    else:
        # determine when the next trigger is (aka ursus bonus time)
        if utc_time <= uto_start:
            next_ursus = uto_start
        elif utc_time <= utt_start:
            next_ursus = utt_start
        else:
            # if the current time has passed for both triggers (ursus times), next_ursus will store the first ursus of the next day
            next_ursus = uto_start + timedelta(days=1)

        # calculate the time remaining til next bonus ursus
        time_remaining = next_ursus - utc_time

        # extract the components of the time_remaining object (timedelta object)
        days = time_remaining.days
        seconds = time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 3600) % 60

        # format the result for time remaining
        time_remaining_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

        # update the ursus_time label with relevant realtime 
        ursus_time_lbl.config(text=f"Next Ursus is at {next_ursus.strftime('%H:%M:%S')} \n Time Remaining until next Ursus: {time_remaining_str}")
        # prompt execution of function every second for a live reading of the ursus time tracker
        ursus_time_lbl.after(1000, bonus_ursus_tracker)

# update time remaining until daily reset
def daily_reset():

    # the new day trigger
    trigger_str = '00:00:00'

    # current time 
    utc_time = dt.datetime.now(timezone.utc)

    # setup datetime obj
    today = utc_time.date()
    trigger = dt.datetime.combine(today, dt.datetime.strptime(trigger_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # calculate time remaining until new day
    time_remaining = (trigger + timedelta(days=1)) - utc_time
    
    # extract components of the time_remaining timedelta obj
    seconds = time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    # create string format of time remaining data
    time_remaining_str = f"Daily Reset in {hours} hours, {minutes} minutes, {seconds} seconds"

    # update the label responsible for displaing the daily reset timer
    daily_reset_lbl.config(text=time_remaining_str)

    # auto execute daily_reset function every second
    daily_reset_lbl.after(1000, daily_reset)

# update time remaining until weekly reset
def weekly_reset():

    # get current utc datetime and other details
    utc_time = dt.datetime.now(timezone.utc)
    today = utc_time.date()
    current_weekday = utc_time.weekday()

    # the target day (i.e. thursday)
    target_weekyday = 3

    # calculate how many days until target day
    days_until_target = (target_weekyday - current_weekday + 7) % 7

    # check to see if today is target day and reset to 7 days if its today
    if days_until_target == 0:
        days_until_target = 7

    # next thursday timedelta obj
    next_thursday_date = today + timedelta(days=days_until_target)

    # target day settings
    trigger_str = '00:00:00'
    trigger_time = dt.datetime.strptime(trigger_str, '%H:%M:%S').time()

    # next thursday datetime obj
    next_thursday = dt.datetime.combine(next_thursday_date, trigger_time, tzinfo=timezone.utc)
    
    # check if today is the target day
    if utc_time.weekday() == 3:
        weekly_reset_lbl.config(text='Weekly Reset is Today')
        weekly_reset_lbl.after(1000, weekly_reset)
    # if its not the target day ..
    else:
        # calcuate the time remaining until next thursday from today
        time_remaining = next_thursday - utc_time

        # extract components from the time_remaining timedelta obj
        days = time_remaining.days
        seconds = time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 3600) % 60

        # string format of time_remaining info
        time_remaining_str = f"Weekly Reset in {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

        # update weekly_reset label
        weekly_reset_lbl.config(text=time_remaining_str)

        # auto execute weekly_reset function after a second
        weekly_reset_lbl.after(1000, weekly_reset)

# temp using blue_button params
utc_livetime_lbl = tk.Label(magenta_frame, font=('Kozuka Gothic Pro B', 12), background='magenta')
ursus_time_lbl = tk.Label(magenta_frame, font=('Kozuka Gothic Pro B', 12), background='magenta')
daily_reset_lbl = tk.Label(magenta_frame, font=('Kozuka Gothic Pro B', 12), background='magenta')
weekly_reset_lbl = tk.Label(magenta_frame, font=('Kozuka Gothic Pro B', 12), background='magenta')

utc_livetime_lbl.grid(row=0, column=0)
ursus_time_lbl.grid(row=1, column=0)
daily_reset_lbl.grid(row=2, column=0)
weekly_reset_lbl.grid(row=3, column=0)

magenta_frame.grid_rowconfigure(0, weight=1)
magenta_frame.grid_rowconfigure(1, weight=1)
magenta_frame.grid_rowconfigure(2, weight=1)
magenta_frame.grid_rowconfigure(3, weight=1)
magenta_frame.grid_columnconfigure(0, weight=1)

# orange frame

bossing_checklist_btn = tk.Button(orange_frame, text='Bossing Checklist', **btn_params)

bossing_checklist_btn.grid(row=0, column=0)

orange_frame.grid_rowconfigure(0, weight=1)
orange_frame.grid_columnconfigure(0, weight=1)

# green frame

# opens website when prompted
def redirect_flame_calc():
    webbrowser.open(r"https://starlinez.github.io/games/maplestory/item-flames")

# opens website when prompted
def redirect_bossing_guide():
    webbrowser.open(r"https://www.youtube.com/watch?v=y74KWpY9xQ0&list=PLa2-sX6gKTH_63Zfjp_W2cmWX7t6rnOuM")

# opens website when prompted
def redirect_wse_calc():
    webbrowser.open(r"https://brendonmay.github.io/wseCalculator/")

guide_calc_lbl = tk.Label(green_frame, text='Guides & Calculators', font=('Kozuka Gothic Pro B', 12), background='green')
flame_calc_btn = tk.Button(green_frame, text='Flame Score Calculator', **btn_params, command=redirect_flame_calc)
bossing_guide_btn = tk.Button(green_frame, text='Curated List of Bossing Guides', **btn_params, command=redirect_bossing_guide)
wse_calc_btn = tk.Button(green_frame, text='Optimize WSE Calculator', **btn_params, command=redirect_wse_calc)

guide_calc_lbl.grid(row=0, columnspan=3)
flame_calc_btn.grid(row=1, column=0)
bossing_guide_btn.grid(row=1, column=1)
wse_calc_btn.grid(row=1, column=2)

green_frame.grid_rowconfigure(0, weight=1)
green_frame.grid_rowconfigure(1, weight=1)
green_frame.grid_columnconfigure(0, weight=1)
green_frame.grid_columnconfigure(1, weight=1)
green_frame.grid_columnconfigure(2, weight=1)

# root configs for resizability ('can ignore for time being, may reinstate later')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# initial function execution to start off the various clocks and time trackers upon app startup
update_utc()
bonus_ursus_tracker()
daily_reset()
weekly_reset()

# loads the existing character entries into the characters dictionary
load_characters()

# load up listbox data
populate_entries()

root.mainloop()

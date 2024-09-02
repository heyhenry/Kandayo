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
    # the main obj
    if isinstance(obj, CharInfo):
        return {
            'ign': obj.ign,
            'job': obj.job,
            'level': obj.level,
            'capped': obj.capped,
            # recursion used here to serialize the sub obj and format as part of main obj
            'bosses': custom_serializer(obj.bosses)
        }
    # the sub obj included in the main obj
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

        # create a defaulted bosslist obj
        boss_list = BossList(False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False, False
                             )

        # create a new character obj
        new_char = CharInfo(ign, job, level, False, boss_list)
        
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
                characters[char_ign] = CharInfo(char_ign, char_info['job'], char_info['level'], char_info['capped'], char_info['bosses'])

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

# bossing checklist popup
def bossing_checklist_popup():

    # checkbutton vars
    cb_cpb = tk.IntVar()
    cb_hh = tk.IntVar()
    cb_cyg = tk.IntVar()
    cb_czak = tk.IntVar()
    cb_pno = tk.IntVar()
    cb_cqueen = tk.IntVar()
    cb_cpierre = tk.IntVar()
    cb_cvonbon = tk.IntVar()
    cb_cvell = tk.IntVar()
    cb_akechi = tk.IntVar()
    cb_hmag = tk.IntVar()
    cb_cpap = tk.IntVar()
    cb_lotus = tk.IntVar()
    cb_damien = tk.IntVar()
    cb_gslime = tk.IntVar()
    cb_lucid = tk.IntVar()
    cb_will = tk.IntVar()
    cb_gloom = tk.IntVar()
    cb_darknell = tk.IntVar()
    cb_vhilla = tk.IntVar()
    cb_seren = tk.IntVar()
    cb_kaling = tk.IntVar() 

    aesthetic_params = {'font': ('Kozuka Gothic Pro B', 12)}

    selected_ign = ''

    # selected character from listbox gets stored in selected_ign
    for i in chars_lb.curselection():
        selected_ign = chars_lb.get(i)

    # validation check to see if a character has been stored in selected_ign
    # if there is no character stored, then show error message and do not execute rest of the function's code
    if selected_ign == '':
        messagebox.showerror('Character Selection Error',
                             'A character has not been selected from the list.')
        # a return statement is required here to let the program know to discontinue the rest of the code 
        # note: unlike in the update_character_popup function, as the aforementioned prevents code execution via 
        # the inability to set the tkinter variables, letting the program know to not run the rest of the function's code
        return

    # load the bosses checkstates
    cb_cpb.set(characters[selected_ign].bosses['Chaos Pink Bean'])
    cb_hh.set(characters[selected_ign].bosses['Hard Hilla'])
    cb_cyg.set(characters[selected_ign].bosses['Cygnus'])
    cb_czak.set(characters[selected_ign].bosses['Chaos Zakum'])
    cb_pno.set(characters[selected_ign].bosses['Princess No'])
    cb_cqueen.set(characters[selected_ign].bosses['Chaos Queen'])
    cb_cpierre.set(characters[selected_ign].bosses['Chaos Pierre'])
    cb_cvonbon.set(characters[selected_ign].bosses['Chaos VonBon'])
    cb_cvell.set(characters[selected_ign].bosses['Chaos Vellum'])
    cb_akechi.set(characters[selected_ign].bosses['Akechi Mitsuhide'])
    cb_hmag.set(characters[selected_ign].bosses['Hard Magnus'])
    cb_cpap.set(characters[selected_ign].bosses['Chaos Papulatus'])
    cb_lotus.set(characters[selected_ign].bosses['Lotus'])
    cb_damien.set(characters[selected_ign].bosses['Damien'])
    cb_gslime.set(characters[selected_ign].bosses['Guardian Slime'])
    cb_lucid.set(characters[selected_ign].bosses['Lucid'])
    cb_will.set(characters[selected_ign].bosses['Will'])
    cb_gloom.set(characters[selected_ign].bosses['Gloom'])
    cb_darknell.set(characters[selected_ign].bosses['Darknell'])
    cb_vhilla.set(characters[selected_ign].bosses['Versus Hilla'])
    cb_seren.set(characters[selected_ign].bosses['Seren'])
    cb_kaling.set(characters[selected_ign].bosses['Kaling'])


    # updating the checkstate of bosses from the bosslist obj of a character
    def updating_bossing_progress(boss_name, cb_boss):
        
        # if user ticks
        if cb_boss.get():
            #change the value of the boss in the boss obj of the selected character
            characters[selected_ign].bosses[boss_name] = True

            # update the new change in the json save file
            json_object = json.dumps(characters, indent=4, default=custom_serializer)

            with open(storage_filename, 'w') as outfile:
                outfile.write(json_object)
        
        # if user unticks
        else:
            characters[selected_ign].bosses[boss_name] = False

            json_object = json.dumps(characters, indent=4, default=custom_serializer)

            with open(storage_filename, 'w') as outfile:
                outfile.write(json_object)

    bc_win = tk.Toplevel(orange_frame)
    bc_win.title('Bossing Checklist')
    # bc_win.geometry()    

    bc_character_lbl = tk.Label(bc_win, text=f"{characters[selected_ign].ign} | {characters[selected_ign].job} | Lv.{characters[selected_ign].level}", **aesthetic_params)
    bc_weeklies_completed_lbl = tk.Checkbutton(bc_win, text=f"Weeklies Completed: {characters[selected_ign].capped}", **aesthetic_params)

    # first column of bosses
    bc_cpb_check = tk.Checkbutton(bc_win, text='Chaos Pink Bean', **aesthetic_params, variable=cb_cpb, command=lambda:updating_bossing_progress('Chaos Pink Bean', cb_cpb))
    bc_hh_check = tk.Checkbutton(bc_win, text='Hard Hilla', **aesthetic_params, variable=cb_hh, command=lambda:updating_bossing_progress('Hard Hilla', cb_hh))
    bc_cyg_check = tk.Checkbutton(bc_win, text='Cygnus', **aesthetic_params, variable=cb_cyg, command=lambda:updating_bossing_progress('Cygnus', cb_cyg))
    bc_czak_check = tk.Checkbutton(bc_win, text='Chaos Zakum', **aesthetic_params, variable=cb_czak, command=lambda:updating_bossing_progress('Chaos Zakum', cb_czak))
    bc_pno_check = tk.Checkbutton(bc_win, text='Princess No', **aesthetic_params, variable=cb_pno, command=lambda:updating_bossing_progress('Princess No', cb_pno))
    bc_cqueen_check = tk.Checkbutton(bc_win, text='Chaos Queen', **aesthetic_params, variable=cb_cqueen, command=lambda:updating_bossing_progress('Chaos Queen', cb_cqueen))
    bc_cpierre_check = tk.Checkbutton(bc_win, text='Chaos Pierre', **aesthetic_params, variable=cb_cpierre, command=lambda:updating_bossing_progress('Chaos Pierre', cb_cpierre))
    bc_cvonbon_check = tk.Checkbutton(bc_win, text='Chaos Von Bon', **aesthetic_params, variable=cb_cvonbon, command=lambda:updating_bossing_progress('Chaos VonBon', cb_cvonbon))
    bc_cvell_check = tk.Checkbutton(bc_win, text='Chaos Vellum', **aesthetic_params, variable=cb_cvell, command=lambda:updating_bossing_progress('Chaos Vellum', cb_cvell))
    bc_akechi_check = tk.Checkbutton(bc_win, text='Akechi Mitsuhide', **aesthetic_params, variable=cb_akechi, command=lambda:updating_bossing_progress('Akechi Mitsuhide', cb_akechi))
    bc_hmag_check = tk.Checkbutton(bc_win, text='Hard Magnus', **aesthetic_params, variable=cb_hmag, command=lambda:updating_bossing_progress('Hard Magnus', cb_hmag))

    # second column of bosses
    bc_cpap_check = tk.Checkbutton(bc_win, text='Chaos Papulatus', **aesthetic_params, variable=cb_cpap, command=lambda:updating_bossing_progress('Chaos Papulatus', cb_cpap))
    bc_lotus_check = tk.Checkbutton(bc_win, text='Lotus', **aesthetic_params, variable=cb_lotus, command=lambda:updating_bossing_progress('Lotus', cb_lotus))
    bc_damien_check = tk.Checkbutton(bc_win, text='Damien', **aesthetic_params, variable=cb_damien, command=lambda:updating_bossing_progress('Damien', cb_damien))
    bc_gslime_check = tk.Checkbutton(bc_win, text='Guardian Slime', **aesthetic_params, variable=cb_gslime, command=lambda:updating_bossing_progress('Guardian Slime', cb_gslime))
    bc_lucid_check = tk.Checkbutton(bc_win, text='Lucid', **aesthetic_params, variable=cb_lucid, command=lambda:updating_bossing_progress('Lucid', cb_lucid))
    bc_will_check = tk.Checkbutton(bc_win, text='Will', **aesthetic_params, variable=cb_will, command=lambda:updating_bossing_progress('Will', cb_will))
    bc_gloom_check = tk.Checkbutton(bc_win, text='Gloom', **aesthetic_params, variable=cb_gloom, command=lambda:updating_bossing_progress('Gloom', cb_gloom))
    bc_darknell_check = tk.Checkbutton(bc_win, text='Darknell', **aesthetic_params, variable=cb_darknell, command=lambda:updating_bossing_progress('Darknell', cb_darknell))
    bc_vhilla_check = tk.Checkbutton(bc_win, text='Versus Hilla', **aesthetic_params, variable=cb_vhilla, command=lambda:updating_bossing_progress('Versus Hilla', cb_vhilla))
    bc_seren_check = tk.Checkbutton(bc_win, text='Seren', **aesthetic_params, variable=cb_seren, command=lambda:updating_bossing_progress('Seren', cb_seren))
    bc_kaling_check = tk.Checkbutton(bc_win, text='Kaling', **aesthetic_params, variable=cb_kaling, command=lambda:updating_bossing_progress('Kaling', cb_kaling))

    bc_close_btn = tk.Button(bc_win, text='Close', **aesthetic_params, command=bc_win.destroy)

    # storing the checkstate values to circumvent python's garbage collection
    bc_cpb_check.var = cb_cpb
    bc_hh_check.var = cb_hh
    bc_cyg_check.var = cb_cyg
    bc_czak_check.var = cb_czak
    bc_pno_check.var = cb_pno
    bc_cqueen_check.var = cb_cqueen
    bc_cpierre_check.var = cb_cpierre
    bc_cvonbon_check.var = cb_cvonbon
    bc_cvell_check.var = cb_cvell
    bc_akechi_check.var = cb_akechi
    bc_hmag_check.var = cb_hmag
    bc_cpap_check.var = cb_cpap
    bc_lotus_check.var = cb_lotus
    bc_damien_check.var = cb_damien
    bc_gslime_check.var = cb_gslime
    bc_lucid_check.var = cb_lucid
    bc_will_check.var = cb_will
    bc_gloom_check.var = cb_gloom
    bc_darknell_check.var = cb_darknell
    bc_vhilla_check.var = cb_vhilla
    bc_seren_check.var = cb_seren
    bc_kaling_check.var = cb_kaling

    # grid layout configs
    bc_character_lbl.grid(row=0, columnspan=2)
    bc_weeklies_completed_lbl.grid(row=1, columnspan=2)

    bc_cpb_check.grid(row=2, column=0, sticky='w')
    bc_hh_check.grid(row=3, column=0, sticky='w')
    bc_cyg_check.grid(row=4, column=0, sticky='w')
    bc_czak_check.grid(row=5, column=0, sticky='w')
    bc_pno_check.grid(row=6, column=0, sticky='w')
    bc_cqueen_check.grid(row=7, column=0, sticky='w')
    bc_cpierre_check.grid(row=8, column=0, sticky='w')
    bc_cvonbon_check.grid(row=9, column=0, sticky='w')
    bc_cvell_check.grid(row=10, column=0, sticky='w')
    bc_akechi_check.grid(row=11, column=0, sticky='w')
    bc_hmag_check.grid(row=12, column=0, sticky='w')

    bc_cpap_check.grid(row=2, column=1, sticky='w')
    bc_lotus_check.grid(row=3, column=1, sticky='w')
    bc_damien_check.grid(row=4, column=1, sticky='w')
    bc_gslime_check.grid(row=5, column=1, sticky='w')
    bc_lucid_check.grid(row=6, column=1, sticky='w')
    bc_will_check.grid(row=7, column=1, sticky='w')
    bc_gloom_check.grid(row=8, column=1, sticky='w')
    bc_darknell_check.grid(row=9, column=1, sticky='w')
    bc_vhilla_check.grid(row=10, column=1, sticky='w')
    bc_seren_check.grid(row=11, column=1, sticky='w')
    bc_kaling_check.grid(row=12, column=1, sticky='w')

    bc_close_btn.grid(row=13, columnspan=2)

    bc_win.grid_rowconfigure(0, weight=1)
    bc_win.grid_rowconfigure(1, weight=1)
    bc_win.grid_rowconfigure(2, weight=1)
    bc_win.grid_rowconfigure(3, weight=1)
    bc_win.grid_rowconfigure(4, weight=1)
    bc_win.grid_rowconfigure(5, weight=1)
    bc_win.grid_rowconfigure(6, weight=1)
    bc_win.grid_rowconfigure(7, weight=1)
    bc_win.grid_rowconfigure(8, weight=1)
    bc_win.grid_rowconfigure(9, weight=1)
    bc_win.grid_rowconfigure(10, weight=1)
    bc_win.grid_rowconfigure(11, weight=1)
    bc_win.grid_rowconfigure(12, weight=1)
    bc_win.grid_rowconfigure(13, weight=1)
    bc_win.grid_columnconfigure(0, weight=1)
    bc_win.grid_columnconfigure(1, weight=1)

bossing_checklist_btn = tk.Button(orange_frame, text='Bossing Checklist', **btn_params, command=bossing_checklist_popup)

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

# print tests
# print(characters['Remu1002'].bosses)
# cpb = 'Chaos Pink Bean'
# print(characters['Remu1002'].bosses[cpb])

root.mainloop()

# note for next session:
# continue working on function 'saving_bossing_progress(v)'
# ^ figure out how to save the state globally in characters and then potentially create an update_character function that doesnt require the call of create_char.

# the 'lambda o:o.__dict__ helped update the json file data for the boss boolean states, but does not save the checkbutton save state, 
# also i dont understand lambda o: o.__dict__ enough, learn and use or find different method to acheive same outcome
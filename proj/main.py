import tkinter as tk
from tkinter import messagebox
from datetime import timezone, timedelta
import datetime as dt
import webbrowser
from charinfo import CharInfo
from bosslist import BossList
from userinfo import UserInfo
import json
import os

# list of character (CharInfo) objects
characters = {}

# save file var
storage_filename = 'characters_save.json'
usr_filename = 'usr_save.json'

# load user
user = {}

# load the user data
def load_user():
    if os.path.exists(usr_filename):
        with open(usr_filename, 'r') as file:
            usr_data = json.load(file)
            for usr, usr_info in usr_data.items():
                user[usr] = UserInfo(usr_info['mesos_balance'], usr_info['boss_crystal_count'])

# // json function //
# custom json serializer
def custom_serializer(obj):
    # CharInfo Object
    if isinstance(obj, CharInfo):
        return {
            'ign': obj.ign,
            'job': obj.job,
            'level': obj.level,
            'boss_list': custom_serializer(obj.boss_list)
        }
    # BossList object
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
    elif isinstance(obj, UserInfo):
        return {
            'mesos_balance': obj.mesos_balance,
            'boss_crystal_count': obj.boss_crystal_count
        }
    return obj

# // yellow functions //
# updates the utc time clock (server time)
def update_utc():
    # get the current utc time
    utc_time = dt.datetime.now(timezone.utc)
    # reformat the time to string
    string_time = utc_time.strftime('%H:%M:%S')
    # update the display label to showcase live time
    utc_livetime_lbl.config(text=f'Server Time: {string_time}')
    # execute the update_utc function after time elapsed (1 second)
    utc_livetime_lbl.after(1000, update_utc)

# ursus time countdown tracker (bonus as in 2x rewards)
def bonus_ursus_tracker():

    # ursus bonus time ranges
    uto_start_str = '01:00:00'
    uto_end_str = '05:00:00'

    utt_start_str = '18:00:00'
    utt_end_str = '22:00:00'

    # get current utc time
    utc_time = dt.datetime.now(timezone.utc)

    # get today's day
    today = utc_time.date()

    # create datetime objects for the ursus times
    uto_start = dt.datetime.combine(today, dt.datetime.strptime(uto_start_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    uto_end = dt.datetime.combine(today, dt.datetime.strptime(uto_end_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    utt_start = dt.datetime.combine(today, dt.datetime.strptime(utt_start_str, '%H:%M:%S').time(), tzinfo=timezone.utc)
    utt_end = dt.datetime.combine(today, dt.datetime.strptime(utt_end_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # check if the server time is currently within the bonus ursus time period
    if utc_time >= uto_start and utc_time <= uto_end:
        ursus_time_lbl.config(text='Active Ursus 2x (Round One)')
        ursus_time_lbl.after(1000, bonus_ursus_tracker)
    elif utc_time >= utt_start and utc_time <= utt_end:
        ursus_time_lbl.config(text='Active Ursus 2x (Round Two)')
        ursus_time_lbl.after(1000, bonus_ursus_tracker)
    else:
        # determine when the next ursus bonus will occur
        if utc_time <= uto_start:
            next_ursus = uto_start
        elif utc_time <= utt_start:
            next_ursus = utt_start
        else:
            # if the current time has passed round two, next_ursus will store the first ursus of the next day
            next_ursus = uto_start + timedelta(days=1)

        # calculate the time remaining til next bonus ursus
        time_remaining = next_ursus - utc_time

        # extract the components of the time_remaining timedelta object
        seconds = time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 4600) % 60

        # format the result for the time remaining
        time_remaining_str = f'{hours}:{minutes}:{seconds}'

        # update the ursus_time_lbl with relevant real time data
        ursus_time_lbl.config(text=f'Next Bonus Ursus: {time_remaining_str}')
        # auto execute function per second
        ursus_time_lbl.after(1000, bonus_ursus_tracker)

# update time remaining until daily reset
def daily_reset():

    # the new day trigger
    trigger_str = '00:00:00'

    # current server time
    utc_time = dt.datetime.now(timezone.utc)

    # setup datetime object
    today = utc_time.date()
    trigger = dt.datetime.combine(today, dt.datetime.strptime(trigger_str, '%H:%M:%S').time(), tzinfo=timezone.utc)

    # calculate time remaining until new day
    time_remaining = (trigger + timedelta(days=1)) - utc_time

    # extract components of the time_remaining timedelta object
    seconds = time_remaining.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    # create string format for time remaining
    time_remaining_str = f'Daily Reset: {hours}:{minutes}:{seconds}'

    # update the label responsible for displaying the daily reset timer
    daily_reset_lbl.config(text=time_remaining_str)

    # auto execute daily_reset() function every second
    daily_reset_lbl.after(1000, daily_reset)

# update time remaining until weekly reset
def weekly_reset():

    # get current server date and time
    utc_time = dt.datetime.now(timezone.utc)
    today = utc_time.date()
    current_weekday = utc_time.weekday()

    # the target day (i.e. thursday)
    target_weekday = 3

    # calculate how many days until target day
    days_until_target = (target_weekday - current_weekday + 7) % 7

    # check to see if today is the target day, and reset to 7 days if it is
    if days_until_target == 0:
        days_until_target = 7

    # next thursday time delta
    next_thursday_date = today + timedelta(days=days_until_target)

    # target day settings
    trigger_str = '00:00:00'
    trigger_time = dt.datetime.strptime(trigger_str, '%H:%M:%S').time()

    # next thursday datetime object
    next_thursday = dt.datetime.combine(next_thursday_date, trigger_time, tzinfo=timezone.utc)

    # check if today is the target day
    if utc_time.weekday() == 3:
        weekly_reset_lbl.config(text='Today')
        weekly_reset_lbl.after(1000, weekly_reset)
    # otherwise
    else:
        #calculate the time remaining until next thursday from today
        time_remaining = next_thursday - utc_time

        # extract components from the time_remaining timedelta object
        days = time_remaining.days
        seconds = time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = (seconds % 3600) % 60

        # string format of the time_remaining data
        time_remaining_str = f'Weekly Reset: {days}:{hours}:{minutes}:{seconds}'

        # update weekly_reset label
        weekly_reset_lbl.config(text=time_remaining_str)

        # auto execute weekly_reset() function after a second
        weekly_reset_lbl.after(1000, weekly_reset)

# // red functions //
# fill listbox 'chars_lb' with all characters found in the 'characters' dictionary
def populate_entries():

    # loop through the 'characters' dictionary and insert their character ign
    for character_ign in characters:
        chars_lb.insert('end', character_ign)

# // blue functions //
# create a new character
def create_character(ign, job, level):

    # create a default BossList object
    boss_list = BossList(False, False, False, False, False, False, False, False, False, False, False,
                            False, False, False, False, False, False, False, False, False, False, False
                            )
    
    # create a new character object
    new_char = CharInfo(ign, job, level, boss_list)

    # add new character object to the 'characters' dictionary
    characters[new_char.ign] = new_char

    # serialize 'characters' dictionary to json
    json_data = json.dumps(characters, indent=4, default=custom_serializer)

    # save 'characters' dictionary to save file
    with open(storage_filename, 'w') as outfile:
        outfile.write(json_data)

    # clear the characters list box
    chars_lb.delete(0, 'end')

    # refill the characters list box with latest data
    populate_entries()

# load save data
def load_characters():

    # check if file exists
    if os.path.exists(storage_filename):
        # read file
        with open(storage_filename, 'r') as file:
            # load the save data
            characters_data = json.load(file)

            # update the 'characters' dictionary with save data
            for char_ign, char_info in characters_data.items():
                characters[char_ign] = CharInfo(char_ign, char_info['job'], char_info['level'], char_info['boss_list'])

# add a new character pop-up winow
def add_character_popup():

    ac_ign = tk.StringVar()
    ac_job = tk.StringVar()
    ac_level = tk.StringVar()

    # check to see if character already exists
    def validate_character_entry(check_ign):
        # if character already exists in 'characters' dictionary, give error message and close window
        if check_ign in characters.keys():
            ac_win.destroy()
            messagebox.showerror('Invalid IGN (Player Name)',
                                 'The IGN (Character Name) has already been registered.')
        # if use has not filled all input fields
        elif ac_ign.get() == '' or ac_job.get() == '' or ac_level.get() == '':
            ac_win.destroy()
            messagebox.showerror('Missing Information',
                                 'All input fields are not filled')
        else:
            # otherwise, update 'characters' dictionary with new entry and close pop-up
            create_character(ac_ign.get(), ac_job.get(), ac_level.get())
            ac_win.destroy()

    # ac short for add_character
    ac_win = tk.Toplevel(blue_frame)
    ac_win.title('Add New Character')
    ac_win.geometry('300x200+650+150')

    ac_title_lbl = tk.Label(ac_win, text='Add New Character', font=('Kozuka Gothic Pro B', 12))
    ac_ign_lbl = tk.Label(ac_win, text='In-Game Name:', font=('Kozuka Gothic Pro B', 12))
    ac_ign_entry = tk.Entry(ac_win, textvariable=ac_ign)
    ac_job_lbl = tk.Label(ac_win, text='Job (Class):', font=('Kozuka Gothic Pro B', 12))
    ac_job_entry = tk.Entry(ac_win, textvariable=ac_job)
    ac_level_lbl = tk.Label(ac_win, text='Level:', font=('Kozuka Gothic Pro B', 12))
    ac_level_entry = tk.Entry(ac_win, textvariable=ac_level)
    ac_submit_btn = tk.Button(ac_win, text='Add to Roster', font=('Kozuka Gothic Pro B', 12), command=lambda:validate_character_entry(ac_ign.get()))
    ac_cancel_btn = tk.Button(ac_win, text='Cancel', font=('Kozuka Gothic Pro B', 12), command=ac_win.destroy)

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

# update an existing character's details pop-up window
def update_character_popup():

    uc_ign = tk.StringVar()
    uc_job = tk.StringVar()
    uc_level = tk.StringVar()

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

            # deletes the old character entry in characters dictionary
            del characters[selected_ign]
            
            # create a new character entry with updated details into the characters dictionary
            create_character(uc_ign.get(), uc_job.get(), uc_level.get())

            # closes the popup window
            uc_win.destroy()

    # set the input fields with existing character data
    uc_ign.set(characters[selected_ign].ign)
    uc_job.set(characters[selected_ign].job)
    uc_level.set(characters[selected_ign].level)

    uc_win = tk.Toplevel(blue_frame)
    uc_win.title('Update Character')
    uc_win.geometry('300x200+650+150')

    uc_title_lbl = tk.Label(uc_win, text='Update Character', font=('Kozuka Gothic Pro B', 12))
    uc_ign_lbl = tk.Label(uc_win, text='In-Game Name:', font=('Kozuka Gothic Pro B', 12))
    uc_ign_entry = tk.Entry(uc_win, textvariable=uc_ign)
    uc_job_lbl = tk.Label(uc_win, text='Job (Class):', font=('Kozuka Gothic Pro B', 12))
    uc_job_entry = tk.Entry(uc_win, textvariable=uc_job)
    uc_level_lbl = tk.Label(uc_win, text='Level:', font=('Kozuka Gothic Pro B', 12))
    uc_level_entry = tk.Entry(uc_win, textvariable=uc_level)
    uc_submit_btn = tk.Button(uc_win, text='Update Roster', font=('Kozuka Gothic Pro B', 12), command=validate_updated_entry)
    uc_cancel_btn = tk.Button(uc_win, text='Cancel', font=('Kozuka Gothic Pro B', 12), command=uc_win.destroy)

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

# delete an existing character
def delete_character():

    # store selected character's key
    selected_ign = ''

    # retrieve the selected character's key
    for i in chars_lb.curselection():
        selected_ign = chars_lb.get(i)

    # validation check if no character has been selected
    if selected_ign == '':
        messagebox.showerror('No Selection Error', 
                             'No character has been selected in the list.')
    else:
        # load and delete the selected character from save data
        with open(storage_filename, 'r') as file:
            json_data = json.load(file)
            del json_data[selected_ign]

        # update the save data
        with open(storage_filename, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)

        # delete the key from the 'characters' dictionary
        del characters[selected_ign]

        # delete all character entries in the current listbox
        chars_lb.delete(0, 'end')

        # update the listbox with latest characters data
        populate_entries()

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

    selected_ign = ''

    # selected character from listbox gets stored in selected_ign
    for i in chars_lb.curselection():
        selected_ign = chars_lb.get(i)

    # load the characters dictionary directly via parsing the json file into a python object
    load_characters()

    # validation check to see if a character has been stored in selected_ign
    # if there is no character stored, then show error message and do not execute rest of the function's code
    if selected_ign == '':
        messagebox.showerror('Character Selection Error',
                             'A character has not been selected from the list.')
        # a return statement is required here to let the program know to discontinue the rest of the code 
        # note: unlike in the update_character_popup function, as the aforementioned prevents code execution via 
        # the inability to set the tkinter variables, letting the program know to not run the rest of the function's code
        return

    # load the boss_list checkstates
    cb_cpb.set(characters[selected_ign].boss_list['Chaos Pink Bean'])
    cb_hh.set(characters[selected_ign].boss_list['Hard Hilla'])
    cb_cyg.set(characters[selected_ign].boss_list['Cygnus'])
    cb_czak.set(characters[selected_ign].boss_list['Chaos Zakum'])
    cb_pno.set(characters[selected_ign].boss_list['Princess No'])
    cb_cqueen.set(characters[selected_ign].boss_list['Chaos Queen'])
    cb_cpierre.set(characters[selected_ign].boss_list['Chaos Pierre'])
    cb_cvonbon.set(characters[selected_ign].boss_list['Chaos VonBon'])
    cb_cvell.set(characters[selected_ign].boss_list['Chaos Vellum'])
    cb_akechi.set(characters[selected_ign].boss_list['Akechi Mitsuhide'])
    cb_hmag.set(characters[selected_ign].boss_list['Hard Magnus'])
    cb_cpap.set(characters[selected_ign].boss_list['Chaos Papulatus'])
    cb_lotus.set(characters[selected_ign].boss_list['Lotus'])
    cb_damien.set(characters[selected_ign].boss_list['Damien'])
    cb_gslime.set(characters[selected_ign].boss_list['Guardian Slime'])
    cb_lucid.set(characters[selected_ign].boss_list['Lucid'])
    cb_will.set(characters[selected_ign].boss_list['Will'])
    cb_gloom.set(characters[selected_ign].boss_list['Gloom'])
    cb_darknell.set(characters[selected_ign].boss_list['Darknell'])
    cb_vhilla.set(characters[selected_ign].boss_list['Versus Hilla'])
    cb_seren.set(characters[selected_ign].boss_list['Seren'])
    cb_kaling.set(characters[selected_ign].boss_list['Kaling'])

    # reset all boss status
    def reset_boss_list():

        # reset all checkbutton variables to False
        cb_cpb.set(False)
        cb_hh.set(False)
        cb_cyg.set(False)
        cb_czak.set(False)
        cb_pno.set(False)
        cb_cqueen.set(False)
        cb_cpierre.set(False)
        cb_cvonbon.set(False)
        cb_cvell.set(False)
        cb_akechi.set(False)
        cb_hmag.set(False)
        cb_cpap.set(False)
        cb_lotus.set(False)
        cb_damien.set(False)
        cb_gslime.set(False)
        cb_lucid.set(False)
        cb_will.set(False)
        cb_gloom.set(False)
        cb_darknell.set(False)
        cb_vhilla.set(False)
        cb_seren.set(False)
        cb_kaling.set(False)

        # loop through all bosses in the selected character's boss_list object
        for boss_name, boss_val in characters[selected_ign].boss_list.items():
            # set boss values to false
            characters[selected_ign].boss_list[boss_name] = False

        # update save data
        json_object = json.dumps(characters, indent=4, default=custom_serializer)

        with open(storage_filename, 'w') as outfile:
            outfile.write(json_object)

    # updating the checkstate of bosses from the boss_list object of a character
    def updating_bossing_progress(boss_name, cb_boss):
        
        # if user ticks
        if cb_boss.get():
            #change the value of the boss in the boss obj of the selected character
            characters[selected_ign].boss_list[boss_name] = True

            # update the new change in the json save file
            json_object = json.dumps(characters, indent=4, default=custom_serializer)

            with open(storage_filename, 'w') as outfile:
                outfile.write(json_object)
        
        # if user unticks
        else:
            characters[selected_ign].boss_list[boss_name] = False

            json_object = json.dumps(characters, indent=4, default=custom_serializer)

            with open(storage_filename, 'w') as outfile:
                outfile.write(json_object)

    bc_win = tk.Toplevel(blue_frame)
    bc_win.title('Bossing Checklist')
    bc_win.geometry('400x700')    

    bc_character_lbl = tk.Label(bc_win, text=f"{characters[selected_ign].ign} | {characters[selected_ign].job} | Lv.{characters[selected_ign].level}", font= ('Kozuka Gothic Pro B', 12))

    # first column of boss_list
    bc_cpb_check = tk.Checkbutton(bc_win, text='Chaos Pink Bean', font= ('Kozuka Gothic Pro B', 12), variable=cb_cpb, command=lambda:updating_bossing_progress('Chaos Pink Bean', cb_cpb))
    bc_hh_check = tk.Checkbutton(bc_win, text='Hard Hilla', font= ('Kozuka Gothic Pro B', 12), variable=cb_hh, command=lambda:updating_bossing_progress('Hard Hilla', cb_hh))
    bc_cyg_check = tk.Checkbutton(bc_win, text='Cygnus', font= ('Kozuka Gothic Pro B', 12), variable=cb_cyg, command=lambda:updating_bossing_progress('Cygnus', cb_cyg))
    bc_czak_check = tk.Checkbutton(bc_win, text='Chaos Zakum', font= ('Kozuka Gothic Pro B', 12), variable=cb_czak, command=lambda:updating_bossing_progress('Chaos Zakum', cb_czak))
    bc_pno_check = tk.Checkbutton(bc_win, text='Princess No', font= ('Kozuka Gothic Pro B', 12), variable=cb_pno, command=lambda:updating_bossing_progress('Princess No', cb_pno))
    bc_cqueen_check = tk.Checkbutton(bc_win, text='Chaos Queen', font= ('Kozuka Gothic Pro B', 12), variable=cb_cqueen, command=lambda:updating_bossing_progress('Chaos Queen', cb_cqueen))
    bc_cpierre_check = tk.Checkbutton(bc_win, text='Chaos Pierre', font= ('Kozuka Gothic Pro B', 12), variable=cb_cpierre, command=lambda:updating_bossing_progress('Chaos Pierre', cb_cpierre))
    bc_cvonbon_check = tk.Checkbutton(bc_win, text='Chaos Von Bon', font= ('Kozuka Gothic Pro B', 12), variable=cb_cvonbon, command=lambda:updating_bossing_progress('Chaos VonBon', cb_cvonbon))
    bc_cvell_check = tk.Checkbutton(bc_win, text='Chaos Vellum', font= ('Kozuka Gothic Pro B', 12), variable=cb_cvell, command=lambda:updating_bossing_progress('Chaos Vellum', cb_cvell))
    bc_akechi_check = tk.Checkbutton(bc_win, text='Akechi Mitsuhide', font= ('Kozuka Gothic Pro B', 12), variable=cb_akechi, command=lambda:updating_bossing_progress('Akechi Mitsuhide', cb_akechi))
    bc_hmag_check = tk.Checkbutton(bc_win, text='Hard Magnus', font= ('Kozuka Gothic Pro B', 12), variable=cb_hmag, command=lambda:updating_bossing_progress('Hard Magnus', cb_hmag))

    # second column of boss_list
    bc_cpap_check = tk.Checkbutton(bc_win, text='Chaos Papulatus', font= ('Kozuka Gothic Pro B', 12), variable=cb_cpap, command=lambda:updating_bossing_progress('Chaos Papulatus', cb_cpap))
    bc_lotus_check = tk.Checkbutton(bc_win, text='Lotus', font= ('Kozuka Gothic Pro B', 12), variable=cb_lotus, command=lambda:updating_bossing_progress('Lotus', cb_lotus))
    bc_damien_check = tk.Checkbutton(bc_win, text='Damien', font= ('Kozuka Gothic Pro B', 12), variable=cb_damien, command=lambda:updating_bossing_progress('Damien', cb_damien))
    bc_gslime_check = tk.Checkbutton(bc_win, text='Guardian Slime', font= ('Kozuka Gothic Pro B', 12), variable=cb_gslime, command=lambda:updating_bossing_progress('Guardian Slime', cb_gslime))
    bc_lucid_check = tk.Checkbutton(bc_win, text='Lucid', font= ('Kozuka Gothic Pro B', 12), variable=cb_lucid, command=lambda:updating_bossing_progress('Lucid', cb_lucid))
    bc_will_check = tk.Checkbutton(bc_win, text='Will', font= ('Kozuka Gothic Pro B', 12), variable=cb_will, command=lambda:updating_bossing_progress('Will', cb_will))
    bc_gloom_check = tk.Checkbutton(bc_win, text='Gloom', font= ('Kozuka Gothic Pro B', 12), variable=cb_gloom, command=lambda:updating_bossing_progress('Gloom', cb_gloom))
    bc_darknell_check = tk.Checkbutton(bc_win, text='Darknell', font= ('Kozuka Gothic Pro B', 12), variable=cb_darknell, command=lambda:updating_bossing_progress('Darknell', cb_darknell))
    bc_vhilla_check = tk.Checkbutton(bc_win, text='Versus Hilla', font= ('Kozuka Gothic Pro B', 12), variable=cb_vhilla, command=lambda:updating_bossing_progress('Versus Hilla', cb_vhilla))
    bc_seren_check = tk.Checkbutton(bc_win, text='Seren', font= ('Kozuka Gothic Pro B', 12), variable=cb_seren, command=lambda:updating_bossing_progress('Seren', cb_seren))
    bc_kaling_check = tk.Checkbutton(bc_win, text='Kaling', font= ('Kozuka Gothic Pro B', 12), variable=cb_kaling, command=lambda:updating_bossing_progress('Kaling', cb_kaling))

    bc_reset_btn = tk.Button(bc_win, text='Reset All', font= ('Kozuka Gothic Pro B', 12), command=reset_boss_list)
    bc_close_btn = tk.Button(bc_win, text='Close', font= ('Kozuka Gothic Pro B', 12), command=bc_win.destroy)

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

    # grid layout configurations
    bc_character_lbl.grid(row=0, columnspan=2)

    bc_cpb_check.grid(row=2, column=0, sticky='w', padx=20)
    bc_hh_check.grid(row=3, column=0, sticky='w', padx=20)
    bc_cyg_check.grid(row=4, column=0, sticky='w', padx=20)
    bc_czak_check.grid(row=5, column=0, sticky='w', padx=20)
    bc_pno_check.grid(row=6, column=0, sticky='w', padx=20)
    bc_cqueen_check.grid(row=7, column=0, sticky='w', padx=20)
    bc_cpierre_check.grid(row=8, column=0, sticky='w', padx=20)
    bc_cvonbon_check.grid(row=9, column=0, sticky='w', padx=20)
    bc_cvell_check.grid(row=10, column=0, sticky='w', padx=20)
    bc_akechi_check.grid(row=11, column=0, sticky='w', padx=20)
    bc_hmag_check.grid(row=12, column=0, sticky='w', padx=20)

    bc_cpap_check.grid(row=2, column=1, sticky='w', padx=20)
    bc_lotus_check.grid(row=3, column=1, sticky='w', padx=20)
    bc_damien_check.grid(row=4, column=1, sticky='w', padx=20)
    bc_gslime_check.grid(row=5, column=1, sticky='w', padx=20)
    bc_lucid_check.grid(row=6, column=1, sticky='w', padx=20)
    bc_will_check.grid(row=7, column=1, sticky='w', padx=20)
    bc_gloom_check.grid(row=8, column=1, sticky='w', padx=20)
    bc_darknell_check.grid(row=9, column=1, sticky='w', padx=20)
    bc_vhilla_check.grid(row=10, column=1, sticky='w', padx=20)
    bc_seren_check.grid(row=11, column=1, sticky='w', padx=20)
    bc_kaling_check.grid(row=12, column=1, sticky='w', padx=20)

    bc_reset_btn.grid(row=13, column=0)
    bc_close_btn.grid(row=13, column=1)

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

# // purple functions //
# add mesos amount to balance
def add_mesos():
    
    mesos_amount = tk.StringVar()

    def topup_balance():

        # validate input
        received_input = mesos_amount.get()

        if received_input.isdigit():
            # updates the mesos balance of the user
            user['usr'].mesos_balance += int(received_input)

            # update the user save file
            json_object = json.dumps(user, indent=4, default=custom_serializer)

            with open(usr_filename, 'w') as outfile:
                outfile.write(json_object)

            # update the mesos balance label
            mesos_balance_display_lbl.config(text=f'{user["usr"].mesos_balance}')

            # close popup
            am_win.destroy()
        else:
            # send error prompt
            messagebox.showerror('Invalid Input', 
                                 'Digits Only')
            # present popup window post closure of error prompt
            am_win.lift()

    # small popup window asking for user input
    am_win = tk.Toplevel(purple_frame)
    am_win.title('Add Mesos')
    am_win.geometry('200x110+900+350')
    am_prompt_lbl = tk.Label(am_win, text='Enter Mesos Amount', font=('Kozuka Gothic Pro B', 12))
    am_amount_entry = tk.Entry(am_win, font=('Kozuka Gothic Pro B', 12), textvariable=mesos_amount)
    am_submit_btn = tk.Button(am_win, text='Add to Balance', font=('Kozuka Gothic Pro B', 12), command=topup_balance)

    am_prompt_lbl.grid(row=0, column=0)
    am_amount_entry.grid(row=1, column=0)
    am_submit_btn.grid(row=2, column=0)

    am_win.grid_rowconfigure(0, weight=1)
    am_win.grid_rowconfigure(1, weight=1)
    am_win.grid_rowconfigure(2, weight=1)
    am_win.grid_columnconfigure(0, weight=1)

# subtract mesos amount from balance
def subtract_mesos():

    mesos_amount = tk.StringVar()

    def reduce_balance():

        received_input = mesos_amount.get()

        if received_input.isdigit():
            # validation to ensure input amount is not larger than balance amount
            if int(received_input) > user['usr'].mesos_balance:
                messagebox.showerror('Invalid Input',
                                     'Your amount exceeds your current mesos balance')
                sm_win.lift()
            else:
                user['usr'].mesos_balance -= int(received_input)

                json_object = json.dumps(user, indent=4, default=custom_serializer)

                with open(usr_filename, 'w') as outfile:
                    outfile.write(json_object)

                mesos_balance_display_lbl.config(text=f'{user["usr"].mesos_balance}')

                sm_win.destroy()
        else:
            messagebox.showerror('Invalid Input',
                                 'Digits Only')
            sm_win.lift()

    # small popup window asking for user input
    sm_win = tk.Toplevel(purple_frame)
    sm_win.title('Subtract Mesos')
    sm_win.geometry('200x110+900+350')
    sm_prompt_lbl = tk.Label(sm_win, text='Enter Mesos Amount', font=('Kozuka Gothic Pro B', 12))
    sm_amount_entry = tk.Entry(sm_win, font=('Kozuka Gothic Pro B', 12), textvariable=mesos_amount)
    sm_submit_btn = tk.Button(sm_win, text='Subtract from Balance', font=('Kozuka Gothic Pro B', 12), command=reduce_balance)

    sm_prompt_lbl.grid(row=0, column=0)
    sm_amount_entry.grid(row=1, column=0)
    sm_submit_btn.grid(row=2, column=0)

    sm_win.grid_rowconfigure(0, weight=1)
    sm_win.grid_rowconfigure(1, weight=1)
    sm_win.grid_rowconfigure(2, weight=1)
    sm_win.grid_columnconfigure(0, weight=1)

# // orange functions // 
# open weblink
def open_hotlink(hotlink):
    webbrowser.open(hotlink)

# editing hotlinks
def edit_hotlinks():

    ehl_win = tk.Toplevel(orange_frame)
    ehl_win.title('Edit Hotlinks')
    ehl_win.geometry('+600+150')

    ehl_first_hotlink_lbl = tk.Label(ehl_win, text='Hot Link 1')
    ehl_first_hotlink_entry = tk.Entry(ehl_win, textvariable=first_hotlink)
    ehl_second_hotlink_lbl = tk.Label(ehl_win, text='Hot Link 2')
    ehl_second_hotlink_entry = tk.Entry(ehl_win, textvariable=second_hotlink)
    ehl_third_hotlink_lbl = tk.Label(ehl_win, text='Hot Link 3')
    ehl_third_hotlink_entry = tk.Entry(ehl_win, textvariable=third_hotlink)
    ehl_edit_btn = tk.Button(ehl_win, text='Save Edit')

    ehl_first_hotlink_lbl.grid(row=0, column=0)
    ehl_first_hotlink_entry.grid(row=0, column=1)
    ehl_second_hotlink_lbl.grid(row=1, column=0)
    ehl_second_hotlink_entry.grid(row=1, column=1)
    ehl_third_hotlink_lbl.grid(row=2, column=0)
    ehl_third_hotlink_entry.grid(row=2, column=1)
    ehl_edit_btn.grid(row=3, columnspan=2)

# load in the user 
load_user()

root = tk.Tk()
# position window display upon open
root.geometry('+600+150')
root.resizable(False, False)

# // Setting up Frames //
yellow_frame = tk.Frame(root, width=800, height=120, bg='yellow', highlightbackground='black', highlightthickness=2, borderwidth=1, padx=5, pady=5)
red_frame = tk.Frame(root, width=300, height=300, bg='red', highlightbackground='black', highlightthickness=1)
blue_frame = tk.Frame(root, width=300, height=100, bg='blue', highlightbackground='black', highlightthickness=1)
purple_frame = tk.Frame(root, width=500, height=400, bg='magenta', highlightbackground='black', highlightthickness=1)
orange_frame = tk.Frame(root, width=500, height=100, bg='orange', highlightbackground='black', highlightthickness=1)

yellow_frame.grid(row=0, columnspan=2, sticky='nswe')
red_frame.grid(row=1, column=0, sticky='nswe')
blue_frame.grid(row=2, column=0, sticky='nswe')
purple_frame.grid(row=1, rowspan=2, column=1, sticky='nswe')
orange_frame.grid(row=2, column=1, sticky='nswe')

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

yellow_frame.grid_propagate(False)
purple_frame.grid_propagate(False)
red_frame.grid_propagate(False)
blue_frame.grid_propagate(False)
orange_frame.grid_propagate(False)

# // yellow frame //
# yellow widgets
utc_livetime_lbl = tk.Label(yellow_frame, font=('Kozuka Gothic Pro B', 12), background='yellow')
ursus_time_lbl = tk.Label(yellow_frame, font=('Kozuka Gothic Pro B', 12), background='yellow')
daily_reset_lbl = tk.Label(yellow_frame, font=('Kozuka Gothic Pro B', 12), background='yellow')
weekly_reset_lbl = tk.Label(yellow_frame, font=('Kozuka Gothic Pro B', 12), background='yellow')

utc_livetime_lbl.grid(row=0, column=0)
ursus_time_lbl.grid(row=1, column=0)
daily_reset_lbl.grid(row=0, column=1)
weekly_reset_lbl.grid(row=1, column=1)

yellow_frame.grid_rowconfigure(0, weight=1)
yellow_frame.grid_rowconfigure(1, weight=1)
yellow_frame.grid_columnconfigure(0, weight=1)
yellow_frame.grid_columnconfigure(1, weight=1)

# // red frame // 
# red widgets
chars_lb = tk.Listbox(red_frame)
clb_scrollbar = tk.Scrollbar(red_frame)

chars_lb.pack(side='left', fill='both', expand=True, padx=(20, 0), pady=20)
clb_scrollbar.pack(side='right', fill='both', padx=(0, 20), pady=20)

chars_lb.config(yscrollcommand=clb_scrollbar.set)
clb_scrollbar.config(command=chars_lb.yview)

# // blue frame // 
# blue widgets
addchar_btn = tk.Button(blue_frame, text='Add Character', font=('Kozuka Gothic Pro B', 10), command=add_character_popup)
updchar_btn = tk.Button(blue_frame, text='Update Character', font=('Kozuka Gothic Pro B', 10), command=update_character_popup)
delchar_btn = tk.Button(blue_frame, text='Delete Character', font=('Kozuka Gothic Pro B', 10), command=delete_character)
bossing_checklist_btn = tk.Button(blue_frame, text='Bossing Checklist', font=('Kozuka Gothic Pro B', 10), command=bossing_checklist_popup)

addchar_btn.grid(row=0, column=0)
updchar_btn.grid(row=0, column=1)
delchar_btn.grid(row=1, column=0)
bossing_checklist_btn.grid(row=1, column=1)

blue_frame.grid_rowconfigure(0, weight=1)
blue_frame.grid_rowconfigure(1, weight=1)
blue_frame.grid_columnconfigure(0, weight=1)
blue_frame.grid_columnconfigure(1, weight=1)

# // purple // 
# purple widgets
mesos_balance_title_lbl = tk.Label(purple_frame, text='Mesos Balance:', font=('Kozuka Gothic Pro B', 12), bg='magenta')
mesos_balance_display_lbl = tk.Label(purple_frame, text=f'{user['usr'].mesos_balance}', font=('Kozuka Gothic Pro B', 10), bg='magenta')
add_mesos_btn = tk.Button(purple_frame, text='Add Mesos', font=('Kozuka Gothic Pro B', 10), command=add_mesos)
remove_mesos_btn = tk.Button(purple_frame, text='Remove Mesos', font=('Kozuka Gothic Pro B', 10), command=subtract_mesos)

bc_remaining_lbl = tk.Label(purple_frame, text=f'Boss Cyrstals Remaining:', font=('Kozuka Gothic Pro B', 12), bg='magenta')
bc_sold_lbl = tk.Label(purple_frame, text=f'Boss Crystals Sold:', font=('Kozuka Gothic Pro B', 12), bg='magenta')
wm_gained_lbl = tk.Label(purple_frame, text=f'Weekly Mesos Gained:', font=('Kozuka Gothic Pro B', 12), bg='magenta')

mesos_balance_title_lbl.place(x=0, y=10, width=500, height=30)
mesos_balance_display_lbl.place(x=0, y=30, width=500, height=30)
add_mesos_btn.place(x=70, y=60, width=150, height=30)
remove_mesos_btn.place(x=280, y=60, width=150, height=30)

bc_remaining_lbl.place(x=25, y=110, width=250, height=30)
bc_sold_lbl.place(x=0, y=155, width=250, height=30)
wm_gained_lbl.place(x=15, y=200, width=250, height=30)

# // orange //
# orange widgets
hotlink_one_btn = tk.Button(orange_frame, text='Hot Link 1', font=('Kozuka Gothic Pro B', 12))
hotlink_two_btn = tk.Button(orange_frame, text='Hot Link 2', font=('Kozuka Gothic Pro B', 12))
hotlink_three_btn = tk.Button(orange_frame, text='Hot Link 3', font=('Kozuka Gothic Pro B', 12))
edit_hotlinks_btn = tk.Button(orange_frame, text='Edit Hot Links', font=('Kozuka Gothic Pro B', 12), command=edit_hotlinks)

hotlink_one_btn.grid(row=0, column=0)
hotlink_two_btn.grid(row=0, column=1)
hotlink_three_btn.grid(row=0, column=2)
edit_hotlinks_btn.grid(row=0, column=3)

orange_frame.grid_rowconfigure(0, weight=1)
orange_frame.grid_columnconfigure(0, weight=1)
orange_frame.grid_columnconfigure(1, weight=1)
orange_frame.grid_columnconfigure(2, weight=1)
orange_frame.grid_columnconfigure(3, weight=1)

# run on startup

# bootup timers
update_utc()
bonus_ursus_tracker()
daily_reset()
weekly_reset()

# load save data to 'characters' dictionary
load_characters()

# load characters data into listbox
populate_entries()

root.mainloop()
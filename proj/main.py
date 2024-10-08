import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import timezone, timedelta
import datetime as dt
import webbrowser
from charinfo import CharInfo
from bosslist import BossList
from userinfo import UserInfo
from boss import Boss
import json
import os
from PIL import Image, ImageTk
import ctypes

# list of character (CharInfo) objects
characters = {}

# checker to ensure only one toplevel widget (popup) is open at a time
current_popup = None

# save file var
storage_filename = './savefiles/characters_save.json'
usr_filename = './savefiles/usr_save.json'

# load user
user = {}

font_choice = 'Kozuka Gothic Pro B'

# checks to see if a popup is currntly open
def is_popup_open():
    if current_popup is not None and current_popup.winfo_exists():
        return current_popup
    return None

# load the user data
def load_user():
    if os.path.exists(usr_filename):
        with open(usr_filename, 'r') as file:
            usr_data = json.load(file)
            for usr, usr_info in usr_data.items():
                user[usr] = UserInfo(usr_info['mesos_balance'], usr_info['weekly_mesos_gained'], usr_info['boss_crystal_reset'], usr_info['boss_crystal_count'], usr_info['boss_crystal_sold'],
                                      usr_info['hotlink_one'], usr_info['hotlink_two'], usr_info['hotlink_three'])

# execute message action/display on mouse hover over widget
def on_hover(mouse_event, status_bar, info_message):
    status_bar.config(text=info_message)

# execute message action/display on mouse hover completion over widget
def on_hover_leave(mouse_event, status_bar):
    status_bar.config(text='')

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
           'Chaos Pink Bean': custom_serializer(obj.cpb),
           'Hard Hilla': custom_serializer(obj.hh),
           'Cygnus': custom_serializer(obj.cyg),
           'Chaos Zakum': custom_serializer(obj.czak),
           'Princess No': custom_serializer(obj.pno),
           'Chaos Queen': custom_serializer(obj.cqueen),
           'Chaos Pierre': custom_serializer(obj.cpierre),
           'Chaos Von Bon': custom_serializer(obj.cvonbon),
           'Chaos Vellum': custom_serializer(obj.cvell),
           'Akechi Mitsuhide': custom_serializer(obj.akechi),
           'Hard Magnus': custom_serializer(obj.hmag),
           'Chaos Papulatus': custom_serializer(obj.cpap),
           'Lotus': custom_serializer(obj.lotus),
           'Damien': custom_serializer(obj.damien),
           'Guardian Slime': custom_serializer(obj.gslime),
           'Lucid': custom_serializer(obj.lucid),
           'Will': custom_serializer(obj.will),
           'Gloom': custom_serializer(obj.gloom),
           'Darknell': custom_serializer(obj.darknell),
           'Versus Hilla': custom_serializer(obj.vhilla),
           'Seren': custom_serializer(obj.seren),
           'Kaling': custom_serializer(obj.kaling),
           'Kalos': custom_serializer(obj.kalos)          
        }
    # Boss object
    elif isinstance(obj, Boss):
        return {
            'boss_name': obj.boss_name,
            'boss_clear': obj.boss_clear,
            'boss_difficulty': obj.boss_difficulty,
            'party_size': obj.party_size
        }
    # User object
    elif isinstance(obj, UserInfo):
        return {
            'mesos_balance': obj.mesos_balance,
            'weekly_mesos_gained': obj.weekly_mesos_gained,
            'boss_crystal_reset': obj.boss_crystal_reset,
            'boss_crystal_count': obj.boss_crystal_count,
            'boss_crystal_sold': obj.boss_crystal_sold,
            'hotlink_one': obj.hotlink_one,
            'hotlink_two': obj.hotlink_two,
            'hotlink_three': obj.hotlink_three
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
        time_remaining_str = f'{hours:02}:{minutes:02}:{seconds:02}'

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
    time_remaining_str = f'Daily Reset: {hours:02}:{minutes:02}:{seconds:02}'

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
        weekly_reset_lbl.config(text='Weekly Reset is Today')
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
        time_remaining_str = f'Weekly Reset: {days:02}:{hours:02}:{minutes:02}:{seconds:02}'

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
    boss_list = BossList(
        cpb = Boss('Chaos Pink Bean', False, 'Select Difficulty', 'Select Party Size'),
        hh = Boss('Hard Hilla', False, 'Select Difficulty', 'Select Party Size'),
        cyg = Boss('Cygnus', False, 'Select Difficulty', 'Select Party Size'),
        czak = Boss('Chaos Zakum', False, 'Select Difficulty', 'Select Party Size'),
        pno = Boss('Princess No', False, 'Select Difficulty', 'Select Party Size'),
        cqueen = Boss('Chaos Queen', False, 'Select Difficulty', 'Select Party Size'),
        cpierre = Boss('Chaos Pierre', False, 'Select Difficulty', 'Select Party Size'),
        cvonbon = Boss('Chaos Von Bon', False, 'Select Difficulty', 'Select Party Size'),
        cvell = Boss('Chaos Vellum', False, 'Select Difficulty', 'Select Party Size'),
        akechi = Boss('Akechi Mitsuhide', False, 'Select Difficulty', 'Select Party Size'),
        hmag = Boss('Hard Magnus', False, 'Select Difficulty', 'Select Party Size'),
        cpap = Boss('Chaos Papulatus', False, 'Select Difficulty', 'Select Party Size'),
        lotus = Boss('Lotus', False, 'Select Difficulty', 'Select Party Size'),
        damien = Boss('Damien', False, 'Select Difficulty', 'Select Party Size'),
        gslime = Boss('Guardian Slime', False, 'Select Difficulty', 'Select Party Size'),
        lucid = Boss('Lucid', False, 'Select Difficulty', 'Select Party Size'),
        will = Boss('Will', False, 'Select Difficulty', 'Select Party Size'),
        gloom = Boss('Gloom', False, 'Select Difficulty', 'Select Party Size'),
        darknell = Boss('Darknell', False, 'Select Difficulty', 'Select Party Size'),
        vhilla = Boss('Versus Hilla', False, 'Select Difficulty', 'Select Party Size'),
        seren = Boss('Seren', False, 'Select Difficulty', 'Select Party Size'),
        kaling = Boss('Kaling', False, 'Select Difficulty', 'Select Party Size'),
        kalos = Boss('Kalos', False, 'Select Difficulty', 'Select Party Size')
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

    # update the save file in real-time
    load_characters()

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

    global ac_win
    global current_popup
    ac_ign = tk.StringVar()
    ac_maple_job_choice = tk.StringVar()
    ac_level = tk.StringVar()

    # check to see if character already exists
    def validate_character_entry(check_ign):
        # if character already exists in 'characters' dictionary, give error message and close window
        if check_ign in characters.keys():
            messagebox.showerror('Invalid IGN (Player Name)',
                                 'The IGN (Character Name) has already been registered.')
            ac_win.lift()
        # if use has not filled all input fields
        elif ac_ign.get() == '' or ac_maple_job_choice.get() == '' or ac_level.get() == '':
            messagebox.showerror('Missing Information',
                                 'All input fields are not filled.')
            ac_win.lift()
        # ensure user doesn't attemp to leave field as default
        elif ac_maple_job_choice.get() == 'Select a Job/Class':
            messagebox.showerror('Invalid Choice',
                                 'You must choose a Job/Class.')
            ac_win.lift()
        # ensure user enters a valid number between 1 and 300
        elif not ac_level.get().isdigit() or int(ac_level.get()) > 300 or int(ac_level.get()) < 1:
            messagebox.showerror('Invalid Level',
                                 'You must enter a valid level.') 
            ac_win.lift()
        else:
            # otherwise, update 'characters' dictionary with new entry and close pop-up
            create_character(ac_ign.get(), ac_maple_job_choice.get(), ac_level.get())
            ac_win.destroy()

    # check to see if a popup is currently opened
    if is_popup_open():
        messagebox.showerror('Active Popup Detected.',
                             'There is already a Popup opened.')
        ac_win.lift()
    else:
        # ac short for add_character
        ac_win = tk.Toplevel(blue_frame, bg='#dbedf3')
        current_popup = ac_win
        ac_win.title('Add New Character')
        ac_win.geometry('400x250+850+300')
        ac_win.resizable(False, False)

        ac_title_lbl = tk.Label(ac_win, text='Add New Character', font=(font_choice, 12), bg='#dbedf3')
        ac_ign_lbl = tk.Label(ac_win, text='In-Game Name:', font=(font_choice, 12), bg='#dbedf3')
        ac_ign_entry = tk.Entry(ac_win, textvariable=ac_ign, font=(font_choice, 12), bg='#ffffff', highlightbackground='#161b28', highlightcolor='#6f85b6', highlightthickness=2)
        ac_job_lbl = tk.Label(ac_win, text='Job (Class):', font=(font_choice, 12), bg='#dbedf3')
        ac_job_dropdown = ttk.Combobox(ac_win, width=24, textvariable=ac_maple_job_choice)
        ac_job_dropdown['values'] = ( 
            'Select a Job/Class',
            'Night Lord',
            'Shadower',
            'Marksman',
            'Bowmaster',
            'Buccaneer',
            'Corsair',
            'Fire/Poison Archmage',
            'Ice/Lightning Archmage',
            'Bishop',
            'Dark Knight',
            'Paladin',
            'Hero',
            'Angelic Buster',
            'Lynn',
            'Khali',
            'Dawn Warrior',
            'Night Walker',
            'Blaze Wizard',
            'Thunder Breaker',
            'Wind Acher',
            'Mihile',
            'Dual Blade',
            'Cannoneer',
            'Lara',
            'Kain',
            'Adele',
            'Hoyoung',
            'Pathfinder',
            'Ark',
            'Illium',
            'Cadena',
            'Aran',
            'Evan',
            'Mercedes',
            'Phantom',
            'Luminous',
            'Shade',
            'Mechanic',
            'Wild Hunter',
            'Battle Mage',
            'Blaster',
            'Demon Slayer',
            'Demon Avenger',
            'Xenon',
            'Kaiser',
            'Kinesis',
            'Zero',
            'Hayato',
            'Kanna'
        )
        ac_job_dropdown.config(background='#ffffff', font=(font_choice, 10), state='readonly')
        ac_job_dropdown.current(0)
        ac_level_lbl = tk.Label(ac_win, text='Level:', font=(font_choice, 12), bg='#dbedf3')
        ac_level_entry = tk.Entry(ac_win, textvariable=ac_level, font=(font_choice, 12), bg='#ffffff', highlightbackground='#161b28', highlightcolor='#6f85b6', highlightthickness=2)
        ac_submit_btn = tk.Button(ac_win, text='Add to Roster', font=(font_choice, 10), width=15, bg='#b5dae6', activebackground='#dbedf3', command=lambda:validate_character_entry(ac_ign.get()))
        ac_cancel_btn = tk.Button(ac_win, text='Cancel', font=(font_choice, 10), width=15, command=ac_win.destroy, bg='#b5dae6', activebackground='#dbedf3')

        ac_title_lbl.grid(row=0, columnspan=2)
        ac_ign_lbl.grid(row=1, column=0, sticky='w', padx=(20, 0))
        ac_ign_entry.grid(row=1, column=1)
        ac_job_lbl.grid(row=2, column=0, sticky='w', padx=(20, 0))
        ac_job_dropdown.grid(row=2, column=1)
        ac_level_lbl.grid(row=3, column=0, sticky='w', padx=(20, 0))
        ac_level_entry.grid(row=3, column=1)
        ac_submit_btn.grid(row=4, column=0, pady=(0, 10))
        ac_cancel_btn.grid(row=4, column=1, pady=(0, 10))

        ac_win.rowconfigure(0, weight=1)
        ac_win.rowconfigure(1, weight=1)
        ac_win.rowconfigure(2, weight=1)
        ac_win.rowconfigure(3, weight=1)
        ac_win.rowconfigure(4, weight=1)
        ac_win.columnconfigure(0, weight=1)
        ac_win.columnconfigure(1, weight=1)

# update an existing character's details pop-up window
def update_character_popup():

    global uc_win
    global current_popup
    uc_ign = tk.StringVar()
    uc_maple_job_choice = tk.StringVar()
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
        return
        
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
            # error message prompt if that is the case
            messagebox.showerror('IGN Error',
                                 'The new IGN already exists for another character in the registered list.')
            uc_win.lift()
        # if use has not filled all input fields
        elif uc_ign.get() == '' or uc_maple_job_choice.get() == '' or uc_level.get() == '':
            messagebox.showerror('Missing Information',
                                 'All input fields are not filled.')
            uc_win.lift()
        # ensure user doesn't attemp to leave field as default
        elif uc_maple_job_choice.get() == 'Select a Job/Class':
            messagebox.showerror('Invalid Choice',
                                 'You must choose a Job/Class.')
            uc_win.lift()
        # ensure user enters a valid number between 1 and 300
        elif not uc_level.get().isdigit() or int(uc_level.get()) > 300 or int(uc_level.get()) < 1:
            messagebox.showerror('Invalid Level',
                                 'You must enter a valid level.') 
            uc_win.lift()
        else:
            # deletes the old character entry in characters dictionary
            del characters[selected_ign]
            
            # create a new character entry with updated details into the characters dictionary
            create_character(uc_ign.get(), uc_maple_job_choice.get(), uc_level.get())

            # closes the popup window
            uc_win.destroy()

    # set the input fields with existing character data
    uc_ign.set(characters[selected_ign].ign)
    uc_level.set(characters[selected_ign].level)

    # check to see if a popup is currently opened
    if is_popup_open():
        messagebox.showerror('Active Popup Detected.',
                             'There is already a Popup opened.')
        uc_win.lift()
    else:
        uc_win = tk.Toplevel(blue_frame, bg='#dbedf3')
        uc_win.title('Update Character')
        uc_win.geometry('400x250+850+300')
        uc_win.resizable(False, False)
        current_popup = uc_win

        uc_title_lbl = tk.Label(uc_win, text='Update Character', font=(font_choice, 12), bg='#dbedf3')
        uc_ign_lbl = tk.Label(uc_win, text='In-Game Name:', font=(font_choice, 12), bg='#dbedf3')
        uc_ign_entry = tk.Entry(uc_win, textvariable=uc_ign, font=(font_choice, 12), bg='#ffffff', highlightbackground='#161b28', highlightcolor='#6f85b6', highlightthickness=2)
        uc_job_lbl = tk.Label(uc_win, text='Job (Class):', font=(font_choice, 12), bg='#dbedf3')
        uc_job_dropdown = ttk.Combobox(uc_win, width=24, textvariable=uc_maple_job_choice)
        uc_job_dropdown['values'] = ( 
            'Night Lord',
            'Shadower',
            'Marksman',
            'Bowmaster',
            'Buccaneer',
            'Corsair',
            'Fire/Poison Archmage',
            'Ice/Lightning Archmage',
            'Bishop',
            'Dark Knight',
            'Paladin',
            'Hero',
            'Angelic Buster',
            'Lynn',
            'Khali',
            'Dawn Warrior',
            'Night Walker',
            'Blaze Wizard',
            'Thunder Breaker',
            'Wind Acher',
            'Mihile',
            'Dual Blade',
            'Cannoneer',
            'Lara',
            'Kain',
            'Adele',
            'Hoyoung',
            'Pathfinder',
            'Ark',
            'Illium',
            'Cadena',
            'Aran',
            'Evan',
            'Mercedes',
            'Phantom',
            'Luminous',
            'Shade',
            'Mechanic',
            'Wild Hunter',
            'Battle Mage',
            'Blaster',
            'Demon Slayer',
            'Demon Avenger',
            'Xenon',
            'Kaiser',
            'Kinesis',
            'Zero',
            'Hayato',
            'Kanna'
        )
        uc_job_dropdown.config(background='#ffffff', font=(font_choice, 10), state='readonly')
        uc_job_dropdown.set(characters[selected_ign].job)
        uc_level_lbl = tk.Label(uc_win, text='Level:', font=(font_choice, 12), bg='#dbedf3')
        uc_level_entry = tk.Entry(uc_win, textvariable=uc_level, font=(font_choice, 12), bg='#ffffff', highlightbackground='#161b28', highlightcolor='#6f85b6', highlightthickness=2)
        uc_submit_btn = tk.Button(uc_win, text='Update Roster', font=(font_choice, 12), width=15, command=validate_updated_entry, bg='#b5dae6', activebackground='#dbedf3')
        uc_cancel_btn = tk.Button(uc_win, text='Cancel', font=(font_choice, 12), width=15, command=uc_win.destroy, bg='#b5dae6', activebackground='#dbedf3')

        uc_title_lbl.grid(row=0, columnspan=2)
        uc_ign_lbl.grid(row=1, column=0, sticky='w', padx=(20, 0))
        uc_ign_entry.grid(row=1, column=1)
        uc_job_lbl.grid(row=2, column=0, sticky='w', padx=(20, 0))
        uc_job_dropdown.grid(row=2, column=1)
        uc_level_lbl.grid(row=3, column=0, sticky='w', padx=(20, 0))
        uc_level_entry.grid(row=3, column=1)
        uc_submit_btn.grid(row=4, column=0, pady=(0, 10))
        uc_cancel_btn.grid(row=4, column=1, pady=(0, 10))

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

# bossing checklist
def bossing_checklist_popup():

    global current_popup
    global bc_win

    font_preset = {'font':(font_choice, 12)}
    selected_ign = ''

    # store selected ign into var for reference 'selected_ign'
    for i in chars_lb.curselection():
        selected_ign = chars_lb.get(i)

    # validation check for valid selection
    if selected_ign == '':
        messagebox.showerror('Character Selection Error',
                             'A character has not been selected from the list.')
        # discontinue with popup
        return

    # check status icons image rendering
    # complete status
    complete_status_icon = Image.open('./img/complete_status.png')
    max_width, max_height = 50,50
    complete_status_icon.thumbnail((max_width, max_height))
    complete_status_icon = ImageTk.PhotoImage(complete_status_icon)

    # incomplete status
    incomplete_status_icon = Image.open('./img/incomplete_status.png')
    max_width, max_height = 50,50
    incomplete_status_icon.thumbnail((max_width, max_height))
    incomplete_status_icon = ImageTk.PhotoImage(incomplete_status_icon)

    # update bossing checklist
    def update_check_status(boss_name, clicked_status, check_id):

        # determines which value change is required based on checkbutton status
        if clicked_status.get():
            characters[selected_ign].boss_list[boss_name]['boss_clear'] = True
            check_id.config(image=complete_status_icon)
            # check_id.image = complete_status_icon
        else:
            characters[selected_ign].boss_list[boss_name]['boss_clear'] = False
            check_id.config(image=incomplete_status_icon)

        # updates the save file
        json_object = json.dumps(characters, indent=4, default=custom_serializer)

        with open(storage_filename, 'w') as outfile:
            outfile.write(json_object)

    # updates the difficulty for each boss based on user input
    def update_bossing_difficulty():

        # dictionary to hold each boss's difficulty value
        boss_difficulty_vars = {
            'Chaos Pink Bean': cpb_difficulty_choice,
            'Hard Hilla': hh_difficulty_choice,
            'Cygnus': cyg_difficulty_choice,
            'Chaos Zakum': czak_difficulty_choice,
            'Princess No': pno_difficulty_choice,
            'Chaos Queen': cqueen_difficulty_choice,
            'Chaos Pierre': cpierre_difficulty_choice,
            'Chaos Von Bon': cvonbon_difficulty_choice,
            'Chaos Vellum': cvell_difficulty_choice,
            'Akechi Mitsuhide': akechi_difficulty_choice,
            'Hard Magnus': hmag_difficulty_choice,
            'Chaos Papulatus': cpap_difficulty_choice,
            'Lotus': lotus_difficulty_choice,
            'Damien': damien_difficulty_choice,
            'Guardian Slime': gslime_difficulty_choice,
            'Lucid': lucid_difficulty_choice,
            'Will': will_difficulty_choice,
            'Gloom': gloom_difficulty_choice,
            'Darknell': darknell_difficulty_choice,
            'Versus Hilla': vhilla_difficulty_choice,
            'Seren': seren_difficulty_choice,
            'Kaling': kaling_difficulty_choice,
            'Kalos': kalos_difficulty_choice
        }

        # loops through and updates each boss's difficulty
        for boss, difficulty_var in boss_difficulty_vars.items():
            # retrieve boss difficulty value for each boss
            difficulty_str = difficulty_var.get()
            # check if the value is a valid digit 
            difficulty = int(difficulty_str) if difficulty_str.isdigit() else difficulty_str
            # update the boss's difficulty accordingly
            characters[selected_ign].boss_list[boss]['boss_difficulty'] = difficulty
        
        # updates the save file
        json_object = json.dumps(characters, indent=4, default=custom_serializer)

        with open(storage_filename, 'w') as outfile:
            outfile.write(json_object)

    # updates the party size for each boss based on user's 
    def update_party_size():

        # dictionary to hold each boss's value for party size
        boss_party_size_vars = {
            'Chaos Pink Bean': cpb_party_size_choice,
            'Hard Hilla': hh_party_size_choice,
            'Cygnus': cyg_party_size_choice,
            'Chaos Zakum': czak_party_size_choice,
            'Princess No': pno_party_size_choice,
            'Chaos Queen': cqueen_party_size_choice,
            'Chaos Pierre': cpierre_party_size_choice,
            'Chaos Von Bon': cvonbon_party_size_choice,
            'Chaos Vellum': cvell_party_size_choice,
            'Akechi Mitsuhide': akechi_party_size_choice,
            'Hard Magnus': hmag_party_size_choice,
            'Chaos Papulatus': cpap_party_size_choice,
            'Lotus': lotus_party_size_choice,
            'Damien': damien_party_size_choice,
            'Guardian Slime': gslime_party_size_choice,
            'Lucid': lucid_party_size_choice,
            'Will': will_party_size_choice,
            'Gloom': gloom_party_size_choice,
            'Darknell': darknell_party_size_choice,
            'Versus Hilla': vhilla_party_size_choice,
            'Seren': seren_party_size_choice,
            'Kaling': kaling_party_size_choice,
            'Kalos': kalos_party_size_choice
        }

        # loops through and updates each boss's party size
        for boss, party_var in boss_party_size_vars.items():
            # retrieve party size value for each boss
            size_str = party_var.get()
            # check if the value is a valid digit 
            size = int(size_str) if size_str.isdigit() else size_str
            # update the boss's party size accordingly
            characters[selected_ign].boss_list[boss]['party_size'] = size

        # updates the save file
        json_object = json.dumps(characters, indent=4, default=custom_serializer)

        with open(storage_filename, 'w') as outfile:
            outfile.write(json_object)

    # updates both boss_difficulty and party_size simultaneously
    def update_all():
        update_bossing_difficulty()
        update_party_size()
        update_weekly_mesos_earned()
        bc_win.destroy()

    # data set for all boss prices based on difficulties
    crystal_data = {
        'Chaos Pink Bean': {
            'Select Difficulty': 64000000
        },
        'Hard Hilla': {
            'Select Difficulty': 56250000
        },
        'Princess No': {
            'Select Difficulty': 81000000
        },
        'Chaos Zakum': {
            'Select Difficulty': 81000000
        },
        'Cygnus': {
            'Easy': 45562500,
            'Normal': 72250000
        },
        'Chaos Queen': {
            'Select Difficulty': 81000000
        },
        'Chaos Pierre': {
            'Select Difficulty': 81000000
        },
        'Chaos Von Bon': {
            'Select Difficulty': 81000000
        },
        'Chaos Vellum': {
            'Select Difficulty': 105062500
        },
        'Akechi Mitsuhide': {
            'Select Difficulty': 144000000
        },
        'Hard Magnus': {
            'Select Difficulty': 95062500
        },
        'Chaos Papulatus': {
            'Select Difficulty': 132250000
        },
        'Lotus': {
            'Normal': 162562500,
            'Hard/Chaos': 370562500,
            'Extreme': 1075000000
        },
        'Damien': {
            'Normal': 169000000,
            'Hard/Chaos': 351562500
        },
        'Guardian Slime': {
            'Normal': 171610000,
            'Hard/Chaos': 451562500
        },
        'Lucid': {
            'Easy': 175562500,
            'Normal': 203062500,
            'Hard/Chaos': 400000000
        },
        'Will': {
            'Easy': 191275000,
            'Normal': 232562500,
            'Hard/Chaos': 441000000
        },
        'Gloom': {
            'Normal': 248062500,
            'Hard/Chaos': 462250000
        },
        'Versus Hilla': {
            'Normal': 447600000,
            'Hard/Chaos': 552250000
        },
        'Darknell': {
            'Normal': 264062500,
            'Hard/Chaos': 484000000
        },
        'Seren': {
            'Normal': 668437500,
            'Hard/Chaos': 756250000,
            'Extreme': 3025000000
        },
        'Kaling': {
            'Easy':  825000000,
            'Normal': 1150000000,
            'Hard/Chaos': 2300000000,
            'Extreme': 4600000000
        },
        'Kalos': {
            'Easy': 750000000,
            'Normal': 1000000000,
            'Hard/Chaos': 2000000000,
            'Extreme': 4000000000
        }
    }

    # updates the weekly mesos earned/gained
    def update_weekly_mesos_earned():
        # variables
        total_earnings = 0
        total_crystals_sold = 0
        character = characters[selected_ign]

        # clean slate value that will gain latest value post function execution
        user['usr'].boss_crystal_sold = 0

        # safety net for glitches or if someone changes the save file default value
        user['usr'].boss_crystal_count = 180

        # loop through character, specifically boss_list object
        for boss_name, boss_details in character.boss_list.items():
            # establish variable references
            boss_difficulty = boss_details['boss_difficulty']
            boss_party_size = boss_details['party_size']
            boss_clear = boss_details['boss_clear']

            # add checks
            # if boss status isn't cleared
            if boss_clear == False:
                continue
            # if the boss party size hasnt been selected (i.e not a number)
            elif isinstance(boss_party_size, str):
                continue
            # otherwise.. 
            else:
                # check if the boss_name and difficulty_level are in the crystal_data dictionary
                if boss_name in crystal_data and boss_difficulty in crystal_data[boss_name]:
                    # formula: mesos earned based on boss, bosses difficulty and size of the party
                    mesos_earned = crystal_data[boss_name][boss_difficulty] / boss_party_size
                    total_earnings += mesos_earned

                    # count crystals sold based on each time mesos is earned
                    total_crystals_sold += 1
                # logge check for error in rendering code, temporary else statement, removed prior finalisation
                else:
                    print(f'Warning: Missing data for {boss_name} with difficulty {boss_difficulty}')

        # update the weekly_mesos_gained variable with latest data 
        user['usr'].weekly_mesos_gained = total_earnings

        # update the amount of boss crystals sold value
        user['usr'].boss_crystal_sold = total_crystals_sold

        # update the user save file
        json_object = json.dumps(user, indent=4, default=custom_serializer)

        with open(usr_filename, 'w') as outfile:
            outfile.write(json_object)

        # update the label text displays, based on latest save file data
        bc_remaining_lbl.config(text=f'Boss Cyrstals Remaining: {user['usr'].boss_crystal_count - user['usr'].boss_crystal_sold}')
        bc_sold_lbl.config(text=f'Boss Crystals Sold: {user['usr'].boss_crystal_sold}')
        wm_gained_lbl.config(text=f'Weekly Mesos Gained: ${user['usr'].weekly_mesos_gained:,.0f}')

    # reset all boss clears
    def reset_clears_only():
        character = characters[selected_ign]
        
        for boss_name in character.boss_list.keys():
            character.boss_list[boss_name]['boss_clear'] = False

        json_object = json.dumps(characters, indent=4, default=custom_serializer)

        with open(storage_filename, 'w') as outfile:
            outfile.write(json_object)

        load_clear_statuses()

    # resets all boss custom presets
    def reset_all():

        # dictionary to hold each boss's value for party size
        boss_party_size_vars = {
            'Chaos Pink Bean': cpb_party_size_choice,
            'Hard Hilla': hh_party_size_choice,
            'Cygnus': cyg_party_size_choice,
            'Chaos Zakum': czak_party_size_choice,
            'Princess No': pno_party_size_choice,
            'Chaos Queen': cqueen_party_size_choice,
            'Chaos Pierre': cpierre_party_size_choice,
            'Chaos Von Bon': cvonbon_party_size_choice,
            'Chaos Vellum': cvell_party_size_choice,
            'Akechi Mitsuhide': akechi_party_size_choice,
            'Hard Magnus': hmag_party_size_choice,
            'Chaos Papulatus': cpap_party_size_choice,
            'Lotus': lotus_party_size_choice,
            'Damien': damien_party_size_choice,
            'Guardian Slime': gslime_party_size_choice,
            'Lucid': lucid_party_size_choice,
            'Will': will_party_size_choice,
            'Gloom': gloom_party_size_choice,
            'Darknell': darknell_party_size_choice,
            'Versus Hilla': vhilla_party_size_choice,
            'Seren': seren_party_size_choice,
            'Kaling': kaling_party_size_choice,
            'Kalos': kalos_party_size_choice
        }

        # dictionary to hold each boss's difficulty value
        boss_difficulty_vars = {
            'Chaos Pink Bean': cpb_difficulty_choice,
            'Hard Hilla': hh_difficulty_choice,
            'Cygnus': cyg_difficulty_choice,
            'Chaos Zakum': czak_difficulty_choice,
            'Princess No': pno_difficulty_choice,
            'Chaos Queen': cqueen_difficulty_choice,
            'Chaos Pierre': cpierre_difficulty_choice,
            'Chaos Von Bon': cvonbon_difficulty_choice,
            'Chaos Vellum': cvell_difficulty_choice,
            'Akechi Mitsuhide': akechi_difficulty_choice,
            'Hard Magnus': hmag_difficulty_choice,
            'Chaos Papulatus': cpap_difficulty_choice,
            'Lotus': lotus_difficulty_choice,
            'Damien': damien_difficulty_choice,
            'Guardian Slime': gslime_difficulty_choice,
            'Lucid': lucid_difficulty_choice,
            'Will': will_difficulty_choice,
            'Gloom': gloom_difficulty_choice,
            'Darknell': darknell_difficulty_choice,
            'Versus Hilla': vhilla_difficulty_choice,
            'Seren': seren_difficulty_choice,
            'Kaling': kaling_difficulty_choice,
            'Kalos': kalos_difficulty_choice
        }

        character = characters[selected_ign]

        # loop through all the boss's variables and set them to default
        for boss_name in character.boss_list.keys():
            character.boss_list[boss_name]['boss_clear'] = False
            character.boss_list[boss_name]['boss_difficulty'] = 'Select Difficulty'
            character.boss_list[boss_name]['party_size'] = 'Select Party Size' 

        # loops through all the variables for party size and difficulty that are used in the widgets for reference
        # and sets them to default for display
        for party_var in boss_party_size_vars.values():
            party_var.set('Select Party Size')

        for difficulty_var in boss_difficulty_vars.values():
            difficulty_var.set('Select Difficulty')

        # updates the save file
        json_object = json.dumps(characters, indent=4, default=custom_serializer)

        with open(storage_filename, 'w') as outfile:
            outfile.write(json_object)

        load_clear_statuses()

    # load the boss_clear values to determine which status icon it should display upon opening the popup
    def load_clear_statuses():

        # dictionary listing boss names to their respective checkbutton widget
        boss_status_ids = {
            'Chaos Pink Bean': cpb_clear_status,
            'Hard Hilla': hh_clear_status,
            'Princess No': pno_clear_status,
            'Chaos Zakum': czak_clear_status,
            'Cygnus': cyg_clear_status,
            'Chaos Queen': cqueen_clear_status,
            'Chaos Pierre': cpierre_clear_status,
            'Chaos Von Bon': cvonbon_clear_status,
            'Chaos Vellum': cvell_clear_status,
            'Akechi Mitsuhide': akechi_clear_status,
            'Hard Magnus': hmag_clear_status,
            'Chaos Papulatus': cpap_clear_status,
            'Lotus': lotus_clear_status,
            'Damien': damien_clear_status,
            'Guardian Slime': gslime_clear_status,
            'Lucid': lucid_clear_status,
            'Will': will_clear_status,
            'Gloom': gloom_clear_status,
            'Versus Hilla': vhilla_clear_status,
            'Darknell': darknell_clear_status,
            'Seren': seren_clear_status,
            'Kaling': kaling_clear_status,
            'Kalos': kalos_clear_status
        }

        character = characters[selected_ign]

        for boss_name, boss_details in character.boss_list.items():
            boss_clear_status = boss_details['boss_clear']
            # determines which status icon to display
            if boss_clear_status == True:
                boss_status_ids[boss_name].config(image=complete_status_icon)
            else:
                boss_status_ids[boss_name].config(image=incomplete_status_icon)

    # check to see if a popup is currently opened
    if is_popup_open():
        messagebox.showerror('Active Popup Detected.',
                             'There is already a Popup opened.')
        bc_win.lift()
    else:
        bc_win = tk.Toplevel(blue_frame, bg='#dbedf3')
        bc_win.title("Bossing Checklist")
        bc_win.geometry('1400x1010+250+10')
        bc_win.resizable(False, False)
        current_popup = bc_win

        # difficulty variations
        # for: Cygnus
        difficulty_a = [
            'Easy',
            'Normal'
        ]
        
        # for: Damien, Guardian Slime, Gloom, Verus Hilla, Darknell
        difficulty_b = [
            'Normal',
            'Hard/Chaos'
        ]

        # for: Lucid, Will
        difficulty_c = [
            'Easy',
            'Normal',
            'Hard/Chaos'
        ]

        # for: Seren, Lotus
        difficulty_d = [
            'Normal',
            'Hard/Chaos',
            'Extreme'
        ]

        # for: Kaling, Kalos
        difficulty_e = [
            'Easy',
            'Normal',
            'Hard/Chaos',
            'Extreme'
        ]

        party_size = [
            'Select Party Size',
            1,
            2,
            3,
            4,
            5,
            6
        ]

        # region - boss variables
        # Chaos Pink Bean Vars
        cpb_difficulty_choice = tk.StringVar()
        cpb_party_size_choice = tk.StringVar()
        cpb_status = tk.IntVar()

        cpb_difficulty_choice.set(characters[selected_ign].boss_list['Chaos Pink Bean']['boss_difficulty'])
        cpb_party_size_choice.set(characters[selected_ign].boss_list['Chaos Pink Bean']['party_size'])
        cpb_status.set(characters[selected_ign].boss_list['Chaos Pink Bean']['boss_clear'])

        # Hard Hilla Vars
        hh_difficulty_choice = tk.StringVar()
        hh_party_size_choice = tk.StringVar()
        hh_status = tk.IntVar()

        hh_difficulty_choice.set(characters[selected_ign].boss_list['Hard Hilla']['boss_difficulty'])
        hh_party_size_choice.set(characters[selected_ign].boss_list['Hard Hilla']['party_size'])
        hh_status.set(characters[selected_ign].boss_list['Hard Hilla']['boss_clear'])

        # Cygnus Vars
        cyg_difficulty_choice = tk.StringVar()
        cyg_party_size_choice = tk.StringVar()
        cyg_status = tk.IntVar()

        cyg_difficulty_choice.set(characters[selected_ign].boss_list['Cygnus']['boss_difficulty'])
        cyg_party_size_choice.set(characters[selected_ign].boss_list['Cygnus']['party_size'])
        cyg_status.set(characters[selected_ign].boss_list['Cygnus']['boss_clear'])

        # Chaos Zakum Vars
        czak_difficulty_choice = tk.StringVar()
        czak_party_size_choice = tk.StringVar()
        czak_status = tk.IntVar()

        czak_difficulty_choice.set(characters[selected_ign].boss_list['Chaos Zakum']['boss_difficulty'])
        czak_party_size_choice.set(characters[selected_ign].boss_list['Chaos Zakum']['party_size'])
        czak_status.set(characters[selected_ign].boss_list['Chaos Zakum']['boss_clear'])

        # Princess No Vars
        pno_difficulty_choice = tk.StringVar()
        pno_party_size_choice = tk.StringVar()
        pno_status = tk.IntVar()

        pno_difficulty_choice.set(characters[selected_ign].boss_list['Princess No']['boss_difficulty'])
        pno_party_size_choice.set(characters[selected_ign].boss_list['Princess No']['party_size'])
        pno_status.set(characters[selected_ign].boss_list['Princess No']['boss_clear'])

        # Chaos Queen Vars
        cqueen_difficulty_choice = tk.StringVar()
        cqueen_party_size_choice = tk.StringVar()
        cqueen_status = tk.IntVar()

        cqueen_difficulty_choice.set(characters[selected_ign].boss_list['Chaos Queen']['boss_difficulty'])
        cqueen_party_size_choice.set(characters[selected_ign].boss_list['Chaos Queen']['party_size'])
        cqueen_status.set(characters[selected_ign].boss_list['Chaos Queen']['boss_clear'])

        # Chaos Pierre Vars
        cpierre_difficulty_choice = tk.StringVar()
        cpierre_party_size_choice = tk.StringVar()
        cpierre_status = tk.IntVar()

        cpierre_difficulty_choice.set(characters[selected_ign].boss_list['Chaos Pierre']['boss_difficulty'])
        cpierre_party_size_choice.set(characters[selected_ign].boss_list['Chaos Pierre']['party_size'])
        cpierre_status.set(characters[selected_ign].boss_list['Chaos Pierre']['boss_clear'])

        # Chaos Von Bon Vars
        cvonbon_difficulty_choice = tk.StringVar()
        cvonbon_party_size_choice = tk.StringVar()
        cvonbon_status = tk.IntVar()

        cvonbon_difficulty_choice.set(characters[selected_ign].boss_list['Chaos Von Bon']['boss_difficulty'])
        cvonbon_party_size_choice.set(characters[selected_ign].boss_list['Chaos Von Bon']['party_size'])
        cvonbon_status.set(characters[selected_ign].boss_list['Chaos Von Bon']['boss_clear'])

        # Chaos Vellum Vars
        cvell_difficulty_choice = tk.StringVar()
        cvell_party_size_choice = tk.StringVar()
        cvell_status = tk.IntVar()

        cvell_difficulty_choice.set(characters[selected_ign].boss_list['Chaos Vellum']['boss_difficulty'])
        cvell_party_size_choice.set(characters[selected_ign].boss_list['Chaos Vellum']['party_size'])
        cvell_status.set(characters[selected_ign].boss_list['Chaos Vellum']['boss_clear'])

        # Akechi Mitsuhide Vars
        akechi_difficulty_choice = tk.StringVar()
        akechi_party_size_choice = tk.StringVar()
        akechi_status = tk.IntVar()

        akechi_difficulty_choice.set(characters[selected_ign].boss_list['Akechi Mitsuhide']['boss_difficulty'])
        akechi_party_size_choice.set(characters[selected_ign].boss_list['Akechi Mitsuhide']['party_size'])
        akechi_status.set(characters[selected_ign].boss_list['Akechi Mitsuhide']['boss_clear'])

        # Hard Magnus Vars
        hmag_difficulty_choice = tk.StringVar()
        hmag_party_size_choice = tk.StringVar()
        hmag_status = tk.IntVar()

        hmag_difficulty_choice.set(characters[selected_ign].boss_list['Hard Magnus']['boss_difficulty'])
        hmag_party_size_choice.set(characters[selected_ign].boss_list['Hard Magnus']['party_size'])
        hmag_status.set(characters[selected_ign].boss_list['Hard Magnus']['boss_clear'])

        # Chaos Papulatus Vars
        cpap_difficulty_choice = tk.StringVar()
        cpap_party_size_choice = tk.StringVar()
        cpap_status = tk.IntVar()

        cpap_difficulty_choice.set(characters[selected_ign].boss_list['Chaos Papulatus']['boss_difficulty'])
        cpap_party_size_choice.set(characters[selected_ign].boss_list['Chaos Papulatus']['party_size'])
        cpap_status.set(characters[selected_ign].boss_list['Chaos Papulatus']['boss_clear'])

        # Lotus Vars
        lotus_difficulty_choice = tk.StringVar()
        lotus_party_size_choice = tk.StringVar()
        lotus_status = tk.IntVar()

        lotus_difficulty_choice.set(characters[selected_ign].boss_list['Lotus']['boss_difficulty'])
        lotus_party_size_choice.set(characters[selected_ign].boss_list['Lotus']['party_size'])
        lotus_status.set(characters[selected_ign].boss_list['Lotus']['boss_clear'])

        # Damien Vars
        damien_difficulty_choice = tk.StringVar()
        damien_party_size_choice = tk.StringVar()
        damien_status = tk.IntVar()

        damien_difficulty_choice.set(characters[selected_ign].boss_list['Damien']['boss_difficulty'])
        damien_party_size_choice.set(characters[selected_ign].boss_list['Damien']['party_size'])
        damien_status.set(characters[selected_ign].boss_list['Damien']['boss_clear'])

        # Guardian Slime Vars
        gslime_difficulty_choice = tk.StringVar()
        gslime_party_size_choice = tk.StringVar()
        gslime_status = tk.IntVar()

        gslime_difficulty_choice.set(characters[selected_ign].boss_list['Guardian Slime']['boss_difficulty'])
        gslime_party_size_choice.set(characters[selected_ign].boss_list['Guardian Slime']['party_size'])
        gslime_status.set(characters[selected_ign].boss_list['Guardian Slime']['boss_clear'])

        # Lucid Vars
        lucid_difficulty_choice = tk.StringVar()
        lucid_party_size_choice = tk.StringVar()
        lucid_status = tk.IntVar()

        lucid_difficulty_choice.set(characters[selected_ign].boss_list['Lucid']['boss_difficulty'])
        lucid_party_size_choice.set(characters[selected_ign].boss_list['Lucid']['party_size'])
        lucid_status.set(characters[selected_ign].boss_list['Lucid']['boss_clear'])

        # Will Vars
        will_difficulty_choice = tk.StringVar()
        will_party_size_choice = tk.StringVar()
        will_status = tk.IntVar()

        will_difficulty_choice.set(characters[selected_ign].boss_list['Will']['boss_difficulty'])
        will_party_size_choice.set(characters[selected_ign].boss_list['Will']['party_size'])
        will_status.set(characters[selected_ign].boss_list['Will']['boss_clear'])

        # Gloom Vars
        gloom_difficulty_choice = tk.StringVar()
        gloom_party_size_choice = tk.StringVar()
        gloom_status = tk.IntVar()

        gloom_difficulty_choice.set(characters[selected_ign].boss_list['Gloom']['boss_difficulty'])
        gloom_party_size_choice.set(characters[selected_ign].boss_list['Gloom']['party_size'])
        gloom_status.set(characters[selected_ign].boss_list['Gloom']['boss_clear'])

        # Darknell Vars
        darknell_difficulty_choice = tk.StringVar()
        darknell_party_size_choice = tk.StringVar()
        darknell_status = tk.IntVar()

        darknell_difficulty_choice.set(characters[selected_ign].boss_list['Darknell']['boss_difficulty'])
        darknell_party_size_choice.set(characters[selected_ign].boss_list['Darknell']['party_size'])
        darknell_status.set(characters[selected_ign].boss_list['Darknell']['boss_clear'])

        # Versus Hilla Vars
        vhilla_difficulty_choice = tk.StringVar()
        vhilla_party_size_choice = tk.StringVar()
        vhilla_status = tk.IntVar()

        vhilla_difficulty_choice.set(characters[selected_ign].boss_list['Versus Hilla']['boss_difficulty'])
        vhilla_party_size_choice.set(characters[selected_ign].boss_list['Versus Hilla']['party_size'])
        vhilla_status.set(characters[selected_ign].boss_list['Versus Hilla']['boss_clear'])

        # Seren Vars
        seren_difficulty_choice = tk.StringVar()
        seren_party_size_choice = tk.StringVar()
        seren_status = tk.IntVar()

        seren_difficulty_choice.set(characters[selected_ign].boss_list['Seren']['boss_difficulty'])
        seren_party_size_choice.set(characters[selected_ign].boss_list['Seren']['party_size'])
        seren_status.set(characters[selected_ign].boss_list['Seren']['boss_clear'])

        # Kaling Vars
        kaling_difficulty_choice = tk.StringVar()
        kaling_party_size_choice = tk.StringVar()
        kaling_status = tk.IntVar()

        kaling_difficulty_choice.set(characters[selected_ign].boss_list['Kaling']['boss_difficulty'])
        kaling_party_size_choice.set(characters[selected_ign].boss_list['Kaling']['party_size'])
        kaling_status.set(characters[selected_ign].boss_list['Kaling']['boss_clear'])

        # Kalos Vars
        kalos_difficulty_choice = tk.StringVar()
        kalos_party_size_choice = tk.StringVar()
        kalos_status = tk.IntVar()

        kalos_difficulty_choice.set(characters[selected_ign].boss_list['Kalos']['boss_difficulty'])
        kalos_party_size_choice.set(characters[selected_ign].boss_list['Kalos']['party_size'])
        kalos_status.set(characters[selected_ign].boss_list['Kalos']['boss_clear'])
        # endregion

        # title and character detail
        bossing_checklist_title = tk.Label(bc_win, text='Bossing Checklist', **font_preset, bg='#dbedf3')
        character_details_lbl = tk.Label(bc_win, text=f'{characters[selected_ign].ign} | {characters[selected_ign].job} | Lv.{characters[selected_ign].level}', **font_preset, bg='#dbedf3')

        # region - open images
        # Render Images
        max_width, max_height = 100, 100

        # opening images
        cpb_icon = Image.open('./img/Chaos_Pink_Bean.webp')
        cpb_icon.thumbnail((max_width, max_height))
        cpb_icon = ImageTk.PhotoImage(cpb_icon)

        hh_icon = Image.open('./img/Hard_Hilla.webp')
        hh_icon.thumbnail((max_width, max_height))
        hh_icon = ImageTk.PhotoImage(hh_icon)

        cyg_icon = Image.open('./img/Cygnus.webp')
        cyg_icon.thumbnail((max_width, max_height))
        cyg_icon = ImageTk.PhotoImage(cyg_icon)

        czak_icon = Image.open('./img/Chaos_Zakum.webp')
        czak_icon.thumbnail((max_width, max_height))
        czak_icon = ImageTk.PhotoImage(czak_icon)

        pno_icon = Image.open('./img/Princess_No.webp')
        pno_icon.thumbnail((max_width, max_height))
        pno_icon = ImageTk.PhotoImage(pno_icon)

        cqueen_icon = Image.open('./img/Chaos_Crimson_Queen.webp')
        cqueen_icon.thumbnail((max_width, max_height))
        cqueen_icon = ImageTk.PhotoImage(cqueen_icon)

        cpierre_icon = Image.open('./img/Chaos_Pierre.webp')
        cpierre_icon.thumbnail((max_width, max_height))
        cpierre_icon = ImageTk.PhotoImage(cpierre_icon)

        cvonbon_icon = Image.open('./img/Chaos_Von_Bon.webp')
        cvonbon_icon.thumbnail((max_width, max_height))
        cvonbon_icon = ImageTk.PhotoImage(cvonbon_icon)

        cvell_icon = Image.open('./img/Chaos_Vellum.webp')
        cvell_icon.thumbnail((max_width, max_height))
        cvell_icon = ImageTk.PhotoImage(cvell_icon)

        akechi_icon = Image.open('./img/Akechi_Mitsuhide.webp')
        akechi_icon.thumbnail((max_width, max_height))
        akechi_icon = ImageTk.PhotoImage(akechi_icon)

        hmag_icon = Image.open('./img/Hard_Magnus.webp')
        hmag_icon.thumbnail((max_width, max_height))
        hmag_icon = ImageTk.PhotoImage(hmag_icon)

        cpap_icon = Image.open('./img/Chaos_Papulatus.webp')
        cpap_icon.thumbnail((max_width, max_height))
        cpap_icon = ImageTk.PhotoImage(cpap_icon)

        lotus_icon = Image.open('./img/Lotus.webp')
        lotus_icon.thumbnail((max_width, max_height))
        lotus_icon = ImageTk.PhotoImage(lotus_icon)

        damien_icon = Image.open('./img/Damien.webp')
        damien_icon.thumbnail((max_width, max_height))
        damien_icon = ImageTk.PhotoImage(damien_icon)

        gslime_icon = Image.open('./img/Guardian_Slime.webp')
        gslime_icon.thumbnail((max_width, max_height))
        gslime_icon = ImageTk.PhotoImage(gslime_icon)

        lucid_icon = Image.open('./img/Lucid.webp')
        lucid_icon.thumbnail((max_width, max_height))
        lucid_icon = ImageTk.PhotoImage(lucid_icon)

        will_icon = Image.open('./img/Will.webp')
        will_icon.thumbnail((max_width, max_height))
        will_icon = ImageTk.PhotoImage(will_icon)

        gloom_icon = Image.open('./img/Gloom.webp')
        gloom_icon.thumbnail((max_width, max_height))
        gloom_icon = ImageTk.PhotoImage(gloom_icon)

        darknell_icon = Image.open('./img/Darknell.webp')
        darknell_icon.thumbnail((max_width, max_height))
        darknell_icon = ImageTk.PhotoImage(darknell_icon)

        vhilla_icon = Image.open('./img/Verus_Hilla.webp')
        vhilla_icon.thumbnail((max_width, max_height))
        vhilla_icon = ImageTk.PhotoImage(vhilla_icon)

        seren_icon = Image.open('./img/Seren.webp')
        seren_icon.thumbnail((max_width, max_height))
        seren_icon = ImageTk.PhotoImage(seren_icon)

        kaling_icon = Image.open('./img/Kaling.webp')
        kaling_icon.thumbnail((max_width, max_height))
        kaling_icon = ImageTk.PhotoImage(kaling_icon)

        kalos_icon = Image.open('./img/Kalos.webp')
        kalos_icon.thumbnail((max_width, max_height))
        kalos_icon = ImageTk.PhotoImage(kalos_icon)
        # endregion

        # region - boss widgets
        # Chaos Pink Bean
        cpb_name = tk.Label(bc_win, text='Chaos Pink Bean', **font_preset, bg='#dbedf3')
        cpb_img = tk.Label(bc_win, image=cpb_icon, bg='#dbedf3')
        cpb_difficulty = tk.OptionMenu(bc_win, cpb_difficulty_choice, *difficulty_a)
        cpb_difficulty.config(state='disabled', font=(font_choice, 8))
        cpb_party_size = tk.OptionMenu(bc_win, cpb_party_size_choice, *party_size)
        cpb_party_size.config(font=(font_choice, 8))
        cpb_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=cpb_status, command=lambda:update_check_status('Chaos Pink Bean', cpb_status, cpb_clear_status), bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')

        # Hard Hilla
        hh_name = tk.Label(bc_win, text='Hard Hilla', **font_preset, bg='#dbedf3')
        hh_img = tk.Label(bc_win, image=hh_icon, bg='#dbedf3')
        hh_difficulty = tk.OptionMenu(bc_win, hh_difficulty_choice, *difficulty_a) 
        hh_difficulty.config(state='disabled', font=(font_choice, 8))
        hh_party_size = tk.OptionMenu(bc_win, hh_party_size_choice, *party_size)
        hh_party_size.config(font=(font_choice, 8))
        hh_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=hh_status, command=lambda:update_check_status('Hard Hilla', hh_status, hh_clear_status), 
                                        bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        hh_clear_status.config(indicatoron=False, borderwidth=0)

        # Cygnus
        cyg_name = tk.Label(bc_win, text='Cygnus', **font_preset, bg='#dbedf3')
        cyg_img = tk.Label(bc_win, image=cyg_icon, bg='#dbedf3')
        cyg_difficulty = tk.OptionMenu(bc_win, cyg_difficulty_choice, *difficulty_a)
        cyg_difficulty.config(font=(font_choice, 8))
        cyg_party_size = tk.OptionMenu(bc_win, cyg_party_size_choice, *party_size)
        cyg_party_size.config(font=(font_choice, 8))
        cyg_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=cyg_status, command=lambda:update_check_status('Cygnus', cyg_status, cyg_clear_status), 
                                        bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        cyg_clear_status.config(indicatoron=False, borderwidth=0)

        # Chaos Zakum
        czak_name = tk.Label(bc_win, text='Chaos Zakum', **font_preset, bg='#dbedf3')
        czak_img = tk.Label(bc_win, image=czak_icon, bg='#dbedf3')
        czak_difficulty = tk.OptionMenu(bc_win, czak_difficulty_choice, *difficulty_a) 
        czak_difficulty.config(state='disabled', font=(font_choice, 8))
        czak_party_size = tk.OptionMenu(bc_win, czak_party_size_choice, *party_size)
        czak_party_size.config(font=(font_choice, 8))
        czak_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=czak_status, command=lambda:update_check_status('Chaos Zakum', czak_status, czak_clear_status), 
                                        bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        czak_clear_status.config(indicatoron=False, borderwidth=0)

        # Princess No
        pno_name = tk.Label(bc_win, text='Princess No', **font_preset, bg='#dbedf3')
        pno_img = tk.Label(bc_win, image=pno_icon, bg='#dbedf3')
        pno_difficulty = tk.OptionMenu(bc_win, pno_difficulty_choice, *difficulty_a) 
        pno_difficulty.config(state='disabled', font=(font_choice, 8))
        pno_party_size = tk.OptionMenu(bc_win, pno_party_size_choice, *party_size)
        pno_party_size.config(font=(font_choice, 8))
        pno_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=pno_status, command=lambda:update_check_status('Princess No', pno_status, pno_clear_status), 
                                        bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        pno_clear_status.config(indicatoron=False, borderwidth=0)

        # Chaos Queen
        cqueen_name = tk.Label(bc_win, text='Chaos Queen', **font_preset, bg='#dbedf3')
        cqueen_img = tk.Label(bc_win, image=cqueen_icon, bg='#dbedf3')
        cqueen_difficulty = tk.OptionMenu(bc_win, cqueen_difficulty_choice, *difficulty_a) 
        cqueen_difficulty.config(state='disabled', font=(font_choice, 8))
        cqueen_party_size = tk.OptionMenu(bc_win, cqueen_party_size_choice, *party_size)
        cqueen_party_size.config(font=(font_choice, 8))
        cqueen_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=cqueen_status, command=lambda:update_check_status('Chaos Queen', cqueen_status, cqueen_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        cqueen_clear_status.config(indicatoron=False, borderwidth=0)

        # Chaos Pierre
        cpierre_name = tk.Label(bc_win, text='Chaos Pierre', **font_preset, bg='#dbedf3')
        cpierre_img = tk.Label(bc_win, image=cpierre_icon, bg='#dbedf3')
        cpierre_difficulty = tk.OptionMenu(bc_win, cpierre_difficulty_choice, *difficulty_a) 
        cpierre_difficulty.config(state='disabled', font=(font_choice, 8))
        cpierre_party_size = tk.OptionMenu(bc_win, cpierre_party_size_choice, *party_size)
        cpierre_party_size.config(font=(font_choice, 8))
        cpierre_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=cpierre_status, command=lambda:update_check_status('Chaos Pierre', cpierre_status, cpierre_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        cpierre_clear_status.config(indicatoron=False, borderwidth=0)

        # Chaos Von Bon
        cvonbon_name = tk.Label(bc_win, text='Chaos Von Bon', **font_preset, bg='#dbedf3')
        cvonbon_img = tk.Label(bc_win, image=cvonbon_icon, bg='#dbedf3')
        cvonbon_difficulty = tk.OptionMenu(bc_win, cvonbon_difficulty_choice, *difficulty_a) 
        cvonbon_difficulty.config(state='disabled', font=(font_choice, 8))
        cvonbon_party_size = tk.OptionMenu(bc_win, cvonbon_party_size_choice, *party_size)
        cvonbon_party_size.config(font=(font_choice, 8))
        cvonbon_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=cvonbon_status, command=lambda:update_check_status('Chaos Von Bon', cvonbon_status, cvonbon_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        cvonbon_clear_status.config(indicatoron=False, borderwidth=0)

        # Chaos Vellum
        cvell_name = tk.Label(bc_win, text='Chaos Vellum', **font_preset, bg='#dbedf3')
        cvell_img = tk.Label(bc_win, image=cvell_icon, bg='#dbedf3')
        cvell_difficulty = tk.OptionMenu(bc_win, cvell_difficulty_choice, *difficulty_a) 
        cvell_difficulty.config(state='disabled', font=(font_choice, 8))
        cvell_party_size = tk.OptionMenu(bc_win, cvell_party_size_choice, *party_size)
        cvell_party_size.config(font=(font_choice, 8))
        cvell_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=cvell_status, command=lambda:update_check_status('Chaos Vellum', cvell_status, cvell_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        cvell_clear_status.config(indicatoron=False, borderwidth=0)

        # Akechi Mitsuhide
        akechi_name = tk.Label(bc_win, text='Akechi Mitsuhide', **font_preset, bg='#dbedf3')
        akechi_img = tk.Label(bc_win, image=akechi_icon, bg='#dbedf3')
        akechi_difficulty = tk.OptionMenu(bc_win, akechi_difficulty_choice, *difficulty_a) 
        akechi_difficulty.config(state='disabled', font=(font_choice, 8))
        akechi_party_size = tk.OptionMenu(bc_win, akechi_party_size_choice, *party_size)
        akechi_party_size.config(font=(font_choice, 8))
        akechi_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=akechi_status, command=lambda:update_check_status('Akechi Mitsuhide', akechi_status, akechi_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        akechi_clear_status.config(indicatoron=False, borderwidth=0)

        # Hard Magnus
        hmag_name = tk.Label(bc_win, text='Hard Magnus', **font_preset, bg='#dbedf3')
        hmag_img = tk.Label(bc_win, image=hmag_icon, bg='#dbedf3')
        hmag_difficulty = tk.OptionMenu(bc_win, hmag_difficulty_choice, *difficulty_a) 
        hmag_difficulty.config(state='disabled', font=(font_choice, 8))
        hmag_party_size = tk.OptionMenu(bc_win, hmag_party_size_choice, *party_size)
        hmag_party_size.config(font=(font_choice, 8))
        hmag_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=hmag_status, command=lambda:update_check_status('Hard Magnus', hmag_status, hmag_clear_status), 
                                        bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        hmag_clear_status.config(indicatoron=False, borderwidth=0)

        # Chaos Papulatus
        cpap_name = tk.Label(bc_win, text='Chaos Papulatus', **font_preset, bg='#dbedf3')
        cpap_img = tk.Label(bc_win, image=cpap_icon, bg='#dbedf3')
        cpap_difficulty = tk.OptionMenu(bc_win, cpap_difficulty_choice, *difficulty_a) 
        cpap_difficulty.config(state='disabled', font=(font_choice, 8))
        cpap_party_size = tk.OptionMenu(bc_win, cpap_party_size_choice, *party_size)
        cpap_party_size.config(font=(font_choice, 8))
        cpap_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=cpap_status, command=lambda:update_check_status('Chaos Papulatus', cpap_status, cpap_clear_status), 
                                        bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        cpap_clear_status.config(indicatoron=False, borderwidth=0)

        # Lotus
        lotus_name = tk.Label(bc_win, text='Lotus', **font_preset, bg='#dbedf3')
        lotus_img = tk.Label(bc_win, image=lotus_icon, bg='#dbedf3')
        lotus_difficulty = tk.OptionMenu(bc_win, lotus_difficulty_choice, *difficulty_d)
        lotus_difficulty.config(font=(font_choice, 8))
        lotus_party_size = tk.OptionMenu(bc_win, lotus_party_size_choice, *party_size)
        lotus_party_size.config(font=(font_choice, 8))
        lotus_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=lotus_status, command=lambda:update_check_status('Lotus', lotus_status, lotus_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        lotus_clear_status.config(indicatoron=False, borderwidth=0)

        # Damien
        damien_name = tk.Label(bc_win, text='Damien', **font_preset, bg='#dbedf3')
        damien_img = tk.Label(bc_win, image=damien_icon, bg='#dbedf3')
        damien_difficulty = tk.OptionMenu(bc_win, damien_difficulty_choice, *difficulty_b)
        damien_difficulty.config(font=(font_choice, 8))
        damien_party_size = tk.OptionMenu(bc_win, damien_party_size_choice, *party_size)
        damien_party_size.config(font=(font_choice, 8))
        damien_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=damien_status, command=lambda:update_check_status('Damien', damien_status, damien_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        damien_clear_status.config(indicatoron=False, borderwidth=0)

        # Guardian Slime
        gslime_name = tk.Label(bc_win, text='Guardian Slime', **font_preset, bg='#dbedf3')
        gslime_img = tk.Label(bc_win, image=gslime_icon, bg='#dbedf3')
        gslime_difficulty = tk.OptionMenu(bc_win, gslime_difficulty_choice, *difficulty_b)
        gslime_difficulty.config(font=(font_choice, 8))
        gslime_party_size = tk.OptionMenu(bc_win, gslime_party_size_choice, *party_size)
        gslime_party_size.config(font=(font_choice, 8))
        gslime_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=gslime_status, command=lambda:update_check_status('Guardian Slime', gslime_status, gslime_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        gslime_clear_status.config(indicatoron=False, borderwidth=0)

        # Lucid
        lucid_name = tk.Label(bc_win, text='Lucid', **font_preset, bg='#dbedf3')
        lucid_img = tk.Label(bc_win, image=lucid_icon, bg='#dbedf3')
        lucid_difficulty = tk.OptionMenu(bc_win, lucid_difficulty_choice, *difficulty_c)
        lucid_difficulty.config(font=(font_choice, 8))
        lucid_party_size = tk.OptionMenu(bc_win, lucid_party_size_choice, *party_size)
        lucid_party_size.config(font=(font_choice, 8))
        lucid_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=lucid_status, command=lambda:update_check_status('Lucid', lucid_status, lucid_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        lucid_clear_status.config(indicatoron=False, borderwidth=0)

        # Will
        will_name = tk.Label(bc_win, text='Will', **font_preset, bg='#dbedf3')
        will_img = tk.Label(bc_win, image=will_icon, bg='#dbedf3')
        will_difficulty = tk.OptionMenu(bc_win, will_difficulty_choice, *difficulty_c)
        will_difficulty.config(font=(font_choice, 8))
        will_party_size = tk.OptionMenu(bc_win, will_party_size_choice, *party_size)
        will_party_size.config(font=(font_choice, 8))
        will_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=will_status, command=lambda:update_check_status('Will', will_status, will_clear_status), 
                                        bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        will_clear_status.config(indicatoron=False, borderwidth=0)

        # Gloom
        gloom_name = tk.Label(bc_win, text='Gloom', **font_preset, bg='#dbedf3')
        gloom_img = tk.Label(bc_win, image=gloom_icon, bg='#dbedf3')
        gloom_difficulty = tk.OptionMenu(bc_win, gloom_difficulty_choice, *difficulty_b)
        gloom_difficulty.config(font=(font_choice, 8))
        gloom_party_size = tk.OptionMenu(bc_win, gloom_party_size_choice, *party_size)
        gloom_party_size.config(font=(font_choice, 8))
        gloom_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=gloom_status, command=lambda:update_check_status('Gloom', gloom_status, gloom_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        gloom_clear_status.config(indicatoron=False, borderwidth=0)

        # Darknell
        darknell_name = tk.Label(bc_win, text='Darknell', **font_preset, bg='#dbedf3')
        darknell_img = tk.Label(bc_win, image=darknell_icon, bg='#dbedf3')
        darknell_difficulty = tk.OptionMenu(bc_win, darknell_difficulty_choice, *difficulty_b)
        darknell_difficulty.config(font=(font_choice, 8))
        darknell_party_size = tk.OptionMenu(bc_win, darknell_party_size_choice, *party_size)
        darknell_party_size.config(font=(font_choice, 8))
        darknell_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=darknell_status, command=lambda:update_check_status('Darknell', darknell_status, darknell_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        darknell_clear_status.config(indicatoron=False, borderwidth=0)

        # Versus Hilla
        vhilla_name = tk.Label(bc_win, text='Versus Hilla', **font_preset, bg='#dbedf3')
        vhilla_img = tk.Label(bc_win, image=vhilla_icon, bg='#dbedf3')
        vhilla_difficulty = tk.OptionMenu(bc_win, vhilla_difficulty_choice, *difficulty_b)
        vhilla_difficulty.config(font=(font_choice, 8))
        vhilla_party_size = tk.OptionMenu(bc_win, vhilla_party_size_choice, *party_size)
        vhilla_party_size.config(font=(font_choice, 8))
        vhilla_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=vhilla_status, command=lambda:update_check_status('Versus Hilla', vhilla_status, vhilla_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        vhilla_clear_status.config(indicatoron=False, borderwidth=0)

        # Seren
        seren_name = tk.Label(bc_win, text='Seren', **font_preset, bg='#dbedf3')
        seren_img = tk.Label(bc_win, image=seren_icon, bg='#dbedf3')
        seren_difficulty = tk.OptionMenu(bc_win, seren_difficulty_choice, *difficulty_d)
        seren_difficulty.config(font=(font_choice, 8))
        seren_party_size = tk.OptionMenu(bc_win, seren_party_size_choice, *party_size)
        seren_party_size.config(font=(font_choice, 8))
        seren_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=seren_status, command=lambda:update_check_status('Seren', seren_status, seren_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        seren_clear_status.config(indicatoron=False, borderwidth=0)

        # Kaling
        kaling_name = tk.Label(bc_win, text='Kaling', **font_preset, bg='#dbedf3')
        kaling_img = tk.Label(bc_win, image=kaling_icon, bg='#dbedf3')
        kaling_difficulty = tk.OptionMenu(bc_win, kaling_difficulty_choice, *difficulty_e)
        kaling_difficulty.config(font=(font_choice, 8))
        kaling_party_size = tk.OptionMenu(bc_win, kaling_party_size_choice, *party_size)
        kaling_party_size.config(font=(font_choice, 8))
        kaling_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=kaling_status, command=lambda:update_check_status('Kaling', kaling_status, kaling_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        kaling_clear_status.config(indicatoron=False, borderwidth=0)

        # Kalos
        kalos_name = tk.Label(bc_win, text='Kalos', **font_preset, bg='#dbedf3')
        kalos_img = tk.Label(bc_win, image=kalos_icon, bg='#dbedf3')
        kalos_difficulty = tk.OptionMenu(bc_win, kalos_difficulty_choice, *difficulty_e)
        kalos_difficulty.config(font=(font_choice, 8))
        kalos_party_size = tk.OptionMenu(bc_win, kalos_party_size_choice, *party_size)
        kalos_party_size.config(font=(font_choice, 8))
        kalos_clear_status = tk.Checkbutton(bc_win, image=incomplete_status_icon, variable=kalos_status, command=lambda:update_check_status('Kalos', kalos_status, kalos_clear_status), 
                                            bg='#dbedf3', indicatoron=False, borderwidth=0, selectcolor='#dbedf3', activebackground='#dbedf3')
        kalos_clear_status.config(indicatoron=False, borderwidth=0)
        # endregion

        # button widgets 
        reset_clears_btn = tk.Button(bc_win, text='Reset Clears Only', **font_preset, width=15, command=reset_clears_only, bg='#b5dae6', activebackground='#dbedf3')
        reset_all_btn = tk.Button(bc_win, text='Reset All', **font_preset, width=15, command=reset_all, bg='#b5dae6', activebackground='#dbedf3')
        update_btn = tk.Button(bc_win, text='Update', **font_preset, width=15, command=update_all, bg='#b5dae6', activebackground='#dbedf3')
        cancel_btn = tk.Button(bc_win, text='Cancel', **font_preset, width=15, command=bc_win.destroy, bg='#b5dae6', activebackground='#dbedf3')

        # load the saved checkbutton status with relevant status icons upon popup's opening
        load_clear_statuses()

        # region - grid layout
        bossing_checklist_title.grid(row=0, columnspan=9)
        character_details_lbl.grid(row=1, columnspan=9)

        cpb_name.grid(row=2, column=0, pady=10, padx=(30, 10))
        cpb_img.grid(row=3, column=0, padx=(30, 10))
        cpb_difficulty.grid(row=4, column=0, padx=(30, 10))
        cpb_party_size.grid(row=5, column=0, padx=(30, 10))
        cpb_clear_status.grid(row=6, column=0, pady=10, padx=(30, 10))

        hh_name.grid(row=2, column=1, pady=10, padx=10)
        hh_img.grid(row=3, column=1, padx=10)
        hh_difficulty.grid(row=4, column=1, padx=10)
        hh_party_size.grid(row=5, column=1, padx=10)
        hh_clear_status.grid(row=6, column=1, pady=10, padx=10)

        cyg_name.grid(row=2, column=2, pady=10, padx=10)
        cyg_img.grid(row=3, column=2, padx=10)
        cyg_difficulty.grid(row=4, column=2, padx=10)
        cyg_party_size.grid(row=5, column=2, padx=10)
        cyg_clear_status.grid(row=6, column=2, pady=10, padx=10)

        czak_name.grid(row=2, column=3, pady=10, padx=10)
        czak_img.grid(row=3, column=3, padx=10)
        czak_difficulty.grid(row=4, column=3, padx=10)
        czak_party_size.grid(row=5, column=3, padx=10)
        czak_clear_status.grid(row=6, column=3, pady=10, padx=10)

        pno_name.grid(row=2, column=4, pady=10, padx=10)
        pno_img.grid(row=3, column=4, padx=10)
        pno_difficulty.grid(row=4, column=4, padx=10)
        pno_party_size.grid(row=5, column=4, padx=10)
        pno_clear_status.grid(row=6, column=4, pady=10, padx=10)

        cqueen_name.grid(row=2, column=5, pady=10, padx=10)
        cqueen_img.grid(row=3, column=5, padx=10)
        cqueen_difficulty.grid(row=4, column=5, padx=10)
        cqueen_party_size.grid(row=5, column=5, padx=10)
        cqueen_clear_status.grid(row=6, column=5, pady=10, padx=10)

        cpierre_name.grid(row=7, column=0, pady=10, padx=(30, 10))
        cpierre_img.grid(row=8, column=0, padx=(30, 10))
        cpierre_difficulty.grid(row=9, column=0, padx=(30, 10))
        cpierre_party_size.grid(row=10, column=0, padx=(30, 10))
        cpierre_clear_status.grid(row=11, column=0, pady=10, padx=(30, 10))

        cvonbon_name.grid(row=7, column=1, pady=10, padx=10)
        cvonbon_img.grid(row=8, column=1, padx=10)
        cvonbon_difficulty.grid(row=9, column=1, padx=10)
        cvonbon_party_size.grid(row=10, column=1, padx=10)
        cvonbon_clear_status.grid(row=11, column=1, pady=10, padx=10)

        cvell_name.grid(row=7, column=2, pady=10, padx=10)
        cvell_img.grid(row=8, column=2, padx=10)
        cvell_difficulty.grid(row=9, column=2, padx=10)
        cvell_party_size.grid(row=10, column=2, padx=10)
        cvell_clear_status.grid(row=11, column=2, pady=10, padx=10)

        akechi_name.grid(row=7, column=3, pady=10, padx=10)
        akechi_img.grid(row=8, column=3, padx=10)
        akechi_difficulty.grid(row=9, column=3, padx=10)
        akechi_party_size.grid(row=10, column=3, padx=10)
        akechi_clear_status.grid(row=11, column=3, pady=10, padx=10)

        hmag_name.grid(row=7, column=4, pady=10, padx=10)
        hmag_img.grid(row=8, column=4, padx=10)
        hmag_difficulty.grid(row=9, column=4, padx=10)
        hmag_party_size.grid(row=10, column=4, padx=10)
        hmag_clear_status.grid(row=11, column=4, pady=10, padx=10)

        cpap_name.grid(row=7, column=5, pady=10, padx=10)
        cpap_img.grid(row=8, column=5, padx=10)
        cpap_difficulty.grid(row=9, column=5, padx=10)
        cpap_party_size.grid(row=10, column=5, padx=10)
        cpap_clear_status.grid(row=11, column=5, pady=10, padx=10)

        lotus_name.grid(row=2, column=6, pady=10, padx=10)
        lotus_img.grid(row=3, column=6, padx=10)
        lotus_difficulty.grid(row=4, column=6, padx=10)
        lotus_party_size.grid(row=5, column=6, padx=10)
        lotus_clear_status.grid(row=6, column=6, pady=10, padx=10)

        damien_name.grid(row=2, column=7, pady=10, padx=10)
        damien_img.grid(row=3, column=7, padx=10)
        damien_difficulty.grid(row=4, column=7, padx=10)
        damien_party_size.grid(row=5, column=7, padx=10)
        damien_clear_status.grid(row=6, column=7, pady=10, padx=10)

        gslime_name.grid(row=2, column=8, pady=10, padx=(10, 30))
        gslime_img.grid(row=3, column=8, padx=(10, 30))
        gslime_difficulty.grid(row=4, column=8, padx=(10, 30))
        gslime_party_size.grid(row=5, column=8, padx=(10, 30))
        gslime_clear_status.grid(row=6, column=8, pady=10, padx=(10, 30))

        lucid_name.grid(row=7, column=6, pady=10, padx=10)
        lucid_img.grid(row=8, column=6, padx=10)
        lucid_difficulty.grid(row=9, column=6, padx=10)
        lucid_party_size.grid(row=10, column=6, padx=10)
        lucid_clear_status.grid(row=11, column=6, pady=10, padx=10)

        will_name.grid(row=7, column=7, pady=10, padx=10)
        will_img.grid(row=8, column=7, padx=10)
        will_difficulty.grid(row=9, column=7, padx=10)
        will_party_size.grid(row=10, column=7, padx=10)
        will_clear_status.grid(row=11, column=7, pady=10, padx=10)

        gloom_name.grid(row=7, column=8, pady=10, padx=(10, 30))
        gloom_img.grid(row=8, column=8, padx=(10, 30))
        gloom_difficulty.grid(row=9, column=8, padx=(10, 30))
        gloom_party_size.grid(row=10, column=8, padx=(10, 30))
        gloom_clear_status.grid(row=11, column=8, pady=10, padx=(10, 30))
        
        darknell_name.grid(row=12, column=0, pady=10, padx=(30, 10))
        darknell_img.grid(row=13, column=0, padx=(30, 10))
        darknell_difficulty.grid(row=14, column=0, padx=(30, 10))
        darknell_party_size.grid(row=15, column=0, padx=(30, 10))
        darknell_clear_status.grid(row=16, column=0, pady=10, padx=(30, 10))

        vhilla_name.grid(row=12, column=1, pady=10, padx=10)
        vhilla_img.grid(row=13, column=1, padx=10)
        vhilla_difficulty.grid(row=14, column=1, padx=10)
        vhilla_party_size.grid(row=15, column=1, padx=10)
        vhilla_clear_status.grid(row=16, column=1, pady=10, padx=10)

        seren_name.grid(row=12, column=2, pady=10, padx=10)
        seren_img.grid(row=13, column=2, padx=10)
        seren_difficulty.grid(row=14, column=2, padx=10)
        seren_party_size.grid(row=15, column=2, padx=10)
        seren_clear_status.grid(row=16, column=2, pady=10, padx=10)

        kaling_name.grid(row=12, column=3, pady=10, padx=10)
        kaling_img.grid(row=13, column=3, padx=10)
        kaling_difficulty.grid(row=14, column=3, padx=10)
        kaling_party_size.grid(row=15, column=3, padx=10)
        kaling_clear_status.grid(row=16, column=3, pady=10, padx=10)

        kalos_name.grid(row=12, column=4, pady=10, padx=10)
        kalos_img.grid(row=13, column=4, padx=10)
        kalos_difficulty.grid(row=14, column=4, padx=10)
        kalos_party_size.grid(row=15, column=4, padx=10)
        kalos_clear_status.grid(row=16, column=4, pady=10, padx=10)

        update_btn.grid(row=23, column=2, pady=(20, 30))
        reset_clears_btn.grid(row=23, column=3, pady=(20, 30))
        reset_all_btn.grid(row=23, column=4, pady=(20, 30))
        cancel_btn.grid(row=23, column=5, pady=(20, 30))

        # endregion

        # region - reference vars
        # save image reference to avoid garbage collection
        cpb_img.image = cpb_icon
        hh_img.image = hh_icon
        cyg_img.image = cyg_icon
        czak_img.image = czak_icon
        pno_img.image = pno_icon
        cqueen_img.image = cqueen_icon
        cpierre_img.image = cpierre_icon
        cvonbon_img.image = cvonbon_icon
        cvell_img.image = cvell_icon
        akechi_img.image = akechi_icon
        hmag_img.image = hmag_icon
        cpap_img.image = cpap_icon
        lotus_img.image = lotus_icon
        damien_img.image = damien_icon
        gslime_img.image = gslime_icon
        lucid_img.image = lucid_icon
        will_img.image = will_icon
        gloom_img.image = gloom_icon
        darknell_img.image = darknell_icon
        vhilla_img.image = vhilla_icon
        seren_img.image = seren_icon
        kaling_img.image = kaling_icon
        kalos_img.image = kalos_icon
        # endregion

# // purple functions //
# add mesos amount to balance
def add_mesos():
    
    global current_popup
    global am_win

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
            mesos_balance_display_lbl.config(text=f'${user["usr"].mesos_balance:,.0f}')

            # close popup
            am_win.destroy()
        else:
            # send error prompt
            messagebox.showerror('Invalid Input', 
                                 'Digits Only')
            # present popup window post closure of error prompt
            am_win.lift()

    # check to see if a popup is currently opened
    if is_popup_open():
        messagebox.showerror('Active Popup Detected.',
                             'There is already a Popup opened.')
        am_win.lift()
    else:
        # small popup window asking for user input
        am_win = tk.Toplevel(purple_frame, bg='#dbedf3')
        am_win.title('Add Mesos')
        am_win.geometry('250x150+900+350')
        am_win.resizable(False, False)
        current_popup = am_win

        am_prompt_lbl = tk.Label(am_win, text='Enter Mesos Amount', font=(font_choice, 12), bg='#dbedf3')
        am_amount_entry = tk.Entry(am_win, font=(font_choice, 12), textvariable=mesos_amount, bg='#ffffff', highlightbackground='#161b28', highlightcolor='#6f85b6', highlightthickness=2)
        am_submit_btn = tk.Button(am_win, text='Add to Balance', font=(font_choice, 12), command=topup_balance, bg='#b5dae6', activebackground='#dbedf3')

        am_prompt_lbl.grid(row=0, column=0)
        am_amount_entry.grid(row=1, column=0)
        am_submit_btn.grid(row=2, column=0, pady=(0, 10))

        am_win.grid_rowconfigure(0, weight=1)
        am_win.grid_rowconfigure(1, weight=1)
        am_win.grid_rowconfigure(2, weight=1)
        am_win.grid_columnconfigure(0, weight=1)

# subtract mesos amount from balance
def subtract_mesos():

    global current_popup
    global sm_win

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

                mesos_balance_display_lbl.config(text=f'${user["usr"].mesos_balance:,.0f}')

                sm_win.destroy()
        else:
            messagebox.showerror('Invalid Input',
                                 'Digits Only')
            sm_win.lift()

    # check to see if a popup is currently opened
    if is_popup_open():
        messagebox.showerror('Active Popup Detected.',
                             'There is already a Popup opened.')
        sm_win.lift()
    else:
        # small popup window asking for user input
        sm_win = tk.Toplevel(purple_frame, bg='#dbedf3')
        sm_win.title('Subtract Mesos')
        sm_win.geometry('250x150+900+350')
        sm_win.resizable(False, False)
        current_popup = sm_win

        sm_prompt_lbl = tk.Label(sm_win, text='Enter Mesos Amount', font=(font_choice, 12), bg='#dbedf3')
        sm_amount_entry = tk.Entry(sm_win, font=(font_choice, 12), textvariable=mesos_amount, bg='#ffffff', highlightbackground='#161b28', highlightcolor='#6f85b6', highlightthickness=2)
        sm_submit_btn = tk.Button(sm_win, text='Subtract from Balance', font=(font_choice, 12), command=reduce_balance, bg='#b5dae6', activebackground='#dbedf3')

        sm_prompt_lbl.grid(row=0, column=0)
        sm_amount_entry.grid(row=1, column=0)
        sm_submit_btn.grid(row=2, column=0, pady=(0, 10))

        sm_win.grid_rowconfigure(0, weight=1)
        sm_win.grid_rowconfigure(1, weight=1)
        sm_win.grid_rowconfigure(2, weight=1)
        sm_win.grid_columnconfigure(0, weight=1)

# rest mesos balance to 0
def reset_mesos():
    user['usr'].mesos_balance = 0

    json_object = json.dumps(user, indent=4, default=custom_serializer)

    with open(usr_filename, 'w') as outfile:
        outfile.write(json_object)

    mesos_balance_display_lbl.config(text=f'${user["usr"].mesos_balance:,.0f}')

# reset the boss stats for the new week (thursdays)
def reset_boss_stats():

    # retrieve the current date information
    utc_time = dt.datetime.now(timezone.utc)
    todays_date = utc_time.date().strftime('%d-%m-%Y')

    # check if today is a thursday and if a reset has already occurred for this week
    if utc_time.weekday() == 3 and user['usr'].boss_crystal_reset != todays_date:
        user['usr'].boss_crystal_reset = todays_date
        # resets weekly boss crystal count
        user['usr'].boss_crystal_count = 180
        # resets boss crystals sold
        user['usr'].boss_crystal_sold = 0
        # resets weekly mesos gained
        user['usr'].weekly_mesos_gained = 0

        # update user save file
        json_object = json.dumps(user, indent=4, default=custom_serializer)

        with open(usr_filename, 'w') as outfile:
            outfile.write(json_object)

# // orange functions // 
# open weblink
def open_hotlink(hotlink):
    # check for empty hotlinks
    if hotlink == '':
        messagebox.showerror('No Link Found',
                             'No link was saved this hotlink.')
        return

    webbrowser.open(hotlink)

# editing hotlinks
def edit_hotlinks():

    global current_popup
    global ehl_win
    first_hotlink = tk.StringVar()
    second_hotlink = tk.StringVar()
    third_hotlink = tk.StringVar()

    # set vars to save data
    first_hotlink.set(user['usr'].hotlink_one)
    second_hotlink.set(user['usr'].hotlink_two)
    third_hotlink.set(user['usr'].hotlink_three)

    # update hotlink values
    def save_edit():
        user['usr'].hotlink_one = first_hotlink.get()
        user['usr'].hotlink_two = second_hotlink.get()
        user['usr'].hotlink_three = third_hotlink.get()

        # save new hotlink data
        json_object = json.dumps(user, indent=4, default=custom_serializer)

        with open(usr_filename, 'w') as outfile:
            outfile.write(json_object)
        
        # close popup
        ehl_win.destroy()

    # check to see if a popup is currently opened
    if is_popup_open():
        messagebox.showerror('Active Popup Detected.',
                             'There is already a Popup opened.')
        ehl_win.lift()
    else:
        ehl_win = tk.Toplevel(orange_frame, bg='#dbedf3')
        ehl_win.title('Edit Hotlinks')
        ehl_win.geometry('500x200+750+350')
        ehl_win.resizable(False, False)
        current_popup = ehl_win

        ehl_hotlinks_title_lbl = tk.Label(ehl_win, text='Edit Hot Links', font=(font_choice, 12), bg='#dbedf3')
        ehl_first_hotlink_lbl = tk.Label(ehl_win, text='Hot Link 1:', font=(font_choice, 12), bg='#dbedf3')
        ehl_first_hotlink_entry = tk.Entry(ehl_win, textvariable=first_hotlink, font=(font_choice, 12), bg='#ffffff', highlightbackground='#161b28', highlightcolor='#6f85b6', highlightthickness=2)
        ehl_second_hotlink_lbl = tk.Label(ehl_win, text='Hot Link 2:', font=(font_choice, 12), bg='#dbedf3')
        ehl_second_hotlink_entry = tk.Entry(ehl_win, textvariable=second_hotlink, font=(font_choice, 12), bg='#ffffff', highlightbackground='#161b28', highlightcolor='#6f85b6', highlightthickness=2)
        ehl_third_hotlink_lbl = tk.Label(ehl_win, text='Hot Link 3:', font=(font_choice, 12), bg='#dbedf3')
        ehl_third_hotlink_entry = tk.Entry(ehl_win, textvariable=third_hotlink, font=(font_choice, 12), bg='#ffffff', highlightbackground='#161b28', highlightcolor='#6f85b6', highlightthickness=2)
        ehl_edit_btn = tk.Button(ehl_win, text='Save Edit', font=(font_choice, 12), command=save_edit, bg='#b5dae6', activebackground='#dbedf3')

        ehl_hotlinks_title_lbl.place(x=0, y=5, width=500, height=30)
        ehl_first_hotlink_lbl.place(x=0, y=40, width=100, height=30)
        ehl_first_hotlink_entry.place(x=100, y=40, width=385, height=30)
        ehl_second_hotlink_lbl.place(x=0, y=80, width=100, height=30)
        ehl_second_hotlink_entry.place(x=100, y=80, width=385, height=30)
        ehl_third_hotlink_lbl.place(x=0, y=120, width=100, height=30)
        ehl_third_hotlink_entry.place(x=100, y=120, width=385, height=30)
        ehl_edit_btn.place(x=200, y=160, width=100, height=30)

# load in the user 
load_user()

# if weekly reset, reset boss crystals
reset_boss_stats()

root = tk.Tk()
myappid = 'kandayo.kandayo.maplestory.bossing' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
# create tkinter compatible image reference
icon_ico = Image.open('./img/kandayo_icon_opaque.ico')
icon_ico.thumbnail((50, 50))
icon_ico = ImageTk.PhotoImage(icon_ico)

# position window display upon open
root.geometry('+600+150')
root.title('Kandayo - Maplestory Weekly Bossing Assistant')
root.resizable(False, False)
root.iconphoto(True, icon_ico)

# // Setting up Frames //
yellow_frame = tk.Frame(root, width=800, height=120, bg='#dbedf3', highlightbackground='#161b28', highlightthickness=2)
red_frame = tk.Frame(root, width=300, height=300, bg='#dbedf3', highlightbackground='#161b28', highlightthickness=2)
blue_frame = tk.Frame(root, width=300, height=100, bg='#dbedf3', highlightbackground='#161b28', highlightthickness=2)
purple_frame = tk.Frame(root, width=500, height=300, bg='#dbedf3', highlightbackground='#161b28', highlightthickness=2)
orange_frame = tk.Frame(root, width=500, height=100, bg='#dbedf3', highlightbackground='#161b28', highlightthickness=2)
grey_frame = tk.Frame(root, width=800, height=30, bg='#dbedf3', highlightbackground='#161b28', highlightthickness=2)

yellow_frame.grid(row=0, columnspan=2, sticky='nswe', padx=10, pady=(10, 0))
red_frame.grid(row=1, column=0, sticky='nswe', padx=(10, 0), pady=(10, 0))
blue_frame.grid(row=2, column=0, sticky='nswe', padx=(10, 0), pady=10)
purple_frame.grid(row=1, column=1, sticky='nswe', padx=10, pady=10)
orange_frame.grid(row=2, column=1, sticky='nswe', padx=10, pady=(0, 10))
grey_frame.grid(row=3, columnspan=2, sticky='nswe', padx=10, pady=(0, 10))

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

yellow_frame.grid_propagate(False)
purple_frame.grid_propagate(False)
red_frame.grid_propagate(False)
blue_frame.grid_propagate(False)
orange_frame.grid_propagate(False)
grey_frame.grid_propagate(False)

# // yellow frame //
# yellow widgets
app_icon_name_img = Image.open('./img/app_icon_name_transparent.png')
app_icon_name_img.thumbnail((200, 200))
app_icon_name_img = ImageTk.PhotoImage(app_icon_name_img)

utc_livetime_lbl = tk.Label(yellow_frame, font=(font_choice, 12), bg='#dbedf3', fg='#283149')
ursus_time_lbl = tk.Label(yellow_frame, font=(font_choice, 12), bg='#dbedf3', fg='#283149')
daily_reset_lbl = tk.Label(yellow_frame, font=(font_choice, 12), bg='#dbedf3', fg='#283149')
weekly_reset_lbl = tk.Label(yellow_frame, font=(font_choice, 12), bg='#dbedf3', fg='#283149')
app_icon_lbl = tk.Label(yellow_frame, font=(font_choice, 12), bg='#dbedf3', fg='#283149', image=app_icon_name_img)

utc_livetime_lbl.grid(row=0, column=0, sticky='w', padx=10)
ursus_time_lbl.grid(row=1, column=0, sticky='w', padx=10)
daily_reset_lbl.grid(row=0, column=1, sticky='w', padx=10)
weekly_reset_lbl.grid(row=1, column=1, sticky='w', padx=10)
app_icon_lbl.grid(row=0, rowspan=2, column=2)

yellow_frame.grid_rowconfigure(0, weight=1)
yellow_frame.grid_rowconfigure(1, weight=1)
yellow_frame.grid_columnconfigure(0, weight=1)
yellow_frame.grid_columnconfigure(1, weight=1)
yellow_frame.grid_columnconfigure(2, weight=1)

# tooltips for yellow frame
utc_livetime_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Current Server Time (Timezone: UTC)'))
utc_livetime_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

ursus_time_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Time Remaining Until Next Ursus 2x Bonus Rewards'))
ursus_time_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

daily_reset_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Time Remaining Until Daily Reset'))
daily_reset_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

weekly_reset_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Time Remaining Until Weekly Reset'))
weekly_reset_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

app_icon_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, "It's Kandayo's Official Mascot!"))
app_icon_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

# // red frame // 
# red widgets
chars_lb = tk.Listbox(red_frame, font=(font_choice, 12), bg='#ffffff', fg='#283149', selectbackground='#b4dae6', justify='center')
clb_scrollbar = tk.Scrollbar(red_frame)

chars_lb.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
clb_scrollbar.pack(side='right', fill='both', padx=(0, 10), pady=10)

chars_lb.config(yscrollcommand=clb_scrollbar.set)
clb_scrollbar.config(command=chars_lb.yview)

chars_lb.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'A List of Registered Characters For Weekly Bossing'))
chars_lb.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

# // blue frame // 
# blue widgets
addchar_btn = tk.Button(blue_frame, text='Add Character', font=(font_choice, 10), bg='#b5dae6', fg='#283149', width=15, activebackground='#dbedf3', command=add_character_popup)
updchar_btn = tk.Button(blue_frame, text='Update Character', font=(font_choice, 10), bg='#b5dae6', fg='#283149', width=15, activebackground='#dbedf3', command=update_character_popup)
delchar_btn = tk.Button(blue_frame, text='Delete Character', font=(font_choice, 10), bg='#b5dae6', fg='#283149', width=15, activebackground='#dbedf3', command=delete_character)
bossing_checklist_btn = tk.Button(blue_frame, text='Bossing Checklist', font=(font_choice, 10), bg='#b5dae6', fg='#283149', width=15, activebackground='#dbedf3', command=bossing_checklist_popup)

addchar_btn.grid(row=0, column=0)
updchar_btn.grid(row=0, column=1)
delchar_btn.grid(row=1, column=0)
bossing_checklist_btn.grid(row=1, column=1)

blue_frame.grid_rowconfigure(0, weight=1)
blue_frame.grid_rowconfigure(1, weight=1)
blue_frame.grid_columnconfigure(0, weight=1)
blue_frame.grid_columnconfigure(1, weight=1)

addchar_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Add A New Character To The Registered List To Track Weekly Bossing'))
addchar_btn.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

updchar_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, "Update A Selected Character's Details"))
updchar_btn.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

delchar_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Delete A Character From The Registered List'))
delchar_btn.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

bossing_checklist_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Manage Weekly Bossing For A Selected Character'))
bossing_checklist_btn.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

# // purple // 
# purple widgets
mesos_balance_title_lbl = tk.Label(purple_frame, text='Mesos Balance:', font=(font_choice, 16), bg='#dbedf3', fg='#283149')
mesos_balance_display_lbl = tk.Label(purple_frame, text=f'${user['usr'].mesos_balance:,.0f}', font=(font_choice, 14), bg='#dbedf3', fg='#283149')
add_mesos_btn = tk.Button(purple_frame, text='Add Mesos', font=(font_choice, 10), activebackground='#dbedf3', command=add_mesos, bg='#b5dae6', fg='#283149', width=15)
remove_mesos_btn = tk.Button(purple_frame, text='Remove Mesos', font=(font_choice, 10), activebackground='#dbedf3', command=subtract_mesos, bg='#b5dae6', fg='#283149', width=15)
reset_balance_btn = tk.Button(purple_frame, text='Reset Balance', font=(font_choice, 10), activebackground='#dbedf3', command=reset_mesos, bg='#b5dae6', fg='#283149', width=15)

bc_remaining_lbl = tk.Label(purple_frame, text=f'Boss Crystals Remaining: {user['usr'].boss_crystal_count - user['usr'].boss_crystal_sold}', font=(font_choice, 16), activebackground='#dbedf3', bg='#dbedf3', fg='#283149')
bc_sold_lbl = tk.Label(purple_frame, text=f'Boss Crystals Sold: {user['usr'].boss_crystal_sold}', font=(font_choice, 16), activebackground='#dbedf3', bg='#dbedf3', fg='#283149')
wm_gained_lbl = tk.Label(purple_frame, text=f'Weekly Mesos Gained: ${user['usr'].weekly_mesos_gained:,.0f}', font=(font_choice, 16), activebackground='#dbedf3', bg='#dbedf3', fg='#283149')

mesos_balance_title_lbl.place(x=0, y=20, width=490, height=30)
mesos_balance_display_lbl.place(x=0, y=50, width=490, height=30)
add_mesos_btn.place(x=60, y=80, width=100, height=30)
remove_mesos_btn.place(x=200, y=80, width=100, height=30)
reset_balance_btn.place(x=340, y=80, width=100, height=30)

bc_remaining_lbl.place(x=0, y=140, width=490, height=30)
bc_sold_lbl.place(x=0, y=185, width=490, height=30)
wm_gained_lbl.place(x=0, y=230, width=490, height=30)

mesos_balance_title_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Current Mesos Balance'))
mesos_balance_title_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

mesos_balance_display_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Current Mesos Balance'))
mesos_balance_display_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

add_mesos_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Add Mesos To The Mesos Balance'))
add_mesos_btn.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

remove_mesos_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Remove Mesos From The Mesos Balance'))
remove_mesos_btn.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

reset_balance_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Reset Mesos Balance to $0'))
reset_balance_btn.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

bc_remaining_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Boss Crystals Remaining To Be Sold Before Weekly Reset'))
bc_remaining_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

bc_sold_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Boss Crystals Sold This Current Week'))
bc_sold_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

wm_gained_lbl.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Amount Of Mesos Gained For The Week From Bossing'))
wm_gained_lbl.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

# // orange //
# orange widgets

edit_cog_img = Image.open('./img/edit_cog.png')
edit_cog_img.thumbnail((100, 100))
edit_cog_img = ImageTk.PhotoImage(edit_cog_img)

hotlink_one_btn = tk.Button(orange_frame, text='Hot Link 1', font=(font_choice, 12), activebackground='#dbedf3', command=lambda:open_hotlink(user['usr'].hotlink_one), bg='#b5dae6', fg='#283149')
hotlink_two_btn = tk.Button(orange_frame, text='Hot Link 2', font=(font_choice, 12), activebackground='#dbedf3', command=lambda:open_hotlink(user['usr'].hotlink_two), bg='#b5dae6', fg='#283149')
hotlink_three_btn = tk.Button(orange_frame, text='Hot Link 3', font=(font_choice, 12), activebackground='#dbedf3', command=lambda:open_hotlink(user['usr'].hotlink_three), bg='#b5dae6', fg='#283149')
edit_hotlinks_btn = tk.Button(orange_frame, text='Edit Hot Links', font=(font_choice, 12), borderwidth=0, image=edit_cog_img, command=edit_hotlinks, bg='#dbedf3', activebackground='#dbedf3')

hotlink_one_btn.grid(row=0, column=0)
hotlink_two_btn.grid(row=0, column=1)
hotlink_three_btn.grid(row=0, column=2)
edit_hotlinks_btn.grid(row=0, column=3)

orange_frame.grid_rowconfigure(0, weight=1)
orange_frame.grid_columnconfigure(0, weight=1)
orange_frame.grid_columnconfigure(1, weight=1)
orange_frame.grid_columnconfigure(2, weight=1)
orange_frame.grid_columnconfigure(3, weight=1)

# tooltip info
hotlink_one_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'First Customised Hot Link (Redirects To The Web)'))

hotlink_two_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Second Customised Hot Link (Redirects To The Web)'))

hotlink_three_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Three Customised Hot Link (Redirects To The Web)'))

edit_hotlinks_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, status_bar_lbl, 'Edit Customised Hot Links'))
edit_hotlinks_btn.bind("<Leave>", lambda mouse_event: on_hover_leave(mouse_event, status_bar_lbl))

# // grey //
# brief information display for widgets upon hover
status_bar_lbl = tk.Label(grey_frame, text='', bg='#dbedf3') # tbd whether to re-incorporate font
status_bar_lbl.pack(fill='x', side='right', padx=10)

# authorship of developer
author_lbl = tk.Label(grey_frame, text='Created By NampaDevelops', padx=10, bg='#dbedf3', font=(font_choice, 8))
author_lbl.pack(side='left')

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
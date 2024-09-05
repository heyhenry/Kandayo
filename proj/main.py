import tkinter as tk
from tkinter import messagebox
from datetime import timezone, timedelta
import datetime as dt
import webbrowser
from charinfo import CharInfo
from bosslist import BossList
from userinfo import UserInfo
from boss import Boss
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
                user[usr] = UserInfo(usr_info['mesos_balance'], usr_info['weekly_mesos_gained'], usr_info['boss_crystal_reset'], usr_info['boss_crystal_count'], usr_info['boss_crystal_sold'],
                                      usr_info['hotlink_one'], usr_info['hotlink_two'], usr_info['hotlink_three'])

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
    ac_win.resizable(False, False)

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
    uc_win.resizable(False, False)

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

# bossing checklist
def bossing_checklist_popup():

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

    # update bossing checklist
    def update_check_status(boss_name, clicked_status):

        # determines which value change is required based on checkbutton status
        if clicked_status.get():
            characters[selected_ign].boss_list[boss_name]['boss_clear'] = True
        else:
            characters[selected_ign].boss_list[boss_name]['boss_clear'] = False

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
    def update_difficulty_party_size():
        update_bossing_difficulty()
        update_party_size()

    bc_win = tk.Toplevel(blue_frame)
    bc_win.title("Bossing Checklist")
    # bc_win.geometry()

    # difficulty variations
    
    # for: Cygnus
    difficulty_a = [
        'Easy',
        'Normal'
    ]
    
    # for: Lotus, Damien, Guardian Slime, Gloom, Verus Hilla, Darknell
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

    # for: Seren
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
        1,
        2,
        3,
        4,
        5,
        6
    ]

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

    # ---> Spacers <---

    # Widgets
    bossing_checklist_title = tk.Label(bc_win, text='Bossing Checklist')
    character_details_lbl = tk.Label(bc_win, text=f'ign | job | Lv.')

    # Chaos Pink Bean
    cpb_name = tk.Label(bc_win, text='Chaos Pink Bean')
    cpb_img = tk.Label(bc_win, text='BOSS IMG HERE')
    cpb_difficulty = tk.OptionMenu(bc_win, cpb_difficulty_choice, *difficulty_a) 
    cpb_difficulty.config(state='disabled')
    cpb_party_size = tk.OptionMenu(bc_win, cpb_party_size_choice, *party_size)
    cpb_clear_status = tk.Checkbutton(bc_win, variable=cpb_status, command=lambda:update_check_status('Chaos Pink Bean', cpb_status))

    # Hard Hilla
    hh_name = tk.Label(bc_win, text='Hard Hilla')
    hh_img = tk.Label(bc_win, text='BOSS IMG HERE')
    hh_difficulty = tk.OptionMenu(bc_win, hh_difficulty_choice, *difficulty_a) 
    hh_difficulty.config(state='disabled')
    hh_party_size = tk.OptionMenu(bc_win, hh_party_size_choice, *party_size)
    hh_clear_status = tk.Checkbutton(bc_win, variable=hh_status, command=lambda:update_check_status('Hard Hilla', hh_status))

    # Cygnus
    cyg_name = tk.Label(bc_win, text='Cygnus')
    cyg_img = tk.Label(bc_win, text='BOSS IMG HERE')
    cyg_difficulty = tk.OptionMenu(bc_win, cyg_difficulty_choice, *difficulty_a)
    cyg_party_size = tk.OptionMenu(bc_win, cyg_party_size_choice, *party_size)
    cyg_clear_status = tk.Checkbutton(bc_win, variable=cyg_status, command=lambda:update_check_status('Cygnus', cyg_status))

    # Chaos Zakum
    czak_name = tk.Label(bc_win, text='Chaos Zakum')
    czak_img = tk.Label(bc_win, text='BOSS IMG HERE')
    czak_difficulty = tk.OptionMenu(bc_win, czak_difficulty_choice, *difficulty_a) 
    czak_difficulty.config(state='disabled')
    czak_party_size = tk.OptionMenu(bc_win, czak_party_size_choice, *party_size)
    czak_clear_status = tk.Checkbutton(bc_win, variable=czak_status, command=lambda:update_check_status('Chaos Zakum', czak_status))

    # Princess No
    pno_name = tk.Label(bc_win, text='Princess No')
    pno_img = tk.Label(bc_win, text='BOSS IMG HERE')
    pno_difficulty = tk.OptionMenu(bc_win, pno_difficulty_choice, *difficulty_a) 
    pno_difficulty.config(state='disabled')
    pno_party_size = tk.OptionMenu(bc_win, pno_party_size_choice, *party_size)
    pno_clear_status = tk.Checkbutton(bc_win, variable=pno_status, command=lambda:update_check_status('Princess No', pno_status))

    # Chaos Queen
    cqueen_name = tk.Label(bc_win, text='Chaos Queen')
    cqueen_img = tk.Label(bc_win, text='BOSS IMG HERE')
    cqueen_difficulty = tk.OptionMenu(bc_win, cqueen_difficulty_choice, *difficulty_a) 
    cqueen_difficulty.config(state='disabled')
    cqueen_party_size = tk.OptionMenu(bc_win, cqueen_party_size_choice, *party_size)
    cqueen_clear_status = tk.Checkbutton(bc_win, variable=cqueen_status, command=lambda:update_check_status('Chaos Queen', cqueen_status))

    # Chaos Pierre
    cpierre_name = tk.Label(bc_win, text='Chaos Pierre')
    cpierre_img = tk.Label(bc_win, text='BOSS IMG HERE')
    cpierre_difficulty = tk.OptionMenu(bc_win, cpierre_difficulty_choice, *difficulty_a) 
    cpierre_difficulty.config(state='disabled')
    cpierre_party_size = tk.OptionMenu(bc_win, cpierre_party_size_choice, *party_size)
    cpierre_clear_status = tk.Checkbutton(bc_win, variable=cpierre_status, command=lambda:update_check_status('Chaos Pierre', cpierre_status))

    # Chaos Von Bon
    cvonbon_name = tk.Label(bc_win, text='Chaos Von Bon')
    cvonbon_img = tk.Label(bc_win, text='BOSS IMG HERE')
    cvonbon_difficulty = tk.OptionMenu(bc_win, cvonbon_difficulty_choice, *difficulty_a) 
    cvonbon_difficulty.config(state='disabled')
    cvonbon_party_size = tk.OptionMenu(bc_win, cvonbon_party_size_choice, *party_size)
    cvonbon_clear_status = tk.Checkbutton(bc_win, variable=cvonbon_status, command=lambda:update_check_status('Chaos Von Bon', cvonbon_status))

    # Chaos Vellum
    cvell_name = tk.Label(bc_win, text='Chaos Vellum')
    cvell_img = tk.Label(bc_win, text='BOSS IMG HERE')
    cvell_difficulty = tk.OptionMenu(bc_win, cvell_difficulty_choice, *difficulty_a) 
    cvell_difficulty.config(state='disabled')
    cvell_party_size = tk.OptionMenu(bc_win, cvell_party_size_choice, *party_size)
    cvell_clear_status = tk.Checkbutton(bc_win, variable=cvell_status, command=lambda:update_check_status('Chaos Vellum', cvell_status))

    # Akechi Mitsuhide
    akechi_name = tk.Label(bc_win, text='Akechi Mitsuhide')
    akechi_img = tk.Label(bc_win, text='BOSS IMG HERE')
    akechi_difficulty = tk.OptionMenu(bc_win, akechi_difficulty_choice, *difficulty_a) 
    akechi_difficulty.config(state='disabled')
    akechi_party_size = tk.OptionMenu(bc_win, akechi_party_size_choice, *party_size)
    akechi_clear_status = tk.Checkbutton(bc_win, variable=akechi_status, command=lambda:update_check_status('Akechi Mitsuhide', akechi_status))

    # Hard Magnus
    hmag_name = tk.Label(bc_win, text='Hard Magnus')
    hmag_img = tk.Label(bc_win, text='BOSS IMG HERE')
    hmag_difficulty = tk.OptionMenu(bc_win, hmag_difficulty_choice, *difficulty_a) 
    hmag_difficulty.config(state='disabled')
    hmag_party_size = tk.OptionMenu(bc_win, hmag_party_size_choice, *party_size)
    hmag_clear_status = tk.Checkbutton(bc_win, variable=hmag_status, command=lambda:update_check_status('Hard Magnus', hmag_status))

    # Chaos Papulatus
    cpap_name = tk.Label(bc_win, text='Chaos Papulatus')
    cpap_img = tk.Label(bc_win, text='BOSS IMG HERE')
    cpap_difficulty = tk.OptionMenu(bc_win, cpap_difficulty_choice, *difficulty_a) 
    cpap_difficulty.config(state='disabled')
    cpap_party_size = tk.OptionMenu(bc_win, cpap_party_size_choice, *party_size)
    cpap_clear_status = tk.Checkbutton(bc_win, variable=cpap_status, command=lambda:update_check_status('Chaos Papulatus', cpap_status))

    # Lotus
    lotus_name = tk.Label(bc_win, text='Lotus')
    lotus_img = tk.Label(bc_win, text='BOSS IMG HERE')
    lotus_difficulty = tk.OptionMenu(bc_win, lotus_difficulty_choice, *difficulty_b)
    lotus_party_size = tk.OptionMenu(bc_win, lotus_party_size_choice, *party_size)
    lotus_clear_status = tk.Checkbutton(bc_win, variable=lotus_status, command=lambda:update_check_status('Lotus', lotus_status))

    # Damien
    damien_name = tk.Label(bc_win, text='Damien')
    damien_img = tk.Label(bc_win, text='BOSS IMG HERE')
    damien_difficulty = tk.OptionMenu(bc_win, damien_difficulty_choice, *difficulty_b)
    damien_party_size = tk.OptionMenu(bc_win, damien_party_size_choice, *party_size)
    damien_clear_status = tk.Checkbutton(bc_win, variable=damien_status, command=lambda:update_check_status('Damien', damien_status))

    # Guardian Slime
    gslime_name = tk.Label(bc_win, text='Guardian Slime')
    gslime_img = tk.Label(bc_win, text='BOSS IMG HERE')
    gslime_difficulty = tk.OptionMenu(bc_win, gslime_difficulty_choice, *difficulty_b)
    gslime_party_size = tk.OptionMenu(bc_win, gslime_party_size_choice, *party_size)
    gslime_clear_status = tk.Checkbutton(bc_win, variable=gslime_status, command=lambda:update_check_status('Guardian Slime', gslime_status))

    # Lucid
    lucid_name = tk.Label(bc_win, text='Lucid')
    lucid_img = tk.Label(bc_win, text='BOSS IMG HERE')
    lucid_difficulty = tk.OptionMenu(bc_win, lucid_difficulty_choice, *difficulty_c)
    lucid_party_size = tk.OptionMenu(bc_win, lucid_party_size_choice, *party_size)
    lucid_clear_status = tk.Checkbutton(bc_win, variable=lucid_status, command=lambda:update_check_status('Lucid', lucid_status))

    # Will
    will_name = tk.Label(bc_win, text='Will')
    will_img = tk.Label(bc_win, text='BOSS IMG HERE')
    will_difficulty = tk.OptionMenu(bc_win, will_difficulty_choice, *difficulty_c)
    will_party_size = tk.OptionMenu(bc_win, will_party_size_choice, *party_size)
    will_clear_status = tk.Checkbutton(bc_win, variable=will_status, command=lambda:update_check_status('Will', will_status))

    # Gloom
    gloom_name = tk.Label(bc_win, text='Gloom')
    gloom_img = tk.Label(bc_win, text='BOSS IMG HERE')
    gloom_difficulty = tk.OptionMenu(bc_win, gloom_difficulty_choice, *difficulty_b)
    gloom_party_size = tk.OptionMenu(bc_win, gloom_party_size_choice, *party_size)
    gloom_clear_status = tk.Checkbutton(bc_win, variable=gloom_status, command=lambda:update_check_status('Gloom', gloom_status))

    # Darknell
    darknell_name = tk.Label(bc_win, text='Darknell')
    darknell_img = tk.Label(bc_win, text='BOSS IMG HERE')
    darknell_difficulty = tk.OptionMenu(bc_win, darknell_difficulty_choice, *difficulty_b)
    darknell_party_size = tk.OptionMenu(bc_win, darknell_party_size_choice, *party_size)
    darknell_clear_status = tk.Checkbutton(bc_win, variable=darknell_status, command=lambda:update_check_status('Darknell', darknell_status))

    # Versus Hilla
    vhilla_name = tk.Label(bc_win, text='Versus Hilla')
    vhilla_img = tk.Label(bc_win, text='BOSS IMG HERE')
    vhilla_difficulty = tk.OptionMenu(bc_win, vhilla_difficulty_choice, *difficulty_b)
    vhilla_party_size = tk.OptionMenu(bc_win, vhilla_party_size_choice, *party_size)
    vhilla_clear_status = tk.Checkbutton(bc_win, variable=vhilla_status, command=lambda:update_check_status('Versus Hilla', vhilla_status))

    # Seren
    seren_name = tk.Label(bc_win, text='Seren')
    seren_img = tk.Label(bc_win, text='BOSS IMG HERE')
    seren_difficulty = tk.OptionMenu(bc_win, seren_difficulty_choice, *difficulty_d)
    seren_party_size = tk.OptionMenu(bc_win, seren_party_size_choice, *party_size)
    seren_clear_status = tk.Checkbutton(bc_win, variable=seren_status, command=lambda:update_check_status('Seren', seren_status))

    # Kaling
    kaling_name = tk.Label(bc_win, text='Kaling')
    kaling_img = tk.Label(bc_win, text='BOSS IMG HERE')
    kaling_difficulty = tk.OptionMenu(bc_win, kaling_difficulty_choice, *difficulty_e)
    kaling_party_size = tk.OptionMenu(bc_win, kaling_party_size_choice, *party_size)
    kaling_clear_status = tk.Checkbutton(bc_win, variable=kaling_status, command=lambda:update_check_status('Kaling', kaling_status))

    # Kalos
    kalos_name = tk.Label(bc_win, text='Kalos')
    kalos_img = tk.Label(bc_win, text='BOSS IMG HERE')
    kalos_difficulty = tk.OptionMenu(bc_win, kalos_difficulty_choice, *difficulty_e)
    kalos_party_size = tk.OptionMenu(bc_win, kalos_party_size_choice, *party_size)
    kalos_clear_status = tk.Checkbutton(bc_win, variable=kalos_status, command=lambda:update_check_status('Kalos', kalos_status))

    # Buttons
    reset_clears = tk.Button(bc_win, text='Reset Clears Only')
    reset_all = tk.Button(bc_win, text='Reset All')
    update_btn = tk.Button(bc_win, text='Update', command=update_difficulty_party_size)
    cancel_btn = tk.Button(bc_win, text='Cancel', command=bc_win.destroy)

    bossing_checklist_title.grid(row=0, columnspan=6)
    character_details_lbl.grid(row=1, columnspan=6)

    cpb_name.grid(row=2, column=0, pady=10, padx=10)
    cpb_img.grid(row=3, column=0, padx=10)
    cpb_difficulty.grid(row=4, column=0, padx=10)
    cpb_party_size.grid(row=5, column=0, padx=10)
    cpb_clear_status.grid(row=6, column=0, pady=10, padx=10)

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

    cpierre_name.grid(row=7, column=0, pady=10, padx=10)
    cpierre_img.grid(row=8, column=0, padx=10)
    cpierre_difficulty.grid(row=9, column=0, padx=10)
    cpierre_party_size.grid(row=10, column=0, padx=10)
    cpierre_clear_status.grid(row=11, column=0, pady=10, padx=10)

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

    lotus_name.grid(row=12, column=0, pady=10, padx=10)
    lotus_img.grid(row=13, column=0, padx=10)
    lotus_difficulty.grid(row=14, column=0, padx=10)
    lotus_party_size.grid(row=15, column=0, padx=10)
    lotus_clear_status.grid(row=16, column=0, pady=10, padx=10)

    damien_name.grid(row=12, column=1, pady=10, padx=10)
    damien_img.grid(row=13, column=1, padx=10)
    damien_difficulty.grid(row=14, column=1, padx=10)
    damien_party_size.grid(row=15, column=1, padx=10)
    damien_clear_status.grid(row=16, column=1, pady=10, padx=10)

    gslime_name.grid(row=12, column=2, pady=10, padx=10)
    gslime_img.grid(row=13, column=2, padx=10)
    gslime_difficulty.grid(row=14, column=2, padx=10)
    gslime_party_size.grid(row=15, column=2, padx=10)
    gslime_clear_status.grid(row=16, column=2, pady=10, padx=10)

    lucid_name.grid(row=12, column=3, pady=10, padx=10)
    lucid_img.grid(row=13, column=3, padx=10)
    lucid_difficulty.grid(row=14, column=3, padx=10)
    lucid_party_size.grid(row=15, column=3, padx=10)
    lucid_clear_status.grid(row=16, column=3, pady=10, padx=10)

    will_name.grid(row=12, column=4, pady=10, padx=10)
    will_img.grid(row=13, column=4, padx=10)
    will_difficulty.grid(row=14, column=4, padx=10)
    will_party_size.grid(row=15, column=4, padx=10)
    will_clear_status.grid(row=16, column=4, pady=10, padx=10)

    gloom_name.grid(row=12, column=5, pady=10, padx=10)
    gloom_img.grid(row=13, column=5, padx=10)
    gloom_difficulty.grid(row=14, column=5, padx=10)
    gloom_party_size.grid(row=15, column=5, padx=10)
    gloom_clear_status.grid(row=16, column=5, pady=10, padx=10)

    darknell_name.grid(row=17, column=0, pady=10, padx=10)
    darknell_img.grid(row=18, column=0, padx=10)
    darknell_difficulty.grid(row=19, column=0, padx=10)
    darknell_party_size.grid(row=20, column=0, padx=10)
    darknell_clear_status.grid(row=21, column=0, pady=10, padx=10)

    vhilla_name.grid(row=17, column=1, pady=10, padx=10)
    vhilla_img.grid(row=18, column=1, padx=10)
    vhilla_difficulty.grid(row=19, column=1, padx=10)
    vhilla_party_size.grid(row=20, column=1, padx=10)
    vhilla_clear_status.grid(row=21, column=1, pady=10, padx=10)

    seren_name.grid(row=17, column=2, pady=10, padx=10)
    seren_img.grid(row=18, column=2, padx=10)
    seren_difficulty.grid(row=19, column=2, padx=10)
    seren_party_size.grid(row=20, column=2, padx=10)
    seren_clear_status.grid(row=21, column=2, pady=10, padx=10)

    kaling_name.grid(row=17, column=3, pady=10, padx=10)
    kaling_img.grid(row=18, column=3, padx=10)
    kaling_difficulty.grid(row=19, column=3, padx=10)
    kaling_party_size.grid(row=20, column=3, padx=10)
    kaling_clear_status.grid(row=21, column=3, pady=10, padx=10)

    kalos_name.grid(row=17, column=4, pady=10, padx=10)
    kalos_img.grid(row=18, column=4, padx=10)
    kalos_difficulty.grid(row=19, column=4, padx=10)
    kalos_party_size.grid(row=20, column=4, padx=10)
    kalos_clear_status.grid(row=21, column=4, pady=10, padx=10)

    update_btn.grid(row=23, column=0)
    reset_clears.grid(row=23, column=1)
    reset_all.grid(row=23, column=2)
    cancel_btn.grid(row=23, column=3)

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
    am_win.resizable(False, False)

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
    sm_win.resizable(False, False)

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

# reset the boss crystals for the new week (thursdays)
def reset_boss_crystals():

    # retrieve the current date information
    utc_time = dt.datetime.now(timezone.utc)
    todays_date = utc_time.date().strftime('%d-%m-%Y')

    # check if today is a thursday and if a reset has already occurred for this week
    if utc_time.weekday() == 3 and user['usr'].boss_crystal_reset != todays_date:
        user['usr'].boss_crystal_reset = todays_date
        user['usr'].boss_crystal_count = 180
        user['usr'].boss_crystal_sold = 0

        # update user save file
        json_object = json.dumps(user, indent=4, default=custom_serializer)

        with open(usr_filename, 'w') as outfile:
            outfile.write(json_object)

# // orange functions // 
# open weblink
def open_hotlink(hotlink):
    webbrowser.open(hotlink)

# editing hotlinks
def edit_hotlinks():

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

    ehl_win = tk.Toplevel(orange_frame, bg='#fef2be')
    ehl_win.title('Edit Hotlinks')
    ehl_win.geometry('500x200+900+350')
    ehl_win.resizable(False, False)

    ehl_hotlinks_title_lbl = tk.Label(ehl_win, text='Edit Hot Links', font=('Kozuka Gothic Pro B', 12), bg='#fef2be')
    ehl_first_hotlink_lbl = tk.Label(ehl_win, text='Hot Link 1:', font=('Kozuka Gothic Pro B', 12), bg='#fef2be')
    ehl_first_hotlink_entry = tk.Entry(ehl_win, textvariable=first_hotlink, font=('Kozuka Gothic Pro B', 12))
    ehl_second_hotlink_lbl = tk.Label(ehl_win, text='Hot Link 2:', font=('Kozuka Gothic Pro B', 12), bg='#fef2be')
    ehl_second_hotlink_entry = tk.Entry(ehl_win, textvariable=second_hotlink, font=('Kozuka Gothic Pro B', 12))
    ehl_third_hotlink_lbl = tk.Label(ehl_win, text='Hot Link 3:', font=('Kozuka Gothic Pro B', 12), bg='#fef2be')
    ehl_third_hotlink_entry = tk.Entry(ehl_win, textvariable=third_hotlink, font=('Kozuka Gothic Pro B', 12))
    ehl_edit_btn = tk.Button(ehl_win, text='Save Edit', font=('Kozuka Gothic Pro B', 12), command=save_edit)

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
reset_boss_crystals()

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

bc_remaining_lbl = tk.Label(purple_frame, text=f'Boss Cyrstals Remaining: {user['usr'].boss_crystal_count - user['usr'].boss_crystal_sold}', font=('Kozuka Gothic Pro B', 12), bg='magenta')
bc_sold_lbl = tk.Label(purple_frame, text=f'Boss Crystals Sold: {user['usr'].boss_crystal_sold}', font=('Kozuka Gothic Pro B', 12), bg='magenta')
wm_gained_lbl = tk.Label(purple_frame, text=f'Weekly Mesos Gained: {user['usr'].weekly_mesos_gained}', font=('Kozuka Gothic Pro B', 12), bg='magenta')

mesos_balance_title_lbl.place(x=0, y=10, width=500, height=30)
mesos_balance_display_lbl.place(x=0, y=30, width=500, height=30)
add_mesos_btn.place(x=70, y=60, width=150, height=30)
remove_mesos_btn.place(x=280, y=60, width=150, height=30)

bc_remaining_lbl.place(x=25, y=110, width=250, height=30)
bc_sold_lbl.place(x=0, y=155, width=250, height=30)
wm_gained_lbl.place(x=15, y=200, width=250, height=30)

# // orange //
# orange widgets
hotlink_one_btn = tk.Button(orange_frame, text='Hot Link 1', font=('Kozuka Gothic Pro B', 12), command=lambda:open_hotlink(user['usr'].hotlink_one))
hotlink_two_btn = tk.Button(orange_frame, text='Hot Link 2', font=('Kozuka Gothic Pro B', 12), command=lambda:open_hotlink(user['usr'].hotlink_two))
hotlink_three_btn = tk.Button(orange_frame, text='Hot Link 3', font=('Kozuka Gothic Pro B', 12), command=lambda:open_hotlink(user['usr'].hotlink_three))
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

# SELF-NOTES (What's on the agenda for next session):
# Updating UI + functionality of bossing checklist
# ----> dropdown to choose party size 1-6
# ----> dropdown to choose difficulty level (easy, normal, hard, extreme)
# ----> revamp UI to include boss img
# ----> revamp UI to be less skinny, more full and wholesome

# UPDATED NOTES FOR NEXT SESSION (prev left, cos could be useful)
# 1. obtain boss images with transparent backgrounds
# 2. implement weekly mesos gained counter
# 2.1 implement reset validation and feature for weekly mesos gained 
# 2.1.1 this could potentially be achieved by utilising the weekly_boss_crystal_reset function... 
#       - just clear the weekly_mesos_gained value if its a new thursday (weekly reset)
# 3. update bosses difficulties
# 3.1 those with multiple difficulties that are viable as weekly clears
# 3.2 those with singular difficulty that are viable as weekly clears
# 3.3 create relevant dictionary/list of difficulties to attach to relevant boss (i.e singulars wont have a dropdown, some will have easy to hard, some will have easy to extreme)
# 4. find out and attach prices to each bosses incl difficulty price adjustments
# 5. do the maths for different received boss crystal price based on party size

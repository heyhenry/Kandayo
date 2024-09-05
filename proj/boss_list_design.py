import tkinter as tk


root = tk.Tk()

difficulties = [
    'Easy',
    'Normal',
    'Hard'
]

party_size = [
    '1',
    '2',
    '3',
    '4',
    '5',
    '6'
]

def prnt_difficulty(prnt):
    print(prnt)   

difficulty_choice = tk.StringVar()
party_size_choice = tk.StringVar()

difficulty_choice.set('Select Difficulty')
party_size_choice.set('Select Party Size')

boss_name = tk.Label(root, text='Golden Circle')
boss_img = tk.Label(root, text='IMG HERE')
boss_difficulty = tk.OptionMenu(root, difficulty_choice, *difficulties, command=lambda prnt: prnt_difficulty(difficulty_choice.get()))
boss_party_size = tk.OptionMenu(root, party_size_choice, *party_size)
boss_clear_status = tk.Checkbutton(root)

boss_name.grid(row=0, column=0, padx=5, pady=5)
boss_img.grid(row=1, column=0, padx=5, pady=5)
boss_difficulty.grid(row=2, column=0, padx=5, pady=5)
boss_party_size.grid(row=3, column=0, padx=5, pady=5)
boss_clear_status.grid(row=4, column=0, padx=5, pady=5)

a_difficulty_choice = tk.StringVar()
a_party_size_choice = tk.StringVar()

a_difficulty_choice.set('Select Difficulty')
a_party_size_choice.set('Select Party Size')

a_boss_name = tk.Label(root, text='Golden Circle')
a_boss_img = tk.Label(root, text='IMG HERE')
a_boss_difficulty = tk.OptionMenu(root, a_difficulty_choice, *difficulties, command=lambda prnt: prnt_difficulty(difficulty_choice.get()))
a_boss_party_size = tk.OptionMenu(root, a_party_size_choice, *party_size)
a_boss_clear_status = tk.Checkbutton(root)

a_boss_name.grid(row=0, column=1, padx=5, pady=5)
a_boss_img.grid(row=1, column=1, padx=5, pady=5)
a_boss_difficulty.grid(row=2, column=1, padx=5, pady=5)
a_boss_party_size.grid(row=3, column=1, padx=5, pady=5)
a_boss_clear_status.grid(row=4, column=1, padx=5, pady=5)

b_difficulty_choice = tk.StringVar()
b_party_size_choice = tk.StringVar()

b_difficulty_choice.set('Select Difficulty')
b_party_size_choice.set('Select Party Size')

b_boss_name = tk.Label(root, text='Golden Circle')
b_boss_img = tk.Label(root, text='IMG HERE')
b_boss_difficulty = tk.OptionMenu(root, b_difficulty_choice, *difficulties, command=lambda prnt: prnt_difficulty(difficulty_choice.get()))
b_boss_party_size = tk.OptionMenu(root, b_party_size_choice, *party_size)
b_boss_clear_status = tk.Checkbutton(root)

b_boss_name.grid(row=0, column=2, padx=5, pady=5)
b_boss_img.grid(row=1, column=2, padx=5, pady=5)
b_boss_difficulty.grid(row=2, column=2, padx=5, pady=5)
b_boss_party_size.grid(row=3, column=2, padx=5, pady=5)
b_boss_clear_status.grid(row=4, column=2, padx=5, pady=5)

c_difficulty_choice = tk.StringVar()
c_party_size_choice = tk.StringVar()

c_difficulty_choice.set('Select Difficulty')
c_party_size_choice.set('Select Party Size')

c_boss_name = tk.Label(root, text='Golden Circle')
c_boss_img = tk.Label(root, text='IMG HERE')
c_boss_difficulty = tk.OptionMenu(root, c_difficulty_choice, *difficulties, command=lambda prnt: prnt_difficulty(difficulty_choice.get()))
c_boss_party_size = tk.OptionMenu(root, c_party_size_choice, *party_size)
c_boss_clear_status = tk.Checkbutton(root)

c_boss_name.grid(row=5, column=1, padx=5, pady=5)
c_boss_img.grid(row=6, column=1, padx=5, pady=5)
c_boss_difficulty.grid(row=7, column=1, padx=5, pady=5)
c_boss_party_size.grid(row=8, column=1, padx=5, pady=5)
c_boss_clear_status.grid(row=9, column=1, padx=5, pady=5)

root.mainloop()
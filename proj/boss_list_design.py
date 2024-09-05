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

difficulty_choice = tk.StringVar()
party_size_choice = tk.StringVar()

difficulty_choice.set('Select Difficulty')
party_size_choice.set('Select Party Size')

boss_name = tk.Label(root, text='Golden Circle')
boss_img = tk.Label(root, text='IMG HERE')
boss_difficulty = tk.OptionMenu(root, difficulty_choice, *difficulties)
boss_party_size = tk.OptionMenu(root, party_size_choice, *party_size)
boss_clear_status = tk.Checkbutton(root)

boss_name.pack()
boss_img.pack()
boss_difficulty.pack()
boss_party_size.pack()
boss_clear_status.pack()

root.mainloop()
from kingdom import Kingdom
import tkinter as tk
import json

terra = Kingdom('Terra', 'Large', 'Grey')
kupo = Kingdom('Kupo', 'Medium', 'Blue')

kingdoms = {}
savefile = 'kingdom_save.json'

# json handling
def custom_serialization(obj : object):
    if isinstance(obj, Kingdom):
        return {
            'Castle Name': obj.castle_name,
            'Castle Size': obj.castle_size,
            'Castle Colour': obj.castle_colour
        }
    return obj

def update_savefile():

    json_object = json.dumps(kingdoms, indent=4, default=custom_serialization)

    with open(savefile, 'w') as outfile:
        outfile.write(json_object)

def load_savefile():

    with open(savefile, 'r') as file:
        json_data = json.load(file)

    # print(json_data)

    for kingdom_name, kingdom_info in json_data.items():
        kingdoms[kingdom_name] = Kingdom(kingdom_info['Castle Name'], kingdom_info['Castle Size'], kingdom_info['Castle Colour'])


    # print(kingdoms)
    
    # for k, v in kingdoms.items():
        # print(vars(v))

# kingdom handling
def create_kingdom(name, size, colour):
    
    new_kingdom = Kingdom(name, size, colour)
    kingdoms[name] = new_kingdom

    # print(kingdoms)

    update_savefile()


root = tk.Tk()
root.title('Kingdom Stories')
root.geometry('300x250+600+150')

kingdom_title = tk.Label(root, text='Kingdom Stories')
kingdom_title.grid(row=0, columnspan=2)

kingdom_listbox = tk.Listbox(root)
kingdom_listbox.grid(rowspan=2, column=0)

def create_kingdom_popup():

    ckp_name = tk.StringVar()
    ckp_size = tk.StringVar()
    ckp_colour = tk.StringVar()

    ckp = tk.Toplevel(root)
    ckp.title('Create a Kingdom')
    ckp.geometry('300x250+600+150')

    kingdom_title_lbl = tk.Label(ckp, text='Create a Kingdom')
    kingdom_title_lbl.grid(row=0, columnspan=2)

    kingdom_name_lbl = tk.Label(ckp, text='Kingdom Name:')
    kingdom_name_entry = tk.Entry(ckp, textvariable=ckp_name)
    kingdom_name_lbl.grid(row=1, column=0)
    kingdom_name_entry.grid(row=1, column=1)

    kingdom_size_lbl = tk.Label(ckp, text='Kingdom Size:')
    kingdom_size_entry = tk.Entry(ckp, textvariable=ckp_size)
    kingdom_size_lbl.grid(row=2, column=0)
    kingdom_size_entry.grid(row=2, column=1)

    kingdom_colour_lbl = tk.Label(ckp, text='Kingdom Colour:')
    kingdom_colour_entry = tk.Entry(ckp, textvariable=ckp_colour)
    kingdom_colour_lbl.grid(row=3, column=0)
    kingdom_colour_entry.grid(row=3, column=1)

    kingdom_create_btn = tk.Button(ckp, text='Create Kingdom', command=lambda:create_kingdom(ckp_name.get(), ckp_size.get(), ckp_colour.get()))
    kingdom_cancel_btn = tk.Button(ckp, text='Cancel', command=lambda:ckp.destroy())
    kingdom_create_btn.grid(row=4, column=0)
    kingdom_cancel_btn.grid(row=4, column=1)

    ckp.grid_rowconfigure(0, weight=1)
    ckp.grid_rowconfigure(1, weight=1)
    ckp.grid_rowconfigure(2, weight=1)
    ckp.grid_rowconfigure(3, weight=1)
    ckp.grid_rowconfigure(4, weight=1)
    ckp.grid_columnconfigure(0, weight=1)
    ckp.grid_columnconfigure(1, weight=1)


kingdom_create_btn = tk.Button(root, text='Create a Kingdom', command=create_kingdom_popup)
kingdom_create_btn.grid(row=1, column=1)
kingdom_update_btn = tk.Button(root, text='Update a Kingdom')
kingdom_update_btn.grid(row=2, column=1)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

load_savefile()

root.mainloop()
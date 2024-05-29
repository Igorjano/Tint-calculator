from tkinter import *
from tkinter import ttk
from tkinter import Radiobutton
from tkinter import messagebox

from PIL import Image, ImageTk
from collections import defaultdict


def set_tint_num(*arg):
    """
    Retrieves the selected value from the tint Combobox, creates Entry widgets for tints and volumes based on that
    value, and places them on the root window. Disables the tint Combobox to prevent further changes.

    Parameters:
    *arg: Optional arguments for cbx work
    """

    start_point = 100
    quantity_of_tints = int(tint_cbx.get())

    for i in range(quantity_of_tints):
        labels_dict['tints_entries'].append(Entry(root, width=5, justify=CENTER, font=('Arial', 10)))
        labels_dict['tints_entries'][i].place(x=102, y=start_point)
        labels_dict['base_dose_entries'].append(Entry(root, width=7, justify=CENTER, font=('Arial', 10)))
        labels_dict['base_dose_entries'][i].place(x=200, y=start_point)
        start_point += 25

    tint_cbx['state'] = 'disabled'


def calculate():
    """
    Calculates the values for each tint based on the input dose amount and updates the UI accordingly.

    Raises:
    ValueError: If invalid input values are entered.
    """

    if result_dict:
        result_dict.clear()
    try:
        dose_amount = float(volume_ent.get())
        for i in range(len(labels_dict['tints_entries'])):
            tint_name = labels_dict['tints_entries'][i].get().upper()
            labels_dict['tints_entries'][i]["state"] = 'disabled'
            tint_volume = float(labels_dict['base_dose_entries'][i].get())

            value = round(tint_volume * dose_amount, 2)

            result_dict[tint_name].append(value)
            result_dict[tint_name].append([])

            y_value, black_scale, red_scale = calculate_result_by_scales(value)

            result_dict[tint_name][1].append(y_value)
            result_dict[tint_name][1].append(black_scale)
            result_dict[tint_name][1].append(red_scale)

    except ValueError:
        messagebox.showinfo("ERROR", "You enter wrong values!")

    ounce_384["state"] = "normal"
    ounce_Y["state"] = "normal"
    print_tints()

    print_ounce_384() if ounce.get() else print_ounce_y()


def calculate_result_by_scales(value):
    """
    Calculates the result by scales based on the input value.

    Parameters:
    value (float): The input value to be calculated.

    Returns:
    tuple: A tuple containing Y value, value on black scale, and red scale values.
    """

    y = "--"
    black = "--"

    # Y value is 48 black scale values and 384 red scale values
    # 10 values on black scale is 80 red scale values
    # 1 value on black scale is 8 red scale values
    if value >= 384:
        y = int(value // 384)
        black = int(value % 384)

        if black < 80:
            red, black = black, "--"
        else:
            black = int((value % 384) // 8)
            red = int(value % 8)
    elif 384 > value >= 80:
        black = int(value // 8)
        red = int(value % 8)
    else:
        red = int(value)

    # The values on scales should be even numbers only
    if black != "--" and black % 2 != 0:
        black -= 1
        red += 8
    if red == 0:
        red = "--"

    return y, black, red


def print_tints():
    """
    Prints tints with background accordingly to its color and updates the UI with the calculated results.

    Raises:
    KeyError: If invalid tint names are entered.
    """

    start_point = 260
    if labels_dict['tints_labels']:
        clear_result_labels()

    try:
        for i, tint_name in enumerate(result_dict.keys()):
            labels_dict['tints_labels'].append(Label(root, text=tint_name,
                                                     justify=CENTER,
                                                     width=5,
                                                     fg=tints_attributes[tint_name][1],
                                                     bg=tints_attributes[tint_name][0]))

            labels_dict['tints_labels'][i].place(x=102, y=start_point)
            start_point += 25

    except KeyError:
        messagebox.showinfo("ERROR", "You enter wrong tint names!")


def print_ounce_384():
    """
    Prints the calculated results in the "Ounce 384" (red scale) format and updates the UI.
    """

    clear_result_labels()
    start_point = 260

    for i, dose in enumerate(result_dict.values()):
        labels_dict['dose_labels'].append(Label(root, text=dose[0], width=7, justify=CENTER, font=("Arial", 10)))
        labels_dict['dose_labels'][i].place(x=200, y=start_point)
        start_point += 25


def print_ounce_y():
    """Prints the calculated results in the "Ounce Y/48/384" (by scales) format and updates the UI."""

    clear_result_labels()
    start_point_y = 260

    for i, values in enumerate(result_dict.values()):
        labels_dict['dose_labels_by_scales'].append([])
        start_point_x = 170

        for j, value in enumerate(values[1]):
            labels_dict['dose_labels_by_scales'][i].append(Label(root, text=value,
                                                             width=7,
                                                             justify=CENTER,
                                                             font=("Arial", 10)))

            labels_dict['dose_labels_by_scales'][i][j].place(x=start_point_x, y=start_point_y)

            start_point_x += 40
        start_point_y += 25


def clear_labels(labels_list):
    """
    Clears the labels from the provided labels list.

    Parameters:
    labels_list (list): The list of labels to be cleared.
    """

    for label in labels_list:
        label.destroy()
    labels_list.clear()


def clear_result_labels():
    """Clears the result labels (calculation) from the UI."""

    clear_labels(labels_dict['dose_labels'])
    [clear_labels(label) for label in labels_dict['dose_labels_by_scales']]
    labels_dict['dose_labels_by_scales'].clear()


def clear_all_labels():
    """Clears all labels from the UI and resets the input fields and controls."""

    clear_result_labels()
    [clear_labels(labels_list) for labels_list in labels_dict.values()]
    volume_ent.delete(0, END)
    ounce_384["state"] = "disabled"
    ounce_Y["state"] = "disabled"
    tint_cbx["state"] = "enabled"
    ounce.set(True)


root = Tk()
root.resizable(False, False)
root.title('Tint Calculator for CABO Manual Tinting Machine')
root.iconbitmap('favicon.ico')

WIDTH = 500
HEIGHT = 500
POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

labels_dict = defaultdict(list)
result_dict = defaultdict(list)

tints_amount = ('1', '2', '3', '4')
tints_attributes = {'WS': ['#666633', '#FFFFFF'], 'XS': ['#000000', '#FFFFFF'], 'JS': ['#000000', '#FFFFFF'],
                    'YS': ['#993300', '#FFFFFF'], 'TS': ['#DAA520', '#FFFFFF'], 'OS': ['#FFFFFF', '#000000'],
                    'VS': ['#B22222', '#FFFFFF'], 'YE': ['#FFFF00', '#000000'], 'BS': ['#800080', '#FFFFFF'],
                    'ZS': ["#4B0082", '#FFFFFF'], 'RS': ['#1E90FF', '#FFFFFF'], 'PT': ['#FF0000', '#FFFFFF'],
                    'GL': ["#FFD700", '#FFFFFF'], 'LS': ['#0000CD', '#FFFFFF'], 'PS': ['#40E0D0', '#FFFFFF'],
                    'US': ["#FF8C00", '#FFFFFF']}

Label(text='Enter values for the calculation', font=('Arial', 12)).place(x=145, y=20)
Label(text='Tint           ', font=('Arial', 10)).place(x=70, y=60)
Label(text='Amount for 1 l(kg)', font=('Arial', 10)).place(x=190, y=60)
Label(text='Dosage for           l(kg)', font=('Arial', 10)).place(x=180, y=210)

tint_cbx = ttk.Combobox(root, width=2, values=tints_amount, textvariable=IntVar(), font=('Arial', 10))
tint_cbx['state'] = 'readonly'
tint_cbx.place(x=102, y=60)
tint_cbx.current(0)
tint_cbx.bind("<<ComboboxSelected>>", set_tint_num)

volume_ent = Entry(width=4, justify=CENTER, font=("Arial", 10))
volume_ent.place(x=250, y=210)

calc_btn = Button(text='Calculate', font=('Arial', 9), width=10)
calc_btn['command'] = calculate
calc_btn.bind('<Return>', lambda e: calculate())
calc_btn.place(x=340, y=105)

clear_btn = Button(text='Clear', font=('Arial', 9), width=10)
clear_btn['command'] = clear_all_labels
clear_btn.bind('<Return>', lambda e: clear_all_labels())
clear_btn.place(x=340, y=145)

ounce = BooleanVar()
ounce.set(True)
ounce_384 = Radiobutton(text='Ounce 384', font=('Arial', 9), variable=ounce, value=True)
ounce_384['command'] = print_ounce_384
ounce_384.place(x=335, y=260)
ounce_384['state'] = 'disabled'
ounce_Y = Radiobutton(text='Ounce Y/48/384', font=('Arial', 9), variable=ounce, value=False)
ounce_Y['command'] = print_ounce_y
ounce_Y.place(x=335, y=290)
ounce_Y['state'] = 'disabled'

image = Image.open('Cabo.jpg')
resized_image = image.resize((190, 190))
img = ImageTk.PhotoImage(resized_image)
Label(root, image=img).place(x=310, y=320)

root.mainloop()


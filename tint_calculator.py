from collections import defaultdict
from tkinter import *
from tkinter import Radiobutton, messagebox, ttk

from PIL import Image, ImageTk


class TintCalculator:
    def __init__(self):
        # self.tints_entries = []
        # self.base_dose_entries = []
        # self.tints_labels = []
        # self.dose_labels = []
        self.labels = defaultdict(list)
        # self.dose_labels_by_scales = []
        self.result = defaultdict(list)

        self.tint_cbx = ttk.Combobox(root, width=2, values=tints_amount, textvariable=IntVar(), font=("Arial", 10))
        self.tint_cbx['state'] = 'readonly'
        self.tint_cbx.place(x=102, y=60)
        self.tint_cbx.current(0)
        self.tint_cbx.bind("<<ComboboxSelected>>", self.set_tint_num)

        self.dose_amt = Entry(width=4, justify=CENTER, font=("Arial", 10))
        self.dose_amt.place(x=250, y=210)

        self.calc_btn = Button(text="Calculate", font=("Arial", 9), width=10)
        self.calc_btn["command"] = self.calculate
        self.calc_btn.bind('<Return>', lambda e: self.calculate())
        self.calc_btn.place(x=340, y=105)

        self.clear_btn = Button(text="Clear", font=("Arial", 9), width=10)
        self.clear_btn["command"] = self.clear_all_labels
        self.clear_btn.bind('<Return>', lambda e: self.clear_all_labels())
        self.clear_btn.place(x=340, y=145)

        self.ounce = BooleanVar()
        self.ounce.set(True)
        self.ounce_384 = Radiobutton(text="Ounce 384", font=("Arial", 9), variable=self.ounce, value=True)
        self.ounce_384["command"] = self.print_ounce_384
        self.ounce_384.place(x=335, y=260)
        self.ounce_384["state"] = "disabled"
        self.ounce_Y = Radiobutton(text="Ounce Y/48/384", font=("Arial", 9), variable=self.ounce, value=False)
        self.ounce_Y["command"] = self.print_ounce_y
        self.ounce_Y.place(x=335, y=290)
        self.ounce_Y["state"] = "disabled"

    def set_tint_num(self, *arg):
        """
        This method retrieves the selected value from the tint Combobox (self.tint_cbx),
        creates Entry widgets for tints and volumes based on that value, and places them on the root window.
        The tint Combobox is then disabled to prevent further changes.
        """

        st = 100
        quantity_of_tints = int(self.tint_cbx.get())
        for i in range(quantity_of_tints):
            self.labels['tints_entries'].append(Entry(root, width=5, justify=CENTER, font=("Arial", 10)))
            self.labels['tints_entries'][i].place(x=102, y=st)
            self.labels['base_dose_entries'].append(Entry(root, width=7, justify=CENTER, font=("Arial", 10)))
            self.labels['base_dose_entries'][i].place(x=200, y=st)
            st += 25
        print(self.result)
        self.tint_cbx["state"] = "disabled"

    def calculate(self):
        """
        Calculates the values for each tint and updates the UI accordingly.

        Raises:
        ValueError: If invalid input values are entered.
        """

        if self.result:
            self.result.clear()
        try:
            dose_amount = float(self.dose_amt.get())
            for i in range(len(self.labels['tints_entries'])):
                tint_name = self.labels['tints_entries'][i].get().upper()
                self.labels['tints_entries'][i]["state"] = 'disabled'
                tint_volume = float(self.labels['base_dose_entries'][i].get())

                res = round(tint_volume * dose_amount, 2)

                self.result[tint_name].append(res)
                self.result[tint_name].append([])

                y_value, black_scale, red_scale = self.calculate_result_by_scales(res)

                self.result[tint_name][1].append(y_value)
                self.result[tint_name][1].append(black_scale)
                self.result[tint_name][1].append(red_scale)
                print(self.result)

        except ValueError:
            messagebox.showinfo("ERROR", "You enter wrong values!")

        self.ounce_384["state"] = "normal"
        self.ounce_Y["state"] = "normal"
        self.print_tints()

        self.print_ounce_384() if self.ounce.get() else self.print_ounce_y()

    @staticmethod
    def calculate_result_by_scales(value):
        y = "--"
        black = "--"
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

        if black != "--" and black % 2 != 0:
            black -= 1
            red += 8
        if red == 0:
            red = "--"

        return y, black, red

    def print_tints(self):
        st = 260
        # if self.tints_labels:
        #     self.clear_result()

        try:
            print(self.result.keys())
            for i, tint_name in enumerate(self.result.keys()):
                self.labels['tints_labels'].append(Label(root, text=tint_name,
                                                     justify=CENTER,
                                                     width=5,
                                                     fg=tints_attributes[tint_name][1],
                                                     bg=tints_attributes[tint_name][0]))

                self.labels['tints_labels'][i].place(x=102, y=st)
                st += 25

        except KeyError:
            messagebox.showinfo("ERROR", "You enter wrong tint names!")

    @staticmethod
    def clear_labels(labels_list):
        for label in labels_list:
            label.destroy()
        labels_list.clear()

    def clear_all_labels(self):
        [self.clear_labels(labels_list) for labels_list in self.labels.values()]
        self.clear_result_labels()
        self.dose_amt.delete(0, END)
        self.ounce_384["state"] = "disabled"
        self.ounce_Y["state"] = "disabled"
        self.tint_cbx["state"] = "enabled"
        self.ounce.set(True)

    def clear_result_labels(self):
        self.clear_labels(self.labels['dose_labels'])
        [self.clear_labels(labels) for labels in self.labels['dose_labels_by_scales']]
        self.labels['dose_labels_by_scales'].clear()

    def print_ounce_384(self):
        self.clear_result_labels()
        start_point = 260

        for i, dose in enumerate(self.result.values()):
            self.labels['dose_labels'].append(Label(root, text=dose[0], width=7, justify=CENTER, font=("Arial", 10)))
            self.labels['dose_labels'][i].place(x=200, y=start_point)
            start_point += 25

    def print_ounce_y(self):
        self.clear_result_labels()
        start_point_y = 260

        for i, values in enumerate(self.result.values()):
            self.labels['dose_labels_by_scales'].append([])
            start_point_x = 170
            for j, value in enumerate(values[1]):
                self.labels['dose_labels_by_scales'][i].append(Label(root, text=value,
                                                                 width=7,
                                                                 justify=CENTER,
                                                                 font=("Arial", 10)))

                self.labels['dose_labels_by_scales'][i][j].place(x=start_point_x, y=start_point_y)

                start_point_x += 40
            start_point_y += 25
        print(self.labels)


if __name__ == '__main__':
    root = Tk()
    root.resizable(False, False)
    root.title("Tint Calculator for CABO Manual Tinting Machine")
    root.iconbitmap('favicon.ico')

    WIDTH = 500
    HEIGHT = 500
    POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
    POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2
    root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

    tints_amount = ('1', '2', '3', '4')
    tints_attributes = {"WS": ["#666633", "#FFFFFF"], "XS": ["#000000", "#FFFFFF"], "JS": ["#000000", "#FFFFFF"],
                 "YS": ["#993300", "#FFFFFF"], "TS": ["#DAA520", "#FFFFFF"], "OS": ["#FFFFFF", "#000000"],
                 "VS": ["#B22222", "#FFFFFF"], "YE": ["#FFFF00", "#000000"], "BS": ["#800080", "#FFFFFF"],
                 "ZS": ["#4B0082", "#FFFFFF"], "RS": ["#1E90FF", "#FFFFFF"], "PT": ["#FF0000", "#FFFFFF"],
                 "GL": ["#FFD700", "#FFFFFF"], "LS": ["#0000CD", "#FFFFFF"], "PS": ["#40E0D0", "#FFFFFF"],
                 "US": ["#FF8C00", "#FFFFFF"]}

    Label(text="Enter values for the calculation", font=("Arial", 12)).place(x=145, y=20)
    Label(text="Tint           ", font=("Arial", 10)).place(x=70, y=60)
    Label(text="Amount for 1 l(kg)", font=("Arial", 10)).place(x=190, y=60)
    Label(text="Dosage for           l(kg)", font=("Arial", 10)).place(x=180, y=210)

    image = Image.open('Cabo.jpg')
    resized_image = image.resize((190, 190))
    img = ImageTk.PhotoImage(resized_image)

    Label(root, image=img).place(x=310, y=320)

    calculator = TintCalculator()
    root.mainloop()

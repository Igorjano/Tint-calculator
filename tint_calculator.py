from tkinter import *
from tkinter import ttk
from tkinter import Radiobutton
from tkinter import messagebox
from collections import defaultdict


class TintCalculator:
    def __init__(self):
        self.tints_entries = []
        self.base_dose_entries = []
        self.tints_labels = []
        self.dose_labels = []
        self.dose_labels_Y = []
        self.tint_names = []
        self.result = []
        self.result_y = []
        self.tint_amt = ('1', '2', '3', '4')
        self.tints_atr = {"WS": ["#666633", "#FFFFFF"], "XS": ["#000000", "#FFFFFF"], "JS": ["#000000", "#FFFFFF"],
                          "YS": ["#993300", "#FFFFFF"], "TS": ["#DAA520", "#FFFFFF"], "OS": ["#FFFFFF", "#000000"],
                          "VS": ["#B22222", "#FFFFFF"], "YE": ["#FFFF00", "#000000"], "BS": ["#800080", "#FFFFFF"],
                          "ZS": ["#4B0082", "#FFFFFF"], "RS": ["#1E90FF", "#FFFFFF"], "PT": ["#FF0000", "#FFFFFF"],
                          "GL": ["#FFD700", "#FFFFFF"], "LS": ["#0000CD", "#FFFFFF"], "PS": ["#40E0D0", "#FFFFFF"],
                          "US": ["#FF8C00", "#FFFFFF"]}

        self.tint_cbx = ttk.Combobox(root, width=2, values=self.tint_amt, textvariable=IntVar(), font=("Arial", 10))
        self.tint_cbx['state'] = 'readonly'
        self.tint_cbx.place(x=102, y=60)
        self.tint_cbx.current(0)
        self.tint_cbx.bind("<<ComboboxSelected>>", self.set_tint_num)

        self.dose_amt = Entry(root, width=4, justify=CENTER, font=("Arial", 10))
        self.dose_amt.place(x=250, y=210)

        self.calc_btn = Button(root, text="Calculate", font=("Arial", 9), width=10)
        self.calc_btn["command"] = self.calculate
        self.calc_btn.bind('<Return>', lambda e: self.calculate())
        self.calc_btn.place(x=340, y=105)

        self.clear_btn = Button(root, text="Clear", font=("Arial", 9), width=10)
        self.clear_btn["command"] = self.clear_all
        self.clear_btn.bind('<Return>', lambda e: self.clear_all())
        self.clear_btn.place(x=340, y=145)

        self.ounce = BooleanVar()
        self.ounce.set(True)
        self.ounce_384 = Radiobutton(root, text="Ounce 384", font=("Arial", 9), variable=self.ounce, value=True)
        self.ounce_384["command"] = self.print_ounce_384
        self.ounce_384.place(x=335, y=260)
        self.ounce_384["state"] = "disabled"
        self.ounce_Y = Radiobutton(root, text="Ounce Y/48/384", font=("Arial", 9), variable=self.ounce, value=False)
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
        amt = int(self.tint_cbx.get())
        for i in range(amt):
            self.tints_entries.append(Entry(root, width=5, justify=CENTER, font=("Arial", 10)))
            self.tints_entries[i].place(x=102, y=st)
            self.base_dose_entries.append(Entry(root, width=7, justify=CENTER, font=("Arial", 10)))
            self.base_dose_entries[i].place(x=200, y=st)
            st += 25
        self.tint_cbx["state"] = "disabled"

    def calculate(self):
        """
        Calculates the values for each tint and updates the UI accordingly.

        Raises:
        ValueError: If invalid input values are entered.
        """

        if self.result:
            self.clear_labels(self.result)
        try:

            for i in range(len(self.tints_entries)):
                result = []
                # tint_name = self.tints_entries[i].get().upper()
                # self.tints_labels.append(tint_name)
                res = round(float(self.base_dose_entries[i].get()) * float(self.dose_amt.get()), 2)
                self.result.append(round(res, 2))

                y_value, black_scale, red_scale = self.calculate_y(res)

                result.append(y_value)
                result.append(black_scale)
                result.append(red_scale)
                self.result_y.append(result)

        except ValueError:
            messagebox.showinfo("ERROR", "You enter wrong values!")

        self.ounce_384["state"] = "normal"
        self.ounce_Y["state"] = "normal"
        self.print_ounce_384()

    @staticmethod
    def calculate_y(res):
        y = "--"
        b = "--"
        if res >= 384:
            y = int(res // 384)
            b = int(res % 384)
            if b < 80:
                r, b = b, "--"
            else:
                b = int((res % 384) // 8)
                r = int(res % 8)
        elif 384 > res >= 80:
            b = int(res // 8)
            r = int(res % 8)
        else:
            r = int(res)
        if b != "--" and b % 2 != 0:
            b -= 1
            r += 8
        if r == 0:
            r = "--"

        return y, b, r

    def print_tints(self):
        st = 250
        if self.tints_labels:
            self.clear_result()
        # try:
        for i in range(len(self.tints_entries)):
            tint_name = self.tints_entries[i].get().upper()
            self.tints_labels.append(Label(root, text=tint_name,
                                           justify=CENTER, width=5,
                                           fg=self.tints_atr[tint_name][1], bg=self.tints_atr[tint_name][0]))
            self.tints_labels[i].place(x=102, y=st)
            st += 25
        # except KeyError:
        #     messagebox.showinfo("ERROR", "You enter wrong tint names!")

    def clear_result(self):
        self.clear_labels(self.tints_labels)
        self.clear_labels(self.dose_labels)
        # self.clear_labels(self.dose_labels_y)

    @staticmethod
    def clear_labels(target):
        for tint in target:
            tint.destroy()
        target.clear()

    def clear_all(self):
        self.tints_entries.clear()
        self.base_dose_entries.clear()
        self.clear_result()
        self.dose_amt.delete(0, END)
        self.ounce_384["state"] = "disabled"
        self.ounce_Y["state"] = "disabled"
        self.tint_cbx["state"] = "enabled"

    def print_ounce_384(self):
        self.print_tints()
        st = 250
        for i in range(len(self.result)):
            self.dose_labels.append(Label(root, text=self.result[i], width=7, justify=CENTER, font=("Arial", 10)))
            self.dose_labels[i].place(x=200, y=st)
            st += 25

    def print_ounce_y(self):
        self.clear_result()
        self.print_tints()

        st_x = 170
        # result = list(self.result)
        # print(result)
        # print(len(result))
        # for tint in range(len(self.tints_entries)):
        #     tint_name = self.tints_entries[tint].get().upper()
        #     self.dose_labels_y[i][tint] =

        for i in range(len(self.result_y)):
            st_y = 250
            # print(values)
            for j in range(len(self.result_y[i])):
                self.dose_labels_Y[i].append(Label(root, text=self.result_y[i][j], width=7, justify=CENTER,
                                                   font=("Arial", 10)))
                print(self.dose_labels_y)
                self.dose_labels_Y[i][j].place(x=st_x, y=st_y)

                st_y += 25
            st_x += 40


if __name__ == '__main__':
    root = Tk()
    root.resizable(False, False)
    root.title("Tint Calculator for CABO Manual Tinting Machine")
    root.iconbitmap('favicon.ico')

    WIDTH = 500
    HEIGHT = 400
    POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
    POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2
    root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")

    Label(text="Enter values for the calculation", font=("Times new roman", 12)).place(x=145, y=20)
    Label(text="Tint           ", font=("Arial", 10)).place(x=70, y=60)
    Label(text="Amount for 1 l(kg)", font=("Arial", 10)).place(x=190, y=60)
    Label(text="Dosage for           l(kg)", font=("Arial", 10)).place(x=180, y=210)

    img1 = PhotoImage('D:\Программы\Cabo-Color-Dettaglio-Tintometro-manuale 2.jpg')

    img2 = PhotoImage('D:\Программы\Cabo-Color-Dettaglio-Tintometro-manuale 2.jpg')
    img3 = PhotoImage('D:\Программы\Cabo-Color-Dettaglio-Tintometro-manuale 2.jpg')

    Label(image=img1, text='dfdfdf', width=25, height=25).place(x=350, y = 20)

    calculator = TintCalculator()
    root.mainloop()

from tkinter import *
from tkinter import ttk
from tkinter import Radiobutton
from tkinter import messagebox


class TintCalculator:
    def __init__(self):
        self.tints_entries = []
        self.base_dose_entries = []
        self.tints_labels = []
        self.dose_labels = []
        self.dose_labels_by_scales = []
        self.tint_names = []
        self.result = []
        self.result_by_scales = []
        self.result_description_labels = []
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

        self.create_result_description_labels()

        if self.result:
            self.result.clear()
            self.result_by_scales.clear()
        try:

            for i in range(len(self.tints_entries)):
                result = []
                res = round(float(self.base_dose_entries[i].get()) * float(self.dose_amt.get()), 2)
                self.result.append(round(res, 2))

                y_value, black_scale, red_scale = self.calculate_scales_values(res)

                result.append(y_value)
                result.append(black_scale)
                result.append(red_scale)
                self.result_by_scales.append(result)

        except ValueError:
            messagebox.showinfo("ERROR", "You enter wrong values!")

        self.ounce_384["state"] = "normal"
        self.ounce_Y["state"] = "normal"

        if self.ounce.get():
            self.print_ounce_384()
        else:
            self.print_ounce_y()

    @staticmethod
    def calculate_scales_values(res):
        """

        :param res:
        :return:
        """

        y = "--"
        black = "--"
        # In this case we have Y value in black scale
        if res >= 384:
            y = int(res // 384)
            black = int(res % 384)
            if black < 80:
                red, black = black, "--"
            else:
                black = int((res % 384) // 8)
                red = int(res % 8)
        # We don't have Y values in black scale, only black scale values
        elif 384 > res >= 80:
            black = int(res // 8)
            red = int(res % 8)
        # We have values only on red scale
        else:
            red = int(res)

        if black != "--" and black % 2 != 0:
            black -= 1
            red += 8

        if red == 0:
            red = "--"

        return y, black, red

    def print_ounce_384(self):
        if self.dose_labels_by_scales:
            [self.clear_labels(label) for label in self.dose_labels_by_scales]
            self.dose_labels_by_scales.clear()
        self.print_tints()
        self.print_ounce_384_label()

        st = 270
        for i in range(len(self.result)):
            self.dose_labels.append(Label(root, text=self.result[i],
                                          width=7,
                                          justify=CENTER,
                                          font=("Arial", 10)))
            self.dose_labels[i].place(x=200, y=st)
            st += 25

    def print_ounce_y(self):
        if self.dose_labels:
            self.clear_labels(self.dose_labels)
        self.print_tints()

        st_y = 270
        for i in range(len(self.result_by_scales)):
            st_x = 170
            self.dose_labels_by_scales.append([])
            for j in range(len(self.result_by_scales[i])):
                self.dose_labels_by_scales[i].append(Label(root, text=self.result_by_scales[i][j],
                                                           width=7,
                                                           justify=CENTER,
                                                           font=("Arial", 10)))
                self.dose_labels_by_scales[i][j].place(x=st_x, y=st_y)
                st_x += 40
            st_y += 25

    def create_result_description_labels(self):
        self.result_description_labels.append(Label(text="Y", font=("Times new roman bold", 10)))
        self.result_description_labels.append(Label(text=48, font=("Times new roman", 10)))
        self.result_description_labels.append(Label(text=384, font=("Times new roman", 11), fg='red'))

    def print_ounce_384_label(self):
        self.result_description_labels[2].place(x=213, y=240)

    def print_description_ounce_by_labels(self):
        pass

    def print_tints(self):
        st = 270
        if self.tints_labels:
            self.clear_result()

        try:
            for i in range(len(self.tints_entries)):
                tint_name = self.tints_entries[i].get().upper()
                self.tints_labels.append(Label(root, text=tint_name,
                                               justify=CENTER,
                                               width=5,
                                               fg=self.tints_atr[tint_name][1],
                                               bg=self.tints_atr[tint_name][0]))

                self.tints_labels[i].place(x=102, y=st)
                st += 25
        except KeyError:
            messagebox.showinfo("ERROR", "You enter wrong tint names!")

    def clear_result(self):
        self.clear_labels(self.tints_labels)
        self.clear_labels(self.dose_labels)
        [self.clear_labels(labels) for labels in self.dose_labels_by_scales]
        self.dose_labels_by_scales.clear()

    def clear_all(self):
        self.clear_result()
        self.clear_labels(self.tints_entries)
        self.clear_labels(self.base_dose_entries)
        self.dose_amt.delete(0, END)
        self.ounce_384["state"] = "disabled"
        self.ounce_Y["state"] = "disabled"
        self.tint_cbx["state"] = "enabled"

    @staticmethod
    def clear_labels(labels_list):
        for label in labels_list:
            label.destroy()
        labels_list.clear()


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

    Label(text="Enter values for the calculation", font=("Times new roman", 12)).place(x=145, y=20)
    Label(text="Tints           ", font=("Arial", 10)).place(x=65, y=60)
    Label(text="Amount for 1 l(kg)", font=("Arial", 10)).place(x=190, y=60)
    Label(text="Dosage for           l(kg)", font=("Arial", 10)).place(x=180, y=210)

    img1 = PhotoImage('D:\Программы\Cabo-Color-Dettaglio-Tintometro-manuale 2.jpg')

    img2 = PhotoImage('D:\Программы\Cabo-Color-Dettaglio-Tintometro-manuale 2.jpg')
    img3 = PhotoImage('D:\Программы\Cabo-Color-Dettaglio-Tintometro-manuale 2.jpg')

    Label(image=img1, text='dfdfdf', width=25, height=25).place(x=350, y = 20)

    calculator = TintCalculator()
    root.mainloop()

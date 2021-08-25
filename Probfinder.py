import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from pathlib import Path
import json
from Probfinder_modules import Calc_module


class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x700")
        self.root.title('PF1e calculator')
        self.root.resizable()

        self.character1 = None
        self.character2 = None

        UIframe = tk.Frame(self.root)
        leftframe = tk.Frame(UIframe)
        rightframe = tk.Frame(UIframe)
        plotframe = tk.Frame(rightframe)
        infoframe = tk.Frame(rightframe)
        statusframe = tk.Frame(self.root)
        UIframe.pack(expand=1, fill="both", side=tk.TOP)
        statusframe.pack(expand=1, fill="both", side=tk.BOTTOM)
        leftframe.pack(expand=1, fill="both", side=tk.LEFT)
        rightframe.pack(expand=1, fill="both", side=tk.RIGHT)
        plotframe.pack(expand=1, fill="both", side=tk.LEFT)
        infoframe.pack(expand=1, fill="both", side=tk.RIGHT)

        # ------ Left frame ------
        lefttop, leftbot = tk.Frame(leftframe), tk.Frame(leftframe)
        lefttop.pack(expand=1, fill="both", side=tk.TOP)
        leftbot.pack(expand=1, fill="both", side=tk.BOTTOM)
        leftleft, leftright = tk.Frame(lefttop), tk.Frame(lefttop)
        leftleft.pack(expand=1, fill="both", side=tk.LEFT)
        leftright.pack(expand=1, fill="both", side=tk.RIGHT)
        
        def input_fields(master, char):
            tk.Label(master, text="Character name").pack()
            name_entry = tk.Entry(master)
            name_entry.pack(expand=1, fill='x')
            tk.Label(master, text="HP").pack()
            HP_entry = tk.Entry(master)
            HP_entry.pack(expand=1, fill='x')
            tk.Label(master, text="Armor class").pack()
            AC_entry = tk.Entry(master)
            AC_entry.pack(expand=1, fill='x')
            tk.Label(master, text="To hit bonus").pack()
            TH_entry = tk.Entry(master)
            TH_entry.pack(expand=1, fill='x')
            tk.Label(master, text="Damage dice").pack()
            dmg_entry = tk.Entry(master)
            dmg_entry.pack(expand=1, fill='x')
            tk.Label(master, text="Precision dice").pack()
            prec_entry = tk.Entry(master)
            prec_entry.pack(expand=1, fill='x')
            tk.Label(master, text="Damage bonus").pack()
            static_entry = tk.Entry(master)
            static_entry.pack(expand=1, fill='x')
            tk.Label(master, text="Crit thresh").pack()
            crit_entry = tk.Entry(master)
            crit_entry.pack(expand=1, fill='x')
            tk.Label(master, text="Crit multiplier").pack()
            mult_entry = tk.Entry(master)
            mult_entry.pack(expand=1, fill='x')
            set_btn = tk.Button(master, text='Set', height=2, command=lambda: self.validate_character(char))
            set_btn.pack(expand=1, fill='x')

            save_btn = tk.Button(master, text='Save', height=2, command=lambda: self.save_character(char))
            save_btn.pack(expand=1, fill='x')

            load_btn = tk.Button(master, text='Load', height=2, command=lambda: self.load_character(char))
            load_btn.pack(expand=1, fill='x')
            return [name_entry, HP_entry, AC_entry, TH_entry, dmg_entry, prec_entry, static_entry, crit_entry, mult_entry]

        self.char1_entries = input_fields(leftleft, 1)
        self.char2_entries = input_fields(leftright, 2)

        calc_btn = tk.Button(leftbot, text='Calculate', height=2, command=self.calculate)
        calc_btn.pack(expand=1, fill='x')

        sim_btn = tk.Button(leftbot, text='Simulate', height=2, command=self.simulate)
        sim_btn.pack(expand=1, fill='x')

        # ------ Plot frame ------

        tabControl = ttk.Notebook(plotframe)

        tabprob = ttk.Frame(tabControl)
        tabcum = ttk.Frame(tabControl)

        self.figprob = Figure(figsize=(4, 4), dpi=100)
        self.subplotprob = self.figprob.add_subplot(111)
        self.canvasprob = FigureCanvasTkAgg(self.figprob, master=tabprob)  # A tk.DrawingArea.

        self.toolbarprob = NavigationToolbar2Tk(self.canvasprob, tabprob)
        self.toolbarprob.update()
        self.canvasprob.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.figcum = Figure(figsize=(4, 4), dpi=100)
        self.subplotcum = self.figcum.add_subplot(111)
        self.canvascum = FigureCanvasTkAgg(self.figcum, master=tabcum)  # A tk.DrawingArea.

        self.toolbarcum = NavigationToolbar2Tk(self.canvascum, tabcum)
        self.toolbarcum.update()
        self.canvascum.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        tabControl.add(tabprob, text='Density')
        tabControl.add(tabcum, text='Cumulative')
        tabControl.pack(expand=1, fill="both")

        # ------ Info frame ------
        self.expval_label_var = tk.StringVar()
        self.expval_label_var.set('Expected values: N/A, N/A')
        self.expval_label = ttk.Label(infoframe, textvariable=self.expval_label_var)
        self.expval_label.config(width=30, font=("Courier", 10))
        self.expval_label.pack(side=tk.TOP, expand=1, fill='x')
        
        self.highest_label_var = tk.StringVar()
        self.highest_label_var.set('Most probable turns: N/A, N/A')
        self.highest_label = ttk.Label(infoframe, textvariable=self.highest_label_var)
        self.highest_label.config(width=30, font=("Courier", 10))
        self.highest_label.pack(side=tk.TOP, expand=1, fill='x')
        
        self.hprob_label_var = tk.StringVar()
        self.hprob_label_var.set('Highest probability: N/A, N/A')
        self.hprob_label = ttk.Label(infoframe, textvariable=self.hprob_label_var)
        self.hprob_label.config(width=30, font=("Courier", 10))
        self.hprob_label.pack(side=tk.TOP, expand=1, fill='x')
        
        self.cum25_label_var = tk.StringVar()
        self.cum25_label_var.set('25% finish threshold: N/A, N/A')
        self.cum25_label = ttk.Label(infoframe, textvariable=self.cum25_label_var)
        self.cum25_label.config(width=30, font=("Courier", 10))
        self.cum25_label.pack(side=tk.TOP, expand=1, fill='x')
        
        self.cum50_label_var = tk.StringVar()
        self.cum50_label_var.set('50% finish threshold: N/A, N/A')
        self.cum50_label = ttk.Label(infoframe, textvariable=self.cum50_label_var)
        self.cum50_label.config(width=30, font=("Courier", 10))
        self.cum50_label.pack(side=tk.TOP, expand=1, fill='x')
        
        self.cum75_label_var = tk.StringVar()
        self.cum75_label_var.set('75% finish threshold: N/A, N/A')
        self.cum75_label = ttk.Label(infoframe, textvariable=self.cum75_label_var)
        self.cum75_label.config(width=30, font=("Courier", 10))
        self.cum75_label.pack(side=tk.TOP, expand=1, fill='x')
        
        self.cum90_label_var = tk.StringVar()
        self.cum90_label_var.set('90% finish threshold: N/A, N/A')
        self.cum90_label = ttk.Label(infoframe, textvariable=self.cum90_label_var)
        self.cum90_label.config(width=30, font=("Courier", 10))
        self.cum90_label.pack(side=tk.TOP, expand=1, fill='x')

        # ------ Bottom frame ------
        self.status_label_var = tk.StringVar()
        self.status_label = ttk.Label(statusframe, textvariable=self.status_label_var, relief=tk.RAISED)
        self.status_label.config(width=200, font=("Courier", 15))
        self.status_label.pack(side=tk.TOP, expand=1, fill='both')

    def validate_character(self, char):
        if char == 1:
            entries = self.char1_entries
        else:
            entries = self.char2_entries
        field_names = ['Name', 'HP', 'AC', 'To hit', 'Damage dice', 'Precision dice', 'Damage bonus', 'Critical thresh', 'Critical multiplier']
        fields = []
        for i, entry in enumerate(entries):
            val = entry.get()
            if len(val) == 0:
                if i == 5:
                    continue
                self.status_label_var.set(f'Field {field_names[i]} is not set!')
                return 0
        fields.append(entries[0].get())
        for i in range(1, 4):
            try:
                fields.append(int(entries[i].get()))
            except ValueError:
                self.status_label_var.set(f'Error in {field_names[i]} field: {entries[i].get()}')
                return 0
        dmg_dice = []
        dmg_string = entries[4].get()
        if 'd' not in dmg_string:
            self.status_label_var.set('Error in damage dice field: Use XdY notation')
            return 0
        dmg = dmg_string.split('+')
        for d in dmg:
            try:
                num, faces = d.split('d')
                dmg_dice.append((int(num), int(faces)))
            except ValueError:
                self.status_label_var.set(f'Error in damage dice field: {d} incorrect')
                return 0
        fields.append(dmg_dice)
        prec_dice = []
        prec_string = entries[5].get()
        if len(prec_string) != 0:
            if 'd' not in prec_string:
                self.status_label_var.set('Error in precision dice field: Use XdY notation')
                return 0
            prec = prec_string.split('+')
            for p in prec:
                try:
                    num, faces = p.split('d')
                    prec_dice.append((int(num), int(faces)))
                except ValueError:
                    self.status_label_var.set(f'Error in damage dice field: {p} incorrect')
                    return 0
        fields.append(prec_dice)
        for i in range(6, 9):
            try:
                fields.append(int(entries[i].get()))
            except ValueError:
                self.status_label_var.set(f'Error in {field_names[i]} field: {entries[i].get()}')
                return 0

        dictionary = {}
        for fn, val in zip(field_names, fields):
            dictionary[fn] = val
        if char == 1:
            self.character1 = dictionary
        else:
            self.character2 = dictionary
        self.status_label_var.set(f'Character {char} set')
        return 1

    def save_character(self, char):
        Path('Characters').mkdir(parents=True, exist_ok=True)
        if char == 1:
            if self.character1 is None:
                if not self.validate_character(char):
                    return
            with open(f'Characters/{self.character1["Name"]}.json', 'w') as outfile:
                json.dump(self.character1, outfile)
        else:
            if self.character2 is None:
                if not self.validate_character(char):
                    return
            with open(f'Characters/{self.character2["Name"]}.json', 'w') as outfile:
                json.dump(self.character2, outfile)
        self.status_label_var.set(f'Character {char} saved')

    def load_character(self, char):
        self.root.withdraw()
        file_selected = filedialog.askopenfile()
        if file_selected == '' or file_selected is None:
            self.status_label_var.set(f'Please select a file')
            self.root.deiconify()
            return
        if file_selected.name.endswith('.json'):
            dictionary = {}
            with open(file_selected.name, 'r') as file:
                dictionary = json.load(file)

            def convert_dice(dice):
                retstr = ""
                for (dn, df) in dice:
                    retstr += f"+{dn}d{df}"
                retstr = retstr[1:]
                return retstr

            vals = [str(dictionary['Name']),
                    str(dictionary['HP']),
                    str(dictionary['AC']),
                    str(dictionary['To hit']),
                    convert_dice(dictionary['Damage dice']),
                    convert_dice(dictionary['Precision dice']),
                    str(dictionary['Damage bonus']),
                    str(dictionary['Critical thresh']),
                    str(dictionary['Critical multiplier'])]
            if char == 1:
                self.character1 = dictionary
                for entry, v in zip(self.char1_entries, vals):
                    entry.delete(0, tk.END)
                    entry.insert(0, v)
            else:
                self.character2 = dictionary
                for entry, v in zip(self.char2_entries, vals):
                    entry.delete(0, tk.END)
                    entry.insert(0, v)

            self.root.deiconify()
        else:
            self.status_label_var.set(f'Please select a JSON file')
            self.root.deiconify()

    def update_plot(self, char1_turns, char1_ps, char2_turns, char2_ps):
        self.subplotprob.clear()
        self.subplotcum.clear()

        char1_cum, char2_cum = np.cumsum(char1_ps), np.cumsum(char2_ps)

        # Expected value:
        char1_expval = np.sum(np.multiply(char1_turns, char1_ps))
        char2_expval = np.sum(np.multiply(char2_turns, char2_ps))
        self.expval_label_var.set(f'Expected values: {char1_expval:.2f}, {char2_expval:.2f}')

        # Maximal value
        char1_max = np.argmax(char1_ps)
        char2_max = np.argmax(char2_ps)
        self.highest_label_var.set(f'Most probable turns: {char1_turns[char1_max]}, {char2_turns[char2_max]}')
        self.hprob_label_var.set(f'Highest probability: {char1_ps[char1_max]:.2f}, {char2_ps[char2_max]:.2f}')

        # Confidences
        char1_25, char2_25 = np.max(np.argmax(char1_cum[char1_cum <= 0.25])), np.max(
            np.argmax(char2_cum[char2_cum <= 0.25]))
        char1_50, char2_50 = np.max(np.argmax(char1_cum[char1_cum <= 0.50])), np.max(
            np.argmax(char2_cum[char2_cum <= 0.50]))
        char1_75, char2_75 = np.max(np.argmax(char1_cum[char1_cum <= 0.75])), np.max(
            np.argmax(char2_cum[char2_cum <= 0.75]))
        char1_90, char2_90 = np.max(np.argmax(char1_cum[char1_cum <= 0.90])), np.max(
            np.argmax(char2_cum[char2_cum <= 0.90]))

        self.cum25_label_var.set(f'25% finish threshold: {char1_turns[char1_25]}, {char2_turns[char2_25]}')
        self.cum50_label_var.set(f'50% finish threshold: {char1_turns[char1_50]}, {char2_turns[char2_50]}')
        self.cum75_label_var.set(f'75% finish threshold: {char1_turns[char1_75]}, {char2_turns[char2_75]}')
        self.cum90_label_var.set(f'90% finish threshold: {char1_turns[char1_90]}, {char2_turns[char2_90]}')

        self.subplotprob.plot(char1_turns, char1_ps)
        self.subplotprob.plot(char2_turns, char2_ps)

        self.subplotprob.fill_between(char1_turns[char1_90:], 0, char1_ps[char1_90:], facecolor='midnightblue',
                                      interpolate=True)
        self.subplotprob.fill_between(char1_turns[char1_75:char1_90 + 1], 0, char1_ps[char1_75:char1_90 + 1],
                                      facecolor='darkblue', interpolate=True)
        self.subplotprob.fill_between(char1_turns[char1_50:char1_75 + 1], 0, char1_ps[char1_50:char1_75 + 1],
                                      facecolor='blue', interpolate=True)
        self.subplotprob.fill_between(char1_turns[char1_25:char1_50 + 1], 0, char1_ps[char1_25:char1_50 + 1],
                                      facecolor='cornflowerblue', interpolate=True)
        self.subplotprob.fill_between(char1_turns[:char1_25 + 1], 0, char1_ps[:char1_25 + 1],
                                      facecolor='lightsteelblue', interpolate=True)

        self.subplotprob.fill_between(char2_turns[char2_90:], 0, char2_ps[char2_90:], facecolor='darkgoldenrod',
                                      interpolate=True)
        self.subplotprob.fill_between(char2_turns[char2_75:char2_90 + 1], 0, char2_ps[char2_75:char2_90 + 1],
                                      facecolor='goldenrod', interpolate=True)
        self.subplotprob.fill_between(char2_turns[char2_50:char2_75 + 1], 0, char2_ps[char2_50:char2_75 + 1],
                                      facecolor='gold', interpolate=True)
        self.subplotprob.fill_between(char2_turns[char2_25:char2_50 + 1], 0, char2_ps[char2_25:char2_50 + 1],
                                      facecolor='yellow', interpolate=True)
        self.subplotprob.fill_between(char2_turns[:char2_25 + 1], 0, char2_ps[0:char2_25 + 1],
                                      facecolor='palegoldenrod', interpolate=True)

        self.subplotprob.set_xlabel('Combat length (turns)')
        self.subplotprob.set_ylabel('Probability')
        self.subplotprob.set_title('Combat length probability')
        self.subplotprob.legend([self.character1['Name'], self.character2['Name']])
        self.canvasprob.draw()

        self.subplotcum.plot(char1_turns, char1_cum)
        self.subplotcum.plot(char2_turns, char2_cum)

        self.subplotcum.fill_between(char1_turns[char1_90:], 0, char1_cum[char1_90:], facecolor='midnightblue',
                                     interpolate=True)
        self.subplotcum.fill_between(char1_turns[char1_75:char1_90 + 1], 0, char1_cum[char1_75:char1_90 + 1],
                                     facecolor='darkblue', interpolate=True)
        self.subplotcum.fill_between(char1_turns[char1_50:char1_75 + 1], 0, char1_cum[char1_50:char1_75 + 1],
                                     facecolor='blue', interpolate=True)
        self.subplotcum.fill_between(char1_turns[char1_25:char1_50 + 1], 0, char1_cum[char1_25:char1_50 + 1],
                                     facecolor='cornflowerblue', interpolate=True)
        self.subplotcum.fill_between(char1_turns[:char1_25 + 1], 0, char1_cum[:char1_25 + 1],
                                     facecolor='lightsteelblue', interpolate=True)

        self.subplotcum.fill_between(char2_turns[char2_90:], 0, char2_cum[char2_90:], facecolor='darkgoldenrod',
                                     interpolate=True)
        self.subplotcum.fill_between(char2_turns[char2_75:char2_90 + 1], 0, char2_cum[char2_75:char2_90 + 1],
                                     facecolor='goldenrod', interpolate=True)
        self.subplotcum.fill_between(char2_turns[char2_50:char2_75 + 1], 0, char2_cum[char2_50:char2_75 + 1],
                                     facecolor='gold', interpolate=True)
        self.subplotcum.fill_between(char2_turns[char2_25:char2_50 + 1], 0, char2_cum[char2_25:char2_50 + 1],
                                     facecolor='yellow', interpolate=True)
        self.subplotcum.fill_between(char2_turns[:char2_25 + 1], 0, char2_cum[0:char2_25 + 1],
                                     facecolor='palegoldenrod', interpolate=True)

        self.subplotcum.set_xlabel('Combat length (turns)')
        self.subplotcum.set_ylabel('Probability')
        self.subplotcum.set_title('Cumulative probability')
        self.subplotcum.legend([self.character1['Name'], self.character2['Name']])
        self.canvascum.draw()

    def calculate(self):
        if self.character1 is not None and self.character2 is not None:
            HP1, HP2 = self.character2['HP'], self.character1['HP']
            AC1, AC2 = self.character2['AC'], self.character1['AC']
            TH1, TH2 = self.character1['To hit'], self.character2['To hit']
            dmg1, dmg2 = self.character1['Damage dice'], self.character2['Damage dice']
            prec1, prec2 = self.character1['Precision dice'], self.character2['Precision dice']
            static1, static2 = self.character1['Damage bonus'], self.character2['Damage bonus']
            cr_thresh1, cr_thresh2 = self.character1['Critical thresh'], self.character2['Critical thresh']
            cr_mul1, cr_mul2 = self.character1['Critical multiplier'], self.character2['Critical multiplier']
            char1_probs = Calc_module.calc_combat_len(HP1, AC1, TH1, dmg1, prec1, static1, cr_thresh1, cr_mul1)
            char2_probs = Calc_module.calc_combat_len(HP2, AC2, TH2, dmg2, prec2, static2, cr_thresh2, cr_mul2)
            char1_turns, char1_ps = list(char1_probs.keys()), list(char1_probs.values())
            char2_turns, char2_ps = list(char2_probs.keys()), list(char2_probs.values())
            self.update_plot(char1_turns, char1_ps, char2_turns, char2_ps)
        else:
            self.status_label_var.set('Not every character has been set yet!')

    def simulate(self):
        if self.character1 is not None and self.character2 is not None:
            HP1, HP2 = self.character2['HP'], self.character1['HP']
            AC1, AC2 = self.character2['AC'], self.character1['AC']
            TH1, TH2 = self.character1['To hit'], self.character2['To hit']
            dmg1, dmg2 = self.character1['Damage dice'], self.character2['Damage dice']
            prec1, prec2 = self.character1['Precision dice'], self.character2['Precision dice']
            static1, static2 = self.character1['Damage bonus'], self.character2['Damage bonus']
            cr_thresh1, cr_thresh2 = self.character1['Critical thresh'], self.character2['Critical thresh']
            cr_mul1, cr_mul2 = self.character1['Critical multiplier'], self.character2['Critical multiplier']
            self.status_label_var.set('Simulating combat for character 1!')
            char1_probs = Calc_module.sim_combat_len(HP1, AC1, TH1, dmg1, prec1, static1, cr_thresh1, cr_mul1, 10000)
            self.status_label_var.set('Simulating combat for character 2!')
            char2_probs = Calc_module.sim_combat_len(HP2, AC2, TH2, dmg2, prec2, static2, cr_thresh2, cr_mul2, 10000)
            self.status_label_var.set('Simulation done!')
            char1_probs = sorted(char1_probs.items())
            char1_turns, char1_ps = [], []
            for p in char1_probs:
                char1_turns.append(p[0])
                char1_ps.append(p[1])
                
            char2_probs = sorted(char2_probs.items())
            char2_turns, char2_ps = [], []
            for p in char2_probs:
                char2_turns.append(p[0])
                char2_ps.append(p[1])
            self.update_plot(char1_turns, char1_ps, char2_turns, char2_ps)
        else:
            self.status_label_var.set('Not every character has been set yet!')

calc = Calculator()
calc.root.mainloop()
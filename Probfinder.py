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

    class Character:
        def __init__(self, root, status_label_var, master):
            self.root = root
            self.status_label_var = status_label_var
            self.dictionary = {}
            self.dictionary["Attacks"] = []
            self.curr_att = 0

            tk.Label(master, text='Character name').pack()
            self.name_entry = tk.Entry(master)
            self.name_entry.pack(expand=1, fill='x')
            tk.Label(master, text='HP').pack()
            self.HP_entry = tk.Entry(master)
            self.HP_entry.pack(expand=1, fill='x')
            tk.Label(master, text='Armor class').pack()
            self.AC_entry = tk.Entry(master)
            self.AC_entry.pack(expand=1, fill='x')

            saves_frame = tk.Frame(master)

            fort_frame = tk.Frame(saves_frame)
            tk.Label(fort_frame, text='Fort save').pack(side=tk.TOP)
            self.fort_entry = tk.Entry(fort_frame, width=3)
            self.fort_entry.pack(expand=1, fill='x', side=tk.BOTTOM)
            fort_frame.pack(expand=1, fill='x', side=tk.LEFT)

            ref_frame = tk.Frame(saves_frame)
            tk.Label(ref_frame, text='Ref save').pack(side=tk.TOP)
            self.ref_entry = tk.Entry(ref_frame, width=3)
            self.ref_entry.pack(expand=1, fill='x', side=tk.BOTTOM)
            ref_frame.pack(expand=1, fill='x', side=tk.LEFT)

            will_frame = tk.Frame(saves_frame)
            tk.Label(will_frame, text='Will save').pack(side=tk.TOP)
            self.will_entry = tk.Entry(will_frame, width=3)
            self.will_entry.pack(expand=1, fill='x', side=tk.BOTTOM)
            will_frame.pack(expand=1, fill='x', side=tk.LEFT)

            saves_frame.pack(expand=1, fill='x')

            spec_dmg_frame1 = tk.Frame(master)
            spec_dmg_frame2 = tk.Frame(master)

            vuln_frame = tk.Frame(spec_dmg_frame1)
            tk.Label(vuln_frame, text='Vulnerability').pack(side=tk.TOP)
            self.vuln_entry = tk.Entry(vuln_frame, width=7)
            self.vuln_entry.pack(expand=1, fill='x', side=tk.BOTTOM)
            vuln_frame.pack(expand=1, fill='x', side=tk.LEFT)

            res_frame = tk.Frame(spec_dmg_frame1)
            tk.Label(res_frame, text='Resistance').pack(side=tk.TOP)
            self.res_entry = tk.Entry(res_frame, width=7)
            self.res_entry.pack(expand=1, fill='x', side=tk.BOTTOM)
            res_frame.pack(expand=1, fill='x', side=tk.LEFT)
            
            imm_frame = tk.Frame(spec_dmg_frame2)
            tk.Label(imm_frame, text='Immunity').pack(side=tk.TOP)
            self.imm_entry = tk.Entry(imm_frame, width=7)
            self.imm_entry.pack(expand=1, fill='x', side=tk.BOTTOM)
            imm_frame.pack(expand=1, fill='x', side=tk.LEFT)

            DR_frame = tk.Frame(spec_dmg_frame2)
            tk.Label(DR_frame, text='DR').pack(side=tk.TOP)
            self.DR_entry = tk.Entry(DR_frame, width=7)
            self.DR_entry.pack(expand=1, fill='x', side=tk.LEFT)
            DR_frame.pack(expand=1, fill='x', side=tk.LEFT)

            spec_dmg_frame1.pack(expand=1, fill='x')
            spec_dmg_frame2.pack(expand=1, fill='x')

            tk.Label(master, text='Concealment').pack()
            self.conc_entry = tk.Entry(master)
            self.conc_entry.pack(expand=1, fill='x')

            attack_frame = tk.Frame(master, borderwidth=3, relief=tk.RAISED)

            metaframe = tk.Frame(attack_frame)

            left_btn = tk.Button(metaframe, text='<', command=lambda: self.change_attack(-1))
            left_btn.pack(side=tk.LEFT, expand=1, fill='both')

            self.att_num_label_var = tk.StringVar()
            self.att_num_label_var.set('Attacks: 1/0')
            self.att_num_label = ttk.Label(metaframe, textvariable=self.att_num_label_var, relief=tk.RAISED)
            self.att_num_label.pack(side=tk.LEFT, expand=1, fill='both')

            right_btn = tk.Button(metaframe, text='>', command=lambda: self.change_attack(1))
            right_btn.pack(side=tk.LEFT, expand=1, fill='both')

            metaframe.pack(expand=1, fill='x')

            metaframe2 = tk.Frame(attack_frame)

            set_btn = tk.Button(metaframe2, text='Set', command=lambda: self.set_attack())
            set_btn.pack(side=tk.LEFT, expand=1, fill='both')
            del_btn = tk.Button(metaframe2, text='Delete', command=lambda: self.delete_attack())
            del_btn.pack(side=tk.LEFT, expand=1, fill='both')

            metaframe2.pack(expand=1, fill='x')

            tk.Label(attack_frame, text='Name').pack()
            self.attname_entry = tk.Entry(attack_frame)
            self.attname_entry.pack(expand=1, fill='x')

            tk.Label(attack_frame, text='Multiattack').pack()
            self.multatt_entry = tk.Entry(attack_frame)
            self.multatt_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='Daily limit').pack()
            self.limit_entry = tk.Entry(attack_frame)
            self.limit_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='Relative frequency').pack()
            self.relfreq_entry = tk.Entry(attack_frame)
            self.relfreq_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='To hit bonus').pack()
            self.TH_entry = tk.Entry(attack_frame)
            self.TH_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='Damage dice').pack()
            self.dmg_entry = tk.Entry(attack_frame)
            self.dmg_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='Precision dice').pack()
            self.prec_entry = tk.Entry(attack_frame)
            self.prec_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='Damage bonus').pack()
            self.static_entry = tk.Entry(attack_frame)
            self.static_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='Crit thresh').pack()
            self.crit_entry = tk.Entry(attack_frame)
            self.crit_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='Crit multiplier').pack()
            self.mult_entry = tk.Entry(attack_frame)
            self.mult_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='Save type').pack()
            self.save_type_entry = tk.Entry(attack_frame)
            self.save_type_entry.pack(expand=1, fill='x')
            tk.Label(attack_frame, text='Save DC').pack()
            self.save_DC_entry = tk.Entry(attack_frame)
            self.save_DC_entry.pack(expand=1, fill='x')

            attack_frame.pack(expand=1, fill='x')

            set_btn = tk.Button(master, text='Set', height=1, command=lambda: self.validate_character())
            set_btn.pack(expand=1, fill='x')

            save_btn = tk.Button(master, text='Save', height=1, command=lambda: self.save_character())
            save_btn.pack(expand=1, fill='x')

            load_btn = tk.Button(master, text='Load', height=1, command=lambda: self.load_character())
            load_btn.pack(expand=1, fill='x')

        @staticmethod
        def convert_dice(dice):
            retstr = ""
            for (dn, df, t) in dice:
                if t != '':
                    retstr += f"+{dn}d{df}/{t}"
                else:
                    retstr += f"+{dn}d{df}"
            retstr = retstr[1:]
            return retstr

        @staticmethod
        def parse_dice(dmg_string):
            dmg_dice = []
            if len(dmg_string) != 0:
                if 'd' not in dmg_string:
                    return 1
                dmg = dmg_string.split('+')
                for dam in dmg:
                    if '/' in dam:
                        d, type = dam.split('/')
                    else:
                        d, type = dam, ''
                    try:
                        num, faces = d.split('d')
                        dmg_dice.append((int(num), int(faces), type))
                    except ValueError:
                        return 2
            return dmg_dice

        def set_attack(self):
            attack = {}
            try:
                name = self.attname_entry.get()
                attack['Name'] = name if len(name) != 0 else 'Basic'

                multatt = self.multatt_entry.get()
                attack['Multiattack'] = int(multatt) if len(multatt) != 0 else 1

                limit = self.limit_entry.get()
                attack['Limit'] = int(limit) if len(limit) != 0 else 0

                reqlfreq = self.relfreq_entry.get()
                attack['Relative frequency'] = int(reqlfreq) if len(reqlfreq) != 0 else 1

                to_hit = self.TH_entry.get()
                attack['To hit'] = int(to_hit) if len(to_hit) != 0 else 0

                dmg_string = self.dmg_entry.get()
                dmg_dice = self.parse_dice(dmg_string)
                if not isinstance(dmg_dice, list):
                    if dmg_dice == 1:
                        self.status_label_var.set('Error in damage dice field: Use XdY/[type] notation')
                    if dmg_dice == 2:
                        self.status_label_var.set(f'Error in damage dice field: One die incorrect')
                attack['Damage dice'] = dmg_dice

                prec_string = self.prec_entry.get()
                prec_dice = self.parse_dice(prec_string)
                if not isinstance(dmg_dice, list):
                    if dmg_dice == 1:
                        self.status_label_var.set('Error in precision dice field: Use XdY/[type] notation')
                    if dmg_dice == 2:
                        self.status_label_var.set(f'Error in precision dice field: One die incorrect')
                attack['Precision dice'] = prec_dice

                static = self.static_entry.get()
                attack['Damage bonus'] = int(static) if len(static) != 0 else 0

                if len(dmg_string) == 0 and len(prec_string) == 0 and len(static) == 0:
                    self.status_label_var.set(f'You must set some form of damage!')
                    return 0

                crit = self.crit_entry.get()
                attack['Critical thresh'] = int(crit) if len(crit) != 0 else 20

                crit_mult = self.mult_entry.get()
                attack['Critical multiplier'] = int(crit_mult) if len(crit_mult) != 0 else 2

                save_type = self.save_type_entry.get()
                if len(save_type) != 0:
                    type, effect = save_type.split('/')
                    if type.lower() in ['fort', 'ref', 'will'] and effect.lower() in ['halve', 'zero']:
                        attack['Save'] = (type, effect)
                    else:
                        self.status_label_var.set(f'For saves, use [Fort/Ref/Will]/[Halve/Zero] format!')
                        return 0
                else:
                    attack['Save'] = ('', '')

                save_DC = self.save_DC_entry.get()
                attack['Save DC'] = int(save_DC) if len(save_DC) != 0 else 0

                if self.curr_att < len(self.dictionary["Attacks"]):
                    self.dictionary["Attacks"][self.curr_att] = attack
                else:
                    self.dictionary["Attacks"].append(attack)

                self.att_num_label_var.set(f'Attacks: {self.curr_att + 1}/{len(self.dictionary["Attacks"])}')
                return 1
            except ValueError:
                self.status_label_var.set(f'Error in one of the attack fields!')
                return 0

        def delete_attack(self):
            if self.curr_att > len(self.dictionary["Attacks"]) != 0:
                self.change_attack(-1, False)
                return
            if len(self.dictionary["Attacks"]) > 1:
                del self.dictionary["Attacks"][self.curr_att]
            if self.curr_att < len(self.dictionary["Attacks"]):
                self.change_attack(0, False)
            else:
                self.change_attack(-1, False)

        def change_attack(self, delta, save=True):
            if save:
                if not self.set_attack():
                    return 0
            new_attack_idx = max(0, self.curr_att + delta)
            self.curr_att = new_attack_idx

            entries = [self.attname_entry, self.multatt_entry, self.limit_entry, self.relfreq_entry, self.TH_entry,
                       self.dmg_entry, self.prec_entry, self.static_entry, self.crit_entry, self.mult_entry,
                       self.save_type_entry, self.save_DC_entry]
            for e in entries:
                e.delete(0, tk.END)
            if new_attack_idx < len(self.dictionary["Attacks"]):
                new_attack = self.dictionary["Attacks"][new_attack_idx]
                self.attname_entry.insert(0, new_attack['Name'])
                self.multatt_entry.insert(0, str(new_attack['Multiattack']))
                self.limit_entry.insert(0, str(new_attack['Limit']))
                self.relfreq_entry.insert(0, str(new_attack['Relative frequency']))
                self.TH_entry.insert(0, str(new_attack['To hit']))

                self.dmg_entry.insert(0, self.convert_dice(new_attack['Damage dice']))
                self.prec_entry.insert(0, self.convert_dice(new_attack['Precision dice']))
                self.static_entry.insert(0, str(new_attack['Damage bonus']))
                self.crit_entry.insert(0, str(new_attack['Critical thresh']))
                self.mult_entry.insert(0, str(new_attack['Critical multiplier']))
                if new_attack['Save'][0] != '':
                    self.save_type_entry.insert(0, f'{new_attack["Save"][0]}/{new_attack["Save"][1]}')
                self.save_DC_entry.insert(0, str(new_attack['Save DC']))

            self.att_num_label_var.set(f'Attacks: {self.curr_att+1}/{len(self.dictionary["Attacks"])}')

        def validate_character(self):
            if not self.set_attack():
                return 0
            field_names = ['Name', 'HP', 'AC', 'Fort', 'Ref', 'Will']
            entries = [self.name_entry, self.HP_entry, self.AC_entry, self.fort_entry, self.ref_entry, self.will_entry]
            for i, entry in enumerate(entries):
                val = entry.get()
                if len(val) == 0:
                    self.status_label_var.set(f'Field {field_names[i]} is not set!')
                    return 0
            self.dictionary['Name'] = self.name_entry.get()
            try:
                self.dictionary['HP'] = int(self.HP_entry.get())
                self.dictionary['AC'] = int(self.AC_entry.get())
                self.dictionary['Fort'] = int(self.fort_entry.get())
                self.dictionary['Ref'] = int(self.ref_entry.get())
                self.dictionary['Will'] = int(self.will_entry.get())

                vuln = self.vuln_entry.get()
                self.dictionary['Vulnerability'] = vuln.split(',') if len(vuln) != 0 else ''
                res = self.res_entry.get()
                self.dictionary['Resistance'] = res.split(',') if len(res) != 0 else ''
                imm = self.imm_entry.get()
                self.dictionary['Immunity'] = imm.split(',') if len(imm) != 0 else ''
                conc = self.conc_entry.get()
                self.dictionary['Concealment'] = int(conc) if len(conc) != 0 else 0
                DR = self.DR_entry.get()
                if len(DR) != 0:
                    DR_val, DR_except = DR.split('/')
                    self.dictionary['DR'] = (DR_val, DR_except.split(','))
                else:
                    self.dictionary['DR'] = (0, '')
            except ValueError:
                self.status_label_var.set(f'Error in one of the character fields')
                return 0
            self.status_label_var.set(f'Character set')
            return 1

        def save_character(self):
            Path('Characters').mkdir(parents=True, exist_ok=True)
            if self.validate_character():
                with open(f'Characters/{self.dictionary["Name"]}.json', 'w') as outfile:
                    json.dump(self.dictionary, outfile)
            self.status_label_var.set(f'Character saved')

        def load_character(self):
            self.root.withdraw()
            file_selected = filedialog.askopenfile()
            if file_selected == '' or file_selected is None:
                self.status_label_var.set(f'Please select a file')
                self.root.deiconify()
                return
            if file_selected.name.endswith('.json'):
                with open(file_selected.name, 'r') as file:
                    self.dictionary = json.load(file)
                entries = [self.name_entry, self.HP_entry, self.AC_entry, self.fort_entry, self.ref_entry,
                           self.will_entry, self.vuln_entry, self.res_entry, self.imm_entry, self.DR_entry,
                           self.conc_entry]
                for e in entries:
                    e.delete(0, tk.END)
                self.name_entry.insert(0, self.dictionary['Name'])
                self.HP_entry.insert(0, str(self.dictionary['HP']))
                self.AC_entry.insert(0, str(self.dictionary['AC']))
                self.fort_entry.insert(0, str(self.dictionary['Fort']))
                self.ref_entry.insert(0, str(self.dictionary['Ref']))
                self.will_entry.insert(0, str(self.dictionary['Will']))

                def convert_list(list_str):
                    retstr = ""
                    for s in list_str:
                        retstr += f'{s},'
                    return retstr[:-1]

                vuln = self.dictionary['Vulnerability']
                res = self.dictionary['Resistance']
                imm = self.dictionary['Immunity']
                if vuln != "":
                    self.vuln_entry.insert(0, convert_list(vuln))
                if res != "":
                    self.res_entry.insert(0, convert_list(res))
                if imm != "":
                    self.imm_entry.insert(0, convert_list(imm))
                DR = self.dictionary['DR']
                if DR[0] != 0:
                    self.DR_entry.insert(0, f'{DR[0]}/{convert_list(DR[1])}')

                self.curr_att = 0
                self.change_attack(0, False)
                self.root.deiconify()
            else:
                self.status_label_var.set(f'Please select a JSON file')
                self.root.deiconify()

        def get_dict(self):
            return self.dictionary

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1680x1024")
        self.root.title('PF1e calculator')
        self.root.resizable()
        self.status_label_var = tk.StringVar()

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
        
        self.char1 = self.Character(self.root, self.status_label_var, leftleft)
        self.char2 = self.Character(self.root, self.status_label_var, leftright)

        calc_btn = tk.Button(leftbot, text='Calculate', height=1, command=self.calculate)
        calc_btn.pack(expand=1, fill='x')

        sim_btn = tk.Button(leftbot, text='Simulate', height=1, command=self.simulate)
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
        self.status_label = ttk.Label(statusframe, textvariable=self.status_label_var, relief=tk.RAISED)
        self.status_label.config(width=200, font=("Courier", 15))
        self.status_label.pack(side=tk.TOP, expand=1, fill='both')

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
        self.subplotprob.legend([self.char1.get_dict()['Name'], self.char2.get_dict()['Name']])
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
        self.subplotcum.legend([self.char1.get_dict()['Name'], self.char2.get_dict()['Name']])
        self.canvascum.draw()

    def calculate(self):
        try:
            character1, character2 = self.char1.get_dict(), self.char2.get_dict()
            HP1, HP2 = character2['HP'], character1['HP']
            AC1, AC2 = character2['AC'], character1['AC']
            saves1, saves2 = (character2['Fort'], character2['Ref'], character2['Will']), (character1['Fort'], character1['Ref'], character1['Will'])
            vuln1, vuln2 = character2['Vulnerability'], character1['Vulnerability']
            res1, res2 = character2['Resistance'], character1['Resistance']
            imm1, imm2 = character2['Immunity'], character1['Immunity']
            conc1, conc2 = character2['Concealment'], character1['Concealment']
            DR1, DR2 = character2['DR'], character1['DR']
            attacks1, attacks2 = character1['Attacks'], character2['Attacks']
            char1_probs = Calc_module.calc_combat_len(HP1, AC1, saves1, vuln1, res1, imm1, conc1, DR1, attacks1)
            char2_probs = Calc_module.calc_combat_len(HP2, AC2, saves2, vuln2, res2, imm2, conc2, DR2, attacks2)
            char1_turns, char1_ps = list(char1_probs.keys()), list(char1_probs.values())
            char2_turns, char2_ps = list(char2_probs.keys()), list(char2_probs.values())
            self.update_plot(char1_turns, char1_ps, char2_turns, char2_ps)
        except KeyError:
            self.status_label_var.set('Not every character has been set yet!')

    def simulate(self):
        try:
            sim_iterations = 30000
            character1, character2 = self.char1.get_dict(), self.char2.get_dict()
            HP1, HP2 = character2['HP'], character1['HP']
            AC1, AC2 = character2['AC'], character1['AC']
            saves1, saves2 = (character2['Fort'], character2['Ref'], character2['Will']), (character1['Fort'], character1['Ref'], character1['Will'])
            vuln1, vuln2 = character2['Vulnerability'], character1['Vulnerability']
            res1, res2 = character2['Resistance'], character1['Resistance']
            imm1, imm2 = character2['Immunity'], character1['Immunity']
            conc1, conc2 = character2['Concealment'], character1['Concealment']
            DR1, DR2 = character2['DR'], character1['DR']
            attacks1, attacks2 = character1['Attacks'], character2['Attacks']
            self.status_label_var.set('Simulating combat for character 1!')
            char1_probs = Calc_module.sim_combat_len(HP1, AC1, saves1, vuln1, res1, imm1, conc1, DR1, attacks1, sim_iterations)
            self.status_label_var.set('Simulating combat for character 2!')
            char2_probs = Calc_module.sim_combat_len(HP2, AC2, saves2, vuln2, res2, imm2, conc2, DR2, attacks2, sim_iterations)
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
        except KeyError:
            self.status_label_var.set('Not every character has been set yet!')

calc = Calculator()
calc.root.mainloop()
import numpy as np
from numpy.polynomial.polynomial import Polynomial, polypow
from scipy.special import comb


def dice_sum(target, dnum, dsides):
    p = target
    n = dnum
    s = dsides
    dsum = 0
    for k in range(0, int(np.floor((p-n)/s)+1)):
        dsum += ((-1)**k)*comb(n, k)*comb(p-s*k-1, n-1)

    return dsum/(dsides**dnum)


def get_density(dnum, dsides):
    min_val = dnum
    max_val = dnum*dsides
    coeffs = [0]*(max_val+1)
    for val in range(min_val, max_val+1):
        coeffs[val] = dice_sum(val, dnum, dsides)
    return np.array(coeffs)


def shift_coeffs(coeffs, shift):
    new_coeffs = np.zeros(coeffs.shape[0] + shift)
    for i, c in enumerate(coeffs):
        new_idx = max(0, i+shift)
        new_coeffs[new_idx] += c
    return new_coeffs


def raise_exponents(coeffs, multiplier):
    new_coeffs = np.zeros(int(np.floor((coeffs.shape[0]-1)*multiplier))+1)
    for i, c in enumerate(coeffs):
        new_idx = int(np.floor(i*multiplier))
        new_coeffs[new_idx] += c
    return new_coeffs


def generating_func(AC, saves, vuln, res, imm, conc, DR, attack):
    TH = attack['To hit']
    crit_thresh = attack['Critical thresh']
    static = attack['Damage bonus']
    dice = attack['Damage dice']
    prec_dice = attack['Precision dice']
    crit_mult = attack['Critical multiplier']
    multi = attack['Multiattack']
    save_type = attack['Save']
    save_DC = attack['Save DC']
    save_mods = {'fort': saves[0], 'ref': saves[1], 'will': saves[2]}
    try:
        save_mod = save_mods[save_type[0].lower()]
        save_effect = save_type[1].lower()
    except KeyError:
        save_mod = 0
        save_effect = ''

    attack_poly = Polynomial([1])
    for att_num in range(0, multi):

        hit_diff = AC - (TH - 5*att_num + 10)
        hit_prob = max(0, min(0.55 - hit_diff * 0.05, 1.0))
        miss_prob = 1 - hit_prob
        crit_range_size = max(0, 20 - crit_thresh + 1)
        hit_range = max(0, min(11 - hit_diff, 20))
        crit_prob = (crit_range_size / 20) * hit_prob
        norm_prob = (hit_range - crit_range_size) / 20 + (crit_range_size / 20) * miss_prob
        hit_prob = norm_prob+crit_prob
        if hit_prob < 0.01:
            continue
        dmg_dice = np.array([1])
        for (dn, df, t) in dice:
            if t in imm:
                continue
            term_density = get_density(dn, df)
            if t in res:
                term_density = raise_exponents(term_density, 0.5)
            if t in vuln:
                term_density = raise_exponents(term_density, 1.5)
            term_poly = Polynomial(dmg_dice)*Polynomial(term_density)
            dmg_dice = term_poly.coef.copy()
        if static[1] in imm:
            pass
        elif static[1] in res:
            dmg_dice = shift_coeffs(dmg_dice, static[0]//2)
        elif static[1] in vuln:
            dmg_dice = shift_coeffs(dmg_dice, 3*static[0]//2)
        else:
            dmg_dice = shift_coeffs(dmg_dice, static[0])

        dice_func = dmg_dice.copy()
        crit_func = raise_exponents(dice_func, crit_mult)
        dice_func.resize(crit_func.shape[0])
        full_dice_gen = dice_func*(norm_prob/hit_prob) + crit_func*(crit_prob/hit_prob)

        prec_func = np.array([1])
        for (dn, df, t) in prec_dice:
            if t in imm:
                continue
            term_density = get_density(dn, df)
            if t in res:
                term_density = raise_exponents(term_density, 0.5)
            if t in vuln:
                term_density = raise_exponents(term_density, 1.5)
            term_poly = Polynomial(prec_func) * Polynomial(term_density)
            prec_func = term_poly.coef.copy()
        full_poly = Polynomial(full_dice_gen)*Polynomial(prec_func)
        if save_effect.lower() in ['halve', 'zero']:
            save_diff = save_DC - (save_mod + 10)
            save_prob = max(0, min(0.55 - save_diff * 0.05, 1.0))
            nosave_prob = 1 - save_prob
            temp = full_poly.coef.copy()
            if save_effect.lower() == 'halve':
                temp = raise_exponents(temp, 0.5)
            elif save_effect.lower() == 'zero':
                temp = np.zeros_like(temp)
                temp[0] = 1
            full_poly = Polynomial(temp)*save_prob + full_poly*nosave_prob

        full_poly = (full_poly*hit_prob)*(1-conc/100)
        full_poly.coef[0] += miss_prob+(hit_prob*conc/100)
        attack_poly = attack_poly*full_poly
    return attack_poly


def calc_combat_len(HP, AC, saves, vuln, res, imm, conc, DR, attacks):
    total_rel_freq = 0
    for attack in attacks:
        total_rel_freq += attack['Relative frequency']
    turn_func = Polynomial([0])
    for attack in attacks:
        attack_func = generating_func(AC, saves, vuln, res, imm, conc, DR, attack)
        turn_func += (attack['Relative frequency']/total_rel_freq)*attack_func
    turn_probs = {}
    sum_prob = 0
    curr_turn_func = Polynomial([1])
    for turn in range(1, 101):
        prev_turn = curr_turn_func.copy()
        prev_turn.coef = prev_turn.coef[:HP]
        this_turn = prev_turn*turn_func
        tp = np.sum(this_turn.coef[HP:])
        turn_probs[turn] = tp
        sum_prob += tp
        if sum_prob >= 0.999:
            break
        curr_turn_func = curr_turn_func*turn_func
    return turn_probs


def sim_combat_len(HP, AC, saves, vuln, res, imm, conc, DR, attacks, sim_num):
    rng = np.random.default_rng()
    total_rel_freq = 0
    for attack in attacks:
        total_rel_freq += attack['Relative frequency']
    att_probs = []
    for attack in attacks:
        att_probs.append(attack['Relative frequency']/total_rel_freq)

    turn_probs = {}
    for _ in range(sim_num + 1):
        dmg = 0
        turn = 0
        while dmg < HP:
            turn += 1
            att_idx = np.random.choice(len(attacks), p=att_probs)
            attack = attacks[att_idx]
            save_type = attack['Save']
            save_DC = attack['Save DC']
            save_mods = {'fort': saves[0], 'ref': saves[1], 'will': saves[2]}
            try:
                save_mod = save_mods[save_type[0].lower()]
                save_effect = save_type[1]
            except KeyError:
                save_mod = 0
                save_effect = ''
            for att_num in range(0, attack['Multiattack']):
                roll = rng.integers(low=1, high=21, size=1)
                if roll + attack['To hit'] - att_num*5 >= AC:
                    if conc != 0:
                        if rng.integers(low=1, high=101, size=1) <= conc:
                            continue
                    mult = 1
                    if roll >= attack['Critical thresh'] and rng.integers(low=1, high=21, size=1) + attack['To hit'] - att_num*5 >= AC:
                        mult = attack['Critical multiplier']
                    die_dmg = 0
                    for (dn, df, t) in attack['Damage dice']:
                        if t in imm:
                            continue
                        vuln_mult = 1
                        if t in vuln:
                            vuln_mult = 1.5
                        if t in res:
                            vuln_mult = 0.5
                        die_dmg += int(np.floor(np.sum(rng.integers(low=1, high=df+1, size=dn))*vuln_mult))
                    prec_dmg = 0
                    for (dn, df, t) in attack['Precision dice']:
                        if t in imm:
                            continue
                        vuln_mult = 1
                        if t in vuln:
                            vuln_mult = 1.5
                        if t in res:
                            vuln_mult = 0.5
                        prec_dmg += int(np.floor(np.sum(rng.integers(low=1, high=df+1, size=dn))*vuln_mult))
                    turn_dmg = (die_dmg + attack['Damage bonus'][0])*mult + prec_dmg
                    #print(save_effect, save_mod, save_DC)
                    if save_effect.lower() in ['halve', 'zero']:
                        if rng.integers(low=1, high=21, size=1) + save_mod >= save_DC:
                            if save_effect.lower() == 'halve':
                                turn_dmg /= 2
                            else:
                                turn_dmg = 0
                    dmg += turn_dmg
        if turn not in turn_probs.keys():
            turn_probs[turn] = 0
        turn_probs[turn] += 1/sim_num
    return turn_probs



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
    return coeffs


def generating_func(AC, saves, vuln, res, imm, conc, DR, attack):
    TH = attack['To hit']
    crit_thresh = attack['Critical thresh']
    static = attack['Damage bonus']
    dice = attack['Damage dice']
    prec_dice = attack['Precision dice']
    crit_mult = attack['Critical multiplier']

    hit_diff = AC - (TH + 10)
    hit_prob = max(0, min(0.55 - hit_diff * 0.05, 1.0))
    miss_prob = 1 - hit_prob
    crit_range_size = max(0, 20 - crit_thresh + 1)
    hit_range = max(0, min(11 - hit_diff, 20))
    crit_prob = (crit_range_size / 20) * hit_prob
    norm_prob = (hit_range - crit_range_size) / 20 + (crit_range_size / 20) * miss_prob
    hit_prob = norm_prob+crit_prob

    dice_func = np.array([1])
    for (dn, df, t) in dice:
        term_density = get_density(dn, df)
        term_poly = Polynomial(dice_func)*Polynomial(term_density)
        dice_func = term_poly.coef.copy()
    temp = np.zeros(dice_func.shape[0] + static)
    for i, coeff in enumerate(dice_func):
        temp[i+static] = coeff
    dice_func = temp.copy()
    crit_func = np.zeros((dice_func.shape[0]-1)*crit_mult+1)
    for i, coeff in enumerate(dice_func):
        crit_func[i*crit_mult] = coeff
    dice_func.resize(crit_func.shape[0])
    full_dice_gen = dice_func*(norm_prob/hit_prob) + crit_func*(crit_prob/hit_prob)
    prec_func = np.array([1])
    for (dn, df, t) in prec_dice:
        term_density = get_density(dn, df)
        term_poly = Polynomial(prec_func) * Polynomial(term_density)
        prec_func = term_poly.coef
    full_poly = Polynomial(full_dice_gen)*Polynomial(prec_func)
    full_poly = full_poly*hit_prob
    full_poly.coef[0] = miss_prob
    return full_poly


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
    return  turn_probs


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
            roll = rng.integers(low=1, high=21, size=1)
            if roll + attack['To hit'] >= AC:
                mult = 1
                if roll >= attack['Critical thresh'] and rng.integers(low=1, high=21, size=1) + attack['To hit'] >= AC:
                    mult = attack['Critical multiplier']
                die_dmg = 0
                for (dn, df, t) in attack['Damage dice']:
                    die_dmg += np.sum(rng.integers(low=1, high=df+1, size=dn))
                prec_dmg = 0
                for (dn, df, t) in attack['Precision dice']:
                    prec_dmg += np.sum(rng.integers(low=1, high=df+1, size=dn))
                dmg += (die_dmg + attack['Damage bonus'])*mult + prec_dmg
        if turn not in turn_probs.keys():
            turn_probs[turn] = 0
        turn_probs[turn] += 1/sim_num
    return turn_probs



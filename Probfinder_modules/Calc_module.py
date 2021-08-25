import numpy as np
from numpy.polynomial.polynomial import Polynomial, polypow
from scipy.special import comb
import matplotlib.pyplot as plt


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


def generating_func(dice, prec_dice, norm_prob, crit_prob, crit_mult, static):
    hit_prob = norm_prob+crit_prob
    dice_func = np.array([1])
    for (dn, df) in dice:
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
    for (dn, df) in prec_dice:
        term_density = get_density(dn, df)
        term_poly = Polynomial(prec_func) * Polynomial(term_density)
        prec_func = term_poly.coef
    full_poly = Polynomial(full_dice_gen)*Polynomial(prec_func)
    full_gen = full_poly.coef
    return full_gen


def calc_combat_len(HP, AC, to_hit, dice, prec_dice, static, crit_thresh, crit_mult):
    r_min, r_max = 0, 0
    for (num, faces) in dice:
        r_min += num
        r_max += num * faces * crit_mult
    for (num, faces) in prec_dice:
        r_min += num
        r_max += num * faces
    min_dmg, max_dmg = r_min + static, r_max + crit_mult*static
    min_hits = min_turns = int(np.ceil(HP/max_dmg))
    max_hits = int(np.ceil(HP/min_dmg))

    hit_diff = AC-(to_hit+10)
    hit_prob = 0.55-hit_diff*0.05
    miss_prob = 1-hit_prob
    crit_range_size = 20-crit_thresh+1
    hit_range = 11-hit_diff
    crit_prob = (crit_range_size/20)*hit_prob
    normal_prob = (hit_range-crit_range_size)/20+(crit_range_size/20)*miss_prob
    gen_func = generating_func(dice, prec_dice, normal_prob, crit_prob, crit_mult, static)
    lethal_density = {0: [1]}
    for hits in range(min_hits, max_hits+1):
        if hits == 0:
            continue
        density = polypow(gen_func, hits-1)
        sublethals = density[:HP].copy()
        density = [0]*len(density)
        density[:HP] = sublethals
        lethal = Polynomial(density)*Polynomial(gen_func)
        lethal_density[hits] = lethal.coef.copy()
    turn_probs = {}
    sum_prob = 0
    for turn in range(min_turns, 101):
        tp = 0
        for num_hits in range(min_hits, max_hits+1):
            if num_hits > turn:
                break
            num_miss = turn - num_hits
            prob_hits = (hit_prob ** num_hits) * (miss_prob ** num_miss) * comb(turn - 1, num_hits - 1)
            tp += np.sum(lethal_density[num_hits][HP:])*prob_hits
        turn_probs[turn] = tp
        sum_prob += tp
        if sum_prob >= 0.999:
            break
    return turn_probs


def sim_combat_len(HP, AC, to_hit, dice, prec_dice, static, crit_thresh, crit_mult, sim_num):
    rng = np.random.default_rng()
    turn_probs = {}
    for _ in range(sim_num+1):
        dmg = 0
        turn = 0
        while dmg < HP:
            turn += 1
            roll = rng.integers(low=1, high=21, size=1)
            if roll + to_hit >= AC:
                mult = 1
                if roll >= crit_thresh and rng.integers(low=1, high=21, size=1) + to_hit >= AC:
                    mult = crit_mult
                die_dmg = 0
                for (dn, df) in dice:
                    die_dmg += np.sum(rng.integers(low=1, high=df+1, size=dn))
                prec_dmg = 0
                for (dn, df) in prec_dice:
                    prec_dmg += np.sum(rng.integers(low=1, high=df+1, size=dn))
                dmg += (die_dmg + static)*mult + prec_dmg
        if turn not in turn_probs.keys():
            turn_probs[turn] = 0
        turn_probs[turn] += 1/sim_num
    return turn_probs

'''HP = 100
damage = '1d4+*2d6+4'
AC = 14
to_hit = 6
crit_thresh = 18
crit_mult = 2
turn_probs = calc_combat_len2(HP, damage, AC, to_hit, crit_thresh, crit_mult)
probs = sorted(turn_probs.items())
probs_turns, probs_vals = [], []
for p in probs:
    probs_turns.append(p[0])
    probs_vals.append(p[1])
    print(p[0], p[1], end=', ')
print('\n', end='')

turn_samples = sim_combat_len(HP, damage, AC, to_hit, crit_thresh, crit_mult)
samples = sorted(turn_samples.items())
samples_turns, samples_vals = [], []
for s in samples:
    samples_turns.append(s[0])
    samples_vals.append(s[1]/30000)
    print(s[0], s[1]/30000, end=', ')
print('\n')

summa = 0
for v in turn_probs.values():
    summa += v
print(f'summa: {summa}')
plt.plot(probs_turns, probs_vals)
plt.plot(samples_turns, samples_vals)
plt.legend(['Probs', 'Sim'])
plt.show()'''



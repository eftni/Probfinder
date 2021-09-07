# Probfinder: A Pathfinder 1e combat probability calculator
Probfinder is a python script for calculating the expected length of a combat encounter between two characters in the Patfinder 1st Edition roleplaying game. 

## Supported features
Currently, Probfinder only supports 1v1 duels, as well as static conditions.
To-hit bonuses, AC and damage aren't allowed to change as the combat progresses.
As such, Probfinder can only simulate attacks that don't inflict status effects on an opponent. (e.g. staggered, nauseated, etc.)
A simulation mode is also included as a backup, however this only supports the features that the calculator does.
Also, simulation is much slower than the calculator.

Currently modelled processes:
1. Attack rolls, with confirmed and unconfirmed criticals
2. Precision damage (i.e. damage that is not multiplied on a critical hit)
3. Calculating several metrics, such as expected value and confidence intervals
4. Support for multiple attack types
5. Multiattack
6. Concealment

## Planned features
1. Support for saving throws to halve or negate damage
2. Support for vulnerability, resistance, immunity and DR
3. Support for changing hit-probabilities (e.g. conditions)
4. Additional metrics (confidence intervals around the expected value)
5. Calculations for most likely winner and expected HP for the victor after the battle

## Notes
Some abilities (such as ones that change enemy AC) are best modelled by an equivalent change to the to-hit bonus of the attack.
Damage types are not hardcoded into the script, and are compared via string matching. This means that if damage types are specified consistently, (i.e. DR: 5/Good, damage dice: 2d6/Good), they will work. This means that damage types can be marked in any way the user sees fit. (Fire, F, etc.)  

If a character has multiple attack types, a relative frequency should also be given. This represents the likelyhood of the character using that attack. For instance, if one attack has a RF of 5 and another 2, then the first attack is used with P = 5/7 ~= 0.71, the second with P = 2/7 ~= 0.28. 

## Implementation notes
The calculations are performed by multiplying the probability generating functions of the individual attacks (as represented by a polynomial) to derive a total distribution of damage values in a single turn (hereafter referred to as the "turn-generating polynomial"). This polynomial is raised to the power of T to determine the probabilities of the total amount of damage dealt by turn T.   

To determine the probability of a character achieving a kill on turn T, first the polynomial of turn T-1 is taken. The coefficients at or above the exponent equal to the HP of the enemy are set to 0 (as that would mean the character has achieved a kill at or before turn T-1), then this is multiplied by the turn-generating polynomial. The final coefficients are summed from the exponent equal to the HP of the enemy to the largest exponent to determine the kill probability.  

Once the cumulative probability density reaches 0.999 or turn 100 is reached, the calculation is stopped.

## Requirements
1. numpy >= 1.17.5
2. matplotlib >= 3.1.3
3. scipy >= 1.7.1
# Probfinder: A Pathfinder 1e combat probability calculator
Probfinder is a python script for calculating the expected length of a combat encounter between two characters in the Patfinder 1st Edition roleplaying game. 

## Supported features
Currently, Probfinder only supports 1v1 duels, as well as static conditions.
To-hit bonuses, AC and damage aren't allowed to change as the combat progresses.
As such, Probfinder can only simulate a single attack type, which cannot inflict status effects on an opponent.
A simulation mode is also included as a backup, however this only supports the features that the calculator does. 

Currently modelled processes:
1. Attack rolls, with confirmed and unconfirmed criticals
2. Precision damage (i.e. damage that is not multiplied on a critical hit)
3. Calculating several metrics, such as expected value and confidence intervals

## Planned features
1. Support for changing hit-probabilities (e.g. multiattack, conditions, etc.)
2. Support for multiple attack types
3. Support for saving throws
4. Additional metrics (confidence intervals around the expected value)
4. Calculations for most likely winner and expected HP for the victor after the battle

## Requirements
1. numpy >= 1.17.5
2. matplotlib >= 3.1.3
3. scipy >= 1.7.1
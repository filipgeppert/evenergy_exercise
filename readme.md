# Exercise
https://gist.github.com/a-grealish/982fefdb9fe822a761e262411e9800a1

# How to run the assignment
1. `python venv env` to install requirements
2. `source env/bin/activate` to activate environment
3. `pip install -r requirements.txt` to install requirements
4. `python main.py` to run an example from the exercise

This will produce an array with 0 (don't charge)/1 (charge) for each minute between plug time in and unplug time.

Example:
```
python main.py
Connection schedule:
[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]
Total charging minutes: 300
Total schedule duration (minutes): 738
```

## How to test
`pytest` from top level directory and activated environment

## Covered edge cases (covered in tests):
1. Same day plug in and unplug 
2. Overnight plug in and unplug
3. Prioritization of charging before unplug time
4. Prioritization of low tariff usage

# Note about implementation
I didn't want to exceed a time limit from the task, thus I list some shortcuts I made:

1. Current solution ignores seconds in provided time strings. Minute was assumed to be a basic unit for computation. Seconds can be supported as a next step.
2. It is required that plug in time and unplug time have the same timezone. Different timezones can be supported as a next step.
3. Current solution supports 24h max duration between plug in and unplug time. Longer duration can be supported as a next step. 
4. `create_charging_schedule` method should be definitely split into smaller functions.

# Stretch questions
## We prioritise price first and then carbon intensity - a JSON file is provided of carbon intensity for Enid's region which should be prioritised as a secondary optimisation
Pseudo code:

1. Based on a json input file create a matrix of carbon intensities (based on `index` field). Matrix should have the same shape as `connection_schedule_low_tariff`.
2. Modify charging strategy, for example:
   1. When there's not enough available minutes in low tariff -> Charge when carbon intensity is lowest.
   2. Create a matrix that is a combination of low tariff prices and carbon intensities. Each part would have its importance (weight). Charge periods would be selected based on multiplication results.  

## Enid lives up North where it gets pretty cold! She knows that her car is more efficient if it has been charging in the hour before her ready by time. So ideally the hour before her ready by time the car will charge.
I Implemented a strategy for charging right before unplugging a car. 
Currently, it's assumed that all available charging should happen as close to unplug time as it's possible. 
It's also possible to support different strategies (for optimal battery charging). 

## It would be nice if Enid moved to spain it would still work - so timezone aware schedules would help

It was assumed that plug in time should have the same timezone as unplug time. 
I wasn't sure how tariff should be influenced by timezone, so currently only one tariff is available. 
Should timezone influence tariff schedule, an array operation for shifting low price zones by timezone offset could be added.

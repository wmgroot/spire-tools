# Spire Tools
A helper tool to automatically generate content for Spire: The City Must Fall.

## Source Material
Spire: The City Must Fall is created and published by Rowan, Rook & Decard.
https://rowanrookanddecard.com/product-category/game-systems/resistance/spire/?v=0b3b97fa6688

## Installation
Clone the source code.
```
cd ~
git clone git@github.com:wmgroot/spire-tools.git
```

Ensure you have Python 3.5+ installed.
```
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python --version
Python 3.10.12
```

Install the command line interface locally.
```
$ pip install -e .
$ spire --version
```

## Use
Run the tool on the command line.
```
spire fallout -r blood -l moderate

Broken Leg (Severe) - Blood

Your leg bones splinter and crack. You can’t walk without
crutches for a month or so, and you’ll automatically fail any
Pursue attempts. Any action where you’d need to be quick
on your feet (fighting, dancing, climbing) is either impossible
or suffers from an increased difficulty.

Broken Arm (Severe) - Blood

Your arm breaks under the strain, and splintered bone juts up
through your skin. You can’t use the arm until it heals (which
will take a month or so, or require powerful healing magic).

Knocked Out (Severe) - Blood

You fall unconscious for several hours, during which time
your enemies get an advantage.
```

### Full Options
```
spire fallout --help
usage: spire [-h] [-v] [-L {info,debug,warn,error}] [-T TABLES] [-R] [-S SEED] -r {blood,mind,silver,shadow,reputation,bond} [-c CLASS] -l {minor,moderate,severe} [-o OUTCOMES] <command>

spire options

positional arguments:
  <command>

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         display the package version
  -L {info,debug,warn,error}, --log_level {info,debug,warn,error}
                        set the desired logging level
  -T TABLES, --tables TABLES
                        path to the tables file
  -R, --rolls_on        show rolled values
  -S SEED, --seed SEED  sets the random generator seed
  -r {blood,mind,silver,shadow,reputation,bond}, --resistance {blood,mind,silver,shadow,reputation,bond}
                        the name of the resistance to roll for
  -c CLASS, --class CLASS
                        the name of the class to roll for to allow class specific fallouts
  -l {minor,moderate,severe}, --level {minor,moderate,severe}
                        the severity of the fallout
  -o OUTCOMES, --outcomes OUTCOMES
                        the maximum number of results to print
```

## TODOs
1. Identify best way to organize special case fallout, such as demonic, occult.

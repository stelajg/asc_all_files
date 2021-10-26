"""
A command-line controlled coffee maker.
"""

import sys

"""
Implement the coffee maker's commands. Interact with the user via stdin and print to stdout.

Requirements:
    - use functions
    - use __main__ code block
    - access and modify dicts and/or lists
    - use at least once some string formatting (e.g. functions such as strip(), lower(),
    format()) and types of printing (e.g. "%s %s" % tuple(["a", "b"]) prints "a b"
    - BONUS: read the coffee recipes from a file, put the file-handling code in another module
    and import it (see the recipes/ folder)

There's a section in the lab with syntax and examples for each requirement.

Feel free to define more commands, other coffee types, more resources if you'd like and have time.
"""

"""
Tips:
*  Start by showing a message to the user to enter a command, remove our initial messages
*  Keep types of available coffees in a data structure such as a list or dict
e.g. a dict with coffee name as a key and another dict with resource mappings (resource:percent)
as value
"""

# Commands
EXIT = "exit"
LIST_COFFEES = "list"
MAKE_COFFEE = "make"  # !!! when making coffee you must first check that you have enough resources!
HELP = "help"
REFILL = "refill"
RESOURCE_STATUS = "status"
commands = [EXIT, LIST_COFFEES, MAKE_COFFEE, REFILL, RESOURCE_STATUS, HELP]

# Coffee examples
ESPRESSO = "espresso"
AMERICANO = "americano"
CAPPUCCINO = "cappuccino"

# Resources examples
WATER = "water"
COFFEE = "coffee"
MILK = "milk"

# Coffee maker's resources - the values represent the fill percents
RESOURCES = {WATER: 100, COFFEE: 100, MILK: 100}

"""
Example result/interactions:

I'm a smart coffee maker
Enter command:
list
americano, cappuccino, espresso
Enter command:
status
water: 100%
coffee: 100%
milk: 100%
Enter command:
make
Which coffee?
espresso
Here's your espresso!
Enter command:
refill
Which resource? Type 'all' for refilling everything
water
water: 100%
coffee: 90%
milk: 100%
Enter command:
exit
"""


# print("I'm a simple coffee maker")
# print("Press enter")
# sys.stdin.readline()

def parse(filepath, separator="="):
    dic = {}
    with open(filepath, "r") as f:
        for line in f:
            line = line.split(separator)
            dic[line[0]] = line[1]
    return dic


def make_coffee(coffee_type):
    coffee_type = coffee_type[:-1]
    path = "recipes/" + coffee_type.lower() + ".txt"
    dicti = parse(path)
    water = RESOURCES[WATER] - int(dicti["water"])
    milk = RESOURCES[MILK] - int(dicti["milk"])
    coffee = RESOURCES[COFFEE] - int(dicti["coffee"])
    if water < 0:
        print("Not enough water")
    elif milk < 0:
        print("Not enough milk")
    elif coffee < 0:
        print("Not enough coffee")
    else:
        RESOURCES[WATER] -= int(dicti["water"])
        RESOURCES[MILK] -= int(dicti["milk"])
        RESOURCES[COFFEE] -= int(dicti["coffee"])
        print("Coffee is ready")


def print_dict(dict):
    for i in dict.keys():
        print(i, ':', dict[i])
    return


def main():
    print("I'm a simple coffee maker")
    print("The commands are:")
    for i in commands:
        print(i.capitalize(), end=" ")
    print()
    print("Choose a command")
    ref = False
    for comm in sys.stdin:
        if comm == "exit\n":
            break
        elif comm == "list\n":
            print(CAPPUCCINO.capitalize())
            print(AMERICANO.capitalize())
            print(ESPRESSO.capitalize())
        elif comm == "make\n":
            print("Which coffee?")
        elif comm == "cappuccino\n":
            make_coffee(comm)
        elif comm == "americano\n":
            make_coffee(comm)
        elif comm == "espresso\n":
            make_coffee(comm)
        elif comm == "refill\n":
            print("What do you want to refill ?")
            ref = True
        elif comm == "status\n":
            print_dict(RESOURCES)
        elif comm == "all\n" and ref is True:
            RESOURCES[WATER] = 100
            RESOURCES[MILK] = 100
            RESOURCES[COFFEE] = 100
            ref = False
        elif comm == "water\n" and ref is True:
            RESOURCES[WATER] = 100
            ref = False
        elif comm == "milk\n" and ref is True:
            RESOURCES[MILK] = 100
            ref = False
        elif comm == "coffee\n" and ref is True:
            RESOURCES[COFFEE] = 100
            ref = False
        else:
            print("Enter command:")


if __name__ == "__main__":
    main()

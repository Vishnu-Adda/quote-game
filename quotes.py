from random import choice
from pyfiglet import figlet_format
from termcolor import colored

# Header w/ random colors, just for flair :)
colors = ("grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white")

header = figlet_format("GUESS THE QUOTE")
header = colored(header, color=choice(colors))
print(header)

# Scraping portion

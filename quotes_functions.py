"""
Separate file for functions
"""
from random import choice
from pyfiglet import figlet_format
from termcolor import colored


# Making the header for flair
def header_init():
    colors = ("grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white")
    header = figlet_format("GUESS THE QUOTE")
    header = colored(header, color=choice(colors))
    print(header)

import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader
from quotes_functions import header_init, goodbye

# Init calls
header_init()


# Game portion
base_url = "http://quotes.toscrape.com/"


def read_quotes(filename):
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    print("Here's a quote: ")
    print(quote['text'])
    print(quote['author'])
    guess = ''
    while guess.lower() != quote['author'].lower() and remaining_guesses > 0:
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}\n")
        if guess == quote['author'].lower():
            print("YOU GOT IT RIGHT!")
            break
        remaining_guesses -= 1
        print_hint(quote, remaining_guesses)

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Do you want to play again? (y/n)")
    if again.lower() in ('yes', 'y'):
        print("OK, LET'S PLAY AGAIN")
        return start_game(quotes)  # executes start_game() while terminating the current function
    else:
        goodbye()


def print_hint(quote, remaining_guesses):
    if remaining_guesses == 3:
        res = requests.get(f"{base_url}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(f"Hint: The author was born on {birth_date} {birth_place}")
    elif remaining_guesses == 2:
        print(f"Hint: The author's first name starts with '{quote['author'][0]}'")
    elif remaining_guesses == 1:
        last_initial = quote['author'].split(" ")[1][0]
        print(f"Hint: The author's last name starts with '{last_initial}'")
    else:
        print(f"Sorry, you ran out of guesses. The answer was '{quote['author']}'")


scraper_quotes = read_quotes("quotes.csv")
start_game(scraper_quotes)

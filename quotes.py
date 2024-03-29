# http://quotes.toscrape.com/
from quotes_functions import header_init, goodbye

# Init calls
header_init()


# Scraping portion
print("Wait while we're scraping!")


def scrape_quotes():
    all_quotes = []
    url = "/page/1"
    while url:
        res = requests.get(f"{base_url}{url}")
        # print(f"Now Scraping {base_url}{url}...")
        soup = BeautifulSoup(res.text, "html.parser")
        quotes = soup.find_all(class_="quote")

        for quote in quotes:
            all_quotes.append({
                "text": quote.find(class_="text").get_text(),
                "author": quote.find(class_="author").get_text(),
                "bio-link": quote.find("a")["href"]
            })

        next_btn = soup.find(class_="next")
        url = next_btn.find("a")["href"] if next_btn else None
        sleep(1)  # So we don't overload their server (or attract attention)
    return all_quotes


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

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Do you want to play again? (y/n)")
    if again.lower() in ('yes', 'y'):
        print("OK, LET'S PLAY AGAIN")
        return start_game(quotes)  # executes start_game() while terminating the current function
    else:
        goodbye()


quotes_scraped = scrape_quotes()
start_game(quotes_scraped)

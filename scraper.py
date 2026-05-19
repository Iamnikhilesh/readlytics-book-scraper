import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://books.toscrape.com/catalogue/"
books_data = []

def get_rating(word):
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return ratings.get(word, 0)

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text.strip()
        rating_word = book.find("p", class_="star-rating")["class"][1]
        rating = get_rating(rating_word)

        books_data.append({
            "Title": title,
            "Price (£)": price,
            "Rating": rating
        })

    # Follow "next" page
    next_btn = soup.find("li", class_="next")
    if next_btn:
        next_page = BASE_URL + next_btn.a["href"]
        scrape_page(next_page)

# Start scraping
scrape_page("https://books.toscrape.com/catalogue/page-1.html")

# Save to CSV
df = pd.DataFrame(books_data)
df.to_csv("books.csv", index=False)
print(f"Done! Scraped {len(df)} books.")
print(df.head())
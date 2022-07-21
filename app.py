from datetime import datetime, timedelta, timezone
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from flask import Flask

app = Flask(__name__)


def get_menu():
    # Step 1: Download HTML from website
    url = "https://www.chipcitycookies.com/chip-nyc-menu/"
    response = requests.get(url)
    cookie_html = response.text

    # Step 2: Parse the cookie menu out of the HTML
    soup = BeautifulSoup(cookie_html)
    results = soup.findAll("div", {"role": "gridcell"})

    day_of_week = (
        datetime.now(timezone(timedelta(hours=-5), "EST")).strftime("%A").upper()
    )

    cookie_tokens = []
    for daily_cookie in results:

        if day_of_week in daily_cookie.text:

            tags = daily_cookie.find_all()
            for tag in tags:
                for text in tag.contents:
                    if isinstance(text, NavigableString):
                        cleaned_texts = text.split("\n")
                        for t in cleaned_texts:
                            if t.strip() and t.strip() not in cookie_tokens:
                                cookie_tokens.append(t.strip())

    text_message = "\n".join(cookie_tokens)
    return text_message


@app.route("/")
def index():
    return get_menu()


if __name__ == "__main__":
    app.run(debug=True)

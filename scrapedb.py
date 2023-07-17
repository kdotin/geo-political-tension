import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_bbc():
    # Connect to SQLite database (or create it)
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (headline text, url text, content text)''')

    # Make a request to the website
    r = requests.get("https://www.bbc.co.uk/news")
    r.content

    # Use the 'html.parser' to parse the page content and store it in a variable.
    soup = BeautifulSoup(r.content, "html.parser")

    # Find all the news headlines on the page
    headline_containers = soup.find_all(class_="gs-c-promo")

    articles = []

    # Loop through the found headlines and print them
    for container in headline_containers[:5]:
        article = {}
        headline = container.find(class_="gs-c-promo-heading__title gel-paragon-bold nw-o-link-split__text")
        if headline:
            article['headline'] = headline.text

        link = container.find('a')
        if link and 'href' in link.attrs:
            article['url'] = "https://www.bbc.co.uk" + link['href']
            r = requests.get(article['url'])
            soup = BeautifulSoup(r.content, "html.parser")
            headline = soup.find('h1', class_='ssrcss-15xko80-StyledHeading e1fj1fc10')
            if headline:
                article['headline'] = headline.text
            content = soup.find('main', {'id': 'main-content'})
            if content:
                article['content'] = content.text

        # Insert article into database
        c.execute("INSERT INTO articles VALUES (?, ?, ?)",
                  (article.get('headline', 'No headline found'),
                   article.get('url', 'No URL found'),
                   article.get('content', 'No content found')))

    # Save (commit) the changes and close the connection to the database
    conn.commit()
    conn.close()

scrape_bbc()

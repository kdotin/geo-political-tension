import requests
from bs4 import BeautifulSoup

def scrape_bbc():
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

        articles.append(article)

    return articles

articles = scrape_bbc()
for article in articles:
    print(f"Headline: {article.get('headline', 'No headline found')}")
    print(f"URL: {article.get('url', 'No URL found')}")
    print(f"Content: {article.get('content', 'No content found')}\n\n")

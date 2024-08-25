import requests
import json
from bs4 import BeautifulSoup
from newspaper import Article

def google_search(query, api_key, cse_id):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
    }
    
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()
    return search_results.get("items", [])
    

def generate_google_dork(query):
    # Basic Google Dorking example, can be expanded as needed
    dork = f'""{query}""'
    return dork

def main():
    # Example: Replace with actual Google API key and Custom Search Engine ID
    api_key = "AIzaSyBEKYB4x20THfOTVegLSCkbDxhxvSBHe4I"
    cse_id = "436ab97bfc11f461e"
    
    user_input = input("Enter news headline or keywords: ")
    dork_query = generate_google_dork(user_input)
    
    print(f"Generated Google Dorking Query: {dork_query}")
    
    results = google_search(dork_query, api_key, cse_id)
    
    if not results:
        print("No results found.")
    else:
        # print("\nTop search results:")
        # with open('links.json', 'w') as json_file:
        #     for result in results:
        #         json_file.write(json.dumps(result["link"]) + '\n')
        # print()
        print("\nTop search results:")
        with open('links.json', 'w') as json_file:
            json.dump([result["link"] for result in results], json_file, indent=4)
        print()

def scrape_article(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return {
        "title": article.title,
        "author": article.authors,
        "date": article.publish_date,
        "summary": article.summary,
        "keywords": article.keywords
    }

def scrape_articles_from_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    if data["results"] == "No results found":
        return "No results found"

    articles = []
    for link in data["links"]:
        article_data = scrape_article(link)
        articles.append(article_data)

    return articles

if __name__ == "__main__":
    main()
    file_path = "links.json"
    articles = scrape_articles_from_json(file_path)
    print(articles)

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

visited_urls = set() 

def save_data_to_file(url, content, depth):
    
    directory = f"data/level_{depth}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    
    filename = os.path.join(
        directory, 
        url.replace("https://", "").replace("/", "_") + ".txt")
    
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"URL: {url}\n\n")
        file.write(content)

def crawl(url, depth, max_depth):
    
    if depth > max_depth:
        return
    
    if url in visited_urls:
        return  
    
    visited_urls.add(url) 
    
    try:
        response = requests.get(url)
        response.raise_for_status()  
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        
        save_data_to_file(url, soup.get_text(), depth)
        
        for link in soup.find_all('a', href=True):
            sub_link = urljoin(url, link['href'])
            crawl(sub_link, depth + 1, max_depth)

    except requests.RequestException as e:
        print(f"Failed to retrieve URL: {url} - {e}")

def main():
    parent_url = "https://www.tymeline.app/"
    max_depth = 2
    crawl(parent_url, 0, max_depth)

if __name__ == "__main__":
    main()

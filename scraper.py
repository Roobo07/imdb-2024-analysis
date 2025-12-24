from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import sqlite3
import os
import time

def scrape_imdb():
    # This will open a Chrome window on your computer
    driver = webdriver.Chrome() 
    driver.get("https://www.imdb.com/search/title/?release_date=2024-01-01,2024-12-31&sort=num_votes,desc")
    time.sleep(5)

    movies = []
    items = driver.find_elements(By.CSS_SELECTOR, ".ipc-metadata-list-summary-item")

    for item in items[:50]: 
        try:
            title = item.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text.split(". ", 1)[-1]
            rating = item.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text
            votes = item.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--voteCount").text.strip('()')
            
            # Basic cleaning for votes
            v = votes.replace('K', '000').replace('M', '000000').replace('.', '').replace(',', '')
            
            movies.append({
                "Title": title, 
                "Rating": float(rating), 
                "Votes": int(v) if v.isdigit() else 0,
                "Genre": "Action" # Placeholder
            })
        except: continue

    driver.quit()
    df = pd.DataFrame(movies)

    # Save to SQL
    conn = sqlite3.connect("imdb_2024.db")
    df.to_sql("movies_2024", conn, if_exists="replace", index=False)
    conn.close()
    print("Scraping complete and Database created!")

if __name__ == "__main__":
    scrape_imdb()
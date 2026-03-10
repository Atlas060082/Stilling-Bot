from bs4 import BeautifulSoup
import requests

page_to_scrape = "https://www.finn.no/job/sea"
response = requests.get(page_to_scrape)
soup = BeautifulSoup(response.text, "html.parser")

# Debug: Skriv ut hele siden for å se strukturen
print("=== HELE HTML ===")
print(soup.prettify()[:2000])  # Første 2000 tegn

print("\n=== SØKER ETTER TITLER ===")
title = soup.find_all("h2", attrs={"class": "t2 md:t1 mb-6"})
print(f"Fant {len(title)} titler")

print("\n=== SØKER ETTER DEADLINES ===")
deadline = soup.find_all("span", attrs={"class": "mt-2 font-bold"})
print(f"Fant {len(deadline)} deadlines")

print("\n=== SØKER ETTER SELSKAPER ===")
company = soup.find_all("p", attrs={"class": "mb-24"})
print(f"Fant {len(company)} selskaper")
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(page_to_scrape, headers=headers)

print = ("text")
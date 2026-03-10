from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from urllib.parse import quote

class FinnJobbScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self._start_browser()

    def _start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

    def hent_annonser(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
        )
        time.sleep(2)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        self.driver.quit()


#Noe galt med attribute på H2, skal undersøke nærmere
        jobber = []
        for annonse in soup.find_all("article"):
            jobber.append({
                "tittel": annonse.find("h2", class_="t2 md:t1 mb-6").text.strip() if annonse.find("h2") else "Ukjent",
                "url": annonse.find("a")["href"] if annonse.find("a") else ""
            })
        return jobber


søkeord = quote("Lærling IT")
scraper = FinnJobbScraper(f"https://www.finn.no/job/fulltime/search.html?q={søkeord}")
resultater = scraper.hent_annonser()

for jobb in resultater:
    print(jobb["tittel"])
    print(jobb["url"])
    print("---")
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import quote


class FinnJobbScraper:
    def __init__(self):
        """
        Konstruktør - vi starter IKKE browser her lenger
        (Det er bedre å gjøre det i hent_annonser())
        """
        self.base_url = "https://www.finn.no/job/fulltime/search.html"
    
    async def hent_annonser(self, search_term):
        """
        Hent jobbannonser fra Finn.no
        
        Args:
            search_term: f.eks "Lærling IT"
        
        Returns:
            Liste med dicts: [{'tittel': '...', 'url': '...'}, ...]
        """
        
        # URL-encoding av søkeord
        encoded_query = quote(search_term)
        url = f"{self.base_url}?q={encoded_query}"
        
        print(f"Henter jobber fra Finn.no for: '{search_term}'")
        print(f"URL: {url}\n")
        
        # START PLAYWRIGHT CONTEXT
        async with async_playwright() as p:
            # Åpne browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # Gå til siden og vent til nettet er ferdig
                print("Laster side...")
                await page.goto(url, wait_until='networkidle', timeout=30000)
                print("Side lastet!\n")
                
                # Hent fullstendig HTML (JavaScript har kjørt)
                html = await page.content()
                
                # Parse med BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                
                # Finn alle jobber
                articles = soup.find_all('article')
                print(f"Fant {len(articles)} jobbannonser\n")
                
                jobber = []
                for annonse in articles:
                    jobb = self._extract_job_data(annonse)
                    if jobb:
                        jobber.append(jobb)
                
                print(f"Ekstrahert {len(jobber)} jobber med data\n")
                return jobber
            
            except Exception as e:
                print(f"Feil ved scraping: {e}")
                return []
            
            finally:
                # Lukk browser (kjøres alltid, selv ved feil)
                await browser.close()
    
    def _extract_job_data(self, annonse):
        """
        Hent data fra en enkelt jobbannonse
        
        Args:
            annonse: BeautifulSoup-element (article-tag)
        
        Returns:
            Dict med jobdata eller None hvis parsing feilet
        """
        try:
            # Hent tittel fra <a class="job-card-link">
            tittel_link = annonse.find("a", class_="job-card-link")
            if not tittel_link:
                return None
            tittel = tittel_link.get_text(strip=True)
            
            # Hent URL fra samme link
            url = tittel_link.get("href", "")
            if not url:
                return None
            
            # Gjør URL komplett hvis den er relativ
            if not url.startswith("http"):
                url = "https://www.finn.no" + url
            
            # Hent firma - <div class="text-caption"><strong>
            firma_elem = annonse.find("div", class_="text-caption")
            firma = firma_elem.get_text(strip=True) if firma_elem else "N/A"
            
            # Hent sted - <span class="block truncate"> inne i første <li>
            location_span = annonse.find("span", class_="block truncate")
            location = location_span.get_text(strip=True) if location_span else "N/A"
            
            # Returner data
            return {
                "tittel": tittel,
                "firma": firma,
                "sted": location,
                "url": url
            }
        
        except Exception as e:
            print(f"Feil ved parsing av jobb: {e}")
            return None


async def main():
    """Hovedfunksjon"""
    scraper = FinnJobbScraper()
    
    # Søk etter jobber
    resultater = await scraper.hent_annonser("Lærling IT")
    
    # Skriv ut resultater
    print("=" * 60)
    print("RESULTATER:")
    print("=" * 60)
    for i, jobb in enumerate(resultater, 1):
        print(f"\n{i}. {jobb['tittel']}")
        print(f"   Firma: {jobb['firma']}")
        print(f"   Sted: {jobb['sted']}")
        print(f"   URL: {jobb['url']}")


if __name__ == "__main__":
    asyncio.run(main())
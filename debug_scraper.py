import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

search_term = "Lærling IT"
encoded_query = quote(search_term)
url = f"https://www.finn.no/job/fulltime/search.html?q={encoded_query}"

print(f"Henter: {url}\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    print(f"Status code: {response.status_code}\n")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.find_all('article')
    print(f"Fant {len(articles)} article-elementer\n")
    
    if articles:
        print("=" * 60)
        print("FØRSTE ARTICLE HTML (første 3000 tegn):")
        print("=" * 60)
        print(articles[0].prettify()[:3000])
        print("\n")
        
        print("=" * 60)
        print("TESTER INNHOLD I FØRSTE ARTICLE:")
        print("=" * 60)
        
        first = articles[0]
        
        h2s = first.find_all('h2')
        print(f"h2-tags: {len(h2s)}")
        for i, h2 in enumerate(h2s[:3]):
            print(f"  {i+1}. {h2.get_text(strip=True)[:100]}")
        
        as_list = first.find_all('a')
        print(f"\na-tags: {len(as_list)}")
        for i, a in enumerate(as_list[:3]):
            href = a.get('href', 'N/A')
            text = a.get_text(strip=True)[:50]
            print(f"  {i+1}. [{text}] href={href}")
        
        spans = first.find_all('span')
        print(f"\nspan-tags: {len(spans)}")
        for i, span in enumerate(spans[:3]):
            text = span.get_text(strip=True)[:80]
            classes = span.get('class', [])
            print(f"  {i+1}. [{text}] class={classes}")
    
    else:
        print("Ingen articles funnet! HTML inneholder:")
        print(response.text[:2000])

except Exception as e:
    print(f"Feil: {e}")
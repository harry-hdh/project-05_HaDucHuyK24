import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from utils import save_to_csv, read_product_csv

CSV_FILE_PATH1 = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info_referrer_url.csv"
CSV_FILE_PATH2 = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info.csv"
SAVE_PATH1 = "/home/hdh99/project-05_HaDucHuyK24/outcome_data/product_info_with_titles.csv"

#ua = UserAgent()

async def fetch_and_parse(session, url, semaphore): # Controls how many requests
    async with semaphore:
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        #     "Accept-Language": "en-US,en;q=0.9",
        # }
        try:
            # Set a timeout so a single slow website won't hang script indefinitely
            timeout = aiohttp.ClientTimeout(total=15)
            async with session.get(url, timeout=timeout) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    title_tag = soup.find('span', class_='base', attrs={"data-ui-id": "page-title-wrapper"})
                    title = title_tag.text.strip() if title_tag else 'No Title Found'
                    return {"referrer_url": url, "title": title}
                else:
                    print(f"Failed to fetch {url}: Status {response.status}")
                    return {"referrer_url": url, "title": "Failed to Fetch"}
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return {"referrer_url": url, "title": "Error Fetching"}

async def scrape_main(save_path, urls):
    sem = asyncio.Semaphore(8)  #1. Limit to 8 concurrent requests
    # 2. Initialize a single client session
    async with aiohttp.ClientSession() as session:
        # 3. Create tasks for all URLs
        tasks = [fetch_and_parse(session, url, sem) for url in urls]
        # 4. Gather results
        results = await asyncio.gather(*tasks)
        # 5. Save results to CSV
        save_to_csv(results, ["referrer_url", "title"], save_path)



# URLS = [record["referrer_url"] for record in read_product_csv(CSV_FILE_PATH1)]
# asyncio.run(scrape_main(SAVE_PATH1))
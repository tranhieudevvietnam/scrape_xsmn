import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_xsmn(date_str):
    url = f'https://xoso.com.vn/xsmn-{date_str}.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = {}
    prize_blocks = soup.select('.results .row')
    for block in prize_blocks:
        prize_name_el = block.select_one('.prize')
        if not prize_name_el:
            continue
        prize_name = prize_name_el.get_text(strip=True)
        prize_numbers = [el.get_text(strip=True) for el in block.select('.number')]
        results[prize_name] = prize_numbers
    return results

if __name__ == '__main__':
    fetch_date = os.getenv('FETCH_DATE')
    if not fetch_date:
        fetch_date = datetime.now().strftime('%d-%m-%Y')

    print(f"Fetching xổ số miền Nam ngày {fetch_date}...")

    data = scrape_xsmn(fetch_date)

    # Tạo thư mục data nếu chưa có
    os.makedirs('data', exist_ok=True)

    filename = f'data/xsmn_{fetch_date}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Đã lưu kết quả vào file {filename}")

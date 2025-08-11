import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_xsmn(date_str):
    url = f'https://xoso.com.vn/xsmn-{date_str}.html'
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = {}

    # Tìm bảng kết quả xổ số miền Nam
    table = soup.find('table', class_='tbl_result')
    if not table:
        print("Không tìm thấy bảng kết quả.")
        return results

    # Mỗi hàng trong table là 1 giải
    for tr in table.find_all('tr'):
        prize_name_td = tr.find('td', class_='prize')
        numbers_td = tr.find_all('td', class_='number')
        if prize_name_td and numbers_td:
            prize_name = prize_name_td.get_text(strip=True)
            numbers = [td.get_text(strip=True) for td in numbers_td if td.get_text(strip=True)]
            results[prize_name] = numbers

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

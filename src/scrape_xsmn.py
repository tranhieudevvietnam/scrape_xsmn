import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

def scrape_xsmn(date_str):
    url = f'https://xoso.com.vn/xsmn-{date_str}.html'
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Không lấy được trang cho ngày {date_str}, status: {resp.status_code}")
        return None
    soup = BeautifulSoup(resp.text, 'html.parser')

    results = {}

    table = soup.find('table', class_='table-result table-xsmn')
    if not table:
        print(f"Không tìm thấy bảng kết quả cho ngày {date_str}.")
        return None

    for tr in table.find_all('tr'):
        prize_name_td = tr.find('td', class_='prize')
        numbers_td = tr.find_all('td', class_='number')
        if prize_name_td and numbers_td:
            prize_name = prize_name_td.get_text(strip=True)
            numbers = [td.get_text(strip=True) for td in numbers_td if td.get_text(strip=True)]
            results[prize_name] = numbers

    return results if results else None

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)

if __name__ == '__main__':
    month = os.getenv('FETCH_MONTH')  # định dạng MM-YYYY, vd: 08-2025
    if not month:
        print("Bạn chưa truyền biến môi trường FETCH_MONTH theo định dạng MM-YYYY, ví dụ 08-2025")
        exit(1)

    try:
        month_dt = datetime.strptime(month, '%m-%Y')
    except:
        print("Định dạng FETCH_MONTH không hợp lệ. Phải là MM-YYYY, ví dụ 08-2025")
        exit(1)

    start_date = month_dt.replace(day=1)
    if month_dt.month == 12:
        end_date = month_dt.replace(year=month_dt.year+1, month=1, day=1) - timedelta(days=1)
    else:
        end_date = month_dt.replace(month=month_dt.month+1, day=1) - timedelta(days=1)

    os.makedirs('data', exist_ok=True)

    for single_date in daterange(start_date, end_date):
        date_str = single_date.strftime('%d-%m-%Y')
        print(f"Fetching ngày {date_str} ...")
        data = scrape_xsmn(date_str)
        if data:
            filename = f'data/xsmn_{date_str}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Đã lưu kết quả vào {filename}")
        else:
            print(f"Không có dữ liệu ngày {date_str} hoặc lỗi lấy dữ liệu.")
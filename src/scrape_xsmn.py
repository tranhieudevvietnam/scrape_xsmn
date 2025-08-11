import requests
from bs4 import BeautifulSoup
import json

def scrape_xsmn(date_str):
    url = f'https://xoso.com.vn/xsmn-{date_str}.html'
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print(f"Không lấy được trang cho ngày {date_str}, status: {resp.status_code}")
        return None

    soup = BeautifulSoup(resp.text, 'html.parser')

    table = soup.find('table', class_='table-result table-xsmn')
    if not table:
        print(f"Không tìm thấy bảng kết quả ngày {date_str}")
        return None

    # Lấy tên các tỉnh (header cột) từ thead
    headers = [th.get_text(strip=True) for th in table.thead.find_all('th')]
    # headers ví dụ: ['G', 'TPHCM', 'Đồng Tháp', 'Cà Mau']

    results = {}
    num_provinces = len(headers) - 1  # trừ cột "G" đầu tiên

    for row in table.tbody.find_all('tr'):
        prize_name = row.find('th').get_text(strip=True)  # Tên giải: G8, G7,..., ĐB
        tds = row.find_all('td')

        for i in range(min(len(tds), num_provinces)):
            province = headers[i + 1]  # i+1 vì cột 0 là cột giải
            numbers = [span.get_text(strip=True) for span in tds[i].find_all('span', class_='xs_prize1')]
            if province not in results:
                results[province] = {}
            results[province][prize_name] = numbers

    return results

if __name__ == "__main__":
    date_str = "11-08-2025"  # Thay ngày bạn muốn lấy dữ liệu vào đây
    data = scrape_xsmn(date_str)
    if data:
        filename = f"xsmn_{date_str}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Đã lưu dữ liệu xổ số miền Nam ngày {date_str} vào file {filename}")
    else:
        print("Không lấy được dữ liệu.")

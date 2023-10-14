import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Khởi tạo trình duyệt (ví dụ: Google Chrome)
driver = webdriver.Chrome()
matchs_by_date = {"listMatchs": {}}

for page_num in range(1, 5):  # Số trang cần lấy (tùy chọn)
    # Tạo URL cho mỗi trang
    url = (
        f"https://www.hkfa.com/en/competitions/fixtures?year=2023-2024&page={page_num}"
    )
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".container"))
    )
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Lấy thông tin về các trận đấu
    match_items = soup.find_all(class_="mb-5")
    # Trích xuất thông tin từ từng trận đấu
    for match_item in match_items:
        match_info_parts = match_item.text.strip().split("\n")
        if len(match_info_parts) >= 9:
            date = match_info_parts[0].strip()

            match_obj = {
                "match_time": match_info_parts[4].strip(),
                "home_score": match_info_parts[2].strip(),
                "guest_score": match_info_parts[3].strip(),
                "match_id": 41185,
                "match_date": match_info_parts[0].strip(),
                "match_round": "d",
                "match_ticket": match_info_parts[-1].strip(),
                "matchStatus": "g",
                "match_status": "e",
                "venue_id": "W",
                "live_icon": [],
                "Venue": {"venue_id": "W", "VenueName": "aF"},
            }
            
            if date not in matchs_by_date["listMatchs"]:
                matchs_by_date["listMatchs"][date] = []
            
            matchs_by_date["listMatchs"][date].append(match_obj)

    print(f"Lấy dữ liệu từ trang {page_num}")

# Đóng trình duyệt
driver.quit()

# Lưu dữ liệu vào file JSON
output_file = "match_data.json"
with open(output_file, "w") as json_file:
    json.dump(matchs_by_date, json_file, indent=4)

print(f"Dữ liệu đã được lưu vào file: {output_file}")

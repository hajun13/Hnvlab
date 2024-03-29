from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import requests
import os
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 이미지를 저장할 폴더 생성
folder_path = 'downloaded_images'
os.makedirs(folder_path, exist_ok=True)

def save_image(url, folder_path, keyword, idx):
    try:
        response = requests.get(url, timeout=10)  # 타임아웃 설정 추가
        if response.status_code == 200:
            file_path = os.path.join(folder_path, f"{keyword}_{idx}.jpg")
            with open(file_path, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print(f"Error - Could not download {url} - {e}")


def scroll_down(driver):
    """페이지 하단까지 스크롤 다운하고 페이지 로딩 대기"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # 페이지가 로드되기를 기다립니다.

# 크롬 드라이버 초기화
path = '/home/hajun/Projects/image/chromedriver-linux64/chromedriver'
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/google-chrome"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--pageLoadStrategy=none")

service = Service(executable_path=path, log_path='chromedriver.log', service_args=['--verbose'])
driver = webdriver.Chrome(service=service, options=chrome_options)

# 구글 이미지 검색 페이지 접속
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")

# 검색어 입력 및 검색 실행
searchKey = input('검색 키워드 입력:')
search_box = driver.find_element(By.NAME, 'q')
search_box.send_keys(searchKey)
search_box.send_keys(Keys.RETURN)

# 이미지 URL 수집
image_urls = set()
while len(image_urls) < 500:
    scroll_down(driver)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.Q4LuWd")))
    images = driver.find_elements(By.CSS_SELECTOR, 'img.Q4LuWd')
    for image in images:
        src = image.get_attribute('src')
        if src and src.startswith('http') and src not in image_urls:
            image_urls.add(src)
            if len(image_urls) >= 500:
                break

# 이미지 다운로드
for idx, url in enumerate(list(image_urls)[:500]):
    save_image(url, folder_path, searchKey, idx)

# 드라이버 종료
driver.close()

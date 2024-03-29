
import ssl
import urllib.request
ssl_context = ssl.create_default_context()
ssl_context.options &= ~ssl.OP_LEGACY_SERVER_CONNECT  # 안전하지 않은 재협상 비활성화

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import urllib.request
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests



# SSL 컨텍스트 생성


# SSL 컨텍스트와 함께 urlopen 사용
response = urllib.request.urlopen("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl", context=ssl_context)

# response = requests.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
searchKey = input('검색 키워드 입력:')
path = '/home/hajun/Projects/image/chromedriver-linux64/chromedriver'
chrome_options = Options()
chrome_options.binary_location = "/usr/bin/google-chrome"
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

service = Service(executable_path=path, log_path='chromedriver.log', service_args=['--verbose'])
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")
elem = driver.find_element("name", "q")

elem.send_keys(searchKey)
elem.send_keys(Keys.RETURN)

SCROLL_PAUSE_TIME = 1
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
        except:
            break
    last_height = new_height

images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
count = 1
max_images = 500  # 목표 이미지 수 설정

downloaded_urls = set()  # 이미 다운로드한 이미지 URL 저장을 위한 세트 초기화

for image in images:
    if count > max_images:  # 원하는 이미지 수에 도달했는지 확인
        break  # 500장의 이미지가 다운로드되면 반복문 탈출

    try:
        image.click()
        time.sleep(0.5)

        imgUrl = driver.find_element(
            By.XPATH,
            '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]'
        ).get_attribute("src")

        if imgUrl in downloaded_urls:  # 이미 다운로드된 URL인 경우 건너뜀
            continue

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')
        ]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(imgUrl, f'./imgs/{searchKey}{str(count)}.jpg')
        count += 1  # 성공적인 다운로드 시에만 카운트 증가
        downloaded_urls.add(imgUrl)  # 다운로드한 URL을 세트에 추가

    except Exception as e:
        print(f'{count}번째 이미지 다운로드 중 오류 발생: ', e)
        continue  # 현재 이미지를 건너뛰고 다음 이미지로 계속 진행

driver.close()  # 모든 작업 완료 후 드라이버 닫기
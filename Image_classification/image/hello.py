import ssl
import urllib.request

# SSL 보안 컨텍스트 설정
ssl_context = ssl.create_default_context()
# 안전하지 않은 SSL 재협상 비활성화
ssl_context.options &= ~ssl.OP_LEGACY_SERVER_CONNECT

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

# SSL 컨텍스트를 사용하여 웹페이지 열기
response = urllib.request.urlopen("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl", context=ssl_context)

# 사용자로부터 이미지 검색 키워드 입력 받기
searchKey = input('검색 키워드 입력:')

# Chrome 드라이버 경로 설정
path = '/home/hajun/Projects/image/chromedriver-linux64/chromedriver'

# Chrome 옵션 설정
chrome_options = Options()
# 머리 없는 모드로 실행
chrome_options.add_argument("--headless")
# 샌드박스 모드 비활성화
chrome_options.add_argument("--no-sandbox")
# /dev/shm 파티션 사용 비활성화
chrome_options.add_argument("--disable-dev-shm-usage")
# 창 크기 설정
chrome_options.add_argument("--window-size=1920,1080")

# Chrome 드라이버 서비스 설정
service = Service(executable_path=path, log_path='chromedriver.log', service_args=['--verbose'])

# 드라이버 초기화
driver = webdriver.Chrome(service=service, options=chrome_options)

# Google 이미지 검색 페이지로 이동
driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl")

# 검색창 찾기 및 검색어 입력 후 검색 실행
elem = driver.find_element("name", "q")
elem.send_keys(searchKey)
elem.send_keys(Keys.RETURN)

# 스크롤 다운을 위한 대기 시간 설정
SCROLL_PAUSE_TIME = 1

# 페이지의 마지막 높이 가져오기
last_height = driver.execute_script("return document.body.scrollHeight")

# 더 많은 이미지 결과를 로드하기 위해 페이지 끝까지 스크롤 다운
while True:
    # 페이지 끝까지 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 페이지 로드를 기다림
    time.sleep(SCROLL_PAUSE_TIME)
    # 새로운 스크롤 높이 계산 및 이전 스크롤 높이와 비교
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            # "결과 더보기" 버튼이 있으면 클릭
            driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()
        except:
            # 더 이상 스크롤할 페이지가 없으면 반복 종료
            break
    last_height = new_height

# 이미지 요소 선택
images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
count = 1
for image in images:
    try:
        # 이미지 클릭
        image.click()
        time.sleep(0.5)
        
        # 큰 이미지의 URL 가져오기
        imgUrl = driver.find_element(
            By.XPATH,
            '//*[@id="Sva75c"]/div[2]/div[2]/div[2]/div[2]/c-wiz/div/div/div/div/div[3]/div[1]/a/img[1]'
        ).get_attribute("src")

        # 이미지 다운로드를 위한 사용자 에이전트 설정
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')
        ]
        urllib.request.install_opener(opener)

        # 이미지 다운로드 및 저장
        urllib.request.urlretrieve
                # 이미지 다운로드 및 저장
        urllib.request.urlretrieve(imgUrl, f'./imgs/{searchKey}{str(count)}.jpg')
        count += 1  # 다운로드한 이미지 수를 증가
    except Exception as e:  # 예외 처리
        print('오류 발생: ', e)  # 오류 메시지 출력
        pass  # 오류 발생 시 해당 이미지 건너뛰고 다음 이미지로 이동

# 모든 작업이 끝나면 웹드라이버 종료
driver.close()


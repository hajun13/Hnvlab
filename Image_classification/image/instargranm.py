import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import io
import time
# 크롬드라이버 위치 설정
DRIVER_PATH = '/home/hajun/Projects/image/chromedriver-linux64/chromedriver'
# 크롬 드라이버 옵션 설정
listm=['IU', 'red velvet seulgi', 'Son Heung min',]
for i in listm:
  options = Options()
  options.add_argument('--headless')  # 창 안띄우기
  options.add_argument('--no-sandbox')  # 리눅스 환경에서 필요한 옵션
  options.add_argument('--disable-dev-shm-usage')  # 리눅스 환경에서 필요한 옵션
  # 검색어 설정
  search_name = i
  # 검색어를 이용한 구글 이미지 검색 url
  url = f'https://www.google.com/search?q={search_name}&source=lnms&tbm=isch'
  # 크롬 드라이버 실행
  service = Service(DRIVER_PATH)
  driver = webdriver.Chrome(service=service, options=options)
  # url 접속
  driver.get(url)
  # 페이지 로드를 위한 대기 시간
  time.sleep(2)
  # 이미지 로딩을 위한 스크롤 다운
  last_height = driver.execute_script("return document.body.scrollHeight")
  while True:
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(1)
      new_height = driver.execute_script("return document.body.scrollHeight")
      if new_height == last_height:
          break
      last_height = new_height
  # 이미지 링크 추출
  soup = BeautifulSoup(driver.page_source, 'html.parser')
  img_tags = soup.find_all('img')
  urls = []
  for img in img_tags:
      try:
          url = img['src']
          if 'http' in url:
              urls.append(url)
      except:
          pass
  # 이미지 다운로드
  os.makedirs(f'./{search_name}', exist_ok=True)
  count = 0
  for url in urls:
      try:
          response = requests.get(url, stream=True)
          # 이미지 사이즈 확인
          img = Image.open(io.BytesIO(response.content))
          width, height = img.size
          if width >= 20 and height >= 20:
              file_name = f'./{search_name}/{search_name}{count}.jpg'
              with open(file_name, 'wb') as out_file:
                  out_file.write(response.content)
              print(f'{file_name} saved')
              count += 1
              if count == 500:
                  break
      except:
          pass
  # 크롬 드라이버 종료
  driver.quit()
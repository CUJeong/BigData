from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import urllib.request

keywords = ["코리안숏헤어", "러시안블루", "말티즈", "포메라니안"]
count = 50

# 웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 창 최대화
driver = webdriver.Chrome(options=options)

# 이미지 검색 URL 접속
for keyword in keywords:
    driver.get(f"https://www.google.com/search?tbm=isch&q={keyword}")
    time.sleep(2)

    # 결과 스크롤 (더 많은 이미지 필요시 주석해제)
    # scroll_pause_time = 1
    # last_height = driver.execute_script("return document.body.scrollHeight")
    #
    # while True:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(scroll_pause_time)
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

    # 폴더 생성
    os.makedirs(keyword, exist_ok=True)

    # 썸네일 이미지 가져오기
    thumbnails = driver.find_elements(By.CSS_SELECTOR, ".H8Rx8c")
    print(f"총 썸네일 수: {len(thumbnails)}")

    # 이미지 저장
    num = 1
    for thumb in thumbnails:
        # 스크롤 및 클릭
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", thumb)
        time.sleep(0.3)

        # a 태그로 감싸진 것 대비: 강제 click 대신 자바스크립트로 click
        driver.execute_script("arguments[0].click();", thumb)
        time.sleep(1)

        # 고해상도 이미지 추출
        imgUrl = driver.find_element(By.CSS_SELECTOR, '.sFlh5c').get_attribute("src")
        print(imgUrl)
        if imgUrl and "http" in imgUrl:
            # 파일 저장
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)

            filepath = f"./{keyword}/{num:03d}.jpg"
            urllib.request.urlretrieve(imgUrl, filepath)
            print(f"✔ {num}번째 이미지 저장 완료: {filepath}")
            num += 1

        if num > count:
            print("✅ 요청한 수량만큼 저장 완료")
            break


driver.quit()

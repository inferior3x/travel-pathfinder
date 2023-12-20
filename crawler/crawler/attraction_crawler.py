import json
import random
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://www.tripadvisor.co.kr/"


def find_attraction(driver, place_keyword, number_of_items):
    # driver.get(url)

    # # 여행지 검색창 누르기
    # search_input = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "#lithium-root > main > div:nth-child(4) > div > div > div.ctKgY > div > form > div > div > input"))
    # )
    # search_input.clear()
    # search_input.send_keys(place_keyword)
    # search_input.send_keys(Keys.ENTER)

    # time.sleep(5)

    # # 즐길거리 클릭
    # things_to_do = driver.find_element(By.CSS_SELECTOR, "#search-filters > ul > li:nth-child(4) > a")
    # things_to_do.click()

    # time.sleep(5)
    # # 결과 데이터 추출
    # attractions_data = []
    # attractions_blocks = WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".location-meta-block"))
    # )[:29]

    # # 가능한 인덱스 범위 내에서 중복되지 않는 랜덤 인덱스 생성
    # random_indices = random.sample(range(len(attractions_blocks)), min(number_of_items * 2, len(attractions_blocks)))


    # for index in random_indices:
    #     block = attractions_blocks[index]
    #     name = block.find_element(By.CSS_SELECTOR, ".result-title").text.strip()
    #     address = block.find_element(By.CSS_SELECTOR, ".address-text").text.strip()
    #     attractions_data.append({"name": name, "address": address})

    attractions_data = []
    attractions_data.append({"name": "도쿄 디즈니시", "address": "1-13, Maihama, 우라야쓰, 치바(현), 관동, 일본"})
    attractions_data.append({"name": "도쿄 타워", "address": "4-2-8, Shibakoen, 미나토, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "오다이바", "address": "2-4-8, Daiba, 미나토, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "에도-도쿄 박물관", "address": "1-4-1 Yokoami, 스미다, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "도쿄역", "address": "1-9-1, Marunouchi, 치요다, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "모리 타워", "address": "6-10-1, Roppongi, 미나토, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "도쿄 스카이 트리", "address": "1 Chome-1-2, Oshiage, 스미다, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "리틀 도쿄", "address": "Downtown, 로스앤젤레스, 캘리포니아"})
    attractions_data.append({"name": "도쿄돔", "address": "1-3-61 Koraku, 분쿄, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "도쿄 국립 박물관", "address": "13-9, Uenokoen, 타이토, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "도쿄 도청", "address": "2-8-1, Nishishinjuku, 신주쿠, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "Tokyo Metropolitan Government Building Observation Decks", "address": "2-8-1, Nishishinjuku, 신주쿠, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "아사쿠사", "address": "Asakusa, 타이토, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "긴자 환락가", "address": "Ginza, 주오, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "도쿄 돔 시티", "address": "Koraku 1-3-61, 분쿄, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "센소지사", "address": "2-3-1, Asakusa, 타이토, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "도쿄도 현대 미술관", "address": "4-1-1 Miyoshi, 고토, 도쿄, 도쿄도, 관동, 일본"})
    attractions_data.append({"name": "도쿄 모노레일", "address": "미나토, 도쿄, 도쿄도, 관동, 일본"})
    # attractions_data.append({"name": "도쿄 대학", "address": "7-3-1 Hongo, 분쿄, 도쿄, 도쿄도, 관동, 일본"})
    # attractions_data.append({"name": "죠죠지", "address": "4-7-35, Shibakoen, 미나토, 도쿄, 도쿄도, 관동, 일본"})

    # 결과 출력
    return attractions_data
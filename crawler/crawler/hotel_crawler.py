import json
import random
import time
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 설정 파일 불러오기
with open('crawler/config/hotel_crawler.json', 'r') as config_file:
    config = json.load(config_file)

# 인원 수와 객실 수 초기화 함수
def reset_persons_and_rooms(driver):
    # 인원 수 줄이기 버튼
    persons_minus_click = driver.find_element(By.CSS_SELECTOR, "body > div.fh-sf-trigger-popup > div > div:nth-child(6) > div.right > div:nth-child(1) > i")
    persons_count = driver.find_element(By.CSS_SELECTOR, "body > div.fh-sf-trigger-popup > div > div:nth-child(6) > div.right > span").text
    # 객실 수 줄이기 버튼
    rooms_minus_click = driver.find_element(By.CSS_SELECTOR, "body > div.fh-sf-trigger-popup > div > div:nth-child(4) > div.right > div:nth-child(1) > i")
    rooms_count = driver.find_element(By.CSS_SELECTOR, "body > div.fh-sf-trigger-popup > div > div:nth-child(4) > div.right > span").text

    # 현재 설정된 인원 수와 객실 수를 확인하고 기본값으로 초기화
    current_persons = int(persons_count)
    current_rooms = int(rooms_count)

    # 객실 수 초기화
    while current_rooms > 1:
        rooms_minus_click.click()
        time.sleep(0.2)
        current_rooms -= 1
        time.sleep(0.2)

    # 인원 수 초기화
    while current_persons > 2:
        persons_minus_click.click()
        time.sleep(0.2)
        current_persons -= 1
        time.sleep(0.2)

def select_date(driver, current_date, checkin_date, date, is_checkout=False):

    # 달력 열기 (체크아웃 날짜 선택 시 이미 열려있는 경우 제외)
    if not is_checkout:
        day_open_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["day_open_btn"])
        day_open_btn.click()
        time.sleep(0.4)

    # 현재 달과 선택할 달 사이의 차이 계산
    # 체크아웃 날짜 선택 시 현재 달력 페이지를 고려
    current_month = current_date.month if not is_checkout else checkin_date.month
    target_month = date.month
    month_difference = (target_month - current_month) % 12

    # 필요한 경우 달력 페이지 넘김
    for _ in range(month_difference):
        next_month_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["month_next_btn"])
        next_month_btn.click()
        time.sleep(0.5)

    # 날짜 클릭
    day_btns = driver.find_elements(By.CSS_SELECTOR, config["selectors"]["day_btn"])
    for btn in day_btns:
        if btn.text == str(date.day):
            btn.click()
            break

# 날짜 객체 생성 함수
def create_date(year, month, day):
    try:
        return datetime(year, month, day)
    except ValueError:
        return None

# 인원, 객실 수 입력받으면 몇 번 클릭할지 계산
def person_and_room(persons, rooms):
    persons_click_times = 0
    rooms_click_times = 0

    if persons > 2:
        persons_click_times = persons - 2
    elif persons == 1:
        persons_click_times = -1

    if rooms != 1:
        rooms_click_times = rooms - 1

    return persons_click_times, rooms_click_times


def find_hotel_and_flight(driver, start_place, flight_destination, departure_date, return_date, person_number, room_number):

    departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d")
    return_date_obj = datetime.strptime(return_date, "%Y-%m-%d")
    # 연도, 월, 일 추출
    departure_month = departure_date_obj.month
    departure_day = departure_date_obj.day
    return_month = return_date_obj.month
    return_day = return_date_obj.day

    # 날짜 계산 전 현재 날짜 가져오기
    current_date = datetime.now()

    # 날짜 유효성 검사를 위한 수정된 부분
    current_year = current_date.year
    checkin_year = current_year if departure_month >= current_date.month else current_year + 1
    checkout_year = checkin_year if return_month >= departure_month else checkin_year + 1

    checkin_date = create_date(checkin_year, departure_month, departure_day)
    checkout_date = create_date(checkout_year, return_month, return_day)

    # 날짜 유효성 검사
    # 날짜 유효성 검사
    max_future_date = current_date + timedelta(days=11 * 30)  # 11개월 후


    if (checkin_date is None) or (checkout_date is None) or not (current_date <= checkin_date <= max_future_date and checkin_date < checkout_date <= max_future_date):
        return json.dumps({
            "success": False,
            "error_message": "잘못된 날짜 입력입니다.",
            },
            ensure_ascii=False)
    

    persons_click_time, rooms_click_time = person_and_room(person_number, room_number)

    driver.get(config["url"])

    # 출발지 항공편 입력
    start_search_btn = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, config["selectors"]["start_search_btn"]))
    )
    time.sleep(0.5)
    start_search_btn.click()

    time.sleep(0.2)
    start_search_btn.click()
    time.sleep(0.2)
    start_search = WebDriverWait(driver,1).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, config["selectors"]["start_search_btn"]))
    )
    start_search.clear()
    time.sleep(0.5)
    start_search.send_keys(start_place)

    time.sleep(0.5)

    # 도착지 항공편 검색
    flight_search_btn = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, config["selectors"]["flight_search_btn"]))
    )
    time.sleep(0.5)
    flight_search_btn.click()
    time.sleep(0.5)
    flight_search_btn.click()
    time.sleep(0.5)

    flight_search = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, config["selectors"]["flight_search_btn"]))
    )
    time.sleep(0.5)
    flight_search.clear()
    time.sleep(0.5)
    flight_search.send_keys(flight_destination)

    time.sleep(0.5)

    # 도착지 호텔 검색
    hotel_search_btn = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, config["selectors"]["hotel_search_btn"]))
    )
    time.sleep(0.5)
    hotel_search_btn.click()
    time.sleep(0.5)
    hotel_search = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, config["selectors"]["hotel_search_btn"]))
    )
    time.sleep(0.5)
    hotel_search.clear()
    time.sleep(0.5)
    hotel_search.send_keys(flight_destination)
    time.sleep(0.6)


    # 체크인 날짜 선택
    select_date(driver, current_date, checkin_date, checkin_date)

    # 체크아웃 날짜 선택
    select_date(driver, current_date, checkin_date, checkout_date, is_checkout=True)

    # 인원 수, 객실 선택
    persons_and_rooms_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["persons_and_rooms_btn"])
    persons_and_rooms_btn.click()

    time.sleep(0.2)
    reset_persons_and_rooms(driver)
    time.sleep(0.3)
    persons_plus_click = driver.find_element(By.CSS_SELECTOR, config["selectors"]["person_plus_btn"])
    persons_minus_click = driver.find_element(By.CSS_SELECTOR, config["selectors"]["person_minus_btn"])

    if persons_click_time == -1:
        persons_minus_click.click()
    else:
        for _ in range(persons_click_time):
            persons_plus_click.click()
            time.sleep(0.3)

    time.sleep(0.2)
    rooms_click_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["rooms_plus_btn"])
    for _ in range(rooms_click_time):
        rooms_click_btn.click()
        time.sleep(0.3)

    # 검색 시작
    search_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["search_btn"])
    search_btn.click()

    # 출발 항공편 정보 수집
    start_flight_info = {
        "airline": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_airline"]).text,
        "start_time": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_start_time"]).text,
        "start_airport": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_start_airport"]).text,
        "end_time": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_end_time"]).text,
        "end_airport": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_end_airport"]).text,
        "time_required": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_time"]).text
    }

    # 귀환 항공편 정보 수집
    comeback_flight_info = {
        "airline": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_airline"]).text,
        "start_time": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_start_time"]).text,
        "start_airport": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_start_airport"]).text,
        "end_time": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_end_time"]).text,
        "end_airport": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_end_airport"]).text,
        "time_required": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_time"]).text
    }


    #랜덤으로 호텔 가져오기

    # 호텔 카드들을 가져오기
    hotel_cards = driver.find_elements(By.CLASS_NAME, "hotel-card")

    # 호텔 카드가 없다면, 더 이상 진행하지 않음
    if not hotel_cards:
        print("No hotel cards found")
        raise Exception("No hotel cards found")

    # 맨 위에서부터 3번째 호텔 카드까지만 고려하여 랜덤으로 선택
    top_hotel_card = hotel_cards[0]  # 처음 세 개의 호텔 카드

    element_location = hotel_cards[2].location

    # 선택된 호텔 카드에서 호텔 이름 추출
    hotel_name = top_hotel_card.find_element(By.CSS_SELECTOR, ".title-info .title").text
    hotel_price = top_hotel_card.find_element(By.CSS_SELECTOR, ".hotel-price .real .fs7").text

    time.sleep(0.5)
    # 선택된 요소의 y 좌표를 사용하여 스크롤
    # driver.execute_script("window.scrollTo(0, arguments[0]);", element_location['y'])
    driver.execute_script("window.scrollBy(0, 450);")
    time.sleep(0.5)

    # 호텔 카드 클릭 (예: 이름을 클릭하여 상세 페이지로 이동)

    name_element = top_hotel_card.find_element(By.CSS_SELECTOR,
                                               "#__next > div.jj-list-container > div:nth-child(5) > div > div.jj-right.pt16 > div:nth-child(2) > div.infinite-scroll-component__outerdiv > div > div:nth-child(1) > div.middle-info > div.poi > div.title-info > span > span.b.fs4.mr4")

    name_element.click()
    time.sleep(0.2)
    hotel_address = driver.find_element(By.CSS_SELECTOR,
                                        "#jjiHotelDetail > div.rel > div.jj-hotel-info.bg7.mb16 > div.right-info > div:nth-child(2) > span.c3.db.mt5.jjic2 > span").text
    hotel_close = driver.find_element(By.CSS_SELECTOR,
                                      "body > div.jji-drawer-root > div > div > div.jji-drawer-header > div.jji-drawer-close.hover-cursor > i")
    hotel_close.click()
    time.sleep(0.2)

    hotel = {"name": hotel_name, "price": hotel_price, "address": hotel_address}

    # 결과 데이터 구조
    data = {
        "hotel": hotel,
        "flights": {
            "departure": start_flight_info,
            "return": comeback_flight_info
        }
    }

    # 데이터를 JSON 형식으로 변환 후 출력
    return data

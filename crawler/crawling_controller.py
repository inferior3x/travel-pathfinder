import sys
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from crawler.hotel_crawler import find_hotel_and_flight
from crawler.attraction_crawler import find_attraction



def main():
    options = Options()
    # 창 없이 실행
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  
    options.capabilities["browserName"] = "chrome"
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)

    

    while True:
        
        #명령어 들어올 때까지 기다림
        # line = sys.stdin.readline()
        # if not line:
            # break  # 명령어가 없으면 중단

        #명령어 json 디코딩
        # cmd = json.loads(line)
        # print(cmd, "asdf")
        # sys.stdout.flush()
        # break

        cmd = {
            "cmd": "plan",
            "departurePlace": "서울",
            "destination": "도쿄",
            "departureDate":"2023-11-21",
            "returnDate":"2023-11-27",
            "travelerNumber":"5",
            "roomNumber":"3",
            "attractionNumber":"1"
        }
        
        #명령어 처리
        if cmd["cmd"] == "plan":    
            #result 초기화
            result = {}

            #호텔/비행기 찾고 관광지 찾아서 각각 result의 속성에 추가
            result.update(find_hotel_and_flight(driver, cmd["departurePlace"], cmd["destination"], cmd["departureDate"], cmd["returnDate"], int(cmd["travelerNumber"]), int(cmd["roomNumber"])))
            result["attractions"] = find_attraction(driver, cmd["destination"], int(cmd["attractionNumber"]))

            #성공 여부
            result["success"] = True

            #result to JSON and print
            print(json.dumps(result, ensure_ascii=False))

            #flush
            sys.stdout.flush()
main()
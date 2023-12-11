import nest_asyncio
import asyncio
import time

nest_asyncio.apply()
import sys
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from crawler.hotel_crawler import find_hotel_and_flight, reset_persons_and_rooms
from crawler.attraction_crawler import find_attraction
from crawler.mp_function import *


def worker(pipe, pid):
    options = Options()
        # 창 없이 실행
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--headless")
    options.capabilities["browserName"] = "chrome"
    driver = webdriver.Chrome(options=options)
    # 화면 크기 설정 (전체 화면 크기의 절반으로 설정)
    screen_width = driver.execute_script("return window.screen.availWidth;")
    screen_height = driver.execute_script("return window.screen.availHeight;")
    driver.set_window_size(screen_width // 2, screen_height)
    if pid == 0:
        driver.set_window_position(0, 0)
    else:
        driver.set_window_position(screen_width // 2, 0)
    driver.implicitly_wait(15)
    while True:
        if pipe.poll():
            cmd = pipe.recv()
            if pid == 0:
                ret = find_hotel_and_flight(driver, cmd["departurePlace"], cmd["destination"], cmd["departureDate"], cmd["returnDate"], int(cmd["travelerNumber"]), int(cmd["roomNumber"]))
                pipe.send(ret)
                driver.quit()
                return
            else:
                ret = find_attraction(driver, cmd["destination"], int(cmd["attractionNumber"]))
                pipe.send(ret)
                driver.quit()
                return

def main():
    while True:
        

        #프로세스 초기화
        parent_pipes, child_pipes = create_pipes(2)
        procs = [] #프로세스 리스트
        for i in range(2):
            proc = create_process(worker, (child_pipes[i], ), i)
            procs.append(proc)

        # #명령어 들어올 때까지 기다림
        line = sys.stdin.readline()
        if not line:
            break  # 명령어가 없으면 중단
        cmd = json.loads(line)
        
        # cmd = {
        #     "cmd": "plan",
        #     "departurePlace": "서울",
        #     "destination": "도쿄",
        #     "departureDate": "2023-12-20",
        #     "returnDate": "2023-12-25",
        #     "travelerNumber": "5",
        #     "roomNumber": "3",
        #     "attractionNumber": "1"
        # }

    
        #명령어 처리
        if cmd["cmd"] == "plan":
            #result 초기화
            result = {}


            parent_pipes[0].send(cmd)
            parent_pipes[1].send(cmd)

            recv_data1 = 0
            recv_data2 = 0
            received_data_num = 0
            while True:
                time.sleep(0.05)
                for i in range(2):
                    if parent_pipes[i].poll():
                        if i == 0:
                            recv_data1 = parent_pipes[i].recv()
                        else:
                            recv_data2 = parent_pipes[i].recv()
                        received_data_num += 1
                if received_data_num == 2:
                    break
            #호텔/비행기 찾고 관광지 찾아서 각각 result의 속성에 추가
            try:
                result.update(recv_data1)
                result["attractions"] = recv_data2
                result["success"] = True
            except:
                result["success"] = False
            

            #result to JSON and print
            print(json.dumps(result, ensure_ascii=False))
            sys.stdout.flush()
        

if __name__ == "__main__":
    main()
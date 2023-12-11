import multiprocessing as mp
import nest_asyncio
import json
import sys
nest_asyncio.apply()

#부모에게 보낼 데이터를 stdout에 넣기
def push_to_stdout(type, data):
    print(json.dumps({'type': type, 'data': data}))

#flush stdout
def flush_stdout():
    sys.stdout.flush()

#부모에게 보낼 데이터를 stdout에 넣기고 flush
def push_and_flush_stdout(type, data=''):
    push_to_stdout(type, data)
    flush_stdout()

# 프로세스 개수만큼 부모와 자식의 파이프를 만들고 반환
def create_pipes(process_number):
    parent_pipes = []
    child_pipes = []
    for _ in range(process_number):
        parent_pipe, child_pipe = mp.Pipe()
        parent_pipes.append(parent_pipe)
        child_pipes.append(child_pipe)
    return (parent_pipes, child_pipes) #([], [])

#프로세스 생성하고 생성한 프로세스의 객체 반환
def create_process(func, args = (), i=-1):
    proc = mp.Process(target=func, args= args + (i,))
    proc.start()

    return proc

#크롤러에게 브라우저 닫으라고 하고 프로세스 닫기
def close_process(proc, pipe, i=-1):
    if proc.is_alive():
        data = ['close']
        pipe.send(data)
        proc.join(timeout=10)
    if proc.is_alive():
        proc.terminate()


import time
import threading

def add_to_total():
    global total 
    for i in range(1000):
        with lock:
            curr = total
            time.sleep(0)
            curr += 1
            total = curr

total = 0
threads = []
lock = threading.Lock()

for i in range(10):
    t = threading.Thread(target=add_to_total)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print(f'{total=}')

import time
import threading

def worker(num, callback): 
  print(f"Worker {num} starting...") 
  time.sleep(num)  # Simulate some work 
  print(f"Worker {num} finished.") 
  callback(num)  # Call the callback 
  

def callback_function(num): 
  print(f"Callback for worker {num} called.") 

if __name__ == "__main__": 
  threads = [] 
  for i in range(5): 
    thread = threading.Thread(target=worker, args=(i, callback_function)) 
    threads.append(thread) 
    thread.start() 

  for thread in threads: 
    thread.join() 
import threading
import logging
import time

def divisors_without_generator(number):
  divisors = []
  for divisor in range(1, number + 1):
    if number % divisor == 0:
      divisors.append(divisor)
      time.sleep(1)
      
  logging.info(f'Divisors of {number}: {divisors}')

def divisors_with_generator(number):
  for divisor in range(1, number + 1):
    if number % divisor == 0:
      time.sleep(1)
      yield divisor

def divisors_consumer(number):
  for d in divisors_with_generator(number):
    logging.info(f'{d} is divisor of {number}')

def find_divisors_threaded(number):
  thread1 = threading.Thread(target=divisors_consumer, args=(number,))
  thread2 = threading.Thread(target=divisors_consumer, args=(number*5,))
  thread3 = threading.Thread(target=divisors_without_generator, args=(number,))
  thread4 = threading.Thread(target=divisors_without_generator, args=(number*5,))
  

  thread1.start()
  thread2.start()
  thread3.start()
  thread4.start()

  thread1.join()
  thread2.join()
  thread3.join()
  thread4.join()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')
    find_divisors_threaded(10000000)
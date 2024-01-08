import time
import random

def random_sleep():
    random_number = random.uniform(0.3, 0.7)
    time.sleep(random_number)

def time_sleep(sleep_time):
    time.sleep(sleep_time)

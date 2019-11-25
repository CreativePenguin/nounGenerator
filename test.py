import time

while True:
  print("tick")
  time.sleep(1200 - time.time() % 1200)

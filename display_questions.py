import time, sys
while True:
    sys.stdout.write("\r" + time.ctime())
    sys.stdout.flush()
    time.sleep(1)
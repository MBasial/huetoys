import sys
import time
for i in range(100):
    time.sleep(0.1)
    y = sys.stdout.write('\b\b')
    x = sys.stdout.write(str(i))
    sys.stdout.flush()

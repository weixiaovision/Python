import threading
import time


def run(n):
    print('task:', n)
    time.sleep(2)
    print('task done:', n)

start_time = time.time()

for i in range(10):
    t = threading.Thread(target=run, args=(i,))
    # t.setDaemon(True)
    t.start()
print('cost:', time.time()-start_time)
print("all thread is done", threading.current_thread(), threading.active_count())
# time.sleep(2)
# print('111')

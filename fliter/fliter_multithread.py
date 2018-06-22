import threadpool
import time

def fun(arg1):
    print('{}'.format(arg1))
    time.sleep(1)


task_pool = threadpool.ThreadPool(80)
requests = threadpool.makeRequests(fun, [x for x in range(100)])
[task_pool.putRequest(req) for req in requests]

task_pool.poll()
task_pool.wait()
task_pool.joinAllDismissedWorkers()
# [pool.putRequest(req) for req in requests]
# task_pool.wait()
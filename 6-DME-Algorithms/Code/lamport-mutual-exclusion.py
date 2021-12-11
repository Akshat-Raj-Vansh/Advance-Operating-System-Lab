import sys
import threading
import time
from random import randint

no_threads = 5
no_requests = 5

print("Threads =", no_threads)
print("Requests =", no_requests)

distribution = []
no = 0
for itr in range(0, no_threads):
    distribution.append(0)
for itr in range(0, no_requests):
    distribution[no] += 1
    no = (no + 1) % no_threads

requestno = 0
y = -1
x = -1
b = []
for itr in range(0, no_threads):
    b.append(0)


def thread_lamport_fast(threadno):
    global distribution
    global requestno
    global no_requests
    global no_threads
    global y
    global x
    global b
    reqs = distribution[threadno]
    time.sleep(1)

    while reqs:
        print(f"Process {threadno} Requesting to Access Critical Section")
        b[threadno] = 1
        x = threadno
        if y != -1:
            b[threadno] = 0
            while (y != -1):
                pass
            continue
        y = threadno

        if x != threadno:
            b[threadno] = 0
            for j in range(0, no_threads):
                while (b[j] != 0):
                    pass
            if y != threadno:
                while (y != -1):
                    pass
                continue
        requestno = requestno + 1
        print(f"Process {threadno} Entering Critical Section")
        reqs = reqs - 1
        print(f"Process {threadno} Exiting Critical Section")
        y = -1
        b[threadno] = 0


print("Running Lamport's fast mutual exclusion algorithm:")
for threadno in range(0, no_threads):
    th = threading.Thread(target=thread_lamport_fast, args=(threadno,))
    th.daemon = True
    th.start()

while (requestno < no_requests):
    pass
time.sleep(1)
print("Finishing Lamport's fast mutual exclusion. All requests served. requestno =", requestno, "\n\n")
time.sleep(20)

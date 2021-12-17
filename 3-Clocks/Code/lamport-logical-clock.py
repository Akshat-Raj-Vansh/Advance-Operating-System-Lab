def logical_number(spno, seno, rpno, reno):
    if(seno != 1):
        P[spno][seno] = P[spno][seno-1]+1
    if(reno != 1):
        P[rpno][reno] = max(P[rpno][reno-1], P[spno][seno])+1
    else:
        P[rpno][reno] = P[spno][seno]+1


def update(process_num, event_number_1, event_number_2):
    if(P[process_num][event_number_1] > P[process_num][event_number_2]):
        P[process_num][event_number_2] = P[process_num][event_number_1]+1


P = {1: {}, 2: {}, 3: {}}

inc = 0

n1 = int(input("Enter the no. of events in Process 1 : "))
e1 = [i for i in range(1, n1 + 1)]
P[1] = {key: inc + key for key in e1}
print(P[1])
print("\n")

n2 = int(input("Enter the no. of events in Process 2 : "))
e2 = [i for i in range(1, n2 + 1)]
P[2] = {key: inc + key for key in e2}
print(P[2])
print("\n")

n3 = int(input("Enter the no. of events in Process 3 : "))
e3 = [i for i in range(1, n3 + 1)]
P[3] = {key: inc + key for key in e3}
print(P[3])
print("\n")

comm = int(input("Enter the no of communication lines : "))
print("\n")

while inc < comm:
    sent = int(input("Enter the sending process number : "))
    recv = int(input("Enter the receiving process number : "))
    sent_event_no = int(input("Enter the sending event number : "))
    recv_event_no = int(input("Enter the receiving event number : "))
    if sent <= 3 and recv <= 3:
        print("P{} --> P{}".format(sent, recv))
        logical_number(sent, sent_event_no, recv, recv_event_no)
        print("New vector value of \"event {}\"  in process P{} is : {} \n".format(
            recv_event_no, recv, P[recv][recv_event_no]))
    else:
        print("Enter the sent/recv within existing process")
    if (recv_event_no + 1) in P[recv]:
        for i in range(recv_event_no + 1, len(P[recv]) + 1):
            P[recv][i] = update(recv, i-1, i)
    inc += 1

print("Final vectors of the 3 process are")
print(P[1])
print(P[2])
print(P[3])
timeout = input('')

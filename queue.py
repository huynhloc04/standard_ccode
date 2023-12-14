import queue

q = queue.Queue()

numbers = [1, 2, 3, 4, 5, 6, 7]

for number in numbers:
    q.put(number)

print(q.get())

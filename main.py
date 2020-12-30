# import random_eqn
import display_questions
# import threading
import time

rows = 5
cols = 5
time_lim = 9.0
start_val = 4
start_diff = 0
diff_increment = 1
diff_change = 10

for i in range(3):
    print(f"LEVEL {i + 1}")
    for i in range(5, 0, -1):
        print(i, end = "\r")
        time.sleep(1)
    
    display_questions.display(rows, cols, time_lim, start_val, start_diff, diff_increment, diff_change).display_table()
    rows -= 1
    cols -= 1
    time_lim -= 2
    start_val += 2


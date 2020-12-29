# import random_eqn
import display_questions
import threading
import time

rows = 5
cols = 5
time = 5.0
start_val = 4
start_diff = 0
diff_increment = 2
diff_change = 10

x = display_questions.display(rows, cols, time, start_val, start_diff, diff_increment, diff_change)
threading.Thread(target = x.display_table).start()


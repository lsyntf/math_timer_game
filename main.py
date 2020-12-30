# import random_eqn
import display_questions
# import threading
import time

rows = 5
cols = 5
time_lim = 5.0
question_size = 11
level_up_thresh = 100
start_val = 4
start_diff = 0
diff_increment = 1
diff_change = 10
lifeline = 1

game = display_questions.display(rows, cols, time_lim, question_size, level_up_thresh, 
start_val, start_diff, diff_increment, diff_change, lifeline)

game.show_questions()
game.answer_question()


# for i in range(3):
#     print(f"LEVEL {i + 1}")
#     for i in range(5, 0, -1):
#         print(i, end = "\r")
#         time.sleep(1)
    
    
#     rows -= 1
#     cols -= 1
#     time_lim -= 2
#     start_val += 2


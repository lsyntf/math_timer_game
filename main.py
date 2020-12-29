# import random_eqn
import display_questions
import threading

def difficulty(correct_ans):
    r = 5
    c = 5
    t = 5
    q = 1
    difficulty = (correct_ans // 10) + 1
    if difficulty == 1:
        return [r, c, t, q]
    div = difficulty // 4
    mod = difficulty % 4
    




x = display_questions.display(5, 5, 5.0)
threading.Thread(target = x.display_table).start()


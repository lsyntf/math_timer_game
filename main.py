# import random_eqn
import display_questions
import threading

x = display_questions.display(5, 5, 5.0)
threading.Thread(target = x.display_table).start()


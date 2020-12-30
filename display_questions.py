import time, sys
from terminaltables import AsciiTable
import os
import threading
import random
import random_eqn

class display:
    def __init__(self, rows, cols, times, question_size, level_up_thresh, start, diff, diff_inc, diff_change, lifeline):
        self.rows = rows
        self.cols = cols

        self.time_limit = times
        self.time_left = times

        self.question_size = question_size

        self.start = start
        self.diff = diff
        self.diff_inc = diff_inc
        self.diff_change = diff_change

        self.lifeline = lifeline
        self.clear_table = 'c'

        self.default_question_cell = ' ' * self.question_size
        self.default_answer_cell = -1

        self.num_correct_ans = 0
        self.level_up_thresh = level_up_thresh
        self.attempts = 0
        self.is_answer_entered = False

        self.available_indices = list(range(0, self.rows * self.cols))

        self.answer_table = self.gen_a_table()
        self.question_table = self.gen_q_table()

        self.questions, self.answers = random_eqn.generate_question(self.start, self.diff, self.diff_inc)

    # define our clear function
    def clear(self):   
        # for windows 
        if os.name == 'nt': 
            _ = os.system('cls') 
    
        # for mac and linux(here, os.name is 'posix') 
        else: 
            _ = os.system('clear') 

    def gen_a_table(self):
        return [self.default_answer_cell] * self.rows * self.cols

    def gen_q_table(self):
        data_table = []
        for i in range(self.cols):
            new = []
            for j in range(self.rows):
                new.append(self.default_question_cell)
            data_table.append(new)
        return data_table

    def resize_question(self, q): # stupid
        while len(q) < self.question_size:
            q += ' '
        return q

    def countdown(self):
        print("Answer|Time")
        while not self.is_answer_entered and self.time_left > 0.0:  
            # self.show_questions()
            # print("Answer|Time")      
            print(f"      |{round(self.time_left)}", end = '\r')     
            for i in range(100):              
                if self.is_answer_entered:
                    break
                time.sleep(0.01)                        
                self.time_left -= 0.01  

    def difficulty(self):
        correct_buf = self.num_correct_ans
        if correct_buf > 0 and correct_buf % self.diff_change == 0 and self.time_left == self.time_limit:
            d = (correct_buf // self.diff_change)
            div = d // 2
            mod = d % 2
            if mod == 1:
                self.diff += 1
            elif mod == 0 and self.time_limit >= 3:
                self.time_limit -= 1
                self.time_left -= 1

    def insert_val(self, question, answer):
        if len(self.available_indices) == 0:
            return
        index_val = random.choice(self.available_indices)
        self.question_table[index_val // self.cols][index_val % self.rows] = question
        self.answer_table[index_val] = answer
        self.available_indices.remove(index_val)

    def remove_val(self, val = -2):
        if val == self.clear_table and self.lifeline > 0:
            self.available_indices = list(range(0, self.rows * self.cols))
            self.answer_table = self.gen_a_table()
            self.question_table = self.gen_q_table()
            self.lifeline -= 1
            self.time_left = self.time_limit
            return
        if val.isnumeric():
            val = int(val)
            answers = self.answer_table.count(val)
            for i in range(answers):
                index_val = self.answer_table.index(val)
                self.question_table[index_val // self.cols].pop(index_val % self.rows)
                self.question_table[index_val // self.cols].insert(index_val % self.rows, self.default_question_cell)
                self.answer_table.remove(val)
                self.answer_table.insert(index_val, self.default_answer_cell)
                self.available_indices.append(index_val)
                self.num_correct_ans += 1
                self.time_left = self.time_limit
            # print(table_a) 

    def user_input(self):    
        # print("Answer|Time")
        self.is_answer_entered = False
        user_answer = input()
        self.is_answer_entered = True    
        self.attempts += 1
        if user_answer != '':
            self.remove_val(user_answer)
        self.difficulty()
        self.show_questions()
        self.answer_question()

    def show_questions(self):   
        # Each table cell must be 11 characters long
        if len(self.available_indices) == 0:
            print("\nThere is no more space! You lose!")
            os._exit(0)
        if self.num_correct_ans == self.level_up_thresh:
            print("\nCongrats, you beat the level!")
            return True
            
        self.clear()  
        self.questions, self.answers = random_eqn.generate_question(self.start, self.diff, self.diff_inc)
        self.insert_val(self.resize_question(self.questions), self.answers)
        print_table = AsciiTable(self.question_table)
        print_table.inner_row_border = True
        print(print_table.table) 
        print(f"Correct Answers: {self.num_correct_ans} | Attempts: {self.attempts} | Lifelines: {self.lifeline}")

        # self.answer_question()   
        
    def answer_question(self):
        before_ans = self.num_correct_ans 
        before_lifeline = self.lifeline
        threading.Thread(target = self.user_input).start() 
        threading.Thread(target = self.countdown).start()

        time.sleep(self.time_limit)
        # print(before_ans, num_correct_ans)
        if before_ans == self.num_correct_ans and before_lifeline == self.lifeline:
            # print(f'\nCorrect Answers: {self.num_correct_ans}')
            print("\nTime's up! You lose!")
            os._exit(0)
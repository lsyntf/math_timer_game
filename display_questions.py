import time, sys
from terminaltables import AsciiTable
import os
import threading
import random
import random_eqn

class display:
    def __init__(self, rows, cols, time, start, diff, diff_inc, diff_change):
        self.rows = rows
        self.cols = cols
        self.size = rows * cols

        self.time_limit = time
        self.count_limit = time

        self.start = start
        self.diff = diff
        self.diff_inc = diff_inc
        self.diff_change = diff_change

        self.default_question_cell = '           '
        self.default_answer_cell = -1

        self.answers_correct = 0
        self.was_correct = 0
        self.attempts = 0
        self.answered = False

        self.compare_list = list(range(0, self.size))

        self.table_answers = self.gen_a_table()
        self.table_display = self.gen_q_table()

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
        return [self.default_answer_cell] * self.size

    def gen_q_table(self):
        data_table = []
        for i in range(self.cols):
            new = []
            for j in range(self.rows):
                new.append(self.default_question_cell)
            data_table.append(new)
        return data_table

    def resize_question(self, q):
        while len(q) < 11:
            q += ' '
        return q

    def countdown(self):
        print("Answer|Time")
        while not self.answered and self.count_limit > 0.0:        
            print(f"      |{round(self.count_limit)}", end = '\r')     
            for i in range(100):              
                if self.answered:
                    break
                time.sleep(0.01)                        
                self.count_limit -= 0.01  

    def difficulty(self):
        correct_buf = self.answers_correct
        if correct_buf > 0 and correct_buf % self.diff_change == 0 and self.was_correct != correct_buf:
            d = (correct_buf // self.diff_change)
            div = d // 2
            mod = d % 2
            if mod == 1:
                self.diff += 1
            if mod == 0:
                self.time_limit -= 1
                self.count_limit -= 1

    def insert_val(self, question, answer):
        if len(self.compare_list) == 0:
            return
        index_val = random.choice(self.compare_list)
        self.table_display[index_val // self.cols][index_val % self.rows] = question
        self.table_answers[index_val] = answer
        self.compare_list.remove(index_val)

    def remove_val(self, val = -2):
        answers = self.table_answers.count(val)
        for i in range(answers):
            index_val = self.table_answers.index(val)
            self.table_display[index_val // self.cols].pop(index_val % self.rows)
            self.table_display[index_val // self.cols].insert(index_val % self.rows, self.default_question_cell)
            self.table_answers.remove(val)
            self.table_answers.insert(index_val, self.default_answer_cell)
            self.compare_list.append(index_val)
            self.answers_correct += 1
        if self.was_correct < self.answers_correct:
            self.count_limit = self.time_limit
        # print(table_a) 

    def answer_question(self):    
        # print("Answer|Time")
        self.answered = False
        user_answer = input()
        self.answered = True    
        self.attempts += 1
        if user_answer != '' and user_answer.isnumeric():
            self.remove_val(int(user_answer))
        self.difficulty()
        self.display_table()
        return

    def display_table(self):   
        # Each table cell must be 11 characters long
        if len(self.compare_list) == 0:
            print("You have reached the end! You lose!")
            os._exit(0)
        self.clear()  
        self.questions, self.answers = random_eqn.generate_question(self.start, self.diff, self.diff_inc)
        self.insert_val(self.resize_question(self.questions), self.answers)
        print_table = AsciiTable(self.table_display)
        print_table.inner_row_border = True
        print(print_table.table)    
        
        before_ans = self.answers_correct 
        self.was_correct = before_ans 
        answer_q = threading.Thread(target = self.answer_question)   
        answer_q.start()
        
        print(f"Correct Answers: {self.answers_correct} | Attempts: {self.attempts}")
        threading.Thread(target= self.countdown).start()

        time.sleep(self.time_limit)
        # print(before_ans, answers_correct)
        if before_ans == self.answers_correct:
            # print(f'\nCorrect Answers: {self.answers_correct}')
            os._exit(0)
            return
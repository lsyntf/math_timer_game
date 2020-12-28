import time, sys
from terminaltables import AsciiTable
import os
import threading
#import numpy as np
import random

rows = 5
cols = 5
size = rows * cols

time_limit = 5.0
count_limit = 5.0

default_question_cell = '           '
default_answer_cell = -1

answers_correct = 0
was_correct = 0
attempts = 0
answered = False

compare_list = list(range(0, size))

test_q = ['1 + 1 =', '2 + 2 =', '5 + 10 =', '20 + 20 =']
test_a = [2, 4, 15, 40]

# define our clear function
def clear():   
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

def gen_a_table(length, vals):
    return [vals] * length

def gen_q_table(row, col, vals):
    data_table = []
    for i in range(col):
        new = []
        for j in range(row):
            new.append(vals)
        data_table.append(new)
    return data_table

def resize_question(q):
    while len(q) < 11:
        q += ' '
    return q

def countdown(timer):
    global count_limit
    global answered
    print("Answer|Time")
    while not answered and count_limit > 0.0:        
        print(f"      |{round(count_limit)}", end = '\r')     
        for i in range(100):              
            if answered:
                break
            time.sleep(0.01)                        
            count_limit -= 0.01  

def insert_val(question, answer, table_q, table_a, table_c, row, col):
    if len(table_c) == 0:
        return
    index_val = random.choice(table_c)
    table_q[index_val // col][index_val % row] = question
    table_a[index_val] = answer
    table_c.remove(index_val)
    # print(table_a)

def remove_val(table_q, table_a, table_c, row, col, val = -2):
    global answers_correct
    global count_limit
    global time_limit
    global was_correct
    answers = table_a.count(val)
    for i in range(answers):
        index_val = table_a.index(val)
        table_q[index_val // col].pop(index_val % row)
        table_q[index_val // col].insert(index_val % row, default_question_cell)
        table_a.remove(val)
        table_a.insert(index_val, default_answer_cell)
        table_c.append(index_val)
        answers_correct += 1
    if was_correct < answers_correct:
        count_limit = time_limit
    # print(table_a) 

def answer_question():    
    # print("Answer|Time")
    global answered   
    global attempts 
    answered = False
    user_answer = input()
    answered = True    
    attempts += 1
    if user_answer != '' and user_answer.isnumeric():
        remove_val(table_display, table_answers, compare_list, rows, cols, int(user_answer))
    display_table(table_answers, table_display, compare_list, rows, cols, time_limit)
    return

def display_table(table_a, table_q, table_c, row, col, timer):   
    global attempts
    global answers_correct
    global was_correct
    global count_limit
    # Each table cell must be 11 characters long
    clear()  
    insert_val(resize_question(test_q[0]), test_a[0], table_q, table_a, table_c, row, col)
    print_table = AsciiTable(table_display)
    print_table.inner_row_border = True
    print(print_table.table)    
    
    before_ans = answers_correct 
    was_correct = before_ans 
    answer_q = threading.Thread(target = answer_question)   
    answer_q.start()
    
    print(f"Correct Answers: {answers_correct} | Attempts: {attempts}")
    threading.Thread(target= countdown, args = (timer,)).start()

    time.sleep(timer)
    # print(before_ans, answers_correct)
    if before_ans == answers_correct:
        print(f'\nCorrect Answers: {answers_correct}')
        os._exit(0)
        return

table_answers = gen_a_table(size, default_answer_cell)
table_display = gen_q_table(rows, cols, default_question_cell)

threading.Thread(target = display_table, args = (table_answers, table_display, compare_list, rows, cols, time_limit)).start()
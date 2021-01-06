import itertools
import random
import math

### GENERATE QUESTION ###
def get_operation():
    OPERATIONS = ["Addition", "Subtraction", "Multiplication", "Division"]

    operation = random.choice(OPERATIONS)
    # print(operation) # For testing

    return operation    

def generate_question(start, difficulty, diff_increment):
    max_num = start + difficulty * diff_increment
    # print(f"max_num: {max_num}")

    num1 = random.randint(0, max_num)
    num2 = random.randint(0, max_num)

    switch = {
        "Addition": gen_add_question,
        "Subtraction": gen_sub_question,
        "Multiplication": gen_mult_question,
        "Division": gen_div_question
    }

    func = switch.get(get_operation(), "Invalid operation")
    return func(num1, num2) # should return top number, operator symbol, bottom number, answer (in order)
    
### ADDITION ###
def gen_add_question(num1, num2):
    # print("add") # For testing
    return f"{num1} + {num2} =", num1 + num2 # addend1, "+", addend2, answer

### SUBTRACTION ###
def gen_sub_question(num1, num2):
    # print("sub") # For testing
    max_num = max(num1, num2)
    min_num = min(num1, num2)
    return f"{max_num} - {min_num} =", max_num - min_num # subtrahend1, "-", subtrahend2, answer

### MULTIPLICATION ###
def gen_mult_question(num1, num2):
    # print("mult") # For testing
    num1 %= 21
    num2 %= 21
    return f"{num1} × {num2} =", num1 * num2 # multiplicand, "×", multiplier, answer

### DIVISION ###
def gen_div_question(num1, num2):
    #print("div") # For testing
    num1 = num1 % 20 + 1
    num2 %= 21
    return f"{num1 * num2} / {num1} =", num2 # dividend, "÷", divisor, answer 

def check_ans(ans, answers):
    return True if ans in answers else False

### Main code ###
# START = 4
# SUCC_INCREMENT = 2
# DIFF_INCREMENT = 2

# successes = 0
# difficulty = 0

# while True:
#     print()
#     print(f"successes: {successes}")
#     print(f"successes % {SUCC_INCREMENT}: {successes % SUCC_INCREMENT}") 
#     print(f"difficulty: {difficulty}")

#     answers = []
#     question, answer = generate_question(START, difficulty, DIFF_INCREMENT)
#     answers.append(answer)

#     user_ans = int(input(question))
#     if check_ans(user_ans, answers):
#         successes += 1
#         if successes % SUCC_INCREMENT == 0:
#             difficulty += 1
#         print("yay")
#     else:
#         print("you succ")

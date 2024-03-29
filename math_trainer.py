# Basic infinite mental math trainer (integers only)
# This is just a fine-tuned script to help me personally practice things
# I struggle with, so there are times tables from 1-30 as well as addition
# and subtraction within that range
# Basically just a fun pasttime
import random
import operator as op
from typing import List, Union
import functools
import time
import argparse


ADD_RANGE = [10, 900]
MUL_RANGE = [2, 30]
DIV_RANGE = [20, 900]



def generate_add_sub_nums(dp=0) -> Union[List[int], List[float]]:
    if dp == 0:
        num1, num2 = random.randint(*ADD_RANGE), random.randint(*ADD_RANGE)
        return num1, num2
    else:
        num1 = round(random.uniform(*ADD_RANGE), dp)
        num2 = round(random.uniform(*ADD_RANGE), dp)
        return num1, num2


def generate_mul_nums(dp=0) -> List[int]:
    # Generate two numbers for timetables
    if dp == 0:
        num1, num2 = random.randint(*MUL_RANGE), random.randint(*MUL_RANGE)
    else:
        num1 = round(random.uniform(*MUL_RANGE), dp)
        num2 = round(random.uniform(*MUL_RANGE), dp)
    return num1, num2


def factors(n: int) -> List[int]:
    return list(set(functools.reduce(list.__add__,
                                     ([i, n // i] for i in range(1, int(n**0.5) + 1)
                                      if n % i == 0))))


def generate_div_nums(dp=0) -> List[int]:
    # Generate one number and then one of its factors
    # This isn't an inversion of the multiplication range since I want to
    # test really random division problems too
    # However, death mode is an inversion bc of irrational numbers
    if dp > 0:
        fac_1, fac_2 = generate_mul_nums(dp = dp)
        num1 = round(fac_1 * fac_2, 2*dp)
        num2 = random.choice([fac_1, fac_2])
    else:
        num1 = random.randint(*DIV_RANGE)
        while len(factors(num1)) <= 2:
            # Avoid primes
            num1 = random.randint(*DIV_RANGE)
        num2 = 1
        while num2 == 1 or num2 == num1:
            # No easy questions
            num2 = random.choice(factors(num1))
    return num1, num2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', "--death", action="store_true")
    parser.add_argument("-t", "--times", action="store_true")
    death_mode = parser.parse_args().death
    times_only = parser.parse_args().times

    if times_only:
        # only practice times tables
        operators = {"*": op.mul}
    else:
        # Generate random operation, much harder
        operators = {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv
        }
    # Death mode has calcs with 2 dp
    dp = 2 if death_mode else 0
    # game loop
    num_questions = 20
    questions_remaining = num_questions
    num_correct = 0
    total_time = 0.
    quit_strs = ["q", "quit"]
    func_chooser = {
        "+": generate_add_sub_nums,
        "-": generate_add_sub_nums,
        "*": generate_mul_nums,
        "/": generate_div_nums
    }
    while questions_remaining > 0:
        current_q_num = num_questions - questions_remaining + 1
        # generate random expression
        operation = random.choice(list(operators.keys()))
        num1, num2 = func_chooser[operation](dp=dp)
        # yes yes eval is evil but I'm only using it locally
        expression = f"{num1} {operation} {num2}"
        true_answer = eval(expression)
        # Need to round bc of floating point arithmetic
        round_dp = dp*2 if operation == "*" else dp
        true_answer = round(true_answer, round_dp)
        # timing for user answer
        start_time = time.time()
        user_answer = input(f"Q{current_q_num} of {num_questions}: {expression.replace('*', 'x')} = ")
        end_time = time.time()
        time_delta = end_time - start_time
        # handle input
        if user_answer.lower().strip() in quit_strs:
            print("Coward!")
            accuracy = num_correct / num_questions
            average_time = total_time / num_questions
            print(f"{num_correct} / {num_questions} correct ({accuracy*100:.2f}%)"
                  f" in {total_time:.2f} [s]")
            print(f"Average time: {average_time:.2f} [s]")
            exit(0)
        else:
            try:
                user_answer = int(user_answer)
            except ValueError:  # invalid input
                user_answer = -1  # always wrong
        if user_answer == true_answer:
            # correct
            print(f"{user_answer} is correct ({time_delta:.2f} [s])")
            num_correct += 1
        else:
            # wrong
            if dp == 0:
                true_answer = int(true_answer)
            print(f"Wrong, actually is {true_answer} "
                  f"({time_delta:.2f}) [s]")

        questions_remaining -= 1
        total_time += time_delta

    # Done!
    print("All done, thanks for playing!")
    accuracy = num_correct / num_questions
    average_time = total_time / num_questions
    print(f"{num_correct} / {num_questions} correct ({accuracy*100:.2f}%)"
            f" in {total_time:.2f} [s]")
    print(f"Average time: {average_time:.2f} [s]")


if __name__ == "__main__":
    main()

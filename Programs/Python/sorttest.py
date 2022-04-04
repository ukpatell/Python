# Original codebase by Rohrbaugh 2021
# Modifications by: patel
# Last modified: April 4, 2022

import csv
import random
import time
from datetime import datetime

# replace yourlastname with your actual last name here
STUDENT_LASTNAME = 'patel'
VERBOSE_OUTPUT = True

# global constants controlling tests
MIN_SIZE = 2
MAX_SIZE = 1024
TRIALS = 20

# global variable used to count steps
step_count = 0


def bubble_sort(list):
    # step_count must be declared global here
    # otherwise it would create a new variable
    global step_count

    for i in range(len(list) - 1):
        for j in range(0, len(list) - i - 1):
            step_count += 1
            if list[j] > list[j + 1]:
                list[j], list[j + 1] = list[j + 1], list[j]


def generate_filename():
    filename = STUDENT_LASTNAME + '_'
    filename += datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename += ".csv"
    return filename


def console_log(message):
    if VERBOSE_OUTPUT:
        print(message)


def main():
    global step_count

    with open(generate_filename(), mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        console_log(f"Testing bubble_sort with {TRIALS} trials on arrays sized {MIN_SIZE} to {MAX_SIZE}")
        output_writer.writerow(['algorithm', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
        output_writer.writerow(['bubble_sort', MIN_SIZE, MAX_SIZE, TRIALS])
        output_writer.writerow([])
        output_writer.writerow(['size', 'avg_time', 'avg_steps'])

        size = MIN_SIZE
        while size <= MAX_SIZE:

            sort_time = 0
            sort_steps = 0

            for t in range(TRIALS):
                # create a list of size elements with values ranging 0..2*size
                list = random.sample(range(0, int(size * 2)), size)

                # record time & reset step_count before sorting
                before_time = datetime.now()
                step_count = 0

                bubble_sort(list)

                # calculate & record elapsed time & steps
                sort_time += (datetime.now() - before_time).microseconds
                sort_steps += step_count

            console_log(f"size: {size}")
            output_writer.writerow([size, sort_time / TRIALS, sort_steps // TRIALS])
            size *= 2


if __name__ == '__main__':
    main()

"""
# CISC 233 LAB 2 Sorting Methods
# Original Author : Eugene Rohrbaugh
# Date Created    : April 4, 2022,
# Date Modified   : April 6, 2022,
# Modifications   : Umangkumar Patel
# Description     : Modify an existing codebase to run a series of tests to illustrate the big-O efficiency
#                   of bubble_sort, insertion_sort, selection_sort, merge_sort, and quick_sort.
# GitHub          : https://github.com/ukpatell/Python.git
# Sources         : https://www.guru99.com/selection-sort-algorithm.html
# Important Note  :
"""

import csv
import math
import random
import time
from datetime import datetime

# replace yourlastname with your actual last name here
import numpy

STUDENT_LASTNAME = 'patel'
VERBOSE_OUTPUT = False

# global constants controlling tests
MIN_SIZE = 2
MAX_SIZE = 1024
TRIALS = 2
PERCENT = 0.05
# global variable used to count steps
comp_count = 0
swap_count = 0

# global variable for configuration management
CONFIG = ['random', 'almost-sorted', 'reverse-sorted']


def almost_sort(arr):
    global PERCENT
    # Sorts the array
    arr.sort()

    # Percentage of length of array for nearly sort
    num = math.ceil(len(arr) * PERCENT)
    # print('Percent: ',num,' Sorted List...', arr)

    # Swap num % of the array size
    for nums in range(num):
        # Generate two separate indexes
        while True:
            index1 = random.randint(0, len(arr) - 1)
            index2 = random.randint(0, len(arr) - 1)
            if index1 != index2:
                break
        temp = arr[index1]
        arr[index1] = arr[index2]
        arr[index2] = temp
    # Return the modified array
    return arr


def reverse_sort(arr):
    pass


def bubble_sort(arr):
    # step_count must be declared global here
    # otherwise it would create a new variable
    global comp_count
    global swap_count

    for i in range(len(arr) - 1):
        for j in range(0, len(arr) - i - 1):
            comp_count += 1
            if arr[j] > arr[j + 1]:
                swap_count += 1
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def selectionSort(itemsList):
    global comp_count
    global swap_count

    n = len(itemsList)
    for i in range(n - 1):
        minValueIndex = i

        for j in range(i + 1, n):
            comp_count += 1
            if itemsList[j] < itemsList[minValueIndex]:
                swap_count += 1
                minValueIndex = j

        comp_count += 1
        if minValueIndex != i:
            swap_count += 1
            temp = itemsList[i]
            itemsList[i] = itemsList[minValueIndex]
            itemsList[minValueIndex] = temp


def insertion_sort(array):
    global comp_count
    global swap_count
    k = 0
    n = len(array) - 1

    # We start from 1 since the first element is trivially sorted
    while k + 1 <= n:
        i = k + 1
        curr_val = array[i]
        swap_count += 1
        while i > 0 and array[i - 1] > curr_val:
            array[i] = array[i - 1]
            i = i - 1
            comp_count += 1
        array[i] = curr_val
        k = k + 1


def generate_filename():
    filename = STUDENT_LASTNAME + '_'
    filename += datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename += ".csv"
    return filename


def console_log(message):
    if VERBOSE_OUTPUT:
        print(message)


def main():
    with open(generate_filename(), mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        def bubblesort_manager():
            global comp_count, swap_count, CONFIG

            for config in CONFIG:
                console_log(f"Testing bubble_sort with {TRIALS} trials on arrays sized {MIN_SIZE} to {MAX_SIZE}")
                output_writer.writerow(['algorithm', 'initial_configuration', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
                output_writer.writerow(['Bubble Sort', config, MIN_SIZE, MAX_SIZE, TRIALS])
                output_writer.writerow(['SIZE', '', 'avg_time', 'avg_comps', 'avg_swaps'])

                size = MIN_SIZE
                while size <= MAX_SIZE:

                    sort_time = 0
                    sort_comps = 0
                    sort_swaps = 0

                    for t in range(TRIALS):
                        # create a list of size elements with values ranging 0..2*size
                        list = random.sample(range(0, int(size * 2)), size)

                        # record time & reset count before sorting
                        if config == 'random':
                            before_time = datetime.now()
                            comp_count = 0
                            swap_count = 0

                            bubble_sort(list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                        elif config == 'almost-sorted':
                            # print('Almost Sort...Trial # ', t)
                            # Sends the list to almost sort
                            # print('Before Sending Almost Sort...',list)
                            # Sort the list before starting the time for accuracy
                            new_list = almost_sort(list)
                            # print('After Sending Almost Sort...',new_list)
                            before_time = datetime.now()
                            comp_count = 0
                            swap_count = 0

                            bubble_sort(new_list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                        elif config == 'reverse-sorted':
                            # Reverse Sort the list
                            list.sort(reverse=True)
                            before_time = datetime.now()
                            comp_count = 0
                            swap_count = 0

                            bubble_sort(list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                    console_log(f"size: {size}")
                    output_writer.writerow([size, '', sort_time / TRIALS, sort_comps // TRIALS, sort_swaps // TRIALS])
                    size *= 2

        def selectionsort_manager():
            global comp_count, swap_count, CONFIG

            for config in CONFIG:
                console_log(f"Testing selection sort with {TRIALS} trials on arrays sized {MIN_SIZE} to {MAX_SIZE}")
                output_writer.writerow([])
                output_writer.writerow(['Algorithm', 'initial_configuration', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
                output_writer.writerow(['Selection Sort', config, MIN_SIZE, MAX_SIZE, TRIALS])
                output_writer.writerow(['SIZE', '', 'avg_time', 'avg_comps', 'avg_swaps'])

                size = MIN_SIZE
                while size <= MAX_SIZE:

                    sort_time = 0
                    sort_comps = 0
                    sort_swaps = 0

                    for t in range(TRIALS):
                        # create a list of size elements with values ranging 0..2*size
                        list = random.sample(range(0, int(size * 2)), size)

                        # record time & reset step_count before sorting
                        if config == 'random':
                            before_time = datetime.now()
                            comp_count = 0
                            swap_count = 0

                            selectionSort(list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                        elif config == 'almost-sorted':
                            # print('Almost Sort...Trial # ', t)
                            # Sends the list to almost sort
                            # print('Before Sending Almost Sort...',list)
                            # Sort the list before starting the time for accuracy
                            new_list = almost_sort(list)
                            # print('After Sending Almost Sort...',new_list)
                            before_time = datetime.now()
                            comp_count = 0
                            swap_count = 0

                            selectionSort(new_list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                        elif config == 'reverse-sorted':
                            # Reverse Sort the list
                            list.sort(reverse=True)
                            before_time = datetime.now()
                            comp_count = 0
                            swap_count = 0

                            selectionSort(list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                    console_log(f"size: {size}")
                    output_writer.writerow([size, '', sort_time / TRIALS, sort_comps // TRIALS, sort_swaps // TRIALS])
                    size *= 2

        def insertionsort_manager():
            global comp_count, swap_count, CONFIG

            for config in CONFIG:
                output_writer.writerow([])
                output_writer.writerow([])
                console_log(f"Testing Insertion Sort with {TRIALS} trials on arrays sized {MIN_SIZE} to {MAX_SIZE}")
                output_writer.writerow(['Algorithm', 'initial_configuration', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
                output_writer.writerow(['Insertion Sort', config, MIN_SIZE, MAX_SIZE, TRIALS])
                output_writer.writerow([])
                output_writer.writerow(['SIZE', '', 'avg_time', 'avg_comps', 'avg_swaps'])

                size = MIN_SIZE
                while size <= MAX_SIZE:

                    sort_time = 0
                    sort_comps = 0
                    sort_swaps = 0

                    for t in range(TRIALS):
                        # create a list of size elements with values ranging 0..2*size
                        list = random.sample(range(0, int(size * 2)), size)

                        # record time & reset step_count before sorting
                        if config == 'random':
                            before_time = datetime.now()
                            comp_count = 0
                            swap_count = 0

                            insertion_sort(list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                        elif config == 'almost-sorted':
                            # print('Almost Sort...Trial # ', t)
                            # Sends the list to almost sort
                            # print('Before Sending Almost Sort...',list)
                            # Sort the list before starting the time for accuracy
                            new_list = almost_sort(list)
                            # print('After Sending Almost Sort...',new_list)
                            before_time = datetime.now()
                            comp_count = 0
                            swap_count = 0

                            insertion_sort(new_list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                        elif config == 'reverse-sorted':
                            # Reverse Sort the list
                            list.sort(reverse=True)
                            before_time = datetime.now()
                            comp_count = 0
                            swap_count = 0

                            insertion_sort(list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                    console_log(f"size: {size}")
                    output_writer.writerow([size, '', sort_time / TRIALS, sort_comps // TRIALS, sort_swaps // TRIALS])
                    size *= 2

        bubblesort_manager()
        selectionsort_manager()
        insertionsort_manager()


if __name__ == '__main__':
    main()
    print('File saved in your project directory.')

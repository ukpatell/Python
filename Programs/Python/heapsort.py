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
#                   https://stackoverflow.com/questions/37267887/python-3-insertion-sort-comparisons-counter
#                   https://towardsdatascience.com/how-to-implement-merge-sort-algorithm-in-python-4662a89ae48c
#                   https://www.programiz.com/dsa/shell-sort





# Important Note  :
"""

import csv
import math
import random
from datetime import datetime

# replace yourlastname with your actual last name here

STUDENT_LASTNAME = 'patel'
VERBOSE_OUTPUT = True

# global constants controlling tests
MIN_SIZE = 64
MAX_SIZE = 8192
TRIALS = 10

# global variable used to count steps
comp_count = 0
swap_count = 0


def generate_filename():
    filename = STUDENT_LASTNAME + '_'
    filename += datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename += ".csv"
    return filename


def console_log(message):
    if VERBOSE_OUTPUT:
        print(message)

    # Heap Sort in python


def heapify(arr, n, i):
    global comp_count, swap_count
    # Find largest among root and children
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    comp_count += 1
    if l < n and arr[i] < arr[l]:
        largest = l

    comp_count += 1
    if r < n and arr[largest] < arr[r]:
        largest = r

    # If root is not largest, swap with largest and continue heapifying
    if largest != i:
        swap_count += 1
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)


def heap_sort(arr):
    global swap_count
    n = len(arr)

    # Build max heap
    for i in range(n // 2, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        # Swap
        swap_count += 1
        arr[i], arr[0] = arr[0], arr[i]

        # Heapify root element
        heapify(arr, i, 0)


def main():
    with open(generate_filename(), mode='w') as output_file:
        output_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        def heap_sort_manager():
            global comp_count, swap_count

            console_log(f"Testing heapsort with {TRIALS} trials on arrays sized {MIN_SIZE} to {MAX_SIZE}")
            output_writer.writerow(['algorithm', 'initial_configuration', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
            output_writer.writerow(['heap_sort', 'random', MIN_SIZE, MAX_SIZE, TRIALS])
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
                    before_time = datetime.now()
                    comp_count = 0
                    swap_count = 0

                    heap_sort(list)
                    # calculate & record elapsed time & steps
                    sort_time += (datetime.now() - before_time).microseconds
                    sort_comps += comp_count
                    sort_swaps += swap_count

                console_log(f"size: {size}")
                output_writer.writerow([size, '', sort_time / TRIALS, sort_comps // TRIALS, sort_swaps // TRIALS])
                size *= 2

        heap_sort_manager()


if __name__ == '__main__':
    print('Please wait...')
    main()
    print('File saved in your project directory.')

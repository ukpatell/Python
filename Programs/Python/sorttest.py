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
#                   https://www.geeksforgeeks.org/python-program-for-quicksort/
#                   https://www.programiz.com/dsa/shell-sort
"""

import csv
import math
import random
from datetime import datetime

# replace yourlastname with your actual last name here

STUDENT_LASTNAME = 'patel'
VERBOSE_OUTPUT = False

# global constants controlling tests
MIN_SIZE = 2
MAX_SIZE = 1024
TRIALS = 20
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


def bubble_sort(arr):
    # step_count must be declared global here
    # otherwise it would create a new variable
    global comp_count, swap_count

    for i in range(len(arr) - 1):
        for j in range(0, len(arr) - i - 1):
            comp_count += 1
            if arr[j] > arr[j + 1]:
                swap_count += 1
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def selection_sort(itemsList):
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


def merge_sort(list):
    # 1. Store the length of the list
    list_length = len(list)

    # 2. List with length less than is already sorted
    if list_length == 1:
        return list

    # 3. Identify the list midpoint and partition the list into a left_partition and a right_partition
    mid_point = list_length // 2

    # 4. To ensure all partitions are broken down into their individual components,
    # the merge_sort function is called and a partitioned portion of the list is passed as a parameter
    left_partition = merge_sort(list[:mid_point])
    right_partition = merge_sort(list[mid_point:])

    # 5. The merge_sort function returns a list composed of a sorted left and right partition.
    return merge(left_partition, right_partition)


# 6. takes in two lists and returns a sorted list made up of the content within the two lists
def merge(left, right):
    global comp_count, swap_count
    # 7. Initialize an empty list output that will be populated with sorted elements.
    # Initialize two variables i and j which are used pointers when iterating through the lists.
    output = []
    i = j = 0

    # 8. Executes the while loop if both pointers i and j are less than the length of the left and right lists
    while i < len(left) and j < len(right):
        # 9. Compare the elements at every position of both lists during each iteration
        comp_count += 1
        if left[i] < right[j]:
            # output is populated with the lesser value
            swap_count += 1
            output.append(left[i])
            # 10. Move pointer to the right
            i += 1
        else:
            swap_count += 1
            output.append(right[j])
            j += 1
    # 11. The remnant elements are picked from the current pointer value to the end of the respective list
    output.extend(left[i:])
    output.extend(right[j:])

    return output


# function to find the partition position
def partition(array, low, high):
    global comp_count, swap_count
    # choose the rightmost element as pivot
    pivot = array[high]

    # pointer for greater element
    i = low - 1

    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        comp_count += 1
        if array[j] <= pivot:
            # if element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # swapping element at i with element at j
            swap_count += 1
            (array[i], array[j]) = (array[j], array[i])

    # swap the pivot element with the greater element specified by i
    swap_count += 1
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    # return the position from where partition is done
    return i + 1


# function to perform quicksort
def quick_sort(array, low, high):
    if low < high:
        # find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)

        # recursive call on the left of pivot
        quick_sort(array, low, pi - 1)

        # recursive call on the right of pivot
        quick_sort(array, pi + 1, high)


def shell_sort(array):
    global comp_count, swap_count

    interval = 1  # Using defined formula min size must be greater than 1 at least
    n = len(array)  # Size of the array

    # Ignoring the comp count to determine the highest interval for accuracy
    # Calculate the highest possible interval to start with
    while interval < (n / 3):
        interval = interval * 3 + 1

    while interval > 0:
        for i in range(interval, n):
            temp = array[i]
            j = i

            comp_count += 2  # 2 comparisons
            while j >= interval and array[j - interval] > temp:
                array[j] = array[j - interval]
                j -= interval

            swap_count += 1
            array[j] = temp
        interval = int((interval - 1) / 3)  # Calculate next lowest interval


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
                output_writer.writerow(['bubble_sort', config, MIN_SIZE, MAX_SIZE, TRIALS])
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
                output_writer.writerow(['Algorithm', 'initial_configuration', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
                output_writer.writerow(['selection_sort', config, MIN_SIZE, MAX_SIZE, TRIALS])
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

                            selection_sort(list)
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

                            selection_sort(new_list)
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

                            selection_sort(list)
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
                console_log(f"Testing Insertion Sort with {TRIALS} trials on arrays sized {MIN_SIZE} to {MAX_SIZE}")
                output_writer.writerow(['Algorithm', 'initial_configuration', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
                output_writer.writerow(['insertion_sort', config, MIN_SIZE, MAX_SIZE, TRIALS])
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

        def mergesort_manager():
            global comp_count, swap_count, CONFIG

            for config in CONFIG:
                console_log(f"Testing Insertion Sort with {TRIALS} trials on arrays sized {MIN_SIZE} to {MAX_SIZE}")
                output_writer.writerow(['Algorithm', 'initial_configuration', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
                output_writer.writerow(['merge', config, MIN_SIZE, MAX_SIZE, TRIALS])
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

                            merge_sort(list)
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

                            merge_sort(new_list)
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

                            merge_sort(list)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                    console_log(f"size: {size}")
                    output_writer.writerow([size, '', sort_time / TRIALS, sort_comps // TRIALS, sort_swaps // TRIALS])
                    size *= 2

        def quicksort_manager():
            global comp_count, swap_count, CONFIG

            for config in CONFIG:
                console_log(f"Testing Quick Sort with {TRIALS} trials on arrays sized {MIN_SIZE} to {MAX_SIZE}")
                output_writer.writerow(['Algorithm', 'initial_configuration', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
                output_writer.writerow(['quick_sort', config, MIN_SIZE, MAX_SIZE, TRIALS])
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

                            # Selecting the last element as the pivot
                            quick_sort(list, 0, len(list) - 1)
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

                            # Selecting the last element as the pivot
                            quick_sort(new_list, 0, len(new_list) - 1)
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

                            quick_sort(list, 0, len(list) - 1)
                            # calculate & record elapsed time & steps
                            sort_time += (datetime.now() - before_time).microseconds
                            sort_comps += comp_count
                            sort_swaps += swap_count
                    console_log(f"size: {size}")
                    output_writer.writerow([size, '', sort_time / TRIALS, sort_comps // TRIALS, sort_swaps // TRIALS])
                    size *= 2

        def shellsort_manager():
            global comp_count, swap_count, CONFIG

            for config in CONFIG:
                console_log(f"Testing Quick Sort with {TRIALS} trials on arrays sized {MIN_SIZE} to {MAX_SIZE}")
                output_writer.writerow(['Algorithm', 'initial_configuration', 'MIN_SIZE', 'MAX_SIZE', 'TRIALS'])
                output_writer.writerow(['shell_sort', config, MIN_SIZE, MAX_SIZE, TRIALS])
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

                            shell_sort(list)
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

                            shell_sort(new_list)
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

                            shell_sort(list)
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
        mergesort_manager()
        quicksort_manager()
        shellsort_manager()


if __name__ == '__main__':
    print('Please wait...')
    main()
    print('File saved in your project directory.')

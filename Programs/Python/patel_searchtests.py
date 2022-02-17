# Name       : Umangkumar Patel
# Date       : February 18, 2022
# Instructor : Professor Eugene
# Description: Run series of tests to illustrate the big-O efficiency
#              of linear search and binary search via random numbers
#              with & without duplicates from (1-100) inclusive
# GitHub     : https://github.com/ukpatell/Python.git
# Sources    : Linear Search: https://www.geeksforgeeks.org/python-program-for-linear-search/
#              Binary Search: https://www.geeksforgeeks.org/python-program-for-binary-search/

import csv
import random
import time

import numpy as np

# Dictionary to store the data for output
# 3 Tests will be performed
Dict = {'Size': [], 'Low': [], 'High': [], 'Duplicate': [], 'Unique': [],
        'LinearSearch': [], 'Start1': [], 'End1': [], 'Total1': [],
        'BinarySearch': [], 'Start2': [], 'End2': [], 'Total2': []}


def list_generator(index):
    size = [1000, 5000, 25000, 75000, 375000, 1875000]  # Different Sizes to be tested
    low, high = 1, int(size[index])  # Range: 1 - Size

    randList = np.random.randint(low, high, size[index])  # Generate Random List
    Dict['Size'].append(size[index])  # Enter Values in Dictionary for Output
    Dict['Low'].append(low)
    Dict['High'].append(high)

    uniqueNum = len(np.unique(randList)) / len(randList)  # Unique Value Calculation
    dupliNum = "{:.2%}".format(1 - uniqueNum)  # Duplicate Values Calculation
    Dict['Unique'].append("{:.2%}".format(uniqueNum))  # Enter Values in Dictionary for output
    Dict['Duplicate'].append(dupliNum)

    key = random.randrange(low, high)  # Value to search in both binary & linear for comparison - Test #1

    linear_search(randList, key)

    sortedList = sorted(randList)  # Sort the list

    startTime = round(time.time() * 1000)  # Start Time for Binary Search Test
    binary_search(sortedList, low, int(size[index]), key, startTime)

    index += 1  # Increase Counter for next size
    if index == len(size):  # Break if reached end of size-array
        return

    list_generator(index)  # Next Size


# Linear Search
def linear_search(arr, value):
    start_time = round(time.time() * 1000)  # Start Time
    for i in range(len(arr)):
        if arr[i] == value:
            end_time = round(time.time() * 1000)  # End Time, if found
            Dict['LinearSearch'].append(f'Success. Element {value} found at index {i}')
            Dict['Start1'].append(start_time)
            Dict['End1'].append(end_time)
            Dict['Total1'].append(end_time - start_time)
            break

        if i == len(arr) - 1 and arr[i] != value:  # Break if element not found
            end_time = round(time.time() * 1000)
            Dict['LinearSearch'].append(f'Element {value} Not Found')
            Dict['Start1'].append(start_time)
            Dict['End1'].append(end_time)
            Dict['Total1'].append(end_time - start_time)
            break


# Binary Search
def binary_search(array, low, high, x, start_time):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if array[mid] == x:
            e_time = round(time.time() * 1000)  # End Time, if found
            Dict['BinarySearch'].append(f'Success. Element {x} found at index {mid}')
            Dict[f'Start2'].append(start_time)
            Dict[f'End2'].append(e_time)
            Dict[f'Total2'].append(e_time - start_time)

            # If element is smaller than mid, then it can only
        # be present in left subarray
        elif array[mid] > x:
            return binary_search(array, low, mid - 1, x, start_time)

        # Else the element can only be present in right subarray
        else:
            return binary_search(array, mid + 1, high, x, start_time)

    else:
        # Element is not present in the array
        e_time = round(time.time_ns() * 1000)  # End Time, if not found
        Dict['BinarySearch'].append(f'Element {x} Not Found')
        Dict['Start2'].append(start_time)
        Dict['End2'].append(e_time)
        Dict['Total2'].append(e_time - start_time)


list_generator(0)

with open("patel_searchtests_output.csv", "w") as f:
    new_val = csv.writer(f)
    new_val.writerow(Dict.keys())
    new_val.writerows(zip(*Dict.values()))

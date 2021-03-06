'''

Problem number - 2
Difficulty rating - Hard
Company - Uber

Given an array of integers, return a new array such that each element at index i 
of the new array is the product of all the numbers in the original array except
the one at i.

For example, if our input was [1, 2, 3, 4, 5], the expected output would be 
[120, 60, 40, 30, 24]. If our input was [3, 2, 1], the expected output would be 
[2, 3, 6].

Follow-up: what if you can't use division?

'''
import numpy as np

def naive(array):
    
    prod = 1
    for i in array :
        prod = prod * i

    ret_arr = []
    for i in array :
        ret_arr.append(int(prod/i))

    return ret_arr

def main():
    
    # generate array
    array = np.random.randint(1,10,5)
    print(array)
    print(naive(array))


if __name__ == "__main__" :
    main()
    
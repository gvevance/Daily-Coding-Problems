'''

Problem number - 1
Difficulty rating - Easy
Company - Google

Given a list of numbers and a number k, return whether any two numbers from the
list add up to k.

For example, given [10, 15, 3, 7] and k of 17, return true since 10 + 7 is 17.

Bonus: Can you do this in one pass?

'''

import numpy as np

def solution_naive(arr,k):
    ''' O(n^2) solution. 
    Logic - For every item in array, see if you have the corresponding array element to its right. '''
    
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            if arr[i]+arr[j] == k :
                return True
    return False

def solution_onepass(arr,k):
    ''' O(n) time complexity, O(n) space complexity. A hashmap or dictionary has O(1) search time.
    If the item (k-array[i]) does not exist to its left (that which is already stored in the dic), add this element.
    Using a set may have saved some more space because we didn't want a value stored for any key although using a 
    dict means we have to store something as value - used Bool. If you store an int, it will take more bytes still.'''
    
    dic = {}
    for i in range(len(arr)):
        if k-arr[i] not in dic :
            dic[arr[i]] = True
        else :
            return True
    
    return False

def solution_onepass_2(arr,k):
    ''' Same as above, but uses less space although space complexity is O(n) too.'''
    
    map = set()
    for i in range(len(arr)):
        if k-arr[i] not in map :
            map.add(arr[i])
        else :
            return True
    
    return False


def main():
    # generate random array of integers
    arr = np.random.randint(low=0,high=100,size=100)
    print(arr)
    k = 170
    print(solution_naive(arr,k))
    print(solution_onepass(arr,k))
    print(solution_onepass_2(arr,k))


if __name__ == "__main__" :
    main()
    

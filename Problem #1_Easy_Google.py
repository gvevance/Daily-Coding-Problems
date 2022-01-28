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
    ''' O(n^2) solution '''
    
    for i in range(len(arr)):
        for j in range(i+1,len(arr)):
            if arr[i]+arr[j] == k :
                return True
    return False

def solution_onepass(arr,k):
    
    dic = {}
    for i in range(len(arr)):
        if k-arr[i] not in dic :
            dic[arr[i]] = True
        else :
            return True
    
    return False


def main():
    # generate random array of integers
    arr = np.random.randint(low=0,high=5,size=10)
    print(arr)
    k = 10
    print(k)
    print(solution_naive(arr,k))
    print(solution_onepass(arr,k))


if __name__=="__main__":
    main()
    

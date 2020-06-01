from typing import List

m = [1, 2, 3, 5]

def missingNumber(nums):
    dum = [None] * len(nums)
    dum[0] = nums[0]
    if len(nums) == 1:
        return nums[0]
    for i in range(1, len(nums)):
        if nums[i] - dum[i-1] == 1:
            dum[i] = nums[i]
        else:
            return dum[i-1]+1

print(list(range(4)))
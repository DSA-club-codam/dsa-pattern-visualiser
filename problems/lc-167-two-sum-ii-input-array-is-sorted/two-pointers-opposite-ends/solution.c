#include <stdlib.h>  // @hide

int* twoSum(int* numbers, int numbersSize, int target, int* returnSize) {
    int left = 0, right = numbersSize - 1;  // start at both ends  // @a:init
    while (left < right) {  // @a:loop
        int total = numbers[left] + numbers[right];  // @a:sum
        if (total == target) {  // found the pair  // @a:check
            int* res = malloc(2 * sizeof(int));  // the caller frees it
            res[0] = left + 1;  // 1-indexed
            res[1] = right + 1;
            *returnSize = 2;
            return res;  // @a:found
        }
        if (total < target) {  // too small: need a bigger left value  // @a:small
            left++;  // @a:left
        } else {  // too big: need a smaller right value
            right--;  // @a:right
        }
    }
    *returnSize = 0;  // never reached: there is always exactly one pair
    return NULL;
}

#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    vector<int> twoSum(vector<int>& numbers, int target) {
        int left = 0, right = (int)numbers.size() - 1;  // start at both ends  // @a:init
        while (left < right) {  // @a:loop
            int total = numbers[left] + numbers[right];  // @a:sum
            if (total == target) {  // found the pair  // @a:check
                return {left + 1, right + 1};  // 1-indexed  // @a:found
            }
            if (total < target) {  // too small: need a bigger left value  // @a:small
                left++;  // @a:left
            } else {  // too big: need a smaller right value
                right--;  // @a:right
            }
        }
        return {};  // never reached: there is always exactly one pair
    }
};

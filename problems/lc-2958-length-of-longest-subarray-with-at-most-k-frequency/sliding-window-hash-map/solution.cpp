#include <algorithm>  // @hide
#include <unordered_map>  // @hide
#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int maxSubarrayLength(vector<int>& nums, int k) {
        unordered_map<int, int> count;  // value -> times it is in the window  // @a:init
        int left = 0;  // left edge of the window
        int longest = 0;  // length of the longest good window so far
        for (int right = 0; right < (int)nums.size(); right++) {  // right edge, moves every step  // @a:loop
            count[nums[right]]++;  // add nums[right] to the window  // @a:expand
            while (count[nums[right]] > k) {  // only nums[right] can be over the limit  // @a:while
                count[nums[left]]--;  // drop nums[left] from the window  // @a:shrink
                left++;
            }
            int length = right - left + 1;  // length of the good window [left, right]
            longest = max(longest, length);  // keep the longest  // @a:update
        }
        return longest;  // @a:return
    }
};

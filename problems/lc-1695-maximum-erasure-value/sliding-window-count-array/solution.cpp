#include <algorithm>  // @hide
#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    int maximumUniqueSubarray(vector<int>& nums) {
        vector<int> count(10001, 0);  // value -> times it is in the window (values are 1..10^4)  // @a:init
        int left = 0;  // left edge of the window
        int total = 0;  // sum of the window nums[left..right]
        int largest = 0;  // largest window sum so far
        for (int right = 0; right < (int)nums.size(); right++) {  // right edge, moves every step  // @a:loop
            count[nums[right]]++;  // add nums[right] to the window  // @a:expand
            total += nums[right];
            while (count[nums[right]] > 1) {  // only nums[right] can be a repeat  // @a:while
                count[nums[left]]--;  // drop nums[left] from the window  // @a:shrink
                total -= nums[left];
                left++;
            }
            largest = max(largest, total);  // unique window: keep the largest sum  // @a:update
        }
        return largest;  // @a:return
    }
};

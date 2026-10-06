#include <utility>  // @hide
#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    void moveZeroes(vector<int>& nums) {
        int slow = 0;  // next free slot for a non-zero  // @a:init
        for (int fast = 0; fast < (int)nums.size(); fast++) {  // fast visits every element once  // @a:loop
            if (nums[fast] != 0) {  // found a non-zero  // @a:check
                swap(nums[slow], nums[fast]);  // send it left  // @a:swap
                slow++;  // slot filled, move on  // @a:advance
            }
        }
        // loop ends: every zero now sits after the last non-zero  // @a:done
    }
};

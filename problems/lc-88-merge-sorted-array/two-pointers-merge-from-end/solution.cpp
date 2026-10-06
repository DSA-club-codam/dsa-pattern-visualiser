#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    void merge(vector<int>& nums1, int m, vector<int>& nums2, int n) {
        int p1 = m - 1;  // last real value in nums1  // @a:init
        int p2 = n - 1;  // last value in nums2
        int write = m + n - 1;  // last slot of nums1: fill from the back
        while (p2 >= 0) {  // nums2 still has values to place  // @a:loop
            if (p1 >= 0 && nums1[p1] > nums2[p2]) {  // the larger value is in nums1  // @a:compare
                nums1[write] = nums1[p1];  // move it to the back  // @a:take1
                p1--;
            } else {
                nums1[write] = nums2[p2];  // the larger value is in nums2, or nums1 is used up  // @a:take2
                p2--;
            }
            write--;  // @a:advance
        }
        // p2 < 0: nums1[0..p1] were already in place  // @a:done
    }
};

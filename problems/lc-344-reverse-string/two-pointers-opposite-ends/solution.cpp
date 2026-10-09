#include <utility>  // @hide
#include <vector>  // @hide
using namespace std;  // @hide

class Solution {
public:
    void reverseString(vector<char>& s) {
        int left = 0, right = (int)s.size() - 1;  // start at both ends  // @a:init
        while (left < right) {  // @a:loop
            swap(s[left], s[right]);  // @a:swap
            left++;  // move both inwards  // @a:move
            right--;
        }
        // loop ends: left and right met or crossed  // @a:done
    }
};

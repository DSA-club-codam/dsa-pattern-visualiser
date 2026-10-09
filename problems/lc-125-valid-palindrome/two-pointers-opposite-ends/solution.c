#include <ctype.h>  // @hide
#include <stdbool.h>  // @hide
#include <string.h>  // @hide

bool isPalindrome(char* s) {
    int left = 0, right = (int)strlen(s) - 1;  // start at both ends  // @a:init
    while (left < right) {  // @a:loop
        while (left < right && !isalnum((unsigned char)s[left])) {  // skip what does not count  // @a:skipLeftLoop
            left++;  // @a:skipLeft
        }
        while (left < right && !isalnum((unsigned char)s[right])) {  // @a:skipRightLoop
            right--;  // @a:skipRight
        }
        if (tolower((unsigned char)s[left]) != tolower((unsigned char)s[right])) {  // compare, ignoring case  // @a:compare
            return false;  // @a:mismatch
        }
        left++;  // move both inwards  // @a:move
        right--;
    }
    return true;  // every pair matched  // @a:done
}

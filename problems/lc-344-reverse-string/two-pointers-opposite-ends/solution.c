void reverseString(char* s, int sSize) {
    int left = 0, right = sSize - 1;  // start at both ends  // @a:init
    while (left < right) {  // @a:loop
        char tmp = s[left];  // swap s[left] and s[right]  // @a:swap
        s[left] = s[right];
        s[right] = tmp;
        left++;  // move both inwards  // @a:move
        right--;
    }
    // loop ends: left and right met or crossed  // @a:done
}

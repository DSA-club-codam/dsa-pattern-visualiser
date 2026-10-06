void moveZeroes(int* nums, int numsSize) {
    int slow = 0;  // next free slot for a non-zero  // @a:init
    for (int fast = 0; fast < numsSize; fast++) {  // fast visits every element once  // @a:loop
        if (nums[fast] != 0) {  // found a non-zero  // @a:check
            int tmp = nums[slow];  // send it left: swap nums[slow] and nums[fast]  // @a:swap
            nums[slow] = nums[fast];
            nums[fast] = tmp;
            slow++;  // slot filled, move on  // @a:advance
        }
    }
    // loop ends: every zero now sits after the last non-zero  // @a:done
}

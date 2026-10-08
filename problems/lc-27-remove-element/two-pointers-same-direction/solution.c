int removeElement(int* nums, int numsSize, int val) {
    int slow = 0;  // next slot for a value we keep  // @a:init
    for (int fast = 0; fast < numsSize; fast++) {  // fast reads every element once  // @a:loop
        if (nums[fast] != val) {  // keep this value  // @a:check
            nums[slow] = nums[fast];  // copy it forward  // @a:write
            slow++;  // slot filled, move on  // @a:advance
        }
    }
    return slow;  // k = number of values kept  // @a:done
}

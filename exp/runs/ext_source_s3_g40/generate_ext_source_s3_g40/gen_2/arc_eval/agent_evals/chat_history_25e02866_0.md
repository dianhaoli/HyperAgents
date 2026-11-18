Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (14x14):
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 3 3 3 3 2 2 2 2 2 2 2 2 2
2 3 3 3 3 2 2 2 2 2 2 2 2 2
2 3 3 1 3 2 2 2 2 2 2 2 2 2
2 3 3 3 3 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 3 3 3 3 2 2 2
2 2 2 2 2 2 2 3 6 6 3 2 2 2
2 2 2 2 2 2 2 3 6 3 3 2 2 2
2 2 2 2 2 2 2 3 3 3 3 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
Output (4x4):
3 3 3 3
3 6 6 3
3 6 1 3
3 3 3 3

## Example 2
Input (16x16):
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 2 1 1 2 2 8 8 8 8 8 8 8 8 8
8 8 2 1 2 2 2 8 8 8 2 2 2 2 2 8
8 8 2 2 2 2 2 8 8 8 2 2 2 4 2 8
8 8 2 2 2 2 2 8 8 8 2 2 2 4 2 8
8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 8
8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 8
8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 2 3 3 3 2 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
Output (5x5):
2 2 2 2 2
2 1 1 4 2
2 1 2 4 2
2 3 3 3 2
2 2 2 2 2

## Test
Input (18x18):
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 3 3 3 3 3 3 4 4 4 4
4 3 3 3 3 3 3 4 3 3 3 3 3 3 4 4 4 4
4 3 3 2 3 3 3 4 3 3 3 3 3 3 4 4 4 4
4 3 2 2 3 3 3 4 3 5 5 3 3 3 4 4 4 4
4 3 3 3 3 3 3 4 3 5 5 3 3 3 4 4 4 4
4 3 3 3 3 3 3 4 3 3 3 3 3 3 4 4 4 4
4 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 4
4 4 3 3 3 3 3 3 4 4 3 3 3 3 3 3 4 4
4 4 3 3 3 3 3 3 4 4 3 3 3 3 1 3 4 4
4 4 3 3 3 8 8 3 4 4 3 3 3 3 3 3 4 4
4 4 3 3 3 8 3 3 4 4 3 3 3 3 3 3 4 4
4 4 3 3 3 3 3 3 4 4 3 3 3 3 3 3 4 4
4 4 4 4 4 4 4 4 4 4 3 3 3 3 3 3 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 1, 3], [3, 3, 2, 3, 3, 3], [3, 5, 5, 8, 8, 3], [3, 5, 5, 8, 3, 3], [3, 3, 3, 3, 3, 3]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (14x14):
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 3 3 3 3 2 2 2 2 2 2 2 2 2
2 3 3 3 3 2 2 2 2 2 2 2 2 2
2 3 3 1 3 2 2 2 2 2 2 2 2 2
2 3 3 3 3 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 3 3 3 3 2 2 2
2 2 2 2 2 2 2 3 6 6 3 2 2 2
2 2 2 2 2 2 2 3 6 3 3 2 2 2
2 2 2 2 2 2 2 3 3 3 3 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2
Output (4x4):
3 3 3 3
3 6 6 3
3 6 1 3
3 3 3 3

## Example 2
Input (16x16):
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 2 1 1 2 2 8 8 8 8 8 8 8 8 8
8 8 2 1 2 2 2 8 8 8 2 2 2 2 2 8
8 8 2 2 2 2 2 8 8 8 2 2 2 4 2 8
8 8 2 2 2 2 2 8 8 8 2 2 2 4 2 8
8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 8
8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 8
8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 2 3 3 3 2 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
Output (5x5):
2 2 2 2 2
2 1 1 4 2
2 1 2 4 2
2 3 3 3 2
2 2 2 2 2

## Test
Input (18x18):
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 3 3 3 3 3 3 4 4 4 4
4 3 3 3 3 3 3 4 3 3 3 3 3 3 4 4 4 4
4 3 3 2 3 3 3 4 3 3 3 3 3 3 4 4 4 4
4 3 2 2 3 3 3 4 3 5 5 3 3 3 4 4 4 4
4 3 3 3 3 3 3 4 3 5 5 3 3 3 4 4 4 4
4 3 3 3 3 3 3 4 3 3 3 3 3 3 4 4 4 4
4 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 4
4 4 3 3 3 3 3 3 4 4 3 3 3 3 3 3 4 4
4 4 3 3 3 3 3 3 4 4 3 3 3 3 1 3 4 4
4 4 3 3 3 8 8 3 4 4 3 3 3 3 3 3 4 4
4 4 3 3 3 8 3 3 4 4 3 3 3 3 3 3 4 4
4 4 3 3 3 3 3 3 4 4 3 3 3 3 3 3 4 4
4 4 4 4 4 4 4 4 4 4 3 3 3 3 3 3 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[3, 3, 3, 3, 3, 3], [3, 3, 3, 3, 1, 3], [3, 3, 2, 3, 3, 3], [3, 2, 2, 8, 8, 3], [3, 5, 5, 8, 3, 3], [3, 3, 3, 3, 3, 3]]</answer>


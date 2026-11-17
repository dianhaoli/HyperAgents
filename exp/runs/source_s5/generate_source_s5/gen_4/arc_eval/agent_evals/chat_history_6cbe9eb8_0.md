Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (14x22):
0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1
1 8 8 8 8 8 8 8 8 8 8 8 1 2 3 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 4 4 4 4 4 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 4 4 4 4 4 4 3 0 6 6 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 6 6 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 2 3 0 1 2
0 8 8 8 8 8 8 8 8 8 8 8 0 1 2 3 0 1 2 3 0 1
1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
Output (12x11):
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 8 8 8 8 8 8 8 8 8 8

## Example 2
Input (13x23):
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 4 4 1 2 0 1
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 8 8 4 4 2 0 1 2
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
0 1 2 0 1 3 3 3 3 3 3 3 3 3 8 6 6 6 8 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 8 8 8 8 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 3 3 3 3 3 3 3 3 3 3 3 0 1 2 0 1 2
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1
Output (9x12):
3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 8 6 6 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3

## Example 3
Input (16x23):
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 3 3 3 3 3 3 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 4 4 4 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 3 3 3 3 3 3 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
Output (8x8):
3 3 3 3 3 3 3 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 3 3 3 3 3 3 3

## Test
Input (19x27):
2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3
1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 3 1 1 9 9 1 3 1 1
2 3 3 8 3 3 2 3 3 2 3 3 2 3 3 8 3 3 2 3 3 9 9 3 2 3 3
1 2 2 8 2 2 1 2 2 1 2 2 1 2 2 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 1 1 3 1 1 8 1 1 3 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 6 6 6 6 6 6 6 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 6 2 1 2 2 8 2 2 6 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 6 1 3 4 4 4 4 1 6 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 3 2 4 4 4 4 3 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 6 2 1 4 4 4 4 2 6 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 6 1 3 1 1 8 1 1 6 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 6 6 6 6 6 6 6 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 2 2 1 2 2 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 1 1 3 1 1 8 1 1 3 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 3 3 2 3 3 8 3 3 2 3 3 2 3 3 2 3 3
1 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1
2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3

Infer one compact transformation rule from the demonstrations and check that it explains every training pair, including object shapes, colors, positions, and grid dimensions. Apply that rule to the test grid; do not assume its output has the same dimensions or layout as the input. Before answering, check the proposed grid cell-by-cell and ensure it follows the rule. If multiple rules fit, choose the simplest rule that explains all examples.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 8], [8, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 4, 4, 4, 4, 0, 0, 0, 6, 0, 0, 8], [8, 6, 4, 4, 4, 4, 0, 0, 0, 6, 0, 0, 8], [8, 6, 4, 4, 4, 4, 0, 0, 0, 6, 9, 9, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 9, 9, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (14x22):
0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1
1 8 8 8 8 8 8 8 8 8 8 8 1 2 3 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 4 4 4 4 4 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 4 4 4 4 4 4 3 0 6 6 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 6 6 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 2 3 0 1 2
0 8 8 8 8 8 8 8 8 8 8 8 0 1 2 3 0 1 2 3 0 1
1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
Output (12x11):
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 8 8 8 8 8 8 8 8 8 8

## Example 2
Input (13x23):
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 4 4 1 2 0 1
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 8 8 4 4 2 0 1 2
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
0 1 2 0 1 3 3 3 3 3 3 3 3 3 8 6 6 6 8 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 8 8 8 8 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 3 3 3 3 3 3 3 3 3 3 3 0 1 2 0 1 2
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1
Output (9x12):
3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 8 6 6 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3

## Example 3
Input (16x23):
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 3 3 3 3 3 3 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 4 4 4 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 3 3 3 3 3 3 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
Output (8x8):
3 3 3 3 3 3 3 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 3 3 3 3 3 3 3

## Test
Input (19x27):
2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3
1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 3 1 1 9 9 1 3 1 1
2 3 3 8 3 3 2 3 3 2 3 3 2 3 3 8 3 3 2 3 3 9 9 3 2 3 3
1 2 2 8 2 2 1 2 2 1 2 2 1 2 2 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 1 1 3 1 1 8 1 1 3 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 6 6 6 6 6 6 6 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 6 2 1 2 2 8 2 2 6 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 6 1 3 4 4 4 4 1 6 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 3 2 4 4 4 4 3 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 6 2 1 4 4 4 4 2 6 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 6 1 3 1 1 8 1 1 6 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 6 6 6 6 6 6 6 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 2 2 1 2 2 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 1 1 3 1 1 8 1 1 3 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 3 3 2 3 3 8 3 3 2 3 3 2 3 3 2 3 3
1 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1
2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3

Infer one compact transformation rule from the demonstrations and check that it explains every training pair, including object shapes, colors, positions, and grid dimensions. Apply that rule to the test grid; do not assume its output has the same dimensions or layout as the input. Before answering, check the proposed grid cell-by-cell and ensure it follows the rule. If multiple rules fit, choose the simplest rule that explains all examples.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Independent verification pass: derive the rule from the demonstrations yourself rather than assuming a familiar ARC pattern. Check whether the scene is best explained by objects, symmetry, movement, repetition, a path or flood fill, color/count relationships, or a composed template. Trace the proposed operation against each training pair and verify that it changes only the cells or objects required by the rule. Recheck dimensions, boundaries, and every unusual test feature before choosing the output.
A previous independent attempt proposed this test grid: [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 8], [8, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 4, 4, 4, 4, 0, 0, 0, 6, 0, 0, 8], [8, 6, 4, 4, 4, 4, 0, 0, 0, 6, 0, 0, 8], [8, 6, 4, 4, 4, 4, 0, 0, 0, 6, 9, 9, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 9, 9, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]. Treat it only as a hypothesis: independently derive the rule and check whether this candidate follows it. Keep it only if it passes that check; otherwise provide the grid that does.
Return the final grid using the requested <answer> JSON tags.

Output: <answer>[[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 8], [8, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 4, 4, 4, 4, 0, 0, 0, 6, 0, 0, 8], [8, 6, 4, 4, 4, 4, 0, 0, 0, 6, 0, 0, 8], [8, 6, 4, 4, 4, 4, 0, 0, 0, 6, 9, 9, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 9, 9, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]</answer>


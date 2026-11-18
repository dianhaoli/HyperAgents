Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (5x5):
0 0 0 0 7
4 4 0 0 7
4 4 0 0 6
0 0 0 0 6
7 7 6 6 6
Output (15x15):
0 0 0 0 0 0 0 0 2 0 0 0 7 7 7
0 0 0 0 0 0 0 2 0 0 0 0 7 7 7
0 0 0 0 0 0 2 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 2 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 2 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 2 0 0 0 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6

## Example 2
Input (5x5):
0 0 0 0 3
0 8 8 0 3
0 8 8 0 3
0 0 0 0 3
3 3 3 3 3
Output (10x10):
2 0 0 0 0 0 0 2 3 3
0 2 0 0 0 0 2 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 2 0 0 0 0 2 0 3 3
2 0 0 0 0 0 0 2 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3

## Example 3
Input (5x5):
0 0 0 0 9
0 1 1 0 9
0 1 1 0 3
0 0 0 0 3
9 9 3 3 4
Output (20x20):
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 9
0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 9 9 9 9
0 0 2 0 0 0 0 0 0 0 0 0 0 2 0 0 9 9 9 9
0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 3 3 3 3
0 0 2 0 0 0 0 0 0 0 0 0 0 2 0 0 3 3 3 3
0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 3 3 3 3
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 3
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4

## Test
Input (5x5):
0 6 6 0 8
0 6 6 0 8
0 0 0 0 1
0 0 0 0 7
8 8 1 7 9

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,0,6,6,6,6,0,0,8,8],[0,0,6,6,6,6,0,0,8,8],[0,0,6,6,6,6,0,0,8,8],[0,0,6,6,6,6,0,0,8,8],[0,0,0,0,0,0,0,0,1,1],[0,0,0,0,0,0,0,0,1,1],[0,2,0,0,0,0,2,0,7,7],[2,0,0,0,0,0,0,2,7,7],[8,8,8,8,1,1,7,7,9,9],[8,8,8,8,1,1,7,7,9,9]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (5x5):
0 0 0 0 7
4 4 0 0 7
4 4 0 0 6
0 0 0 0 6
7 7 6 6 6
Output (15x15):
0 0 0 0 0 0 0 0 2 0 0 0 7 7 7
0 0 0 0 0 0 0 2 0 0 0 0 7 7 7
0 0 0 0 0 0 2 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 2 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 2 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 2 0 0 0 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6

## Example 2
Input (5x5):
0 0 0 0 3
0 8 8 0 3
0 8 8 0 3
0 0 0 0 3
3 3 3 3 3
Output (10x10):
2 0 0 0 0 0 0 2 3 3
0 2 0 0 0 0 2 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 2 0 0 0 0 2 0 3 3
2 0 0 0 0 0 0 2 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3

## Example 3
Input (5x5):
0 0 0 0 9
0 1 1 0 9
0 1 1 0 3
0 0 0 0 3
9 9 3 3 4
Output (20x20):
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 9
0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 9 9 9 9
0 0 2 0 0 0 0 0 0 0 0 0 0 2 0 0 9 9 9 9
0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 3 3 3 3
0 0 2 0 0 0 0 0 0 0 0 0 0 2 0 0 3 3 3 3
0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 3 3 3 3
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 3
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4

## Test
Input (5x5):
0 6 6 0 8
0 6 6 0 8
0 0 0 0 1
0 0 0 0 7
8 8 1 7 9

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Make this a genuinely independent second attempt. Before considering the previous candidate below, infer the transformation from the demonstrations again and work out the test output on your own. Then use the candidate only as an audit: check that it has the right dimensions and that its cells follow the rule demonstrated by every training pair. If it disagrees with your independently derived result or fails any check, return your corrected result; do not copy it merely because it is provided. If it passes, you may return it. Previous candidate (for audit only): [[0, 0, 6, 6, 6, 6, 0, 0, 8, 8], [0, 0, 6, 6, 6, 6, 0, 0, 8, 8], [0, 0, 6, 6, 6, 6, 0, 0, 8, 8], [0, 0, 6, 6, 6, 6, 0, 0, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 2, 0, 0, 0, 0, 2, 0, 7, 7], [2, 0, 0, 0, 0, 0, 0, 2, 7, 7], [8, 8, 8, 8, 1, 1, 7, 7, 9, 9], [8, 8, 8, 8, 1, 1, 7, 7, 9, 9]]
Return one output grid in the required <answer> tags.

Output: <answer>[[0,0,6,6,6,6,0,0,8,8],[0,0,6,6,6,6,0,0,8,8],[0,0,6,6,6,6,0,0,8,8],[0,0,6,6,6,6,0,0,8,8],[0,2,0,0,0,0,2,0,1,1],[2,0,0,0,0,0,0,2,1,1],[0,0,0,0,0,0,0,0,7,7],[0,0,0,0,0,0,0,0,7,7],[8,8,8,8,1,1,7,7,9,9],[8,8,8,8,1,1,7,7,9,9]]</answer>


Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Reason from the examples rather than guessing: compare input/output dimensions, colors, object counts and positions; identify what changes and what stays invariant; then check that the proposed rule explains every training pair before applying it. Preserve exact grid dimensions and use only colors supported by the examples or test input.

## Example 1
Input (4x4):
0 6 0 0
4 6 0 3
4 6 3 0
4 3 3 0
Output (8x8):
0 3 3 4 4 3 3 0
0 3 6 4 4 6 3 0
3 0 6 4 4 6 0 3
0 0 6 0 0 6 0 0
0 0 6 0 0 6 0 0
3 0 6 4 4 6 0 3
0 3 6 4 4 6 3 0
0 3 3 4 4 3 3 0

## Example 2
Input (3x3):
3 0 0
3 4 0
3 4 2
Output (6x6):
2 4 3 3 4 2
0 4 3 3 4 0
0 0 3 3 0 0
0 0 3 3 0 0
0 4 3 3 4 0
2 4 3 3 4 2

## Test
Input (8x8):
0 0 1 0 0 0 0 0
0 2 1 0 9 0 0 0
0 2 1 0 9 0 0 0
0 2 1 0 9 1 1 1
9 2 0 0 9 0 0 0
9 2 0 0 9 0 0 9
1 2 0 0 9 0 0 9
9 9 0 0 9 0 0 9

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[9,0,0,9,0,0,9,9,9,9,0,0,9,0,0,9],[9,0,0,9,0,0,2,1,1,2,0,0,9,0,0,9],[9,0,0,9,0,0,2,9,9,2,0,0,9,0,0,9],[0,0,0,9,0,0,2,9,9,2,0,0,9,0,0,0],[1,1,1,9,0,1,2,0,0,2,1,0,9,1,1,1],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[1,1,1,9,0,1,2,0,0,2,1,0,9,1,1,1],[0,0,0,9,0,0,2,9,9,2,0,0,9,0,0,0],[9,0,0,9,0,0,2,9,9,2,0,0,9,0,0,9],[9,0,0,9,0,0,2,1,1,2,0,0,9,0,0,9],[9,0,0,9,0,0,9,9,9,9,0,0,9,0,0,9]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Reason from the examples rather than guessing: compare input/output dimensions, colors, object counts and positions; identify what changes and what stays invariant; then check that the proposed rule explains every training pair before applying it. Preserve exact grid dimensions and use only colors supported by the examples or test input.

## Example 1
Input (4x4):
0 6 0 0
4 6 0 3
4 6 3 0
4 3 3 0
Output (8x8):
0 3 3 4 4 3 3 0
0 3 6 4 4 6 3 0
3 0 6 4 4 6 0 3
0 0 6 0 0 6 0 0
0 0 6 0 0 6 0 0
3 0 6 4 4 6 0 3
0 3 6 4 4 6 3 0
0 3 3 4 4 3 3 0

## Example 2
Input (3x3):
3 0 0
3 4 0
3 4 2
Output (6x6):
2 4 3 3 4 2
0 4 3 3 4 0
0 0 3 3 0 0
0 0 3 3 0 0
0 4 3 3 4 0
2 4 3 3 4 2

## Test
Input (8x8):
0 0 1 0 0 0 0 0
0 2 1 0 9 0 0 0
0 2 1 0 9 0 0 0
0 2 1 0 9 1 1 1
9 2 0 0 9 0 0 0
9 2 0 0 9 0 0 9
1 2 0 0 9 0 0 9
9 9 0 0 9 0 0 9

## Verification pass
A previous attempt at this puzzle produced the response below. Treat it only as a candidate, not as ground truth. Re-derive the transformation from the training pairs, check the candidate against that rule and the test grid, and correct it if needed. If it is sound, returning the same grid is appropriate.
<answer>[[9,0,0,9,0,0,9,9,9,9,0,0,9,0,0,9],[9,0,0,9,0,0,2,1,1,2,0,0,9,0,0,9],[9,0,0,9,0,0,2,9,9,2,0,0,9,0,0,9],[0,0,0,9,0,0,2,9,9,2,0,0,9,0,0,0],[1,1,1,9,0,1,2,0,0,2,1,0,9,1,1,1],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[1,1,1,9,0,1,2,0,0,2,1,0,9,1,1,1],[0,0,0,9,0,0,2,9,9,2,0,0,9,0,0,0],[9,0,0,9,0,0,2,9,9,2,0,0,9,0,0,9],[9,0,0,9,0,0,2,1,1,2,0,0,9,0,0,9],[9,0,0,9,0,0,9,9,9,9,0,0,9,0,0,9]]</answer>

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[9,0,0,9,0,0,9,9,9,9,0,0,9,0,0,9],[9,0,0,9,0,0,2,1,1,2,0,0,9,0,0,9],[9,0,0,9,0,0,2,9,9,2,0,0,9,0,0,9],[0,0,0,9,0,0,2,9,9,2,0,0,9,0,0,0],[1,1,1,9,0,1,2,0,0,2,1,0,9,1,1,1],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[0,0,9,0,1,2,0,0,0,0,2,1,0,9,0,0],[1,1,1,9,0,1,2,0,0,2,1,0,9,1,1,1],[0,0,0,9,0,0,2,9,9,2,0,0,9,0,0,0],[9,0,0,9,0,0,2,9,9,2,0,0,9,0,0,9],[9,0,0,9,0,0,2,1,1,2,0,0,9,0,0,9],[9,0,0,9,0,0,9,9,9,9,0,0,9,0,0,9]]</answer>


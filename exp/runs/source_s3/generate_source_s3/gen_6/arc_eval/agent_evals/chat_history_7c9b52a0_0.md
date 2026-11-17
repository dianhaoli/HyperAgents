Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Compare every example carefully: identify which objects, colors, shapes, positions, counts, and grid dimensions change or stay fixed. Prefer the simplest rule that explains all examples, and check that it also applies to the test. Before answering, verify the output's dimensions, every changed cell, and preservation of cells that should remain unchanged. Do not merely copy an example or assume a familiar rule without checking it against all demonstrations.

## Example 1
Input (16x16):
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8
8 1 1 0 0 8 8 8 8 0 0 3 3 8 8 8
8 0 0 0 0 8 8 8 8 0 0 0 0 8 8 8
8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8
8 8 8 0 0 2 0 8 8 8 8 8 8 8 8 8
8 8 8 0 2 2 0 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8
8 8 8 8 8 8 8 8 8 0 0 0 4 8 8 8
8 8 8 8 8 8 8 8 8 0 0 0 4 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
Output (3x4):
0 0 3 3
1 1 2 4
0 2 2 4

## Example 2
Input (16x16):
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 1 1 1 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 1 1 1 3 3 0 0 1 1
1 0 2 2 0 1 1 1 1 1 3 3 0 0 1 1
1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 4 4 4 4 1 1 1 1 1 1 1
1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1
1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1
1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
Output (4x4):
4 4 4 4
3 3 0 0
3 3 0 0
0 2 2 0

## Example 3
Input (16x16):
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 0 1 0 0 0 9 9 9 9 9 9 9 9 9
9 9 1 1 0 0 0 9 9 9 9 9 9 9 9 9
9 9 0 1 1 0 0 9 9 9 9 9 9 9 9 9
9 9 0 0 0 0 0 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 0 0 0 0 0 9 9 9 9 9
9 9 9 9 9 9 0 0 2 2 0 9 9 9 9 9
9 9 9 9 9 9 0 0 0 2 0 9 9 9 9 9
9 9 9 9 9 9 0 0 0 2 0 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
Output (4x5):
0 1 0 0 0
1 1 2 2 0
0 1 1 2 0
0 0 0 2 0

## Test
Input (16x16):
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 2 0 1 1 1 1 0 0 3 1 1 1 1 1
1 2 2 0 1 1 1 1 0 0 3 1 1 1 1 1
1 0 0 0 1 1 1 1 0 0 0 1 1 1 1 1
1 0 0 0 1 1 1 1 0 0 0 1 1 1 1 1
1 0 0 0 1 1 1 1 0 0 0 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 0 0 0 1 1 1 1 1 1 1 1 1 1
1 1 1 0 0 0 1 1 1 1 1 0 0 0 1 1
1 1 1 4 4 4 1 1 1 1 1 0 0 0 1 1
1 1 1 0 4 0 1 1 1 1 1 0 0 0 1 1
1 1 1 0 0 0 1 1 1 1 1 6 0 0 1 1
1 1 1 1 1 1 1 1 1 1 1 6 6 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0, 2, 3], [2, 2, 3], [0, 0, 4], [6, 4, 0], [6, 6, 0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Compare every example carefully: identify which objects, colors, shapes, positions, counts, and grid dimensions change or stay fixed. Prefer the simplest rule that explains all examples, and check that it also applies to the test. Before answering, verify the output's dimensions, every changed cell, and preservation of cells that should remain unchanged. Do not merely copy an example or assume a familiar rule without checking it against all demonstrations.

## Example 1
Input (16x16):
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8
8 1 1 0 0 8 8 8 8 0 0 3 3 8 8 8
8 0 0 0 0 8 8 8 8 0 0 0 0 8 8 8
8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 0 0 0 0 8 8 8 8 8 8 8 8 8
8 8 8 0 0 2 0 8 8 8 8 8 8 8 8 8
8 8 8 0 2 2 0 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8
8 8 8 8 8 8 8 8 8 0 0 0 4 8 8 8
8 8 8 8 8 8 8 8 8 0 0 0 4 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
Output (3x4):
0 0 3 3
1 1 2 4
0 2 2 4

## Example 2
Input (16x16):
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 1 1 1 1 1 0 0 0 0 1 1
1 0 0 0 0 1 1 1 1 1 3 3 0 0 1 1
1 0 2 2 0 1 1 1 1 1 3 3 0 0 1 1
1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 4 4 4 4 1 1 1 1 1 1 1
1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1
1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1
1 1 1 1 1 0 0 0 0 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
Output (4x4):
4 4 4 4
3 3 0 0
3 3 0 0
0 2 2 0

## Example 3
Input (16x16):
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 0 1 0 0 0 9 9 9 9 9 9 9 9 9
9 9 1 1 0 0 0 9 9 9 9 9 9 9 9 9
9 9 0 1 1 0 0 9 9 9 9 9 9 9 9 9
9 9 0 0 0 0 0 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 0 0 0 0 0 9 9 9 9 9
9 9 9 9 9 9 0 0 2 2 0 9 9 9 9 9
9 9 9 9 9 9 0 0 0 2 0 9 9 9 9 9
9 9 9 9 9 9 0 0 0 2 0 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
Output (4x5):
0 1 0 0 0
1 1 2 2 0
0 1 1 2 0
0 0 0 2 0

## Test
Input (16x16):
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 0 2 0 1 1 1 1 0 0 3 1 1 1 1 1
1 2 2 0 1 1 1 1 0 0 3 1 1 1 1 1
1 0 0 0 1 1 1 1 0 0 0 1 1 1 1 1
1 0 0 0 1 1 1 1 0 0 0 1 1 1 1 1
1 0 0 0 1 1 1 1 0 0 0 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 0 0 0 1 1 1 1 1 1 1 1 1 1
1 1 1 0 0 0 1 1 1 1 1 0 0 0 1 1
1 1 1 4 4 4 1 1 1 1 1 0 0 0 1 1
1 1 1 0 4 0 1 1 1 1 1 0 0 0 1 1
1 1 1 0 0 0 1 1 1 1 1 6 0 0 1 1
1 1 1 1 1 1 1 1 1 1 1 6 6 0 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0, 2, 3], [2, 2, 3], [4, 4, 4], [6, 4, 0]]</answer>


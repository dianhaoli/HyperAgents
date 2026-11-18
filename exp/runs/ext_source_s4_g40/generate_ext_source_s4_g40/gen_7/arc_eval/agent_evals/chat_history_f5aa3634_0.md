Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

Use all demonstration pairs as evidence, not just the most visually salient feature. Compare input and output dimensions, colors, objects, and positions in each pair; infer a rule that explains every pair, then check the proposed test output against that rule. Distinguish objects from background or isolated markers, and check alignment or repetition when relevant. Do not assume cells are unchanged unless the examples support it. Make the output dimensions consistent with the demonstrated transformation and include every output cell.

## Example 1
Input (15x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 2 2 8 0 0 0 0 0 0 0 0 0
0 3 2 8 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 1 2 0 0 0 0 0
0 0 0 8 0 0 0 2 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 0 6 8 0 0
0 0 8 8 8 0 0 0 6 6 8 0 0
0 0 5 5 5 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0
Output (3x3):
0 8 0
8 8 8
5 5 5
Input/output cell comparison: Cell-by-cell comparison is unavailable because the grid dimensions differ.

## Example 2
Input (10x13):
0 0 5 8 8 0 0 0 0 0 0 0 0
0 3 5 3 8 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 7 2 0
0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 3 5 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 5 8 8 0
0 0 3 2 0 0 0 0 3 5 3 8 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
Output (3x4):
0 5 8 8
3 5 3 8
0 3 3 0
Input/output cell comparison: Cell-by-cell comparison is unavailable because the grid dimensions differ.

## Example 3
Input (15x15):
0 0 2 8 0 0 0 0 0 0 0 5 9 0 0
0 0 8 2 0 0 0 0 0 7 7 5 9 0 0
0 8 8 0 0 0 0 0 0 0 5 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0
0 3 4 3 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 5 9 0
0 0 0 0 0 0 0 0 0 0 7 7 5 9 0
0 0 0 0 0 0 0 0 0 0 0 5 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (3x4):
0 0 5 9
7 7 5 9
0 5 7 0
Input/output cell comparison: Cell-by-cell comparison is unavailable because the grid dimensions differ.

## Test
Input (15x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 5 5 5 0 0 0 0 8 5 5 8 0
0 0 0 5 9 5 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 8 3 0 0 0 0 0
0 0 0 0 0 0 0 3 4 3 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0 0
0 2 2 0 0 0 0 0 4 0 0 0 0 0 0
0 7 2 0 0 0 0 0 0 0 0 3 8 3 0
0 0 7 7 0 0 0 0 0 0 0 3 4 3 0
0 0 0 7 0 0 0 0 2 0 0 0 4 0 0
0 0 0 0 0 0 0 1 2 0 0 0 4 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[3, 8, 3], [3, 4, 3], [0, 4, 0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

Use all demonstration pairs as evidence, not just the most visually salient feature. Compare input and output dimensions, colors, objects, and positions in each pair; infer a rule that explains every pair, then check the proposed test output against that rule. Distinguish objects from background or isolated markers, and check alignment or repetition when relevant. Do not assume cells are unchanged unless the examples support it. Make the output dimensions consistent with the demonstrated transformation and include every output cell.

## Example 1
Input (15x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 2 2 8 0 0 0 0 0 0 0 0 0
0 3 2 8 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 1 1 0 0 0 0
0 0 0 0 0 0 1 2 0 0 0 0 0
0 0 0 8 0 0 0 2 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 8 0 0 0 0 0 6 8 0 0
0 0 8 8 8 0 0 0 6 6 8 0 0
0 0 5 5 5 0 0 0 0 4 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0
Output (3x3):
0 8 0
8 8 8
5 5 5
Input/output cell comparison: Cell-by-cell comparison is unavailable because the grid dimensions differ.

## Example 2
Input (10x13):
0 0 5 8 8 0 0 0 0 0 0 0 0
0 3 5 3 8 0 0 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 7 7 2 0
0 0 0 0 0 0 0 0 0 0 2 2 0
0 0 3 5 2 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 5 8 8 0
0 0 3 2 0 0 0 0 3 5 3 8 0
0 0 0 0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
Output (3x4):
0 5 8 8
3 5 3 8
0 3 3 0
Input/output cell comparison: Cell-by-cell comparison is unavailable because the grid dimensions differ.

## Example 3
Input (15x15):
0 0 2 8 0 0 0 0 0 0 0 5 9 0 0
0 0 8 2 0 0 0 0 0 7 7 5 9 0 0
0 8 8 0 0 0 0 0 0 0 5 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0
0 3 4 3 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 5 9 0
0 0 0 0 0 0 0 0 0 0 7 7 5 9 0
0 0 0 0 0 0 0 0 0 0 0 5 7 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (3x4):
0 0 5 9
7 7 5 9
0 5 7 0
Input/output cell comparison: Cell-by-cell comparison is unavailable because the grid dimensions differ.

## Test
Input (15x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 0
0 0 0 5 5 5 0 0 0 0 8 5 5 8 0
0 0 0 5 9 5 0 0 0 0 0 0 0 0 0
0 0 0 0 9 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 8 3 0 0 0 0 0
0 0 0 0 0 0 0 3 4 3 0 0 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0 0 0 0
0 2 2 0 0 0 0 0 4 0 0 0 0 0 0
0 7 2 0 0 0 0 0 0 0 0 3 8 3 0
0 0 7 7 0 0 0 0 0 0 0 3 4 3 0
0 0 0 7 0 0 0 0 2 0 0 0 4 0 0
0 0 0 0 0 0 0 1 2 0 0 0 4 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[3, 8, 3], [3, 4, 3], [0, 4, 0]]</answer>


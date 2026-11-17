Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule, check that it reproduces every demonstration exactly, and apply it to the test input.

## Example 1
Input (7x7):
0 0 0 0 0 0 0
0 1 1 1 1 1 0
0 0 2 2 2 0 0
0 0 2 2 2 0 0
0 3 3 3 3 3 0
0 0 0 3 0 0 0
0 0 0 0 0 0 0
Output (7x7):
0 0 0 0 0 0 0
0 3 3 3 3 3 0
0 0 0 3 0 0 0
0 0 2 2 2 0 0
0 0 2 2 2 0 0
0 1 1 1 1 1 0
0 0 0 0 0 0 0

## Example 2
Input (13x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 1 1 1 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 5 5 5 5 5 5 5 0 0 0
0 0 0 5 5 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
Output (13x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0
0 0 0 5 5 0 0 0 5 5 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 1 1 1 0 1 1 1 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0

## Example 3
Input (13x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 1 0 0 0 0 0 1 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
Output (13x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 1 0 0 0 0 0 1 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0

## Test
Input (13x10):
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 0 0
0 0 3 0 3 3 0 3 0 0
0 0 3 3 3 3 3 3 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 0 0 2 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 4 4 4 4 4 4 0 0
0 0 0 8 0 0 8 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,0,0,0,0,0,0,0,0,0],[0,0,6,6,6,6,0,0,0,0],[0,0,0,8,0,0,8,0,0,0],[0,0,0,0,8,8,0,0,0,0],[0,0,4,4,4,4,4,4,0,0],[0,0,0,2,2,2,2,0,0,0],[0,0,0,2,0,0,2,0,0,0],[0,0,0,2,2,2,2,0,0,0],[0,0,0,0,2,2,0,0,0,0],[0,0,3,3,3,3,3,3,0,0],[0,0,3,0,3,3,0,3,0,0],[0,0,3,3,3,3,3,3,0,0],[0,0,0,0,0,0,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule, check that it reproduces every demonstration exactly, and apply it to the test input.

## Example 1
Input (7x7):
0 0 0 0 0 0 0
0 1 1 1 1 1 0
0 0 2 2 2 0 0
0 0 2 2 2 0 0
0 3 3 3 3 3 0
0 0 0 3 0 0 0
0 0 0 0 0 0 0
Output (7x7):
0 0 0 0 0 0 0
0 3 3 3 3 3 0
0 0 0 3 0 0 0
0 0 2 2 2 0 0
0 0 2 2 2 0 0
0 1 1 1 1 1 0
0 0 0 0 0 0 0

## Example 2
Input (13x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 1 1 1 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 5 5 5 5 5 5 5 0 0 0
0 0 0 5 5 0 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
Output (13x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0
0 0 0 5 5 0 0 0 5 5 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 3 0 3 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 2 0 0 0 0 0 2 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 1 1 1 0 1 1 1 0 0 0
0 0 0 0 0 1 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0

## Example 3
Input (13x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 1 0 0 0 0 0 1 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
Output (13x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 1 0 0 0 0 0 1 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 3 3 3 3 3 3 3 0 0 0
0 0 0 2 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 8 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0

## Test
Input (13x10):
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 0 0
0 0 3 0 3 3 0 3 0 0
0 0 3 3 3 3 3 3 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 2 0 0 2 0 0 0
0 0 0 2 2 2 2 0 0 0
0 0 0 0 2 2 0 0 0 0
0 0 4 4 4 4 4 4 0 0
0 0 0 8 0 0 8 0 0 0
0 0 0 0 8 8 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

A first attempt proposed this candidate test output:
[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 6, 0, 0, 0, 0], [0, 0, 0, 8, 0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 8, 8, 0, 0, 0, 0], [0, 0, 4, 4, 4, 4, 4, 4, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 2, 2, 0, 0, 0, 0], [0, 0, 3, 3, 3, 3, 3, 3, 0, 0], [0, 0, 3, 0, 3, 3, 0, 3, 0, 0], [0, 0, 3, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
Do not assume that candidate is correct. Independently infer and re-check the rule against every training input-output pair, then compare the rule's result with the candidate. Correct any mismatch and return your best final grid in the required <answer> tags.

Output: <answer>[[0,0,0,0,0,0,0,0,0,0],[0,0,6,6,6,6,0,0,0,0],[0,0,0,8,0,0,8,0,0,0],[0,0,0,0,8,8,0,0,0,0],[0,0,4,4,4,4,4,4,0,0],[0,0,0,2,2,2,2,0,0,0],[0,0,0,2,0,0,2,0,0,0],[0,0,0,2,2,2,2,0,0,0],[0,0,0,0,2,2,0,0,0,0],[0,0,3,3,3,3,3,3,0,0],[0,0,3,0,3,3,0,3,0,0],[0,0,3,3,3,3,3,3,0,0],[0,0,0,0,0,0,0,0,0,0]]</answer>


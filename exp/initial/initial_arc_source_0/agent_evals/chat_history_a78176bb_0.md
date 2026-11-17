Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (10x10):
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 5 9 0 0 0
0 0 0 0 0 5 5 9 0 0
0 0 0 0 0 5 5 5 9 0
0 0 0 0 0 5 5 5 5 9
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
Output (10x10):
0 0 0 0 0 9 0 0 0 0
9 0 0 0 0 0 9 0 0 0
0 9 0 0 0 0 0 9 0 0
0 0 9 0 0 0 0 0 9 0
0 0 0 9 0 0 0 0 0 9
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 9 0

## Example 2
Input (10x10):
7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 7 5 5 0 0 0 0
0 0 0 0 7 5 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7
Output (10x10):
7 0 0 0 7 0 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 0 7 0 0 0 7 0 0
0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7

## Example 3
Input (10x10):
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 2 5 5 0 0 0 0 0
0 0 0 2 5 0 0 0 0 0
0 0 0 5 2 0 0 0 0 0
0 0 0 5 5 2 0 0 0 0
0 0 0 5 5 5 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0
Output (10x10):
0 0 0 2 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 2 0 0 0 2 0 0
0 0 0 0 2 0 0 0 2 0
2 0 0 0 0 2 0 0 0 2
0 2 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 2 0

## Test
Input (10x10):
0 1 0 0 0 0 0 0 0 0
0 0 1 5 5 0 0 0 0 0
0 0 0 1 5 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 5 1 0 0 0 0
0 0 0 0 5 5 1 0 0 0
0 0 0 0 5 5 5 1 0 0
0 0 0 0 5 5 5 5 1 0
0 0 0 0 5 5 5 5 5 1
0 0 0 0 0 0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,1,0,0,0,1,0,0,0,0],[0,0,1,0,0,0,1,0,0,0],[0,0,0,1,0,0,0,1,0,0],[0,0,0,0,1,0,0,0,1,0],[1,0,0,0,0,1,0,0,0,1],[0,1,0,0,0,0,1,0,0,0],[0,0,1,0,0,0,0,1,0,0],[0,0,0,1,0,0,0,0,1,0],[0,0,0,0,1,0,0,0,0,1],[0,0,0,0,0,1,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (10x10):
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 5 9 0 0 0
0 0 0 0 0 5 5 9 0 0
0 0 0 0 0 5 5 5 9 0
0 0 0 0 0 5 5 5 5 9
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
Output (10x10):
0 0 0 0 0 9 0 0 0 0
9 0 0 0 0 0 9 0 0 0
0 9 0 0 0 0 0 9 0 0
0 0 9 0 0 0 0 0 9 0
0 0 0 9 0 0 0 0 0 9
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 9 0

## Example 2
Input (10x10):
7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 7 5 5 0 0 0 0
0 0 0 0 7 5 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7
Output (10x10):
7 0 0 0 7 0 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 0 7 0 0 0 7 0 0
0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7

## Example 3
Input (10x10):
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 2 5 5 0 0 0 0 0
0 0 0 2 5 0 0 0 0 0
0 0 0 5 2 0 0 0 0 0
0 0 0 5 5 2 0 0 0 0
0 0 0 5 5 5 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0
Output (10x10):
0 0 0 2 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 2 0 0 0 2 0 0
0 0 0 0 2 0 0 0 2 0
2 0 0 0 0 2 0 0 0 2
0 2 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 2 0

## Test
Input (10x10):
0 1 0 0 0 0 0 0 0 0
0 0 1 5 5 0 0 0 0 0
0 0 0 1 5 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 5 1 0 0 0 0
0 0 0 0 5 5 1 0 0 0
0 0 0 0 5 5 5 1 0 0
0 0 0 0 5 5 5 5 1 0
0 0 0 0 5 5 5 5 5 1
0 0 0 0 0 0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,1,0,1,0,0,0,0,0,0],[0,0,1,0,1,0,0,0,0,0],[0,0,0,1,0,1,0,0,0,0],[0,0,0,0,1,0,1,0,0,0],[0,0,0,0,0,1,0,1,0,0],[1,0,0,0,0,0,1,0,1,0],[0,1,0,0,0,0,0,1,0,1],[0,0,1,0,0,0,0,0,1,0],[0,0,0,1,0,0,0,0,0,1],[0,0,0,0,1,0,0,0,0,0]]</answer>


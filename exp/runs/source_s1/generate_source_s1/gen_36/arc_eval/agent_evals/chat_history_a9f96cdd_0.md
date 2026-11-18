Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (3x5):
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
Output (3x5):
0 0 0 0 0
0 8 0 7 0
0 0 0 0 0

## Example 2
Input (3x5):
0 0 0 0 0
0 0 0 0 0
0 0 0 0 2
Output (3x5):
0 0 0 0 0
0 0 0 3 0
0 0 0 0 0

## Example 3
Input (3x5):
0 0 0 0 0
0 0 0 2 0
0 0 0 0 0
Output (3x5):
0 0 3 0 6
0 0 0 0 0
0 0 8 0 7

## Example 4
Input (3x5):
0 0 0 0 0
0 2 0 0 0
0 0 0 0 0
Output (3x5):
3 0 6 0 0
0 0 0 0 0
8 0 7 0 0

## Test
Input (3x5):
0 0 0 0 0
0 0 0 0 2
0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0, 0, 0, 0, 0], [0, 0, 0, 3, 0], [0, 0, 0, 8, 0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (3x5):
0 0 2 0 0
0 0 0 0 0
0 0 0 0 0
Output (3x5):
0 0 0 0 0
0 8 0 7 0
0 0 0 0 0

## Example 2
Input (3x5):
0 0 0 0 0
0 0 0 0 0
0 0 0 0 2
Output (3x5):
0 0 0 0 0
0 0 0 3 0
0 0 0 0 0

## Example 3
Input (3x5):
0 0 0 0 0
0 0 0 2 0
0 0 0 0 0
Output (3x5):
0 0 3 0 6
0 0 0 0 0
0 0 8 0 7

## Example 4
Input (3x5):
0 0 0 0 0
0 2 0 0 0
0 0 0 0 0
Output (3x5):
3 0 6 0 0
0 0 0 0 0
8 0 7 0 0

## Test
Input (3x5):
0 0 0 0 0
0 0 0 0 2
0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

FRESH INDEPENDENT SOLVE: derive the transformation from the training pairs without assuming any previous answer. Check that the same concrete rule reproduces every demonstrated output, including cells that stay unchanged and any dimension changes. Only then apply it to the test input; verify the output dimensions and changed regions against that rule. Return the resulting grid inside <answer> tags, with nothing else inside the tags.

Output: <answer>[[0, 0, 0, 0, 0], [0, 0, 0, 3, 0], [0, 0, 0, 0, 0]]</answer>


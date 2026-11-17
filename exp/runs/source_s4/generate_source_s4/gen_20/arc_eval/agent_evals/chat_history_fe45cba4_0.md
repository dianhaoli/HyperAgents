Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule, check that it reproduces every demonstration exactly, and apply it to the test input.

## Example 1
Input (8x8):
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
2 7 7 7 7 9 9 9
2 2 2 7 7 7 7 7
2 2 2 7 7 2 2 2
2 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
Output (8x8):
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
7 7 7 7 7 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2

## Example 2
Input (8x8):
7 7 7 7 7 9 9 9
9 7 7 7 7 7 9 9
9 9 7 7 7 9 9 9
9 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
Output (8x8):
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2

## Test
Input (16x16):
7 7 7 7 7 7 7 7 7 7 9 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 9 9 9 9 9 9
8 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
8 8 7 8 7 7 7 7 7 7 7 7 7 7 7 7
8 8 8 8 8 7 7 7 7 7 7 7 7 7 7 7
8 8 7 8 7 7 7 7 7 7 8 8 8 8 8 8
8 7 7 7 7 7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 7 7 7 7 7 7 7 7 8 8
7 7 7 7 7 7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 7 7 7 7 8 8 8 8 8 8
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule, check that it reproduces every demonstration exactly, and apply it to the test input.

## Example 1
Input (8x8):
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
2 7 7 7 7 9 9 9
2 2 2 7 7 7 7 7
2 2 2 7 7 2 2 2
2 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
Output (8x8):
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
7 7 7 7 7 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2

## Example 2
Input (8x8):
7 7 7 7 7 9 9 9
9 7 7 7 7 7 9 9
9 9 7 7 7 9 9 9
9 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
Output (8x8):
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2

## Test
Input (16x16):
7 7 7 7 7 7 7 7 7 7 9 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 9 9 9 9 9 9
8 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
8 8 7 8 7 7 7 7 7 7 7 7 7 7 7 7
8 8 8 8 8 7 7 7 7 7 7 7 7 7 7 7
8 8 7 8 7 7 7 7 7 7 8 8 8 8 8 8
8 7 7 7 7 7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 7 7 7 7 7 7 7 7 8 8
7 7 7 7 7 7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 7 7 7 7 8 8 8 8 8 8
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

For this verification call, first derive the test output independently from the demonstrations, without consulting the candidate shown below. Check that your inferred rule reproduces every training output exactly. Only after deriving your own test grid, compare it with the first attempt; do not copy that candidate unless your independently checked rule supports it. Return the grid supported by the demonstrations in the required <answer> tags.

First-attempt candidate (for comparison only after your derivation):
[[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]

Output: <answer>[[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]</answer>


Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

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

Infer one compact transformation rule from the demonstrations and check that it explains every training pair, including object shapes, colors, positions, and grid dimensions. Apply that rule to the test grid; do not assume its output has the same dimensions or layout as the input. Before answering, check the proposed grid cell-by-cell and ensure it follows the rule. If multiple rules fit, choose the simplest rule that explains all examples.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[7,7,7,7,7,7,7,7,7,7,9,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,7,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,7,7,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

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

Infer one compact transformation rule from the demonstrations and check that it explains every training pair, including object shapes, colors, positions, and grid dimensions. Apply that rule to the test grid; do not assume its output has the same dimensions or layout as the input. Before answering, check the proposed grid cell-by-cell and ensure it follows the rule. If multiple rules fit, choose the simplest rule that explains all examples.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[7,7,7,7,7,7,7,7,7,7,9,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,7,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,9,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]]</answer>


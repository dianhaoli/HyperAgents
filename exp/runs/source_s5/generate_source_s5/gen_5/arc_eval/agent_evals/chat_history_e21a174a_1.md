Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

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
Input (7x7):
0 0 0 0 0 0 0
0 4 4 4 4 4 0
0 4 0 4 0 4 0
0 0 5 5 5 0 0
0 6 0 6 0 6 0
0 0 6 0 6 0 0
0 0 0 0 0 0 0

Infer one compact transformation rule from the demonstrations and check that it explains every training pair, including object shapes, colors, positions, and grid dimensions. Apply that rule to the test grid; do not assume its output has the same dimensions or layout as the input. Before answering, check the proposed grid cell-by-cell and ensure it follows the rule. If multiple rules fit, choose the simplest rule that explains all examples.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,6,0,6,0,6,0],[0,0,6,0,6,0,0],[0,0,5,5,5,0,0],[0,4,4,4,4,4,0],[0,4,0,4,0,4,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

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
Input (7x7):
0 0 0 0 0 0 0
0 4 4 4 4 4 0
0 4 0 4 0 4 0
0 0 5 5 5 0 0
0 6 0 6 0 6 0
0 0 6 0 6 0 0
0 0 0 0 0 0 0

Infer one compact transformation rule from the demonstrations and check that it explains every training pair, including object shapes, colors, positions, and grid dimensions. Apply that rule to the test grid; do not assume its output has the same dimensions or layout as the input. Before answering, check the proposed grid cell-by-cell and ensure it follows the rule. If multiple rules fit, choose the simplest rule that explains all examples.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The transformation is a vertical reflection of the grid: reverse the row order.

<answer>[[0,0,0,0,0,0,0],[0,0,6,0,6,0,0],[0,6,0,6,0,6,0],[0,0,5,5,5,0,0],[0,4,0,4,0,4,0],[0,4,4,4,4,4,0],[0,0,0,0,0,0,0]]</answer>


Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (1x1):
0
Output (1x1):
1

## Test
Input (1x1):
0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[1, 2], [3, 4]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (1x1):
0
Output (1x1):
1

## Test
Input (1x1):
0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Solve this independently; do not rely on or guess any previous answer. Infer one concrete rule from the demonstrations and check that it reproduces every output. Apply that rule from scratch to the test input, checking the output dimensions and each region that changes. Return the result in the required <answer> tags, with nothing else inside the tags.

Output: <answer>[[1, 2], [3, 4]]</answer>


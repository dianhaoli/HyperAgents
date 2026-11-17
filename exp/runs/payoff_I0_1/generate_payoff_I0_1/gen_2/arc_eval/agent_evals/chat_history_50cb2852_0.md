Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Treat every demonstration as an exact constraint: identify what changes and what stays fixed, infer one simple rule that explains all pairs, and check the proposed output's dimensions and cells against that rule. Consider object shape, position, color, symmetry, repetition, and whether the task crops, expands, or preserves the grid; do not assume any one of these applies.

## Example 1
Input (12x11):
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
Output (12x11):
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 8 8 2 0 0 0 0 0 0
0 2 8 8 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 8 8 8 8 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0

## Example 2
Input (13x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
Output (13x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 8 8 8 2 0 0 0 1 8 1 0 0
0 0 2 8 8 8 2 0 0 0 1 1 1 0 0
0 0 2 8 8 8 2 0 0 0 0 0 0 0 0
0 0 2 8 8 8 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3

## Example 3
Input (12x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
Output (12x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 8 8 2 0 0 0
3 8 8 3 0 0 2 8 8 2 0 0 0
3 8 8 3 0 0 2 8 8 2 0 0 0
3 3 3 3 0 0 2 8 8 2 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0

## Test
Input (14x13):
0 1 1 1 1 1 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,1,1,1,1,1,0,0,0,0,0,0,0],[0,1,8,8,8,1,0,0,1,1,1,0,0],[0,1,8,8,8,1,0,0,1,8,1,0,0],[0,1,8,8,8,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,2,2,2,2,2,2,0,0,0,0,0],[0,0,2,8,8,8,8,2,0,0,0,0,0],[0,0,2,8,8,8,8,2,0,3,3,3,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,2,2,2,2,2,2,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,3,3,3]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Treat every demonstration as an exact constraint: identify what changes and what stays fixed, infer one simple rule that explains all pairs, and check the proposed output's dimensions and cells against that rule. Consider object shape, position, color, symmetry, repetition, and whether the task crops, expands, or preserves the grid; do not assume any one of these applies.

Use a fresh derivation from the examples rather than repeating a remembered or assumed answer. In particular, verify the rule against every example before applying it to the test.

## Example 1
Input (12x11):
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
Output (12x11):
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 8 8 2 0 0 0 0 0 0
0 2 8 8 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 8 8 8 8 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0

## Example 2
Input (13x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
Output (13x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 8 8 8 2 0 0 0 1 8 1 0 0
0 0 2 8 8 8 2 0 0 0 1 1 1 0 0
0 0 2 8 8 8 2 0 0 0 0 0 0 0 0
0 0 2 8 8 8 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3

## Example 3
Input (12x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
Output (12x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 8 8 2 0 0 0
3 8 8 3 0 0 2 8 8 2 0 0 0
3 8 8 3 0 0 2 8 8 2 0 0 0
3 3 3 3 0 0 2 8 8 2 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0

## Test
Input (14x13):
0 1 1 1 1 1 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,1,1,1,1,1,0,0,0,0,0,0,0],[0,1,1,1,1,1,0,0,1,1,1,0,0],[0,1,8,8,8,1,0,0,1,8,1,0,0],[0,1,1,1,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,2,2,2,2,2,2,0,0,0,0,0],[0,0,2,8,8,8,8,2,0,0,0,0,0],[0,0,2,8,8,8,8,2,0,3,3,3,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,2,2,2,2,2,2,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,3,3,3]]</answer>


Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Analyze the demonstrations systematically: identify the background and the distinct objects; compare their colors, shapes, sizes, positions, counts, and input/output dimensions; then state a single rule that explains every pair. Check the rule against each demonstration before applying it. Do not assume the output has the same dimensions as the input; reproduce the complete grid with exact row lengths and only colors justified by the pattern.

## Example 1
Input (10x10):
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
Output (10x10):
0 0 2 0 2 0 0 2 0 0
0 0 2 0 2 0 0 2 0 0
0 0 2 0 2 0 0 2 0 0
0 0 2 0 2 5 0 2 0 0
0 0 2 0 2 0 0 2 0 0
0 5 2 0 2 0 0 2 0 0
0 2 2 0 2 0 0 2 5 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0

## Example 2
Input (10x10):
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 2 0 0 0
Output (10x10):
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 5 2 0 0
0 2 0 0 2 0 2 2 0 0
0 2 5 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0

## Test
Input (10x10):
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 2 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The 2s extend upward in their columns. Where a 5 lies on one of those columns, it remains in place and the 2s form a small rightward detour around it.

<answer>[[0,2,0,0,2,0,0,0,2,0],[0,2,0,0,2,0,0,0,2,0],[0,2,0,0,2,0,0,5,2,0],[0,2,0,0,2,0,0,0,2,0],[0,5,2,0,2,0,0,0,2,0],[0,2,2,0,2,0,0,0,2,0],[0,2,0,0,5,2,0,0,2,0],[0,2,0,0,2,2,0,0,2,0],[0,2,0,0,2,0,0,0,2,0],[0,2,0,0,2,0,0,0,2,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Analyze the demonstrations systematically: identify the background and the distinct objects; compare their colors, shapes, sizes, positions, counts, and input/output dimensions; then state a single rule that explains every pair. Check the rule against each demonstration before applying it. Do not assume the output has the same dimensions as the input; reproduce the complete grid with exact row lengths and only colors justified by the pattern.

## Example 1
Input (10x10):
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 2 0 0
Output (10x10):
0 0 2 0 2 0 0 2 0 0
0 0 2 0 2 0 0 2 0 0
0 0 2 0 2 0 0 2 0 0
0 0 2 0 2 5 0 2 0 0
0 0 2 0 2 0 0 2 0 0
0 5 2 0 2 0 0 2 0 0
0 2 2 0 2 0 0 2 5 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0

## Example 2
Input (10x10):
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 2 0 0 0
Output (10x10):
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 0 2 0 0
0 2 0 0 2 0 5 2 0 0
0 2 0 0 2 0 2 2 0 0
0 2 5 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0
0 2 0 0 2 0 2 0 0 0

## Test
Input (10x10):
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 0 0 2 0 0 0 2 0

## Candidate from the first attempt
The response below is only a hypothesis and may contain a wrong rule or grid. Solve the puzzle again from the demonstrations before consulting it; then compare it with your result. Keep it only if it follows from a rule that explains every example. Correct any error, and return your independently checked result.
The 2s extend upward in their columns. Where a 5 lies on one of those columns, it remains in place and the 2s form a small rightward detour around it.

<answer>[[0,2,0,0,2,0,0,0,2,0],[0,2,0,0,2,0,0,0,2,0],[0,2,0,0,2,0,0,5,2,0],[0,2,0,0,2,0,0,0,2,0],[0,5,2,0,2,0,0,0,2,0],[0,2,2,0,2,0,0,0,2,0],[0,2,0,0,5,2,0,0,2,0],[0,2,0,0,2,2,0,0,2,0],[0,2,0,0,2,0,0,0,2,0],[0,2,0,0,2,0,0,0,2,0]]</answer>

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The 2s extend upward from each bottom seed. When a 5 blocks one of those columns, the 2s remain on its right in the same row and the row below. The 5 at row 2, column 7 does not block a seed column.

<answer>[[0,2,0,0,2,0,0,0,2,0],[0,2,0,0,2,0,0,0,2,0],[0,2,0,0,2,0,0,5,2,0],[0,2,0,0,2,0,0,0,2,0],[0,5,2,0,2,0,0,0,2,0],[0,2,2,0,2,0,0,0,2,0],[0,2,0,0,5,2,0,0,2,0],[0,2,0,0,2,2,0,0,2,0],[0,2,0,0,2,0,0,0,2,0],[0,2,0,0,2,0,0,0,2,0]]</answer>


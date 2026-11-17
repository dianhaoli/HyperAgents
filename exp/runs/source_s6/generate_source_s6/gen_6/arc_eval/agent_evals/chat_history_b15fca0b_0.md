Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Analyze the demonstrations systematically: identify the background and the distinct objects; compare their colors, shapes, sizes, positions, counts, and input/output dimensions; then state a single rule that explains every pair. Check the rule against each demonstration before applying it. Do not assume the output has the same dimensions as the input; reproduce the complete grid with exact row lengths and only colors justified by the pattern.

## Example 1
Input (6x6):
0 0 0 0 0 2
0 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 0
2 0 0 0 0 0
0 0 0 0 0 0
Output (6x6):
4 4 4 4 4 2
4 1 1 1 1 1
4 4 4 4 4 4
1 1 1 1 1 4
2 4 4 4 4 4
0 0 0 0 0 0

## Example 2
Input (5x5):
0 0 0 1 2
0 0 0 1 0
0 1 0 1 0
0 1 0 0 0
2 1 0 0 0
Output (5x5):
0 0 0 1 2
4 4 4 1 4
4 1 4 1 4
4 1 4 4 4
2 1 0 0 0

## Example 3
Input (6x6):
2 0 0 0 0 0
1 1 1 1 0 0
0 0 0 0 0 0
0 0 0 1 1 1
0 0 0 0 0 2
0 0 0 0 0 0
Output (6x6):
2 4 4 4 4 0
1 1 1 1 4 0
0 0 4 4 4 0
0 0 4 1 1 1
0 0 4 4 4 2
0 0 0 0 0 0

## Example 4
Input (10x10):
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 1 0 1 1 0 1 0 1 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
Output (10x10):
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 4
0 0 0 1 1 0 0 0 1 4
4 4 4 1 1 4 4 4 1 4
4 1 4 1 1 4 1 4 1 4
4 1 4 4 4 4 1 4 4 4
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0

## Example 5
Input (5x5):
2 1 1 1 2
0 1 0 1 0
0 1 0 1 0
0 1 0 1 0
0 0 0 0 0
Output (5x5):
2 1 1 1 2
4 1 0 1 4
4 1 0 1 4
4 1 0 1 4
4 4 4 4 4

## Test
Input (10x10):
2 1 0 0 0 1 0 0 0 2
0 1 0 0 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 0 0 1 0 0 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[2,1,0,0,0,1,0,0,0,2],[4,1,0,0,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,4,4,1,0,0,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,4,4,4,4]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Analyze the demonstrations systematically: identify the background and the distinct objects; compare their colors, shapes, sizes, positions, counts, and input/output dimensions; then state a single rule that explains every pair. Check the rule against each demonstration before applying it. Do not assume the output has the same dimensions as the input; reproduce the complete grid with exact row lengths and only colors justified by the pattern.

## Example 1
Input (6x6):
0 0 0 0 0 2
0 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 0
2 0 0 0 0 0
0 0 0 0 0 0
Output (6x6):
4 4 4 4 4 2
4 1 1 1 1 1
4 4 4 4 4 4
1 1 1 1 1 4
2 4 4 4 4 4
0 0 0 0 0 0

## Example 2
Input (5x5):
0 0 0 1 2
0 0 0 1 0
0 1 0 1 0
0 1 0 0 0
2 1 0 0 0
Output (5x5):
0 0 0 1 2
4 4 4 1 4
4 1 4 1 4
4 1 4 4 4
2 1 0 0 0

## Example 3
Input (6x6):
2 0 0 0 0 0
1 1 1 1 0 0
0 0 0 0 0 0
0 0 0 1 1 1
0 0 0 0 0 2
0 0 0 0 0 0
Output (6x6):
2 4 4 4 4 0
1 1 1 1 4 0
0 0 4 4 4 0
0 0 4 1 1 1
0 0 4 4 4 2
0 0 0 0 0 0

## Example 4
Input (10x10):
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 1 0 1 1 0 1 0 1 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
Output (10x10):
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 4
0 0 0 1 1 0 0 0 1 4
4 4 4 1 1 4 4 4 1 4
4 1 4 1 1 4 1 4 1 4
4 1 4 4 4 4 1 4 4 4
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0

## Example 5
Input (5x5):
2 1 1 1 2
0 1 0 1 0
0 1 0 1 0
0 1 0 1 0
0 0 0 0 0
Output (5x5):
2 1 1 1 2
4 1 0 1 4
4 1 0 1 4
4 1 0 1 4
4 4 4 4 4

## Test
Input (10x10):
2 1 0 0 0 1 0 0 0 2
0 1 0 0 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 0 0 1 0 0 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 0 0 0

## Candidate from the first attempt
The response below is only a hypothesis and may contain a wrong rule or grid. Solve the puzzle again from the demonstrations before consulting it; then compare it with your result. Keep it only if it follows from a rule that explains every example. Correct any error, and return your independently checked result.
<answer>[[2,1,0,0,0,1,0,0,0,2],[4,1,0,0,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,4,4,1,0,0,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,4,4,4,4]]</answer>

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[2,1,0,0,0,1,0,0,0,2],[4,1,0,0,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,4,4,1,0,0,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,4,4,4,4]]</answer>


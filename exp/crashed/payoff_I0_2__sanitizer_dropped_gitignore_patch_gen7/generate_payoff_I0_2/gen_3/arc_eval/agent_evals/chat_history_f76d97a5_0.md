Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one hidden transformation rule. Infer a precise rule from all of the demonstrations, then apply it to the test input.

Reason carefully about what changes and what stays fixed. Check that your proposed rule reproduces every training output, including colors, positions, shapes, and grid dimensions, before applying it to the test. Do not assume that a pattern or color is irrelevant just because it appears only once.

## Example 1
Input (5x5):
5 5 6 6 6
6 5 5 6 6
6 6 5 5 6
6 6 6 5 5
5 6 6 6 5
Output (5x5):
6 6 0 0 0
0 6 6 0 0
0 0 6 6 0
0 0 0 6 6
6 0 0 0 6

## Example 2
Input (3x3):
4 5 4
5 5 5
4 5 4
Output (3x3):
0 4 0
4 4 4
0 4 0

## Example 3
Input (5x5):
9 5 9 9 9
9 9 5 5 9
9 5 9 9 9
9 9 5 9 9
9 9 9 5 5
Output (5x5):
0 9 0 0 0
0 0 9 9 0
0 9 0 0 0
0 0 9 0 0
0 0 0 9 9

## Test
Input (5x5):
3 3 3 5 3
3 5 3 3 3
3 5 5 3 5
3 3 3 5 3
5 5 5 3 3

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[3, 3, 3, 0, 3], [3, 0, 3, 3, 3], [3, 0, 0, 3, 0], [3, 3, 3, 0, 3], [0, 0, 0, 3, 3]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one hidden transformation rule. Infer a precise rule from all of the demonstrations, then apply it to the test input.

Reason carefully about what changes and what stays fixed. Check that your proposed rule reproduces every training output, including colors, positions, shapes, and grid dimensions, before applying it to the test. Do not assume that a pattern or color is irrelevant just because it appears only once.

## Example 1
Input (5x5):
5 5 6 6 6
6 5 5 6 6
6 6 5 5 6
6 6 6 5 5
5 6 6 6 5
Output (5x5):
6 6 0 0 0
0 6 6 0 0
0 0 6 6 0
0 0 0 6 6
6 0 0 0 6

## Example 2
Input (3x3):
4 5 4
5 5 5
4 5 4
Output (3x3):
0 4 0
4 4 4
0 4 0

## Example 3
Input (5x5):
9 5 9 9 9
9 9 5 5 9
9 5 9 9 9
9 9 5 9 9
9 9 9 5 5
Output (5x5):
0 9 0 0 0
0 0 9 9 0
0 9 0 0 0
0 0 9 0 0
0 0 0 9 9

## Test
Input (5x5):
3 3 3 5 3
3 5 3 3 3
3 5 5 3 5
3 3 3 5 3
5 5 5 3 3

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[3, 3, 3, 0, 3], [3, 0, 3, 3, 3], [3, 0, 0, 3, 0], [3, 3, 3, 0, 3], [0, 0, 0, 3, 3]]</answer>


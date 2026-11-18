Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule, check that it reproduces every demonstration exactly, and apply it to the test input.

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

Output: <answer>[[2,1,4,4,4,1,4,4,4,2],[4,1,4,4,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,4,4,1,4,4,4,1,4,4],[4,4,4,1,0,1,4,1,4,4],[4,4,4,1,0,1,4,1,4,4],[4,4,4,1,0,1,4,1,4,4],[4,4,4,1,0,1,4,4,4,4]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule, check that it reproduces every demonstration exactly, and apply it to the test input.

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

A first attempt proposed this candidate test output:
[[2, 1, 4, 4, 4, 1, 4, 4, 4, 2], [4, 1, 4, 4, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 4, 4, 1, 4, 4, 4, 1, 4, 4], [4, 4, 4, 1, 0, 1, 4, 1, 4, 4], [4, 4, 4, 1, 0, 1, 4, 1, 4, 4], [4, 4, 4, 1, 0, 1, 4, 1, 4, 4], [4, 4, 4, 1, 0, 1, 4, 4, 4, 4]]
Do not assume that candidate is correct. Independently infer and re-check the rule against every training input-output pair, then compare the rule's result with the candidate. The first candidate will also be kept as an answer, so use this call to maximize the chance of a second exact match: if the examples support a plausible different interpretation, return the test grid for that alternative; otherwise confirm the original candidate. Do not invent an unsupported alternative. Return one grid in the required <answer> tags.

Output: <answer>[[2,1,4,4,4,1,4,4,4,2],[4,1,4,4,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,4,4,1,4,4,4,1,4,4],[4,4,4,1,0,1,4,1,4,4],[4,4,4,1,0,1,4,1,4,4],[4,4,4,1,0,1,4,1,4,4],[4,4,4,1,0,1,4,4,4,4]]</answer>


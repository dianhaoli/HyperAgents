Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

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

Output: <answer>[[2,1,0,0,0,1,0,0,0,2],[4,1,4,4,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,4,4,1,4,4,4,1,4,4],[4,4,4,1,4,1,4,1,4,4],[4,4,4,1,4,1,4,1,4,4],[4,4,4,1,4,1,4,1,4,4],[4,4,4,1,4,1,4,4,4,4]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

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

SECOND-PASS CHECK (use this order):
1. Ignore any earlier proposed answer. Infer a concrete transformation from the training pairs alone, and check that it reproduces every demonstration.
2. Apply that transformation from scratch to the test input. Check the result's dimensions, color mapping, object placement, and every changed region against the rule. Do not copy a demonstration output.
3. Only after deriving your own test grid, compare it cell by cell with this previous candidate (which may be wrong): [[2, 1, 0, 0, 0, 1, 0, 0, 0, 2], [4, 1, 4, 4, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 4, 4, 1, 4, 4, 4, 1, 4, 4], [4, 4, 4, 1, 4, 1, 4, 1, 4, 4], [4, 4, 4, 1, 4, 1, 4, 1, 4, 4], [4, 4, 4, 1, 4, 1, 4, 1, 4, 4], [4, 4, 4, 1, 4, 1, 4, 4, 4, 4]]
If they differ, resolve the discrepancy using the rule and demonstrations, not by favoring either grid. Return the independently verified test grid inside <answer> tags, with nothing else inside the tags.

Output: <answer>[[2,1,0,0,0,1,0,0,0,2],[4,1,4,4,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,4,4,1,4,4,4,1,4,4],[4,4,4,1,4,1,4,1,4,4],[4,4,4,1,4,1,4,1,4,4],[4,4,4,1,4,1,4,1,4,4],[4,4,4,1,4,1,4,4,4,4]]</answer>


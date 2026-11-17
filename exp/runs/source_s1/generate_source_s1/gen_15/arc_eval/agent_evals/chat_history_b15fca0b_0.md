Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input. Treat the change audit after each example as evidence: the same concrete rule must account for every listed edit and every unchanged cell in every demonstration.

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
Change audit (input value -> output value; coordinates are zero-based): 18 changed cell(s): 0->4: 18 cell(s) at (0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (3,5), (4,1), (4,2), (4,3), (4,4), (4,5)

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
Change audit (input value -> output value; coordinates are zero-based): 11 changed cell(s): 0->4: 11 cell(s) at (1,0), (1,1), (1,2), (1,4), (2,0), (2,2), (2,4), (3,0), (3,2), (3,3), (3,4)

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
Change audit (input value -> output value; coordinates are zero-based): 12 changed cell(s): 0->4: 12 cell(s) at (0,1), (0,2), (0,3), (0,4), (1,4), (2,2), (2,3), (2,4), (3,2), (4,2), (4,3), (4,4)

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
Change audit (input value -> output value; coordinates are zero-based): 25 changed cell(s): 0->4: 25 cell(s) at (1,9), (2,9), (3,0), (3,1), (3,2), (3,5), (3,6), (3,7), (3,9), (4,0), (4,2), (4,5), (4,7), (4,9), (5,0), (5,2), (5,3), (5,4), (5,5), (5,7), (5,8), (5,9), (6,0), (7,0), (8,0)

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
Change audit (input value -> output value; coordinates are zero-based): 11 changed cell(s): 0->4: 11 cell(s) at (1,0), (1,4), (2,0), (2,4), (3,0), (3,4), (4,0), (4,1), (4,2), (4,3), (4,4)

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

Output: <answer>[[2,1,4,4,4,1,4,4,4,2],[4,1,4,4,4,1,4,1,0,0],[4,1,4,1,4,1,4,1,0,0],[4,1,4,1,4,1,4,1,0,0],[4,1,4,1,4,1,4,1,0,0],[4,4,4,1,4,4,4,1,0,0],[0,0,0,1,0,1,0,1,0,0],[0,0,0,1,0,1,0,1,0,0],[0,0,0,1,0,1,0,1,0,0],[0,0,0,1,0,1,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input. Treat the change audit after each example as evidence: the same concrete rule must account for every listed edit and every unchanged cell in every demonstration.

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
Change audit (input value -> output value; coordinates are zero-based): 18 changed cell(s): 0->4: 18 cell(s) at (0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (3,5), (4,1), (4,2), (4,3), (4,4), (4,5)

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
Change audit (input value -> output value; coordinates are zero-based): 11 changed cell(s): 0->4: 11 cell(s) at (1,0), (1,1), (1,2), (1,4), (2,0), (2,2), (2,4), (3,0), (3,2), (3,3), (3,4)

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
Change audit (input value -> output value; coordinates are zero-based): 12 changed cell(s): 0->4: 12 cell(s) at (0,1), (0,2), (0,3), (0,4), (1,4), (2,2), (2,3), (2,4), (3,2), (4,2), (4,3), (4,4)

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
Change audit (input value -> output value; coordinates are zero-based): 25 changed cell(s): 0->4: 25 cell(s) at (1,9), (2,9), (3,0), (3,1), (3,2), (3,5), (3,6), (3,7), (3,9), (4,0), (4,2), (4,5), (4,7), (4,9), (5,0), (5,2), (5,3), (5,4), (5,5), (5,7), (5,8), (5,9), (6,0), (7,0), (8,0)

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
Change audit (input value -> output value; coordinates are zero-based): 11 changed cell(s): 0->4: 11 cell(s) at (1,0), (1,4), (2,0), (2,4), (3,0), (3,4), (4,0), (4,1), (4,2), (4,3), (4,4)

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

Make this a fresh, independent solve: do not assume or reuse any earlier proposed rule or grid. Infer a concrete rule from the training pairs, check that it reproduces every demonstrated output, then apply it to the test input. Verify the dimensions and changed cells against that rule before returning the grid in <answer> tags, with nothing else inside the tags.

Output: <answer>[[2,1,0,0,0,1,4,4,4,2],[4,1,0,0,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,1,0,1,0,1,0,1,4,4],[4,4,4,1,0,0,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,4,4,4,4]]</answer>


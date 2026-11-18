Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input. Use the change audits as evidence: the same rule must explain every edit and every unchanged cell.

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

Output: <answer>[[2, 1, 0, 0, 0, 1, 0, 0, 0, 2], [4, 1, 4, 4, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 4, 4, 1, 4, 4, 4, 1, 4, 4], [0, 0, 0, 1, 0, 1, 0, 1, 4, 4], [0, 0, 0, 1, 0, 1, 0, 1, 4, 4], [0, 0, 0, 1, 0, 1, 0, 1, 4, 4], [0, 0, 0, 1, 4, 1, 4, 4, 4, 4]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input. Use the change audits as evidence: the same rule must explain every edit and every unchanged cell.

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

Check this first-pass candidate against the demonstrations; it is a hypothesis, not a trusted answer: [[2, 1, 0, 0, 0, 1, 0, 0, 0, 2], [4, 1, 4, 4, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 1, 4, 1, 4, 1, 4, 1, 4, 4], [4, 4, 4, 1, 4, 4, 4, 1, 4, 4], [0, 0, 0, 1, 0, 1, 0, 1, 4, 4], [0, 0, 0, 1, 0, 1, 0, 1, 4, 4], [0, 0, 0, 1, 0, 1, 0, 1, 4, 4], [0, 0, 0, 1, 4, 1, 4, 4, 4, 4]]
Candidate edit audit (test input -> candidate; coordinates are zero-based): 44 changed cell(s): 0->4: 44 cell(s) at (1,0), (1,2), (1,3), (1,4), (1,6), (1,8), (1,9), (2,0), (2,2), (2,4), (2,6), (2,8), (2,9), (3,0), (3,2), (3,4), (3,6), (3,8), (3,9), (4,0), (4,2), (4,4), (4,6), (4,8), (4,9), (5,0), (5,1), (5,2), (5,4), (5,5), (5,6), (5,8), (5,9), (6,8), (6,9), (7,8), (7,9), (8,8), (8,9), (9,4), (9,6), (9,7), (9,8), (9,9)
Derive the rule from every training pair before deciding. For a same-size candidate, account for every listed edit and verify that every cell not listed remains unchanged for a reason supported by the demonstrations. Do not extend a pattern beyond its demonstrated bounds or fill a cell just because it appears to complete a shape. Correct unjustified edits or omissions, and return the verified grid in <answer> tags only.

Output: <answer>[[2,1,0,0,0,1,0,0,0,2],[4,1,4,4,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,4,4,1,4,4,4,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,0,1,0,1,4,4],[4,4,4,1,4,1,4,4,4,4]]</answer>


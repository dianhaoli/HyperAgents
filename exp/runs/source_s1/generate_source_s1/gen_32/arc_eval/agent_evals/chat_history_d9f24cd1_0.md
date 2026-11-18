Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input. Use each training change audit as evidence: your rule must explain every changed cell and why the other cells remain unchanged.

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
Training change audit (zero-based; 28 changed cell(s)): 0->2: 28 at [(0, 2), (0, 4), (0, 7), (1, 2), (1, 4), (1, 7), (2, 2), (2, 4), (2, 7), (3, 2), (3, 4), (3, 7), (4, 2), (4, 4), (4, 7), (5, 2), (5, 4), (5, 7), (6, 1), (6, 2), (6, 4), (6, 7), (7, 1), (7, 4), (7, 7), (8, 1), (8, 4), (8, 7)]

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
Training change audit (zero-based; 28 changed cell(s)): 0->2: 28 at [(0, 1), (0, 4), (0, 7), (1, 1), (1, 4), (1, 7), (2, 1), (2, 4), (2, 7), (3, 1), (3, 4), (3, 7), (4, 1), (4, 4), (4, 6), (4, 7), (5, 1), (5, 4), (5, 6), (6, 1), (6, 4), (6, 6), (7, 1), (7, 4), (7, 6), (8, 1), (8, 4), (8, 6)]

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

Output: <answer>[[0,0,2,0,2,2,0,0,2,0],[0,0,2,0,2,2,0,0,2,0],[0,0,2,0,2,2,0,5,2,0],[0,0,2,0,2,2,0,0,2,0],[0,5,2,0,2,2,0,0,2,0],[0,2,2,0,2,2,0,0,2,0],[0,2,0,0,5,2,0,0,2,0],[0,2,0,0,2,2,0,0,2,0],[0,2,0,0,2,2,0,0,2,0],[0,2,0,0,2,0,0,0,2,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input. Use each training change audit as evidence: your rule must explain every changed cell and why the other cells remain unchanged.

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
Training change audit (zero-based; 28 changed cell(s)): 0->2: 28 at [(0, 2), (0, 4), (0, 7), (1, 2), (1, 4), (1, 7), (2, 2), (2, 4), (2, 7), (3, 2), (3, 4), (3, 7), (4, 2), (4, 4), (4, 7), (5, 2), (5, 4), (5, 7), (6, 1), (6, 2), (6, 4), (6, 7), (7, 1), (7, 4), (7, 7), (8, 1), (8, 4), (8, 7)]

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
Training change audit (zero-based; 28 changed cell(s)): 0->2: 28 at [(0, 1), (0, 4), (0, 7), (1, 1), (1, 4), (1, 7), (2, 1), (2, 4), (2, 7), (3, 1), (3, 4), (3, 7), (4, 1), (4, 4), (4, 6), (4, 7), (5, 1), (5, 4), (5, 6), (6, 1), (6, 4), (6, 6), (7, 1), (7, 4), (7, 6), (8, 1), (8, 4), (8, 6)]

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

Independently verify this candidate: [[0, 0, 2, 0, 2, 2, 0, 0, 2, 0], [0, 0, 2, 0, 2, 2, 0, 0, 2, 0], [0, 0, 2, 0, 2, 2, 0, 5, 2, 0], [0, 0, 2, 0, 2, 2, 0, 0, 2, 0], [0, 5, 2, 0, 2, 2, 0, 0, 2, 0], [0, 2, 2, 0, 2, 2, 0, 0, 2, 0], [0, 2, 0, 0, 5, 2, 0, 0, 2, 0], [0, 2, 0, 0, 2, 2, 0, 0, 2, 0], [0, 2, 0, 0, 2, 2, 0, 0, 2, 0], [0, 2, 0, 0, 2, 0, 0, 0, 2, 0]]
Infer the rule from the demonstrations and check that it explains every input/output pair. Apply that rule to the test input, then compare the result with the candidate. Do not accept the candidate just because it looks plausible, and do not copy a demonstration output. If it is wrong, correct it. Return the verified test grid in the required <answer> tags; put nothing else inside the tags.

Output: <answer>[[0, 0, 2, 0, 2, 2, 0, 0, 2, 0], [0, 0, 2, 0, 2, 2, 0, 0, 2, 0], [0, 0, 2, 0, 2, 2, 0, 5, 2, 0], [0, 0, 2, 0, 2, 2, 0, 0, 2, 0], [0, 5, 2, 0, 2, 2, 0, 0, 2, 0], [0, 2, 2, 0, 2, 2, 0, 0, 2, 0], [0, 2, 0, 0, 5, 2, 0, 0, 2, 0], [0, 2, 0, 0, 2, 2, 0, 0, 2, 0], [0, 2, 0, 0, 2, 0, 0, 0, 2, 0], [0, 2, 0, 0, 2, 0, 0, 0, 2, 0]]</answer>


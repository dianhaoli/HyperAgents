Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Compare every example carefully: identify which objects, colors, shapes, positions, counts, and grid dimensions change or stay fixed. Prefer the simplest rule that explains all examples, and check that it also applies to the test. Before answering, verify the output's dimensions, every changed cell, and preservation of cells that should remain unchanged. Do not merely copy an example or assume a familiar rule without checking it against all demonstrations.

## Example 1
Input (10x10):
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 5 9 0 0 0
0 0 0 0 0 5 5 9 0 0
0 0 0 0 0 5 5 5 9 0
0 0 0 0 0 5 5 5 5 9
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
Output (10x10):
0 0 0 0 0 9 0 0 0 0
9 0 0 0 0 0 9 0 0 0
0 9 0 0 0 0 0 9 0 0
0 0 9 0 0 0 0 0 9 0
0 0 0 9 0 0 0 0 0 9
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 9 0

## Example 2
Input (10x10):
7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 7 5 5 0 0 0 0
0 0 0 0 7 5 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7
Output (10x10):
7 0 0 0 7 0 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 0 7 0 0 0 7 0 0
0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7

## Example 3
Input (10x10):
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 2 5 5 0 0 0 0 0
0 0 0 2 5 0 0 0 0 0
0 0 0 5 2 0 0 0 0 0
0 0 0 5 5 2 0 0 0 0
0 0 0 5 5 5 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0
Output (10x10):
0 0 0 2 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 2 0 0 0 2 0 0
0 0 0 0 2 0 0 0 2 0
2 0 0 0 0 2 0 0 0 2
0 2 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 2 0

## Test
Input (10x10):
0 1 0 0 0 0 0 0 0 0
0 0 1 5 5 0 0 0 0 0
0 0 0 1 5 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 5 1 0 0 0 0
0 0 0 0 5 5 1 0 0 0
0 0 0 0 5 5 5 1 0 0
0 0 0 0 5 5 5 5 1 0
0 0 0 0 5 5 5 5 5 1
0 0 0 0 0 0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Compare every example carefully: identify which objects, colors, shapes, positions, counts, and grid dimensions change or stay fixed. Prefer the simplest rule that explains all examples, and check that it also applies to the test. Before answering, verify the output's dimensions, every changed cell, and preservation of cells that should remain unchanged. Do not merely copy an example or assume a familiar rule without checking it against all demonstrations.

## Example 1
Input (10x10):
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 5 9 0 0 0
0 0 0 0 0 5 5 9 0 0
0 0 0 0 0 5 5 5 9 0
0 0 0 0 0 5 5 5 5 9
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
Output (10x10):
0 0 0 0 0 9 0 0 0 0
9 0 0 0 0 0 9 0 0 0
0 9 0 0 0 0 0 9 0 0
0 0 9 0 0 0 0 0 9 0
0 0 0 9 0 0 0 0 0 9
0 0 0 0 9 0 0 0 0 0
0 0 0 0 0 9 0 0 0 0
0 0 0 0 0 0 9 0 0 0
0 0 0 0 0 0 0 9 0 0
0 0 0 0 0 0 0 0 9 0

## Example 2
Input (10x10):
7 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 7 5 5 0 0 0 0
0 0 0 0 7 5 0 0 0 0
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7
Output (10x10):
7 0 0 0 7 0 0 0 0 0
0 7 0 0 0 7 0 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 0 7 0 0 0 7 0 0
0 0 0 0 7 0 0 0 7 0
0 0 0 0 0 7 0 0 0 7
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 7

## Example 3
Input (10x10):
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 0 2 5 5 0 0 0 0 0
0 0 0 2 5 0 0 0 0 0
0 0 0 5 2 0 0 0 0 0
0 0 0 5 5 2 0 0 0 0
0 0 0 5 5 5 2 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 2 0
Output (10x10):
0 0 0 2 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0
0 2 0 0 0 2 0 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 0 2 0 0 0 2 0 0
0 0 0 0 2 0 0 0 2 0
2 0 0 0 0 2 0 0 0 2
0 2 0 0 0 0 2 0 0 0
0 0 2 0 0 0 0 2 0 0
0 0 0 2 0 0 0 0 2 0

## Test
Input (10x10):
0 1 0 0 0 0 0 0 0 0
0 0 1 5 5 0 0 0 0 0
0 0 0 1 5 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 5 1 0 0 0 0
0 0 0 0 5 5 1 0 0 0
0 0 0 0 5 5 5 1 0 0
0 0 0 0 5 5 5 5 1 0
0 0 0 0 5 5 5 5 5 1
0 0 0 0 0 0 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

## Independent verification of a first-pass answer
A first-pass candidate is included below. Treat it as a hypothesis, not as ground truth. Independently derive the rule from all demonstrations, then check the candidate against it at the cell and object level. Pay particular attention to cells left unchanged: infer from the examples the exact conditions under which a cell changes, rather than assuming that all background cells, an entire region, or a familiar pattern should be altered. Consider boundaries, barriers, and connectivity only when the examples support them. Correct any part of the candidate that the demonstrated rule contradicts; do not merely repeat it. Return your final grid in the required <answer> JSON tags.
First-pass candidate: [[0, 1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

Output: <answer>[[0,1,0,0,0,1,0,0,0,0],[0,0,1,0,0,0,1,0,0,0],[0,0,0,1,0,0,0,1,0,0],[0,0,0,0,1,0,0,0,1,0],[1,0,0,0,0,1,0,0,0,1],[0,1,0,0,0,0,1,0,0,0],[0,0,1,0,0,0,0,1,0,0],[0,0,0,1,0,0,0,0,1,0],[0,0,0,0,1,0,0,0,0,1],[0,0,0,0,0,1,0,0,0,0]]</answer>


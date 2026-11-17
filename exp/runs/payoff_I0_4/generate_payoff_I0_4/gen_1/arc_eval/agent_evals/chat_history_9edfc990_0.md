Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (15x15):
0 0 2 0 9 6 5 5 5 0 2 1 0 0 0
3 0 4 4 9 0 0 0 3 9 0 0 0 5 0
8 9 2 0 1 0 6 8 0 0 0 8 0 8 0
6 0 4 0 4 0 0 1 6 1 6 9 1 4 2
7 7 7 3 0 0 6 4 0 4 0 1 3 0 0
7 6 0 4 0 2 0 0 4 0 8 0 0 7 6
0 0 4 7 8 3 0 4 0 0 5 0 6 0 3
0 8 0 0 2 0 0 0 1 0 2 0 0 1 0
3 3 1 0 2 0 0 6 0 8 6 0 0 0 0
0 0 0 0 0 8 0 0 0 9 0 4 0 2 8
0 0 4 1 4 9 0 7 0 1 0 5 0 0 8
7 2 0 0 4 5 1 0 9 0 0 6 4 0 0
0 0 0 0 9 6 3 1 3 3 9 0 0 0 5
0 5 0 4 0 7 9 9 0 0 0 0 9 4 0
0 9 8 8 0 6 8 0 0 0 8 0 0 0 0
Output (15x15):
0 0 2 0 9 6 5 5 5 0 2 1 1 1 1
3 0 4 4 9 1 1 1 3 9 1 1 1 5 1
8 9 2 1 1 1 6 8 1 1 1 8 1 8 1
6 0 4 1 4 1 1 1 6 1 6 9 1 4 2
7 7 7 3 1 1 6 4 0 4 1 1 3 0 0
7 6 0 4 1 2 1 1 4 1 8 1 1 7 6
0 0 4 7 8 3 1 4 1 1 5 1 6 1 3
0 8 1 1 2 1 1 1 1 1 2 1 1 1 1
3 3 1 1 2 1 1 6 1 8 6 1 1 1 1
1 1 1 1 1 8 1 1 1 9 1 4 1 2 8
1 1 4 1 4 9 1 7 1 1 1 5 1 1 8
7 2 1 1 4 5 1 1 9 1 1 6 4 1 1
1 1 1 1 9 6 3 1 3 3 9 1 1 1 5
1 5 1 4 0 7 9 9 1 1 1 1 9 4 1
1 9 8 8 0 6 8 1 1 1 8 1 1 1 1

## Example 2
Input (13x13):
9 0 0 0 0 2 8 0 9 0 2 0 9
1 0 0 6 0 0 0 0 0 0 0 9 5
9 0 4 9 3 0 0 5 7 0 8 0 8
0 0 8 6 0 6 0 1 0 0 0 4 1
3 6 0 1 0 3 9 0 0 4 5 7 2
0 8 0 0 0 0 0 0 7 1 8 0 0
9 0 0 2 0 0 0 7 5 7 0 8 4
0 0 0 8 7 5 0 0 7 0 0 5 0
9 9 0 0 0 0 5 0 0 5 0 0 0
8 0 0 8 0 6 5 0 0 0 0 9 0
4 0 0 6 0 7 9 9 8 0 5 7 3
0 0 0 0 0 0 0 7 2 0 0 0 8
0 0 0 7 5 0 5 0 0 0 0 0 3
Output (13x13):
9 1 1 1 1 2 8 1 9 1 2 0 9
1 1 1 6 1 1 1 1 1 1 1 9 5
9 1 4 9 3 1 1 5 7 1 8 0 8
1 1 8 6 1 6 1 1 1 1 1 4 1
3 6 1 1 1 3 9 1 1 4 5 7 2
0 8 1 1 1 1 1 1 7 1 8 0 0
9 1 1 2 1 1 1 7 5 7 1 8 4
1 1 1 8 7 5 1 1 7 1 1 5 1
9 9 1 1 1 1 5 1 1 5 1 1 1
8 1 1 8 1 6 5 1 1 1 1 9 1
4 1 1 6 1 7 9 9 8 1 5 7 3
1 1 1 1 1 1 1 7 2 1 1 1 8
1 1 1 7 5 1 5 1 1 1 1 1 3

## Example 3
Input (16x16):
7 4 4 0 4 0 0 6 1 1 1 0 0 6 0 5
1 1 3 3 4 0 3 8 5 3 4 5 0 8 2 8
8 0 4 8 8 5 0 9 0 0 0 5 5 8 5 8
0 2 6 0 0 0 0 3 0 1 0 8 0 4 0 8
8 0 2 8 0 7 0 0 0 9 0 7 3 0 3 6
0 0 0 0 0 0 5 3 0 6 0 6 0 4 5 7
6 6 0 0 3 1 0 0 2 5 0 0 0 3 4 5
7 0 7 8 0 1 0 0 0 9 0 7 3 0 3 0
0 6 0 0 5 6 6 5 9 8 3 9 0 7 0 0
7 5 0 0 0 8 0 6 9 0 0 7 1 0 0 0
6 5 3 4 3 0 6 9 4 1 8 9 2 8 7 7
8 6 8 6 3 2 7 3 0 2 0 0 2 1 0 0
9 0 0 0 6 1 8 0 3 3 0 2 0 2 1 4
0 4 0 0 0 0 1 0 0 0 6 0 4 4 5 6
0 5 0 8 3 2 1 0 5 9 1 8 7 0 2 7
0 9 0 1 8 6 0 9 9 8 0 9 0 0 3 0
Output (16x16):
7 4 4 0 4 0 0 6 1 1 1 1 1 6 0 5
1 1 3 3 4 0 3 8 5 3 4 5 1 8 2 8
8 1 4 8 8 5 1 9 1 1 1 5 5 8 5 8
0 2 6 1 1 1 1 3 1 1 1 8 0 4 0 8
8 1 2 8 1 7 1 1 1 9 1 7 3 0 3 6
1 1 1 1 1 1 5 3 1 6 1 6 1 4 5 7
6 6 1 1 3 1 1 1 2 5 1 1 1 3 4 5
7 0 7 8 1 1 1 1 1 9 1 7 3 0 3 1
0 6 0 0 5 6 6 5 9 8 3 9 1 7 1 1
7 5 0 0 0 8 0 6 9 1 1 7 1 1 1 1
6 5 3 4 3 0 6 9 4 1 8 9 2 8 7 7
8 6 8 6 3 2 7 3 0 2 0 0 2 1 1 1
9 1 1 1 6 1 8 1 3 3 0 2 0 2 1 4
0 4 1 1 1 1 1 1 1 1 6 0 4 4 5 6
0 5 1 8 3 2 1 1 5 9 1 8 7 0 2 7
0 9 1 1 8 6 1 9 9 8 1 9 0 0 3 0

## Test
Input (16x16):
0 0 0 8 0 5 0 0 9 0 6 0 0 0 0 5
6 7 6 0 4 0 2 0 0 8 3 6 2 0 0 0
0 0 0 7 0 0 5 4 1 0 1 7 6 0 0 0
0 5 8 0 9 0 0 2 2 0 8 0 4 0 0 7
4 0 0 4 2 2 7 3 2 0 6 4 9 9 9 0
0 1 8 0 5 0 0 0 2 0 0 8 0 9 6 6
9 9 0 2 8 0 0 3 0 0 2 0 0 5 8 0
1 3 0 1 6 1 0 0 0 8 0 0 0 4 0 0
0 0 4 0 7 4 0 0 4 0 0 5 8 0 4 0
0 0 0 6 0 6 0 0 0 0 0 8 0 1 4 4
0 9 0 0 9 0 0 0 0 0 1 5 0 6 0 0
6 0 7 5 9 0 7 0 0 0 4 6 0 2 8 0
5 0 0 0 1 0 2 4 8 0 0 3 0 9 0 8
1 0 0 2 4 0 0 0 1 7 0 0 0 0 5 0
6 9 0 0 7 7 1 0 2 0 0 9 1 0 3 0
1 8 3 0 0 9 7 0 2 7 2 0 8 9 0 0

Solve the task by inferring one precise transformation from the demonstrations. Before deciding, inspect the grids systematically: compare dimensions, colors, connected objects and their bounding boxes; look for repeated motifs, symmetry, reflection, rotation, completion of partial patterns, and changes in object size or position. Do not assume the output is the input with only a small local edit. Derive the rule from the examples, then check that it reproduces every demonstrated output exactly. Apply that same rule to the test. Preserve the full grid and its dimensions unless the examples show a dimension change. Give a brief explanation outside the answer tags, then end with the complete output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: The transformation changes every zero in a 4-connected region that touches an existing 1 into a 1. Other zeros and all nonzero cells remain unchanged.

<answer>[[0,0,0,8,0,5,1,1,9,0,6,0,0,0,0,5],[6,7,6,0,4,0,2,1,1,8,3,6,2,0,0,0],[0,0,0,7,0,0,5,4,1,1,1,7,6,0,0,0],[0,5,8,0,9,0,0,2,2,1,8,0,4,0,0,7],[4,1,1,4,2,2,7,3,2,1,6,4,9,9,9,0],[1,1,8,0,5,1,1,1,2,1,1,8,0,9,6,6],[9,9,1,2,8,1,1,3,1,1,2,0,0,5,8,0],[1,3,1,1,6,1,1,1,1,8,0,0,0,4,0,0],[1,1,4,1,7,4,1,1,4,1,1,5,8,1,4,0],[1,1,1,6,0,6,1,1,1,1,1,8,1,1,4,4],[1,9,1,1,9,1,1,1,1,1,1,5,1,6,0,0],[6,1,7,5,9,1,7,1,1,1,4,6,1,2,8,0],[5,1,1,1,1,1,2,4,8,1,1,3,1,9,0,8],[1,1,1,2,4,1,1,1,1,7,1,1,1,1,5,0],[6,9,1,1,7,7,1,1,2,1,1,9,1,1,3,0],[1,8,3,1,1,9,7,1,2,7,2,0,8,9,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (15x15):
0 0 2 0 9 6 5 5 5 0 2 1 0 0 0
3 0 4 4 9 0 0 0 3 9 0 0 0 5 0
8 9 2 0 1 0 6 8 0 0 0 8 0 8 0
6 0 4 0 4 0 0 1 6 1 6 9 1 4 2
7 7 7 3 0 0 6 4 0 4 0 1 3 0 0
7 6 0 4 0 2 0 0 4 0 8 0 0 7 6
0 0 4 7 8 3 0 4 0 0 5 0 6 0 3
0 8 0 0 2 0 0 0 1 0 2 0 0 1 0
3 3 1 0 2 0 0 6 0 8 6 0 0 0 0
0 0 0 0 0 8 0 0 0 9 0 4 0 2 8
0 0 4 1 4 9 0 7 0 1 0 5 0 0 8
7 2 0 0 4 5 1 0 9 0 0 6 4 0 0
0 0 0 0 9 6 3 1 3 3 9 0 0 0 5
0 5 0 4 0 7 9 9 0 0 0 0 9 4 0
0 9 8 8 0 6 8 0 0 0 8 0 0 0 0
Output (15x15):
0 0 2 0 9 6 5 5 5 0 2 1 1 1 1
3 0 4 4 9 1 1 1 3 9 1 1 1 5 1
8 9 2 1 1 1 6 8 1 1 1 8 1 8 1
6 0 4 1 4 1 1 1 6 1 6 9 1 4 2
7 7 7 3 1 1 6 4 0 4 1 1 3 0 0
7 6 0 4 1 2 1 1 4 1 8 1 1 7 6
0 0 4 7 8 3 1 4 1 1 5 1 6 1 3
0 8 1 1 2 1 1 1 1 1 2 1 1 1 1
3 3 1 1 2 1 1 6 1 8 6 1 1 1 1
1 1 1 1 1 8 1 1 1 9 1 4 1 2 8
1 1 4 1 4 9 1 7 1 1 1 5 1 1 8
7 2 1 1 4 5 1 1 9 1 1 6 4 1 1
1 1 1 1 9 6 3 1 3 3 9 1 1 1 5
1 5 1 4 0 7 9 9 1 1 1 1 9 4 1
1 9 8 8 0 6 8 1 1 1 8 1 1 1 1

## Example 2
Input (13x13):
9 0 0 0 0 2 8 0 9 0 2 0 9
1 0 0 6 0 0 0 0 0 0 0 9 5
9 0 4 9 3 0 0 5 7 0 8 0 8
0 0 8 6 0 6 0 1 0 0 0 4 1
3 6 0 1 0 3 9 0 0 4 5 7 2
0 8 0 0 0 0 0 0 7 1 8 0 0
9 0 0 2 0 0 0 7 5 7 0 8 4
0 0 0 8 7 5 0 0 7 0 0 5 0
9 9 0 0 0 0 5 0 0 5 0 0 0
8 0 0 8 0 6 5 0 0 0 0 9 0
4 0 0 6 0 7 9 9 8 0 5 7 3
0 0 0 0 0 0 0 7 2 0 0 0 8
0 0 0 7 5 0 5 0 0 0 0 0 3
Output (13x13):
9 1 1 1 1 2 8 1 9 1 2 0 9
1 1 1 6 1 1 1 1 1 1 1 9 5
9 1 4 9 3 1 1 5 7 1 8 0 8
1 1 8 6 1 6 1 1 1 1 1 4 1
3 6 1 1 1 3 9 1 1 4 5 7 2
0 8 1 1 1 1 1 1 7 1 8 0 0
9 1 1 2 1 1 1 7 5 7 1 8 4
1 1 1 8 7 5 1 1 7 1 1 5 1
9 9 1 1 1 1 5 1 1 5 1 1 1
8 1 1 8 1 6 5 1 1 1 1 9 1
4 1 1 6 1 7 9 9 8 1 5 7 3
1 1 1 1 1 1 1 7 2 1 1 1 8
1 1 1 7 5 1 5 1 1 1 1 1 3

## Example 3
Input (16x16):
7 4 4 0 4 0 0 6 1 1 1 0 0 6 0 5
1 1 3 3 4 0 3 8 5 3 4 5 0 8 2 8
8 0 4 8 8 5 0 9 0 0 0 5 5 8 5 8
0 2 6 0 0 0 0 3 0 1 0 8 0 4 0 8
8 0 2 8 0 7 0 0 0 9 0 7 3 0 3 6
0 0 0 0 0 0 5 3 0 6 0 6 0 4 5 7
6 6 0 0 3 1 0 0 2 5 0 0 0 3 4 5
7 0 7 8 0 1 0 0 0 9 0 7 3 0 3 0
0 6 0 0 5 6 6 5 9 8 3 9 0 7 0 0
7 5 0 0 0 8 0 6 9 0 0 7 1 0 0 0
6 5 3 4 3 0 6 9 4 1 8 9 2 8 7 7
8 6 8 6 3 2 7 3 0 2 0 0 2 1 0 0
9 0 0 0 6 1 8 0 3 3 0 2 0 2 1 4
0 4 0 0 0 0 1 0 0 0 6 0 4 4 5 6
0 5 0 8 3 2 1 0 5 9 1 8 7 0 2 7
0 9 0 1 8 6 0 9 9 8 0 9 0 0 3 0
Output (16x16):
7 4 4 0 4 0 0 6 1 1 1 1 1 6 0 5
1 1 3 3 4 0 3 8 5 3 4 5 1 8 2 8
8 1 4 8 8 5 1 9 1 1 1 5 5 8 5 8
0 2 6 1 1 1 1 3 1 1 1 8 0 4 0 8
8 1 2 8 1 7 1 1 1 9 1 7 3 0 3 6
1 1 1 1 1 1 5 3 1 6 1 6 1 4 5 7
6 6 1 1 3 1 1 1 2 5 1 1 1 3 4 5
7 0 7 8 1 1 1 1 1 9 1 7 3 0 3 1
0 6 0 0 5 6 6 5 9 8 3 9 1 7 1 1
7 5 0 0 0 8 0 6 9 1 1 7 1 1 1 1
6 5 3 4 3 0 6 9 4 1 8 9 2 8 7 7
8 6 8 6 3 2 7 3 0 2 0 0 2 1 1 1
9 1 1 1 6 1 8 1 3 3 0 2 0 2 1 4
0 4 1 1 1 1 1 1 1 1 6 0 4 4 5 6
0 5 1 8 3 2 1 1 5 9 1 8 7 0 2 7
0 9 1 1 8 6 1 9 9 8 1 9 0 0 3 0

## Test
Input (16x16):
0 0 0 8 0 5 0 0 9 0 6 0 0 0 0 5
6 7 6 0 4 0 2 0 0 8 3 6 2 0 0 0
0 0 0 7 0 0 5 4 1 0 1 7 6 0 0 0
0 5 8 0 9 0 0 2 2 0 8 0 4 0 0 7
4 0 0 4 2 2 7 3 2 0 6 4 9 9 9 0
0 1 8 0 5 0 0 0 2 0 0 8 0 9 6 6
9 9 0 2 8 0 0 3 0 0 2 0 0 5 8 0
1 3 0 1 6 1 0 0 0 8 0 0 0 4 0 0
0 0 4 0 7 4 0 0 4 0 0 5 8 0 4 0
0 0 0 6 0 6 0 0 0 0 0 8 0 1 4 4
0 9 0 0 9 0 0 0 0 0 1 5 0 6 0 0
6 0 7 5 9 0 7 0 0 0 4 6 0 2 8 0
5 0 0 0 1 0 2 4 8 0 0 3 0 9 0 8
1 0 0 2 4 0 0 0 1 7 0 0 0 0 5 0
6 9 0 0 7 7 1 0 2 0 0 9 1 0 3 0
1 8 3 0 0 9 7 0 2 7 2 0 8 9 0 0

A previous attempt proposed this solution (it may be wrong):
The transformation changes every zero in a 4-connected region that touches an existing 1 into a 1. Other zeros and all nonzero cells remain unchanged.

<answer>[[0,0,0,8,0,5,1,1,9,0,6,0,0,0,0,5],[6,7,6,0,4,0,2,1,1,8,3,6,2,0,0,0],[0,0,0,7,0,0,5,4,1,1,1,7,6,0,0,0],[0,5,8,0,9,0,0,2,2,1,8,0,4,0,0,7],[4,1,1,4,2,2,7,3,2,1,6,4,9,9,9,0],[1,1,8,0,5,1,1,1,2,1,1,8,0,9,6,6],[9,9,1,2,8,1,1,3,1,1,2,0,0,5,8,0],[1,3,1,1,6,1,1,1,1,8,0,0,0,4,0,0],[1,1,4,1,7,4,1,1,4,1,1,5,8,1,4,0],[1,1,1,6,0,6,1,1,1,1,1,8,1,1,4,4],[1,9,1,1,9,1,1,1,1,1,1,5,1,6,0,0],[6,1,7,5,9,1,7,1,1,1,4,6,1,2,8,0],[5,1,1,1,1,1,2,4,8,1,1,3,1,9,0,8],[1,1,1,2,4,1,1,1,1,7,1,1,1,1,5,0],[6,9,1,1,7,7,1,1,2,1,1,9,1,1,3,0],[1,8,3,1,1,9,7,1,2,7,2,0,8,9,0,0]]</answer>

Now act as a careful independent verifier, not a copy editor. Infer the rule afresh from the demonstrations, check it against every input/output pair, and inspect whether the proposed grid follows that rule cell by cell. In particular, check repeated motifs and their completion, symmetry/reflection/rotation, object boundaries, colors, and dimensions. Correct the grid if the candidate is inconsistent; if it is consistent, return it unchanged. Briefly explain the rule outside the answer tags. End with the complete output grid inside <answer></answer> tags as a JSON list of rows, with nothing else inside the tags.

Output: The rule is to change zero cells in 4-connected zero regions that touch an existing 1 into 1s. Other zeros and all nonzero cells remain unchanged. The proposed grid is consistent with this rule.

<answer>[[0,0,0,8,0,5,1,1,9,0,6,0,0,0,0,5],[6,7,6,0,4,0,2,1,1,8,3,6,2,0,0,0],[0,0,0,7,0,0,5,4,1,1,1,7,6,0,0,0],[0,5,8,0,9,0,0,2,2,1,8,0,4,0,0,7],[4,1,1,4,2,2,7,3,2,1,6,4,9,9,9,0],[1,1,8,0,5,1,1,1,2,1,1,8,0,9,6,6],[9,9,1,2,8,1,1,3,1,1,2,0,0,5,8,0],[1,3,1,1,6,1,1,1,1,8,0,0,0,4,0,0],[1,1,4,1,7,4,1,1,4,1,1,5,8,1,4,0],[1,1,1,6,0,6,1,1,1,1,1,8,1,1,4,4],[1,9,1,1,9,1,1,1,1,1,1,5,1,6,0,0],[6,1,7,5,9,1,7,1,1,1,4,6,1,2,8,0],[5,1,1,1,1,1,2,4,8,1,1,3,1,9,0,8],[1,1,1,2,4,1,1,1,1,7,1,1,1,1,5,0],[6,9,1,1,7,7,1,1,2,1,1,9,1,1,3,0],[1,8,3,1,1,9,7,1,2,7,2,0,8,9,0,0]]</answer>


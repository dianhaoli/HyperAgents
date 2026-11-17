Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (14x14):
0 0 0 0 5 5 5 5 5 0 0 0 3 0
0 0 0 0 5 5 5 5 5 3 0 0 0 0
0 0 0 3 5 5 5 5 5 0 0 3 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
3 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 3 0 3 0
0 3 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 3 0 5 5 5 5 5 0 0 0 3 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 3 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
Output (14x14):
0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 5 0 0 0
0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0

## Example 2
Input (14x14):
0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (14x14):
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 5 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 5 0 0 5 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Example 3
Input (14x14):
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 1 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (14x14):
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 5 5 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 5 0 5 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Test
Input (14x14):
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 4 0 0 5 5 0 0 4 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 4 0 5 5 0 0 0 0 0 0 0
0 4 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 4 0 0 0 4 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 4 0 4 0 5 5 0 0 0 4 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 4 0

Solve the task by inferring one precise transformation from the demonstrations. Before deciding, inspect the grids systematically: compare dimensions, colors, connected objects and their bounding boxes; look for repeated motifs, symmetry, reflection, rotation, completion of partial patterns, and changes in object size or position. Do not assume the output is the input with only a small local edit. Derive the rule from the examples, then check that it reproduces every demonstrated output exactly. Apply that same rule to the test. Preserve the full grid and its dimensions unless the examples show a dimension change. Give a brief explanation outside the answer tags, then end with the complete output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: The colored markers disappear, and the 5-bar extends toward each side by the number of markers in that row and direction. All other cells remain unchanged.

<answer>[[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,5,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,5,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,5,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,0,0,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (14x14):
0 0 0 0 5 5 5 5 5 0 0 0 3 0
0 0 0 0 5 5 5 5 5 3 0 0 0 0
0 0 0 3 5 5 5 5 5 0 0 3 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
3 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 3 0 3 0
0 3 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 3 0 5 5 5 5 5 0 0 0 3 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 3 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
Output (14x14):
0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 5 0 0 0
0 0 0 5 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 5 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0
0 0 0 0 5 5 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 5 0 0 0 0 0

## Example 2
Input (14x14):
0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (14x14):
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 5 0 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 5 0 0 5 0 0 0 0 5 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Example 3
Input (14x14):
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 1 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (14x14):
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 5 0 0 0 5 5 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5
0 5 0 5 0 0 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Test
Input (14x14):
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 4 0 0 5 5 0 0 4 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 4 0 5 5 0 0 0 0 0 0 0
0 4 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 4 0 0 0 4 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 4 0 4 0 5 5 0 0 0 4 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 0 0
0 0 0 0 0 5 5 0 0 0 0 0 4 0

A previous attempt proposed this solution (it may be wrong):
The colored markers disappear, and the 5-bar extends toward each side by the number of markers in that row and direction. All other cells remain unchanged.

<answer>[[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,5,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,5,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,5,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,0,0,0,0,0,0]]</answer>

Now act as a careful independent verifier, not a copy editor. Infer the rule afresh from the demonstrations, check it against every input/output pair, and inspect whether the proposed grid follows that rule cell by cell. In particular, check repeated motifs and their completion, symmetry/reflection/rotation, object boundaries, colors, and dimensions. Correct the grid if the candidate is inconsistent; if it is consistent, return it unchanged. Briefly explain the rule outside the answer tags. End with the complete output grid inside <answer></answer> tags as a JSON list of rows, with nothing else inside the tags.

Output: The markers are removed, and the 5-bar extends toward each side by the number of markers on that side in the corresponding row. The proposed grid matches this rule.

<answer>[[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,5,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,5,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,5,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,0,0,0,0,0,0]]</answer>


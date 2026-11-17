Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one transformation rule. Infer a rule that explains every pair, then apply it to the test input.

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

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, apply the proposed rule to each training input and check that the resulting grid matches its demonstrated output exactly, including dimensions and individual cells. Do not add changes that the rule does not explain.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: The less frequent nonzero color is replaced by 0, and the more frequent color is replaced by the less frequent color. Applying that rule gives:

<answer>[[5, 5, 5, 0, 5], [5, 0, 5, 5, 5], [5, 0, 0, 5, 0], [5, 5, 5, 0, 5], [0, 0, 0, 5, 5]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one transformation rule. Infer a rule that explains every pair, then apply it to the test input.

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

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, apply the proposed rule to each training input and check that the resulting grid matches its demonstrated output exactly, including dimensions and individual cells. Do not add changes that the rule does not explain.

Independent second solve: infer the rule afresh from the demonstrations without seeing or relying on another proposed answer. Use a complementary analysis: compare dimensions and color counts, then inspect repeated subgrids, connected objects, symmetry, and relative positions. Consider whether the rule changes selected cells or rearranges, crops, or expands the grid. Prefer the simplest rule that matches every training pair exactly, then derive the test grid from it.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: In each example, the more frequent nonzero color is preserved and the less frequent color is replaced with 0. In the test grid, 3 appears 16 times and 5 appears 9 times, so replace every 5 with 0.

<answer>[[3, 3, 3, 0, 3], [3, 0, 3, 3, 3], [3, 0, 0, 3, 0], [3, 3, 3, 0, 3], [0, 0, 0, 3, 3]]</answer>


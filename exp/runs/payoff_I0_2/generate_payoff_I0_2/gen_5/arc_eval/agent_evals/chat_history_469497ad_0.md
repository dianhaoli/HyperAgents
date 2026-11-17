Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one transformation rule. Infer a rule that explains every pair, then apply it to the test input.

## Example 1
Input (5x5):
0 0 0 0 7
4 4 0 0 7
4 4 0 0 6
0 0 0 0 6
7 7 6 6 6
Output (15x15):
0 0 0 0 0 0 0 0 2 0 0 0 7 7 7
0 0 0 0 0 0 0 2 0 0 0 0 7 7 7
0 0 0 0 0 0 2 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 2 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 2 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 2 0 0 0 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6

## Example 2
Input (5x5):
0 0 0 0 3
0 8 8 0 3
0 8 8 0 3
0 0 0 0 3
3 3 3 3 3
Output (10x10):
2 0 0 0 0 0 0 2 3 3
0 2 0 0 0 0 2 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 2 0 0 0 0 2 0 3 3
2 0 0 0 0 0 0 2 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3

## Example 3
Input (5x5):
0 0 0 0 9
0 1 1 0 9
0 1 1 0 3
0 0 0 0 3
9 9 3 3 4
Output (20x20):
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 9
0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 9 9 9 9
0 0 2 0 0 0 0 0 0 0 0 0 0 2 0 0 9 9 9 9
0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 3 3 3 3
0 0 2 0 0 0 0 0 0 0 0 0 0 2 0 0 3 3 3 3
0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 3 3 3 3
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 3
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4

## Test
Input (5x5):
0 6 6 0 8
0 6 6 0 8
0 0 0 0 1
0 0 0 0 7
8 8 1 7 9

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, apply the proposed rule to each training input and check that the resulting grid matches its demonstrated output exactly, including dimensions and individual cells. Do not add changes that the rule does not explain.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: The five distinct nonzero colors set the enlargement factor to 5. The 2×2 block of 6s expands accordingly, with diagonal 2s in the two empty cells diagonally below it.

<answer>[[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0],[0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],[0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0],[0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one transformation rule. Infer a rule that explains every pair, then apply it to the test input.

## Example 1
Input (5x5):
0 0 0 0 7
4 4 0 0 7
4 4 0 0 6
0 0 0 0 6
7 7 6 6 6
Output (15x15):
0 0 0 0 0 0 0 0 2 0 0 0 7 7 7
0 0 0 0 0 0 0 2 0 0 0 0 7 7 7
0 0 0 0 0 0 2 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 7 7 7
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
4 4 4 4 4 4 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 2 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 2 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 2 0 0 0 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6
7 7 7 7 7 7 6 6 6 6 6 6 6 6 6

## Example 2
Input (5x5):
0 0 0 0 3
0 8 8 0 3
0 8 8 0 3
0 0 0 0 3
3 3 3 3 3
Output (10x10):
2 0 0 0 0 0 0 2 3 3
0 2 0 0 0 0 2 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 0 8 8 8 8 0 0 3 3
0 2 0 0 0 0 2 0 3 3
2 0 0 0 0 0 0 2 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3

## Example 3
Input (5x5):
0 0 0 0 9
0 1 1 0 9
0 1 1 0 3
0 0 0 0 3
9 9 3 3 4
Output (20x20):
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 9
0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 9 9 9 9
0 0 2 0 0 0 0 0 0 0 0 0 0 2 0 0 9 9 9 9
0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 9 9 9 9
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 3 3 3 3
0 0 0 2 0 0 0 0 0 0 0 0 2 0 0 0 3 3 3 3
0 0 2 0 0 0 0 0 0 0 0 0 0 2 0 0 3 3 3 3
0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 3 3 3 3
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 3
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4
9 9 9 9 9 9 9 9 3 3 3 3 3 3 3 3 4 4 4 4

## Test
Input (5x5):
0 6 6 0 8
0 6 6 0 8
0 0 0 0 1
0 0 0 0 7
8 8 1 7 9

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, apply the proposed rule to each training input and check that the resulting grid matches its demonstrated output exactly, including dimensions and individual cells. Do not add changes that the rule does not explain.

Independent second solve: infer the rule afresh from the demonstrations without seeing or relying on another proposed answer. Use a complementary analysis: compare dimensions and color counts, then inspect repeated subgrids, connected objects, symmetry, and relative positions. Consider whether the rule changes selected cells or rearranges, crops, or expands the grid. Prefer the simplest rule that matches every training pair exactly, then derive the test grid from it.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: The grid is enlarged by the number of distinct nonzero colors: 5, so the output is 25×25. Each input cell becomes a 5×5 block. The zero cell at row 2, column 0 is diagonally adjacent to a colored cell, so its block contains a diagonal of 2s.

<answer>[[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[0,0,0,0,0,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,8,8,8,8,8],[2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],[0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],[0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],[0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],[0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,7,7,7],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9],[8,8,8,8,8,8,8,8,8,8,1,1,1,1,1,7,7,7,7,7,9,9,9,9,9]]</answer>


Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one transformation rule. Infer a rule that explains every pair, then apply it to the test input.

## Example 1
Input (13x16):
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 5 0 0 5 5
0 0 0 5 0 0 0 5 0 0 0 5 0 0 5 0
0 0 0 5 0 0 0 5 5 5 5 5 5 5 5 0
0 0 0 5 0 0 0 5 0 0 0 0 0 0 5 0
0 0 0 5 5 5 5 5 0 0 0 0 0 0 5 5
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
Output (13x16):
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 5 0 0 5 5
0 0 0 5 4 4 4 5 0 0 0 5 0 0 5 4
0 0 0 5 4 4 4 5 5 5 5 5 5 5 5 4
0 0 0 5 4 4 4 5 0 0 0 0 0 0 5 4
0 0 0 5 5 5 5 5 0 0 0 0 0 0 5 5
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0

## Example 2
Input (12x19):
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 5
5 5 0 0 0 5 5 5 5 0 0 0 0 5 0 0 0 5 0
0 5 5 5 5 5 0 0 5 5 5 5 5 5 5 5 5 5 0
5 5 0 0 0 5 0 0 5 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 5 0 0 5 0 0 0 0 5 0 0 0 5 5
0 0 0 0 0 5 0 0 5 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 5 0 0 5 0 0 5 0 0 5 0 0 0 0
0 0 0 0 0 5 5 5 5 0 0 5 0 0 5 5 5 5 5
0 0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
Output (12x19):
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 5
5 5 0 0 0 5 5 5 5 0 0 0 0 5 0 0 0 5 4
4 5 5 5 5 5 4 4 5 5 5 5 5 5 5 5 5 5 4
5 5 0 0 0 5 4 4 5 0 0 0 0 5 0 0 0 5 4
0 0 0 0 0 5 4 4 5 0 0 0 0 5 0 0 0 5 5
0 0 0 0 0 5 4 4 5 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 5 4 4 5 0 0 5 4 4 5 0 0 0 0
0 0 0 0 0 5 5 5 5 0 0 5 4 4 5 5 5 5 5
0 0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0

## Example 3
Input (15x17):
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 5 5 5 5 0
5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 5 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 5 5
0 0 0 5 5 5 5 0 0 0 0 5 0 0 0 5 0
5 5 5 5 0 0 5 0 0 0 0 5 5 5 5 5 0
0 0 0 5 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
Output (15x17):
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 5 5 5 5 0
5 5 5 5 5 5 5 5 5 5 5 5 4 4 4 5 0
0 0 0 0 0 5 0 0 0 0 0 5 4 4 4 5 5
0 0 0 5 5 5 5 0 0 0 0 5 4 4 4 5 0
5 5 5 5 4 4 5 0 0 0 0 5 5 5 5 5 0
0 0 0 5 4 4 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 4 4 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 4 4 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 4 4 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0

## Test
Input (16x18):
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 5 5 5 5 5 0 0 0 5 0 0 5 0
5 5 5 5 5 5 0 0 0 5 5 5 5 5 0 0 5 5
0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 5 0
0 5 0 0 0 5 5 5 5 5 0 0 0 5 5 5 5 0
0 5 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 0 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, apply the proposed rule to each training input and check that the resulting grid matches its demonstrated output exactly, including dimensions and individual cells. Do not add changes that the rule does not explain.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: The transformation fills each 4-connected region of zeros enclosed by 5s with color 4. In the test grid, there are two such regions.

<answer>[[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[0,0,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,5,0,0,0],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,5,0,0,0],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,5,0,0,0],[0,0,0,0,0,0,0,5,0,0,0,0,0,5,5,5,5,0],[0,0,0,0,0,5,5,5,5,5,0,0,0,5,4,4,5,0],[5,5,5,5,5,5,4,4,4,5,5,5,5,5,4,4,5,5],[0,5,0,0,0,5,4,4,4,5,0,0,0,5,4,4,5,0],[0,5,0,0,0,5,5,5,5,5,0,0,0,5,5,5,5,0],[0,5,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,0,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one transformation rule. Infer a rule that explains every pair, then apply it to the test input.

## Example 1
Input (13x16):
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 5 0 0 5 5
0 0 0 5 0 0 0 5 0 0 0 5 0 0 5 0
0 0 0 5 0 0 0 5 5 5 5 5 5 5 5 0
0 0 0 5 0 0 0 5 0 0 0 0 0 0 5 0
0 0 0 5 5 5 5 5 0 0 0 0 0 0 5 5
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
Output (13x16):
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 5 0 0 0 5 0 0 5 5
0 0 0 5 4 4 4 5 0 0 0 5 0 0 5 4
0 0 0 5 4 4 4 5 5 5 5 5 5 5 5 4
0 0 0 5 4 4 4 5 0 0 0 0 0 0 5 4
0 0 0 5 5 5 5 5 0 0 0 0 0 0 5 5
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0

## Example 2
Input (12x19):
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 5
5 5 0 0 0 5 5 5 5 0 0 0 0 5 0 0 0 5 0
0 5 5 5 5 5 0 0 5 5 5 5 5 5 5 5 5 5 0
5 5 0 0 0 5 0 0 5 0 0 0 0 5 0 0 0 5 0
0 0 0 0 0 5 0 0 5 0 0 0 0 5 0 0 0 5 5
0 0 0 0 0 5 0 0 5 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 5 0 0 5 0 0 5 0 0 5 0 0 0 0
0 0 0 0 0 5 5 5 5 0 0 5 0 0 5 5 5 5 5
0 0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
Output (12x19):
0 0 0 0 0 0 0 0 0 0 0 0 0 5 0 0 0 5 5
5 5 0 0 0 5 5 5 5 0 0 0 0 5 0 0 0 5 4
4 5 5 5 5 5 4 4 5 5 5 5 5 5 5 5 5 5 4
5 5 0 0 0 5 4 4 5 0 0 0 0 5 0 0 0 5 4
0 0 0 0 0 5 4 4 5 0 0 0 0 5 0 0 0 5 5
0 0 0 0 0 5 4 4 5 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 5 4 4 5 0 0 5 4 4 5 0 0 0 0
0 0 0 0 0 5 5 5 5 0 0 5 4 4 5 5 5 5 5
0 0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0 0

## Example 3
Input (15x17):
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 5 5 5 5 0
5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 5 0
0 0 0 0 0 5 0 0 0 0 0 5 0 0 0 5 5
0 0 0 5 5 5 5 0 0 0 0 5 0 0 0 5 0
5 5 5 5 0 0 5 0 0 0 0 5 5 5 5 5 0
0 0 0 5 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 0 0 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 0 0 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
Output (15x17):
0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 5 5 5 5 5 0
5 5 5 5 5 5 5 5 5 5 5 5 4 4 4 5 0
0 0 0 0 0 5 0 0 0 0 0 5 4 4 4 5 5
0 0 0 5 5 5 5 0 0 0 0 5 4 4 4 5 0
5 5 5 5 4 4 5 0 0 0 0 5 5 5 5 5 0
0 0 0 5 4 4 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 4 4 5 0 0 0 0 0 5 0 0 0 0
0 0 0 5 5 5 5 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
5 5 5 5 5 5 5 5 5 5 5 4 4 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 4 4 5 0 0 0
0 0 0 0 0 5 0 0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0 0

## Test
Input (16x18):
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 5 5 5 5 0
0 0 0 0 0 5 5 5 5 5 0 0 0 5 0 0 5 0
5 5 5 5 5 5 0 0 0 5 5 5 5 5 0 0 5 5
0 5 0 0 0 5 0 0 0 5 0 0 0 5 0 0 5 0
0 5 0 0 0 5 5 5 5 5 0 0 0 5 5 5 5 0
0 5 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 0 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, apply the proposed rule to each training input and check that the resulting grid matches its demonstrated output exactly, including dimensions and individual cells. Do not add changes that the rule does not explain.

Independent second solve: infer the rule afresh from the demonstrations without seeing or relying on another proposed answer. Use a complementary analysis: compare dimensions and color counts, then inspect repeated subgrids, connected objects, symmetry, and relative positions. Consider whether the rule changes selected cells or rearranges, crops, or expands the grid. Prefer the simplest rule that matches every training pair exactly, then derive the test grid from it.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: <answer>[[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,5,4,4,4],[0,0,0,0,0,0,0,5,4,4,4,4,4,4,5,4,4,4],[0,0,0,0,0,0,0,5,4,4,4,4,4,4,5,4,4,4],[0,0,0,0,0,0,0,5,4,4,4,4,4,5,5,5,5,4],[0,0,0,0,0,5,5,5,5,5,4,4,4,5,4,4,5,4],[5,5,5,5,5,5,4,4,4,5,5,5,5,5,4,4,5,5],[4,5,0,0,0,5,4,4,4,5,0,0,0,5,4,4,5,0],[4,5,0,0,0,5,5,5,5,5,0,0,0,5,5,5,0,0],[4,5,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,4,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0]]</answer>


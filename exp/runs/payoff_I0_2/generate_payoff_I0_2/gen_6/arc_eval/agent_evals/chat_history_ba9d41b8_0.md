Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one transformation rule. Infer a rule that explains every pair, then apply it to the test input.

## Example 1
Input (13x15):
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (13x15):
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 0 1 0 1 0 0 0 0 0 0 0 0 0 0
1 1 0 1 1 0 0 0 0 0 0 0 0 0 0
1 0 1 0 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 0 8 0 8 0 8 0 8 8 0
0 0 0 0 8 8 0 8 0 8 0 8 0 8 0
0 0 0 0 8 0 8 0 8 0 8 0 8 8 0
0 0 0 0 8 8 0 8 0 8 0 8 0 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Example 2
Input (16x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (16x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 0 2 0 2 0 2 0 2 2 0
0 0 0 0 2 2 0 2 0 2 0 2 0 2 0
0 0 0 0 2 0 2 0 2 0 2 0 2 2 0
0 0 0 0 2 2 0 2 0 2 0 2 0 2 0
0 0 0 0 2 0 2 0 2 0 2 0 2 2 0
0 0 0 0 2 2 0 2 0 2 0 2 0 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Example 3
Input (17x16):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (17x16):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 0 3 0 3 0 3 3 0 0 0 0 0 0
0 0 3 3 0 3 0 3 0 3 0 0 0 0 0 0
0 0 3 0 3 0 3 0 3 3 0 0 0 0 0 0
0 0 3 3 0 3 0 3 0 3 0 0 0 0 0 0
0 0 3 0 3 0 3 0 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 0 4 0 4 0 4 4 0 0 8 0 8 0 8 8
4 4 0 4 0 4 0 4 0 0 8 8 0 8 0 8
4 0 4 0 4 0 4 4 0 0 8 0 8 0 8 8
4 4 0 4 0 4 0 4 0 0 8 8 8 8 8 8
4 0 4 0 4 0 4 4 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Test
Input (19x19):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, apply the proposed rule to each training input and check that the resulting grid matches its demonstrated output exactly, including dimensions and individual cells. Do not add changes that the rule does not explain.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: Each solid rectangle keeps its perimeter. Inside it, cells whose local row and column indices have an even sum are changed to 0. This reproduces the perforated rectangles in all three examples.

<answer>[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0],[0,8,0,8,0,8,0,8,8,0,7,7,7,7,7,7,7,7,0],[0,8,8,0,8,0,8,0,8,0,7,0,7,0,7,0,7,7,0],[0,8,0,8,0,8,0,8,8,0,7,7,0,7,0,7,0,7,0],[0,8,8,0,8,0,8,0,8,0,7,0,7,0,7,0,7,7,0],[0,8,0,8,0,8,0,8,8,0,7,7,0,7,0,7,0,7,0],[0,8,8,0,8,0,8,0,8,0,7,0,7,0,7,0,7,7,0],[0,8,8,8,8,8,8,8,8,0,7,7,7,7,7,7,7,7,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,6,6,6,6,6,6,6,6,6,6,6,0,4,4,4,4,4,0],[0,6,0,6,0,6,0,6,0,6,0,6,0,4,0,4,0,4,0],[0,6,6,0,6,0,6,0,6,0,6,6,0,4,4,0,4,4,0],[0,6,0,6,0,6,0,6,0,6,0,6,0,4,0,4,0,4,0],[0,6,6,0,6,0,6,0,6,0,6,6,0,4,4,0,4,4,0],[0,6,0,6,0,6,0,6,0,6,0,6,0,4,4,4,4,4,0],[0,6,6,0,6,0,6,0,6,0,6,6,0,0,0,0,0,0,0],[0,6,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one transformation rule. Infer a rule that explains every pair, then apply it to the test input.

## Example 1
Input (13x15):
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (13x15):
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 0 1 0 1 0 0 0 0 0 0 0 0 0 0
1 1 0 1 1 0 0 0 0 0 0 0 0 0 0
1 0 1 0 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 8 0 8 0 8 0 8 0 8 8 0
0 0 0 0 8 8 0 8 0 8 0 8 0 8 0
0 0 0 0 8 0 8 0 8 0 8 0 8 8 0
0 0 0 0 8 8 0 8 0 8 0 8 0 8 0
0 0 0 0 8 8 8 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Example 2
Input (16x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (16x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 2 0 2 0 2 0 2 0 2 2 0
0 0 0 0 2 2 0 2 0 2 0 2 0 2 0
0 0 0 0 2 0 2 0 2 0 2 0 2 2 0
0 0 0 0 2 2 0 2 0 2 0 2 0 2 0
0 0 0 0 2 0 2 0 2 0 2 0 2 2 0
0 0 0 0 2 2 0 2 0 2 0 2 0 2 0
0 0 0 0 2 2 2 2 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Example 3
Input (17x16):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (17x16):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 3 0 3 0 3 0 3 3 0 0 0 0 0 0
0 0 3 3 0 3 0 3 0 3 0 0 0 0 0 0
0 0 3 0 3 0 3 0 3 3 0 0 0 0 0 0
0 0 3 3 0 3 0 3 0 3 0 0 0 0 0 0
0 0 3 0 3 0 3 0 3 3 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0 8 8 8 8 8 8
4 0 4 0 4 0 4 4 0 0 8 0 8 0 8 8
4 4 0 4 0 4 0 4 0 0 8 8 0 8 0 8
4 0 4 0 4 0 4 4 0 0 8 0 8 0 8 8
4 4 0 4 0 4 0 4 0 0 8 8 8 8 8 8
4 0 4 0 4 0 4 4 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

## Test
Input (19x19):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, apply the proposed rule to each training input and check that the resulting grid matches its demonstrated output exactly, including dimensions and individual cells. Do not add changes that the rule does not explain.

Independent second solve: infer the rule afresh from the demonstrations without seeing or relying on another proposed answer. Use a complementary analysis: compare dimensions and color counts, then inspect repeated subgrids, connected objects, symmetry, and relative positions. Consider whether the rule changes selected cells or rearranges, crops, or expands the grid. Prefer the simplest rule that matches every training pair exactly, then derive the test grid from it.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: Each colored rectangle keeps its border. Inside, cells whose row and column offsets from the rectangle’s top-left corner have the same parity are changed to 0.

<answer>[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0],[0,8,0,8,0,8,0,8,8,0,7,7,7,7,7,7,7,7,0],[0,8,8,0,8,0,8,0,8,0,7,0,7,0,7,0,7,7,0],[0,8,0,8,0,8,0,8,8,0,7,7,0,7,0,7,0,7,0],[0,8,8,0,8,0,8,0,8,0,7,0,7,0,7,0,7,7,0],[0,8,0,8,0,8,0,8,8,0,7,7,0,7,0,7,0,7,0],[0,8,8,0,8,0,8,0,8,0,7,0,7,0,7,0,7,7,0],[0,8,8,8,8,8,8,8,8,0,7,7,7,7,7,7,7,7,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,6,6,6,6,6,6,6,6,6,6,6,0,4,4,4,4,4,0],[0,6,0,6,0,6,0,6,0,6,0,6,0,4,0,4,0,4,0],[0,6,6,0,6,0,6,0,6,0,6,6,0,4,4,0,4,4,0],[0,6,0,6,0,6,0,6,0,6,0,6,0,4,0,4,0,4,0],[0,6,6,0,6,0,6,0,6,0,6,6,0,4,4,0,4,4,0],[0,6,0,6,0,6,0,6,0,6,0,6,0,4,4,4,4,4,0],[0,6,6,0,6,0,6,0,6,0,6,6,0,0,0,0,0,0,0],[0,6,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,0,0]]</answer>


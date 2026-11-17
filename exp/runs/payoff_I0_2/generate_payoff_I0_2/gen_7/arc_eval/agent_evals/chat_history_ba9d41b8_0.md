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

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, state one concise rule and explain how it reproduces each training output; if the rule does not account for every example, revise it rather than guessing. Then apply the rule to the test input. Check that each training result matches exactly, including dimensions and individual cells, and do not add changes the rule does not explain.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: **Rule:** For each solid rectangle, keep its border unchanged. Within the interior, change a cell to 0 when its row and column indices relative to the rectangle’s top-left corner have the same parity. All other cells remain unchanged. This reproduces the two rectangles in Example 1, the rectangle in Example 2, and all three rectangles in Example 3.

Applying the rule to the four rectangles in the test input gives:

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

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, state one concise rule and explain how it reproduces each training output; if the rule does not account for every example, revise it rather than guessing. Then apply the rule to the test input. Check that each training result matches exactly, including dimensions and individual cells, and do not add changes the rule does not explain.

A first attempt proposed this test output (it may be wrong):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0
0 8 0 8 0 8 0 8 8 0 7 7 7 7 7 7 7 7 0
0 8 8 0 8 0 8 0 8 0 7 0 7 0 7 0 7 7 0
0 8 0 8 0 8 0 8 8 0 7 7 0 7 0 7 0 7 0
0 8 8 0 8 0 8 0 8 0 7 0 7 0 7 0 7 7 0
0 8 0 8 0 8 0 8 8 0 7 7 0 7 0 7 0 7 0
0 8 8 0 8 0 8 0 8 0 7 0 7 0 7 0 7 7 0
0 8 8 8 8 8 8 8 8 0 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 6 6 6 0 4 4 4 4 4 0
0 6 0 6 0 6 0 6 0 6 0 6 0 4 0 4 0 4 0
0 6 6 0 6 0 6 0 6 0 6 6 0 4 4 0 4 4 0
0 6 0 6 0 6 0 6 0 6 0 6 0 4 0 4 0 4 0
0 6 6 0 6 0 6 0 6 0 6 6 0 4 4 0 4 4 0
0 6 0 6 0 6 0 6 0 6 0 6 0 4 4 4 4 4 0
0 6 6 0 6 0 6 0 6 0 6 6 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0
Independently infer the rule from the examples. Audit this proposal against the rule, especially its dimensions, object placement, colors, and cells that should remain unchanged. Return a corrected grid if any part fails; keep it only if the same rule explains it and every training pair.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: **Rule:** For each solid colored rectangle, preserve its one-cell border. Inside the border, change cells to 0 when their local row and column offsets have the same parity; leave all other cells and the surrounding grid unchanged.

This reproduces Example 1’s 5×5 and 6×10 rectangles, Example 2’s 8×10 rectangle, and all three rectangles in Example 3. The proposed test output follows the same rule and retains the 19×19 dimensions and object positions.

<answer>[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0],[0,8,0,8,0,8,0,8,8,0,7,7,7,7,7,7,7,7,0],[0,8,8,0,8,0,8,0,8,0,7,0,7,0,7,0,7,7,0],[0,8,0,8,0,8,0,8,8,0,7,7,0,7,0,7,0,7,0],[0,8,8,0,8,0,8,0,8,0,7,0,7,0,7,0,7,7,0],[0,8,0,8,0,8,0,8,8,0,7,7,0,7,0,7,0,7,0],[0,8,8,0,8,0,8,0,8,0,7,0,7,0,7,0,7,7,0],[0,8,8,8,8,8,8,8,8,0,7,7,7,7,7,7,7,7,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,6,6,6,6,6,6,6,6,6,6,6,0,4,4,4,4,4,0],[0,6,0,6,0,6,0,6,0,6,0,6,0,4,0,4,0,4,0],[0,6,6,0,6,0,6,0,6,0,6,6,0,4,4,0,4,4,0],[0,6,0,6,0,6,0,6,0,6,0,6,0,4,0,4,0,4,0],[0,6,6,0,6,0,6,0,6,0,6,6,0,4,4,0,4,4,0],[0,6,0,6,0,6,0,6,0,6,0,6,0,4,4,4,4,4,0],[0,6,6,0,6,0,6,0,6,0,6,6,0,0,0,0,0,0,0],[0,6,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,0,0]]</answer>


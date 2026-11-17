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

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, state one concise rule and explain how it reproduces each training output; if the rule does not account for every example, revise it rather than guessing. Then apply the rule to the test input. Check that each training result matches exactly, including dimensions and individual cells, and do not add changes the rule does not explain.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: Rule: Change only zeros inside closed regions formed by the 5s; the grid edge can complete a boundary. This fills Example 1’s two enclosed regions, Example 2’s three, and Example 3’s three, while leaving all other cells unchanged. In the test, the enclosed regions are the small pocket at row 4, columns 1–2; the upper-right pocket; the lower-left pocket; and the lower-right pocket.

<answer>[[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,5,4,4,4],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,5,4,4,4],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,5,4,4,4],[0,0,0,0,0,0,0,5,0,0,0,0,0,5,5,5,5,4],[0,0,0,0,0,5,5,5,5,5,0,0,0,5,4,4,5,0],[5,5,4,4,4,5,0,0,0,5,5,5,5,5,4,4,5,5],[0,5,4,4,4,5,0,0,0,5,0,0,0,5,4,4,5,0],[0,5,0,0,0,5,5,5,5,5,0,0,0,5,5,5,5,0],[0,5,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,0,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0]]</answer>

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

Solve systematically: compare input/output dimensions, colors, unchanged cells, and object positions in every example. Consider whether the rule uses objects or connected components, a frame or grid, repetition/tiling, reflection/rotation, cropping/expansion, or movement and interaction. Infer the background from the examples rather than assuming color 0 is background. Before answering, state one concise rule and explain how it reproduces each training output; if the rule does not account for every example, revise it rather than guessing. Then apply the rule to the test input. Check that each training result matches exactly, including dimensions and individual cells, and do not add changes the rule does not explain.

A first attempt proposed this test output (it may be wrong):
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
4 4 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 0 0 0 0 5 0 0 0 0 0 0 5 4 4 4
0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 4 4 4
0 0 0 0 0 0 0 5 0 0 0 0 0 0 5 4 4 4
0 0 0 0 0 0 0 5 0 0 0 0 0 5 5 5 5 4
0 0 0 0 0 5 5 5 5 5 0 0 0 5 4 4 5 0
5 5 4 4 4 5 0 0 0 5 5 5 5 5 4 4 5 5
0 5 4 4 4 5 0 0 0 5 0 0 0 5 4 4 5 0
0 5 0 0 0 5 5 5 5 5 0 0 0 5 5 5 5 0
0 5 0 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 0 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
Independently infer the rule from the examples. Audit this proposal against the rule, especially its dimensions, object placement, colors, and cells that should remain unchanged. Return a corrected grid if any part fails; keep it only if the same rule explains it and every training pair.
End your response with the output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: Rule: Fill each zero region that is enclosed by 5s and/or the grid edge with 4; leave open regions and all 5s unchanged. This fills the enclosed pockets in each training example, including the pockets touching a grid edge.

The proposal is not consistent with this rule: it changes 5s in row 9, fills an open region in rows 10–11, and misses enclosed cells, including the middle pocket and the edge pockets.

<answer>[[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,5,4,4,4],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,5,4,4,4],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,5,4,4,4],[0,0,0,0,0,0,0,5,0,0,0,0,0,5,5,5,5,4],[0,0,0,0,0,5,5,5,5,5,0,0,0,5,4,4,5,4],[5,5,5,5,5,5,4,4,4,5,5,5,5,5,4,4,5,5],[4,5,0,0,0,5,4,4,4,5,0,0,0,5,4,4,5,0],[4,5,0,0,0,5,5,5,5,5,0,0,0,5,5,5,5,0],[4,5,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,4,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0]]</answer>


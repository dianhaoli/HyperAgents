Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one rule mapping input grids to output grids. Infer the precise rule and apply it to the test input. Check that your proposed rule reproduces every demonstration exactly before applying it. Do not assume the output has the same dimensions as the input; follow the examples and avoid changing unrelated cells.

Compare the examples carefully: note grid dimensions, object shapes and positions, colors, symmetry, and repeated or unusual features. Test the proposed rule against every example.

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

Give the output grid for the test input. Verify its shape and each cell against the inferred rule. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The 4s are projected toward the 5 barrier. On each row, each 4 on a side adds one 5 extending out from that side of the barrier; all original 4s are removed. This reproduces the examples, including consecutive extensions when several markers share a projection line. The output remains 14×14.

<answer>[[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,5,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,5,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,5,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,0,0,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs share one rule mapping input grids to output grids. Infer the precise rule and apply it to the test input. Check that your proposed rule reproduces every demonstration exactly before applying it. Do not assume the output has the same dimensions as the input; follow the examples and avoid changing unrelated cells.

Analyze this puzzle independently using a structural approach: identify the background, objects or repeated regions, their colors and positions, and exactly what changes from input to output in each example. Compare those changes across all examples, separate the shared rule from incidental details, and check whether the output is assembled, expanded, or rearranged.

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

Give the output grid for the test input. Verify its shape and each cell against the inferred rule. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The 5s form a vertical barrier in columns 5–6. On each side, the 4-markers are replaced by 5s stacked outward from the barrier, with one new 5 per marker in that row. The output remains 14×14; all other cells stay unchanged.

<answer>[[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,5,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,5,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,5,5,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,0,0,0,0,0,0,0],[0,0,0,0,0,5,5,5,0,0,0,0,0,0]]</answer>


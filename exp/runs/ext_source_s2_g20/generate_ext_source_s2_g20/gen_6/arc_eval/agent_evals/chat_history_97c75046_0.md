Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
First identify a precise rule that explains every demonstration pair, then check that rule against each pair before using it. Account for changes in grid dimensions, cell positions, colors, and cells that stay unchanged. Use all examples to distinguish plausible rules; do not assume the test output has the same dimensions as its input or guess by visual similarity.
Mechanical inventories follow each grid: color counts and four-connected component sizes/bounds (coordinates start at 0). Use them only as aids, not as assumptions about which cells form a semantic object; verify the proposed rule on the exact grids.

## Example 1
Input (10x6):
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 5
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 0
7 7 7 7 0 0
7 7 0 0 0 0
7 0 0 0 0 0
7 7 7 0 0 0
Inventory: color 0: 15 cells, 1 four-connected component(s) [15@r5-9,c1-5]; color 5: 1 cells, 1 four-connected component(s) [1@r2-2,c5-5]; color 7: 44 cells, 1 four-connected component(s) [44@r0-9,c0-5]
Output (10x6):
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 0
7 7 7 5 0 0
7 7 0 0 0 0
7 0 0 0 0 0
7 7 7 0 0 0
Inventory: color 0: 15 cells, 1 four-connected component(s) [15@r5-9,c1-5]; color 5: 1 cells, 1 four-connected component(s) [1@r6-6,c3-3]; color 7: 44 cells, 1 four-connected component(s) [44@r0-9,c0-5]

## Example 2
Input (6x8):
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 0 7
7 7 7 7 7 0 0 7
7 5 7 7 0 0 0 7
Inventory: color 0: 6 cells, 1 four-connected component(s) [6@r3-5,c4-6]; color 5: 1 cells, 1 four-connected component(s) [1@r5-5,c1-1]; color 7: 41 cells, 1 four-connected component(s) [41@r0-5,c0-7]
Output (6x8):
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 5 7
7 7 7 7 7 7 0 7
7 7 7 7 7 0 0 7
7 7 7 7 0 0 0 7
Inventory: color 0: 6 cells, 1 four-connected component(s) [6@r3-5,c4-6]; color 5: 1 cells, 1 four-connected component(s) [1@r2-2,c6-6]; color 7: 41 cells, 1 four-connected component(s) [41@r0-5,c0-7]

## Example 3
Input (12x8):
7 7 7 7 7 7 7 7
0 0 7 7 7 7 7 7
0 0 0 0 7 7 7 7
0 0 0 0 0 0 7 7
0 0 0 0 7 7 7 7
0 0 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
5 7 7 7 7 7 7 7
Inventory: color 0: 18 cells, 1 four-connected component(s) [18@r1-5,c0-5]; color 5: 1 cells, 1 four-connected component(s) [1@r11-11,c0-0]; color 7: 77 cells, 1 four-connected component(s) [77@r0-11,c0-7]
Output (12x8):
7 7 7 7 7 7 7 7
0 0 7 7 7 7 7 7
0 0 0 0 7 7 7 7
0 0 0 0 0 0 7 7
0 0 0 0 7 7 7 7
0 0 7 7 7 7 7 7
5 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
Inventory: color 0: 18 cells, 1 four-connected component(s) [18@r1-5,c0-5]; color 5: 1 cells, 1 four-connected component(s) [1@r6-6,c0-0]; color 7: 77 cells, 1 four-connected component(s) [77@r0-11,c0-7]

## Test
Input (10x16):
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 0 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 0 0 7 7 7 7 7 7 7 7 7 7 7
7 7 7 0 0 0 7 7 7 7 7 7 7 7 7 7
7 7 7 0 0 0 7 7 7 7 7 7 7 7 7 7
7 7 7 0 0 0 0 7 7 7 7 7 7 7 7 7
7 7 7 0 0 0 0 0 7 7 7 7 7 7 7 7
7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7
7 7 0 0 0 0 0 0 0 0 7 7 5 7 7 7
Inventory: color 0: 33 cells, 1 four-connected component(s) [33@r2-9,c2-9]; color 5: 1 cells, 1 four-connected component(s) [1@r9-9,c12-12]; color 7: 126 cells, 1 four-connected component(s) [126@r0-9,c0-15]

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: In each example, the 5 is relocated to extend the outline of the 0 shape, and its original cell becomes 7. In the test, the matching continuation is immediately to the right of the bottom row of 0s, at row 9, column 10.

<answer>[[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,0,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,0,0,7,7,7,7,7,7,7,7],[7,7,0,0,0,0,0,0,0,7,7,7,7,7,7,7],[7,7,0,0,0,0,0,0,0,0,5,7,7,7,7,7]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
First identify a precise rule that explains every demonstration pair, then check that rule against each pair before using it. Account for changes in grid dimensions, cell positions, colors, and cells that stay unchanged. Use all examples to distinguish plausible rules; do not assume the test output has the same dimensions as its input or guess by visual similarity.
Mechanical inventories follow each grid: color counts and four-connected component sizes/bounds (coordinates start at 0). Use them only as aids, not as assumptions about which cells form a semantic object; verify the proposed rule on the exact grids.

## Example 1
Input (10x6):
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 5
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 0
7 7 7 7 0 0
7 7 0 0 0 0
7 0 0 0 0 0
7 7 7 0 0 0
Inventory: color 0: 15 cells, 1 four-connected component(s) [15@r5-9,c1-5]; color 5: 1 cells, 1 four-connected component(s) [1@r2-2,c5-5]; color 7: 44 cells, 1 four-connected component(s) [44@r0-9,c0-5]
Output (10x6):
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 7
7 7 7 7 7 0
7 7 7 5 0 0
7 7 0 0 0 0
7 0 0 0 0 0
7 7 7 0 0 0
Inventory: color 0: 15 cells, 1 four-connected component(s) [15@r5-9,c1-5]; color 5: 1 cells, 1 four-connected component(s) [1@r6-6,c3-3]; color 7: 44 cells, 1 four-connected component(s) [44@r0-9,c0-5]

## Example 2
Input (6x8):
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 0 7
7 7 7 7 7 0 0 7
7 5 7 7 0 0 0 7
Inventory: color 0: 6 cells, 1 four-connected component(s) [6@r3-5,c4-6]; color 5: 1 cells, 1 four-connected component(s) [1@r5-5,c1-1]; color 7: 41 cells, 1 four-connected component(s) [41@r0-5,c0-7]
Output (6x8):
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 5 7
7 7 7 7 7 7 0 7
7 7 7 7 7 0 0 7
7 7 7 7 0 0 0 7
Inventory: color 0: 6 cells, 1 four-connected component(s) [6@r3-5,c4-6]; color 5: 1 cells, 1 four-connected component(s) [1@r2-2,c6-6]; color 7: 41 cells, 1 four-connected component(s) [41@r0-5,c0-7]

## Example 3
Input (12x8):
7 7 7 7 7 7 7 7
0 0 7 7 7 7 7 7
0 0 0 0 7 7 7 7
0 0 0 0 0 0 7 7
0 0 0 0 7 7 7 7
0 0 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
5 7 7 7 7 7 7 7
Inventory: color 0: 18 cells, 1 four-connected component(s) [18@r1-5,c0-5]; color 5: 1 cells, 1 four-connected component(s) [1@r11-11,c0-0]; color 7: 77 cells, 1 four-connected component(s) [77@r0-11,c0-7]
Output (12x8):
7 7 7 7 7 7 7 7
0 0 7 7 7 7 7 7
0 0 0 0 7 7 7 7
0 0 0 0 0 0 7 7
0 0 0 0 7 7 7 7
0 0 7 7 7 7 7 7
5 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
Inventory: color 0: 18 cells, 1 four-connected component(s) [18@r1-5,c0-5]; color 5: 1 cells, 1 four-connected component(s) [1@r6-6,c0-0]; color 7: 77 cells, 1 four-connected component(s) [77@r0-11,c0-7]

## Test
Input (10x16):
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 0 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 0 0 7 7 7 7 7 7 7 7 7 7 7
7 7 7 0 0 0 7 7 7 7 7 7 7 7 7 7
7 7 7 0 0 0 7 7 7 7 7 7 7 7 7 7
7 7 7 0 0 0 0 7 7 7 7 7 7 7 7 7
7 7 7 0 0 0 0 0 7 7 7 7 7 7 7 7
7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7
7 7 0 0 0 0 0 0 0 0 7 7 5 7 7 7
Inventory: color 0: 33 cells, 1 four-connected component(s) [33@r2-9,c2-9]; color 5: 1 cells, 1 four-connected component(s) [1@r9-9,c12-12]; color 7: 126 cells, 1 four-connected component(s) [126@r0-9,c0-15]

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,0,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,0,0,7,7,7,7,7,7,7,7],[7,7,0,0,0,0,0,0,0,0,5,7,7,7,7,7],[7,7,0,0,0,0,0,0,0,0,7,7,7,7,7,7]]</answer>


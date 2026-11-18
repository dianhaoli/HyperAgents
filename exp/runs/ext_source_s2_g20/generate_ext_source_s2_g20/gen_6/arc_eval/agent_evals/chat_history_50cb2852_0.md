Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
First identify a precise rule that explains every demonstration pair, then check that rule against each pair before using it. Account for changes in grid dimensions, cell positions, colors, and cells that stay unchanged. Use all examples to distinguish plausible rules; do not assume the test output has the same dimensions as its input or guess by visual similarity.
Mechanical inventories follow each grid: color counts and four-connected component sizes/bounds (coordinates start at 0). Use them only as aids, not as assumptions about which cells form a semantic object; verify the proposed rule on the exact grids.

## Example 1
Input (12x11):
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
Inventory: color 0: 98 cells, 1 four-connected component(s) [98@r0-11,c0-10]; color 1: 18 cells, 1 four-connected component(s) [18@r7-9,c2-7]; color 2: 16 cells, 1 four-connected component(s) [16@r1-4,c1-4]
Output (12x11):
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 8 8 2 0 0 0 0 0 0
0 2 8 8 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 8 8 8 8 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
Inventory: color 0: 98 cells, 1 four-connected component(s) [98@r0-11,c0-10]; color 1: 14 cells, 1 four-connected component(s) [14@r7-9,c2-7]; color 2: 12 cells, 1 four-connected component(s) [12@r1-4,c1-4]; color 8: 8 cells, 2 four-connected component(s) [4@r2-3,c2-3; 4@r8-8,c3-6]

## Example 2
Input (13x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
Inventory: color 0: 121 cells, 1 four-connected component(s) [121@r0-12,c0-14]; color 1: 9 cells, 1 four-connected component(s) [9@r1-3,c10-12]; color 2: 30 cells, 1 four-connected component(s) [30@r1-6,c2-6]; color 3: 35 cells, 1 four-connected component(s) [35@r8-12,c8-14]
Output (13x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 8 8 8 2 0 0 0 1 8 1 0 0
0 0 2 8 8 8 2 0 0 0 1 1 1 0 0
0 0 2 8 8 8 2 0 0 0 0 0 0 0 0
0 0 2 8 8 8 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
Inventory: color 0: 121 cells, 1 four-connected component(s) [121@r0-12,c0-14]; color 1: 8 cells, 1 four-connected component(s) [8@r1-3,c10-12]; color 2: 18 cells, 1 four-connected component(s) [18@r1-6,c2-6]; color 3: 20 cells, 1 four-connected component(s) [20@r8-12,c8-14]; color 8: 28 cells, 3 four-connected component(s) [12@r2-5,c3-5; 1@r2-2,c11-11; 15@r9-11,c9-13]

## Example 3
Input (12x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
Inventory: color 0: 84 cells, 1 four-connected component(s) [84@r0-11,c0-12]; color 1: 32 cells, 1 four-connected component(s) [32@r8-11,c2-9]; color 2: 24 cells, 1 four-connected component(s) [24@r1-6,c6-9]; color 3: 16 cells, 1 four-connected component(s) [16@r2-5,c0-3]
Output (12x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 8 8 2 0 0 0
3 8 8 3 0 0 2 8 8 2 0 0 0
3 8 8 3 0 0 2 8 8 2 0 0 0
3 3 3 3 0 0 2 8 8 2 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
Inventory: color 0: 84 cells, 1 four-connected component(s) [84@r0-11,c0-12]; color 1: 20 cells, 1 four-connected component(s) [20@r8-11,c2-9]; color 2: 16 cells, 1 four-connected component(s) [16@r1-6,c6-9]; color 3: 12 cells, 1 four-connected component(s) [12@r2-5,c0-3]; color 8: 24 cells, 3 four-connected component(s) [8@r2-5,c7-8; 4@r3-4,c1-2; 12@r9-10,c3-8]

## Test
Input (14x13):
0 1 1 1 1 1 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
Inventory: color 0: 89 cells, 1 four-connected component(s) [89@r0-13,c0-12]; color 1: 29 cells, 2 four-connected component(s) [20@r0-3,c1-5; 9@r1-3,c8-10]; color 2: 36 cells, 1 four-connected component(s) [36@r5-10,c2-7]; color 3: 28 cells, 1 four-connected component(s) [28@r7-13,c9-12]

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,1,1,1,1,1,0,0,0,0,0,0,0],[0,1,8,8,8,1,0,0,1,1,1,0,0],[0,1,8,8,8,1,0,0,1,8,1,0,0],[0,1,1,1,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,2,2,2,2,2,2,0,0,0,0,0],[0,0,2,8,8,8,8,2,0,0,0,0,0],[0,0,2,8,8,8,8,2,0,3,3,3,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,8,8,3]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
First identify a precise rule that explains every demonstration pair, then check that rule against each pair before using it. Account for changes in grid dimensions, cell positions, colors, and cells that stay unchanged. Use all examples to distinguish plausible rules; do not assume the test output has the same dimensions as its input or guess by visual similarity.
Mechanical inventories follow each grid: color counts and four-connected component sizes/bounds (coordinates start at 0). Use them only as aids, not as assumptions about which cells form a semantic object; verify the proposed rule on the exact grids.

## Example 1
Input (12x11):
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
Inventory: color 0: 98 cells, 1 four-connected component(s) [98@r0-11,c0-10]; color 1: 18 cells, 1 four-connected component(s) [18@r7-9,c2-7]; color 2: 16 cells, 1 four-connected component(s) [16@r1-4,c1-4]
Output (12x11):
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 8 8 2 0 0 0 0 0 0
0 2 8 8 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 1 8 8 8 8 1 0 0 0
0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
Inventory: color 0: 98 cells, 1 four-connected component(s) [98@r0-11,c0-10]; color 1: 14 cells, 1 four-connected component(s) [14@r7-9,c2-7]; color 2: 12 cells, 1 four-connected component(s) [12@r1-4,c1-4]; color 8: 8 cells, 2 four-connected component(s) [4@r2-3,c2-3; 4@r8-8,c3-6]

## Example 2
Input (13x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
Inventory: color 0: 121 cells, 1 four-connected component(s) [121@r0-12,c0-14]; color 1: 9 cells, 1 four-connected component(s) [9@r1-3,c10-12]; color 2: 30 cells, 1 four-connected component(s) [30@r1-6,c2-6]; color 3: 35 cells, 1 four-connected component(s) [35@r8-12,c8-14]
Output (13x15):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 1 1 1 0 0
0 0 2 8 8 8 2 0 0 0 1 8 1 0 0
0 0 2 8 8 8 2 0 0 0 1 1 1 0 0
0 0 2 8 8 8 2 0 0 0 0 0 0 0 0
0 0 2 8 8 8 2 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 8 8 8 8 8 3
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3
Inventory: color 0: 121 cells, 1 four-connected component(s) [121@r0-12,c0-14]; color 1: 8 cells, 1 four-connected component(s) [8@r1-3,c10-12]; color 2: 18 cells, 1 four-connected component(s) [18@r1-6,c2-6]; color 3: 20 cells, 1 four-connected component(s) [20@r8-12,c8-14]; color 8: 28 cells, 3 four-connected component(s) [12@r2-5,c3-5; 1@r2-2,c11-11; 15@r9-11,c9-13]

## Example 3
Input (12x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
Inventory: color 0: 84 cells, 1 four-connected component(s) [84@r0-11,c0-12]; color 1: 32 cells, 1 four-connected component(s) [32@r8-11,c2-9]; color 2: 24 cells, 1 four-connected component(s) [24@r1-6,c6-9]; color 3: 16 cells, 1 four-connected component(s) [16@r2-5,c0-3]
Output (12x13):
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
3 3 3 3 0 0 2 8 8 2 0 0 0
3 8 8 3 0 0 2 8 8 2 0 0 0
3 8 8 3 0 0 2 8 8 2 0 0 0
3 3 3 3 0 0 2 8 8 2 0 0 0
0 0 0 0 0 0 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0
Inventory: color 0: 84 cells, 1 four-connected component(s) [84@r0-11,c0-12]; color 1: 20 cells, 1 four-connected component(s) [20@r8-11,c2-9]; color 2: 16 cells, 1 four-connected component(s) [16@r1-6,c6-9]; color 3: 12 cells, 1 four-connected component(s) [12@r2-5,c0-3]; color 8: 24 cells, 3 four-connected component(s) [8@r2-5,c7-8; 4@r3-4,c1-2; 12@r9-10,c3-8]

## Test
Input (14x13):
0 1 1 1 1 1 0 0 0 0 0 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 1 1 1 1 1 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0 0
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 2 2 2 2 2 2 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
0 0 0 0 0 0 0 0 0 3 3 3 3
Inventory: color 0: 89 cells, 1 four-connected component(s) [89@r0-13,c0-12]; color 1: 29 cells, 2 four-connected component(s) [20@r0-3,c1-5; 9@r1-3,c8-10]; color 2: 36 cells, 1 four-connected component(s) [36@r5-10,c2-7]; color 3: 28 cells, 1 four-connected component(s) [28@r7-13,c9-12]

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,1,1,1,1,1,0,0,0,0,0,0,0],[0,1,8,8,8,1,0,0,1,1,1,0,0],[0,1,8,8,8,1,0,0,1,8,1,0,0],[0,1,1,1,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,2,2,2,2,2,2,0,0,0,0,0],[0,0,2,8,8,8,8,2,0,0,0,0,0],[0,0,2,8,8,8,8,2,0,3,3,3,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,2,8,8,8,8,2,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,8,8,3],[0,0,0,0,0,0,0,0,0,3,3,3,3]]</answer>


Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
First identify a precise rule that explains every demonstration pair, then check that rule against each pair before using it. Account for changes in grid dimensions, cell positions, colors, and cells that stay unchanged. Use all examples to distinguish plausible rules; do not assume the test output has the same dimensions as its input or guess by visual similarity.
Mechanical inventories follow each grid: color counts and four-connected component sizes/bounds (coordinates start at 0). Use them only as aids, not as assumptions about which cells form a semantic object; verify the proposed rule on the exact grids.

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
Inventory: color 0: 160 cells, 7 four-connected component(s) [45@r0-10,c0-4; 26@r0-5,c6-10; 20@r0-5,c12-15; 9@r5-7,c4-6; 3@r5-7,c15-15; 52@r7-12,c6-15; 5@r12-12,c0-4]; color 5: 48 cells, 1 four-connected component(s) [48@r0-12,c0-15]
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
Inventory: color 0: 148 cells, 5 four-connected component(s) [45@r0-10,c0-4; 26@r0-5,c6-10; 20@r0-5,c12-15; 52@r7-12,c6-15; 5@r12-12,c0-4]; color 4: 12 cells, 2 four-connected component(s) [9@r5-7,c4-6; 3@r5-7,c15-15]; color 5: 48 cells, 1 four-connected component(s) [48@r0-12,c0-15]

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
Inventory: color 0: 160 cells, 10 four-connected component(s) (largest component sizes: 47, 36, 20, 19, 14); color 5: 68 cells, 1 four-connected component(s) [68@r0-11,c0-18]
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
Inventory: color 0: 142 cells, 6 four-connected component(s) [20@r0-1,c0-12; 6@r0-1,c14-16; 47@r3-11,c0-5; 36@r3-11,c7-12; 14@r3-6,c14-18; 19@r8-11,c14-18]; color 4: 18 cells, 4 four-connected component(s) [3@r1-3,c18-18; 1@r2-2,c0-0; 10@r2-6,c6-7; 4@r6-7,c12-13]; color 5: 68 cells, 1 four-connected component(s) [68@r0-11,c0-18]

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
Inventory: color 0: 175 cells, 11 four-connected component(s) (largest component sizes: 38, 34, 19, 18, 15); color 5: 80 cells, 1 four-connected component(s) [80@r0-14,c0-16]
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
Inventory: color 0: 156 cells, 8 four-connected component(s) [10@r0-1,c0-4; 18@r0-2,c6-16; 8@r3-4,c0-4; 38@r3-10,c6-11; 34@r4-14,c13-16; 19@r6-10,c0-4; 15@r12-14,c0-4; 14@r12-14,c6-11]; color 4: 19 cells, 3 four-connected component(s) [9@r2-4,c12-14; 6@r5-7,c4-5; 4@r11-12,c11-12]; color 5: 80 cells, 1 four-connected component(s) [80@r0-14,c0-16]

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
Inventory: color 0: 204 cells, 12 four-connected component(s) (largest component sizes: 48, 30, 30, 26, 23); color 5: 84 cells, 1 four-connected component(s) [84@r0-15,c0-17]

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],[5,5,5,0,0,0,0,5,4,4,4,4,4,4,5,4,4,4],[0,0,0,0,0,0,0,5,4,4,4,4,4,4,5,4,4,4],[0,0,0,0,0,0,0,5,4,4,4,4,4,4,5,4,4,4],[0,0,0,0,0,0,0,5,4,4,4,4,4,5,5,5,5,4],[0,0,0,0,0,5,5,5,5,5,4,4,4,5,4,4,5,4],[5,5,5,5,5,5,4,4,4,5,5,5,5,5,4,4,5,5],[0,5,0,0,0,5,4,4,4,5,0,0,0,5,4,4,5,0],[0,5,0,0,0,5,5,5,5,5,0,0,0,5,5,5,5,0],[0,5,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,4,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
First identify a precise rule that explains every demonstration pair, then check that rule against each pair before using it. Account for changes in grid dimensions, cell positions, colors, and cells that stay unchanged. Use all examples to distinguish plausible rules; do not assume the test output has the same dimensions as its input or guess by visual similarity.
Mechanical inventories follow each grid: color counts and four-connected component sizes/bounds (coordinates start at 0). Use them only as aids, not as assumptions about which cells form a semantic object; verify the proposed rule on the exact grids.

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
Inventory: color 0: 160 cells, 7 four-connected component(s) [45@r0-10,c0-4; 26@r0-5,c6-10; 20@r0-5,c12-15; 9@r5-7,c4-6; 3@r5-7,c15-15; 52@r7-12,c6-15; 5@r12-12,c0-4]; color 5: 48 cells, 1 four-connected component(s) [48@r0-12,c0-15]
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
Inventory: color 0: 148 cells, 5 four-connected component(s) [45@r0-10,c0-4; 26@r0-5,c6-10; 20@r0-5,c12-15; 52@r7-12,c6-15; 5@r12-12,c0-4]; color 4: 12 cells, 2 four-connected component(s) [9@r5-7,c4-6; 3@r5-7,c15-15]; color 5: 48 cells, 1 four-connected component(s) [48@r0-12,c0-15]

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
Inventory: color 0: 160 cells, 10 four-connected component(s) (largest component sizes: 47, 36, 20, 19, 14); color 5: 68 cells, 1 four-connected component(s) [68@r0-11,c0-18]
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
Inventory: color 0: 142 cells, 6 four-connected component(s) [20@r0-1,c0-12; 6@r0-1,c14-16; 47@r3-11,c0-5; 36@r3-11,c7-12; 14@r3-6,c14-18; 19@r8-11,c14-18]; color 4: 18 cells, 4 four-connected component(s) [3@r1-3,c18-18; 1@r2-2,c0-0; 10@r2-6,c6-7; 4@r6-7,c12-13]; color 5: 68 cells, 1 four-connected component(s) [68@r0-11,c0-18]

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
Inventory: color 0: 175 cells, 11 four-connected component(s) (largest component sizes: 38, 34, 19, 18, 15); color 5: 80 cells, 1 four-connected component(s) [80@r0-14,c0-16]
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
Inventory: color 0: 156 cells, 8 four-connected component(s) [10@r0-1,c0-4; 18@r0-2,c6-16; 8@r3-4,c0-4; 38@r3-10,c6-11; 34@r4-14,c13-16; 19@r6-10,c0-4; 15@r12-14,c0-4; 14@r12-14,c6-11]; color 4: 19 cells, 3 four-connected component(s) [9@r2-4,c12-14; 6@r5-7,c4-5; 4@r11-12,c11-12]; color 5: 80 cells, 1 four-connected component(s) [80@r0-14,c0-16]

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
Inventory: color 0: 204 cells, 12 four-connected component(s) (largest component sizes: 48, 30, 30, 26, 23); color 5: 84 cells, 1 four-connected component(s) [84@r0-15,c0-17]

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The rule is to recolor enclosed zero pockets to 4, treating the grid edge as a wall where it completes a pocket’s boundary; open zero regions remain unchanged. This matches the filled pockets in all three examples, including the single edge pocket in Example 2. In the test, the pockets have sizes 2, 26, 6, 6, and 1.

<answer>[[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],[5,5,5,0,0,0,0,5,4,4,4,4,4,4,5,0,0,0],[0,0,0,0,0,0,0,5,4,4,4,4,4,4,5,0,0,0],[0,0,0,0,0,0,0,5,4,4,4,4,4,4,5,0,0,0],[0,0,0,0,0,0,0,5,4,4,4,4,4,5,5,5,5,0],[0,0,0,0,0,5,5,5,5,5,4,4,4,5,4,4,5,0],[5,5,5,5,5,5,4,4,4,5,5,5,5,5,4,4,5,5],[0,5,0,0,0,5,4,4,4,5,0,0,0,5,4,4,5,0],[0,5,0,0,0,5,5,5,5,5,0,0,0,5,5,5,5,0],[0,5,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,4,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0],[5,5,5,0,0,0,0,5,0,0,0,0,0,0,0,0,0,0]]</answer>


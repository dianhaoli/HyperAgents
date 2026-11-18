Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (5x5):
3 2 0 2 2
3 3 0 2 2
0 0 0 0 0
3 2 0 3 2
3 3 0 3 3
Output (5x5):
3 3 0 3 2
3 3 0 3 3
0 0 0 0 0
3 3 0 3 3
3 3 0 3 3
Change audit (input value -> output value; coordinates are zero-based): 6 changed cell(s): 2->3: 6 cell(s) at (0,1), (0,3), (1,3), (1,4), (3,1), (3,4)

## Example 2
Input (5x5):
1 1 0 1 1
1 8 0 1 8
0 0 0 5 0
5 1 5 8 5
5 5 0 8 8
Output (5x5):
1 1 0 1 1
1 1 0 1 1
0 0 0 0 0
1 1 0 1 1
1 1 0 1 8
Change audit (input value -> output value; coordinates are zero-based): 10 changed cell(s): 5->0: 2 cell(s) at (2,3), (3,2); 5->1: 4 cell(s) at (3,0), (3,4), (4,0), (4,1); 8->1: 4 cell(s) at (1,1), (1,4), (3,3), (4,3)

## Example 3
Input (11x11):
3 3 4 0 3 3 4 0 4 4 4
3 3 4 0 3 3 4 0 4 4 4
4 3 3 0 4 3 3 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
3 3 4 0 3 3 4 0 4 4 4
3 3 4 0 3 3 4 5 4 4 4
4 3 3 0 5 3 3 0 4 4 4
0 0 0 0 5 5 0 0 0 0 0
4 4 4 5 5 5 4 0 3 3 4
4 5 5 5 3 3 4 0 3 3 4
4 4 5 0 4 3 3 0 4 3 3
Output (11x11):
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 4 3 3
0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 4 3 3
0 0 0 0 0 0 0 0 0 0 0
3 3 4 0 3 3 3 0 3 3 3
3 3 4 0 3 3 3 0 3 3 3
4 3 3 0 3 3 3 0 3 3 3
Change audit (input value -> output value; coordinates are zero-based): 44 changed cell(s): 4->3: 33 cell(s) at (0,2), (0,6), (0,8), (0,9), (1,2), (1,6), (1,8), (1,9), (2,0), (2,4), (2,9), (2,10), (4,2), (4,6), (4,8), (4,9), (5,2), (5,6), (5,8), (5,9), (6,0), (6,9), (6,10), (8,0), (8,1), (8,6), (8,10), (9,0), (9,6), (9,10), (10,1), (10,4), (10,8); 5->0: 5 cell(s) at (5,7), (7,4), (7,5), (8,3), (9,3); 5->3: 5 cell(s) at (6,4), (8,4), (8,5), (9,1), (10,2); 5->4: 1 cell(s) at (9,2)

## Example 4
Input (11x11):
4 4 2 0 4 4 2 0 2 2 2
2 4 2 0 2 4 2 0 2 2 2
4 4 4 0 4 4 4 5 2 2 5
0 0 0 0 0 0 0 0 0 0 5
2 2 2 0 4 4 2 5 2 2 2
2 2 2 0 2 5 2 5 5 2 2
2 2 5 0 4 5 5 0 2 5 2
0 0 5 0 0 0 0 0 0 0 0
4 5 5 5 4 4 2 5 4 4 2
5 5 5 0 2 5 2 0 2 4 2
4 5 4 0 4 4 4 0 4 4 4
Output (11x11):
4 4 4 0 4 4 4 0 4 4 2
4 4 4 0 4 4 4 0 2 4 2
4 4 4 0 4 4 4 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
4 4 2 0 4 4 4 0 4 4 2
2 4 2 0 4 4 4 0 2 4 2
4 4 4 0 4 4 4 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 4 4 4 0 4 4 4
4 4 4 0 4 4 4 0 4 4 4
4 4 4 0 4 4 4 0 4 4 4
Change audit (input value -> output value; coordinates are zero-based): 51 changed cell(s): 2->4: 30 cell(s); per-row counts row 0: 4, row 1: 5, row 2: 2, row 4: 5, row 5: 4, row 6: 4, row 8: 2, row 9: 4; 5->0: 7 cell(s); per-row counts row 2: 1, row 3: 1, row 4: 1, row 5: 1, row 7: 1, row 8: 2; 5->2: 1 cell(s); per-row counts row 5: 1; 5->4: 13 cell(s); per-row counts row 2: 1, row 5: 1, row 6: 4, row 8: 2, row 9: 4, row 10: 1

## Test
Input (19x19):
1 1 1 2 0 1 1 1 2 0 1 1 1 2 0 2 5 2 2
1 2 2 1 0 1 2 2 1 0 1 2 2 1 0 5 5 2 2
2 1 1 1 0 2 1 1 1 0 2 1 1 1 0 5 2 2 2
1 2 1 1 0 1 2 1 1 0 1 2 1 1 0 5 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0
1 1 1 2 0 2 2 2 2 0 2 2 2 5 5 5 1 1 2
1 2 2 1 5 5 5 2 2 0 2 2 5 5 0 1 2 2 1
2 1 1 5 5 5 2 2 2 0 2 5 5 2 0 2 5 5 1
1 2 5 5 0 2 2 2 2 5 5 5 5 5 5 5 2 5 5
0 0 5 0 0 0 0 0 5 5 0 5 0 0 0 0 0 5 5
2 2 5 5 0 1 1 5 5 5 1 5 1 2 0 1 1 5 2
5 5 5 5 0 1 2 2 1 5 5 5 5 1 0 1 5 5 1
2 2 2 2 0 2 1 1 1 5 5 1 5 5 0 5 5 1 1
2 2 2 2 0 1 2 1 1 5 1 5 5 5 5 5 2 1 1
0 0 0 0 0 0 0 0 0 5 5 5 0 5 5 0 0 0 0
1 1 1 2 0 2 2 2 2 5 1 1 1 5 5 5 1 1 2
1 2 2 1 0 2 2 2 5 0 5 2 5 5 5 5 2 2 1
2 1 1 1 0 2 2 5 2 0 5 5 1 1 5 2 1 1 1
1 2 1 1 0 2 2 2 2 0 1 5 5 5 5 1 2 1 1

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and explain every listed changed cell using one concrete rule that works for every pair. Also check the unchanged cells: do not alter cells merely to complete a shape or extend a pattern beyond the bounds supported by the examples. If dimensions change, account for that explicitly. Reject or revise any rule that cannot explain all demonstrated edits and non-edits. Then apply the verified rule to the test and check its dimensions and bounds.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The zero rows and columns are structural separators, so the grids divide into equal-sized fields. The recurring fields establish a primary color and a secondary-color stencil. Normalize fields to the primary color; retain the stencil only where the secondary-color structure is supported at the outer edge. A 5 marks an overwritten cell: restore it to the separator zero or to the value specified by the field. This accounts for the recolorings in the demonstrations, including the 5s on separators and the intact lower-right stencil in Example 4. In the test, the repeated 4×4 motif gives the 2-stencil; I keep it only in supported outer-edge fields and do not extend it into interior fields.

The output remains 19×19. All separator rows and columns are zero.

<answer>[[1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 2], [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 2, 2, 1], [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, 1, 1, 1], [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 2, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 2], [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 2, 2, 1], [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, 1, 1, 1], [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 2, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 2, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 2, 2, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1], [2, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 2, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 2, 0, 1, 1, 1, 2, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 2, 2, 1, 0, 1, 2, 2, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1], [2, 1, 1, 1, 0, 2, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1], [1, 2, 1, 1, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (5x5):
3 2 0 2 2
3 3 0 2 2
0 0 0 0 0
3 2 0 3 2
3 3 0 3 3
Output (5x5):
3 3 0 3 2
3 3 0 3 3
0 0 0 0 0
3 3 0 3 3
3 3 0 3 3
Change audit (input value -> output value; coordinates are zero-based): 6 changed cell(s): 2->3: 6 cell(s) at (0,1), (0,3), (1,3), (1,4), (3,1), (3,4)

## Example 2
Input (5x5):
1 1 0 1 1
1 8 0 1 8
0 0 0 5 0
5 1 5 8 5
5 5 0 8 8
Output (5x5):
1 1 0 1 1
1 1 0 1 1
0 0 0 0 0
1 1 0 1 1
1 1 0 1 8
Change audit (input value -> output value; coordinates are zero-based): 10 changed cell(s): 5->0: 2 cell(s) at (2,3), (3,2); 5->1: 4 cell(s) at (3,0), (3,4), (4,0), (4,1); 8->1: 4 cell(s) at (1,1), (1,4), (3,3), (4,3)

## Example 3
Input (11x11):
3 3 4 0 3 3 4 0 4 4 4
3 3 4 0 3 3 4 0 4 4 4
4 3 3 0 4 3 3 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
3 3 4 0 3 3 4 0 4 4 4
3 3 4 0 3 3 4 5 4 4 4
4 3 3 0 5 3 3 0 4 4 4
0 0 0 0 5 5 0 0 0 0 0
4 4 4 5 5 5 4 0 3 3 4
4 5 5 5 3 3 4 0 3 3 4
4 4 5 0 4 3 3 0 4 3 3
Output (11x11):
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 4 3 3
0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 3 3 4
3 3 3 0 3 3 3 0 4 3 3
0 0 0 0 0 0 0 0 0 0 0
3 3 4 0 3 3 3 0 3 3 3
3 3 4 0 3 3 3 0 3 3 3
4 3 3 0 3 3 3 0 3 3 3
Change audit (input value -> output value; coordinates are zero-based): 44 changed cell(s): 4->3: 33 cell(s) at (0,2), (0,6), (0,8), (0,9), (1,2), (1,6), (1,8), (1,9), (2,0), (2,4), (2,9), (2,10), (4,2), (4,6), (4,8), (4,9), (5,2), (5,6), (5,8), (5,9), (6,0), (6,9), (6,10), (8,0), (8,1), (8,6), (8,10), (9,0), (9,6), (9,10), (10,1), (10,4), (10,8); 5->0: 5 cell(s) at (5,7), (7,4), (7,5), (8,3), (9,3); 5->3: 5 cell(s) at (6,4), (8,4), (8,5), (9,1), (10,2); 5->4: 1 cell(s) at (9,2)

## Example 4
Input (11x11):
4 4 2 0 4 4 2 0 2 2 2
2 4 2 0 2 4 2 0 2 2 2
4 4 4 0 4 4 4 5 2 2 5
0 0 0 0 0 0 0 0 0 0 5
2 2 2 0 4 4 2 5 2 2 2
2 2 2 0 2 5 2 5 5 2 2
2 2 5 0 4 5 5 0 2 5 2
0 0 5 0 0 0 0 0 0 0 0
4 5 5 5 4 4 2 5 4 4 2
5 5 5 0 2 5 2 0 2 4 2
4 5 4 0 4 4 4 0 4 4 4
Output (11x11):
4 4 4 0 4 4 4 0 4 4 2
4 4 4 0 4 4 4 0 2 4 2
4 4 4 0 4 4 4 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
4 4 2 0 4 4 4 0 4 4 2
2 4 2 0 4 4 4 0 2 4 2
4 4 4 0 4 4 4 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 4 4 4 0 4 4 4
4 4 4 0 4 4 4 0 4 4 4
4 4 4 0 4 4 4 0 4 4 4
Change audit (input value -> output value; coordinates are zero-based): 51 changed cell(s): 2->4: 30 cell(s); per-row counts row 0: 4, row 1: 5, row 2: 2, row 4: 5, row 5: 4, row 6: 4, row 8: 2, row 9: 4; 5->0: 7 cell(s); per-row counts row 2: 1, row 3: 1, row 4: 1, row 5: 1, row 7: 1, row 8: 2; 5->2: 1 cell(s); per-row counts row 5: 1; 5->4: 13 cell(s); per-row counts row 2: 1, row 5: 1, row 6: 4, row 8: 2, row 9: 4, row 10: 1

## Test
Input (19x19):
1 1 1 2 0 1 1 1 2 0 1 1 1 2 0 2 5 2 2
1 2 2 1 0 1 2 2 1 0 1 2 2 1 0 5 5 2 2
2 1 1 1 0 2 1 1 1 0 2 1 1 1 0 5 2 2 2
1 2 1 1 0 1 2 1 1 0 1 2 1 1 0 5 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 0 0 0
1 1 1 2 0 2 2 2 2 0 2 2 2 5 5 5 1 1 2
1 2 2 1 5 5 5 2 2 0 2 2 5 5 0 1 2 2 1
2 1 1 5 5 5 2 2 2 0 2 5 5 2 0 2 5 5 1
1 2 5 5 0 2 2 2 2 5 5 5 5 5 5 5 2 5 5
0 0 5 0 0 0 0 0 5 5 0 5 0 0 0 0 0 5 5
2 2 5 5 0 1 1 5 5 5 1 5 1 2 0 1 1 5 2
5 5 5 5 0 1 2 2 1 5 5 5 5 1 0 1 5 5 1
2 2 2 2 0 2 1 1 1 5 5 1 5 5 0 5 5 1 1
2 2 2 2 0 1 2 1 1 5 1 5 5 5 5 5 2 1 1
0 0 0 0 0 0 0 0 0 5 5 5 0 5 5 0 0 0 0
1 1 1 2 0 2 2 2 2 5 1 1 1 5 5 5 1 1 2
1 2 2 1 0 2 2 2 5 0 5 2 5 5 5 5 2 2 1
2 1 1 1 0 2 2 5 2 0 5 5 1 1 5 2 1 1 1
1 2 1 1 0 2 2 2 2 0 1 5 5 5 5 1 2 1 1

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and explain every listed changed cell using one concrete rule that works for every pair. Also check the unchanged cells: do not alter cells merely to complete a shape or extend a pattern beyond the bounds supported by the examples. If dimensions change, account for that explicitly. Reject or revise any rule that cannot explain all demonstrated edits and non-edits. Then apply the verified rule to the test and check its dimensions and bounds.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Make this a fresh, independent solve: do not assume or reuse any earlier proposed rule or grid. Infer a concrete rule from the training pairs, check that it reproduces every demonstrated output, then apply it to the test input. Verify the dimensions and changed cells against that rule before returning the grid in <answer> tags, with nothing else inside the tags.

Output: The zero rails divide the grids into equal-sized tiles. In the 5-marked examples, the repeated mixed-color tiles provide a stencil: those tiles are normalized to their background color, while tiles dominated by the other color are redrawn with the corresponding minority-color motif. 5s on the rails become 0; inside tiles they are repaired to the tile’s background or motif. Example 1 has no 5-marked stencil, so its nonzero minority color is normalized to the majority color. These rules account for the listed changes and the unchanged cells; the test remains 19×19.

For the test, the repeated 4×4 motif has 2s at local positions (0,3), (1,1), (1,2), (2,0), and (3,1). The 2-dominant tiles are redrawn with that motif; the other tiles become 1, and the separator rails remain 0.

<answer>[[1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,2],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,2,2,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,2,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,2,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,0,1,1,1,2,0,1,1,1,2,0,1,1,1,1],[1,1,1,1,0,1,2,2,1,0,1,2,2,1,0,1,1,1,1],[1,1,1,1,0,2,1,1,1,0,2,1,1,1,0,1,1,1,1],[1,1,1,1,0,1,2,1,1,0,1,2,1,1,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,2,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1],[1,2,2,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1],[2,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1],[1,2,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[1,1,1,1,0,1,1,1,2,0,1,1,1,1,0,1,1,1,1],[1,1,1,1,0,1,2,2,1,0,1,1,1,1,0,1,1,1,1],[1,1,1,1,0,2,1,1,1,0,1,1,1,1,0,1,1,1,1],[1,1,1,1,0,1,2,1,1,0,1,1,1,1,0,1,1,1,1]]</answer>


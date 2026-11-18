Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Use each training change audit as evidence: explain every listed edit and why other cells stay unchanged. Do not infer a rule from changed cells alone; check that the same rule reproduces every full example.

## Example 1
Input (6x6):
0 0 0 0 0 2
0 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 0
2 0 0 0 0 0
0 0 0 0 0 0
Output (6x6):
4 4 4 4 4 2
4 1 1 1 1 1
4 4 4 4 4 4
1 1 1 1 1 4
2 4 4 4 4 4
0 0 0 0 0 0
Change audit (18 unchanged): 0->4 at [0:0-4, 1:0, 2:0-5, 3:5, 4:1-5].

## Example 2
Input (5x5):
0 0 0 1 2
0 0 0 1 0
0 1 0 1 0
0 1 0 0 0
2 1 0 0 0
Output (5x5):
0 0 0 1 2
4 4 4 1 4
4 1 4 1 4
4 1 4 4 4
2 1 0 0 0
Change audit (14 unchanged): 0->4 at [1:0-2, 1:4, 2:0, 2:2, 2:4, 3:0, 3:2-4].

## Example 3
Input (6x6):
2 0 0 0 0 0
1 1 1 1 0 0
0 0 0 0 0 0
0 0 0 1 1 1
0 0 0 0 0 2
0 0 0 0 0 0
Output (6x6):
2 4 4 4 4 0
1 1 1 1 4 0
0 0 4 4 4 0
0 0 4 1 1 1
0 0 4 4 4 2
0 0 0 0 0 0
Change audit (24 unchanged): 0->4 at [0:1-4, 1:4, 2:2-4, 3:2, 4:2-4].

## Example 4
Input (10x10):
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 1 0 1 1 0 1 0 1 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
Output (10x10):
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 4
0 0 0 1 1 0 0 0 1 4
4 4 4 1 1 4 4 4 1 4
4 1 4 1 1 4 1 4 1 4
4 1 4 4 4 4 1 4 4 4
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
Change audit (75 unchanged): 0->4 at [1:9, 2:9, 3:0-2, 3:5-7, 3:9, 4:0, 4:2, 4:5, 4:7, 4:9, 5:0, 5:2-5, 5:7-9, 6:0, 7:0, 8:0].

## Example 5
Input (5x5):
2 1 1 1 2
0 1 0 1 0
0 1 0 1 0
0 1 0 1 0
0 0 0 0 0
Output (5x5):
2 1 1 1 2
4 1 0 1 4
4 1 0 1 4
4 1 0 1 4
4 4 4 4 4
Change audit (14 unchanged): 0->4 at [1:0, 1:4, 2:0, 2:4, 3:0, 3:4, 4:0-4].

## Test
Input (10x10):
2 1 0 0 0 1 0 0 0 2
0 1 0 0 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 0 0 1 0 0 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The 2s are route endpoints, 1s block movement, and movement is orthogonal through 0s. The changed cells are exactly the zeros lying on at least one shortest route between the two 2s; other zeros would require a detour or are dead ends.

- Example 1: The audited cells form the shortest corridor through rows 0–4; the bottom row is a detour.
- Example 2: The audited cells form the shortest corridor through rows 1–3. The other zeros are branches off that corridor.
- Example 3: The audited cells form the shortest corridor between the endpoints; the side pockets are not on a shortest route.
- Example 4: Each audited segment lies on a shortest route through the right, middle, and left corridors; the other open cells require detours.
- Example 5: The shortest route goes around the vertical barriers along the sides and bottom. The central pocket is a dead end.

For the test, the shortest corridor uses the top opening on the right and the row-1 opening on the left; lower side branches are not on a shortest route.

<answer>[[2,1,0,0,0,1,4,4,4,2],[4,1,4,4,4,1,4,1,0,0],[4,1,4,1,4,1,4,1,0,0],[4,1,4,1,4,1,4,1,0,0],[4,1,4,1,4,1,4,1,0,0],[4,4,4,1,4,4,4,1,0,0],[0,0,0,1,0,1,4,1,0,0],[0,0,0,1,0,1,4,1,0,0],[0,0,0,1,0,1,4,1,0,0],[0,0,0,1,0,1,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.
Use each training change audit as evidence: explain every listed edit and why other cells stay unchanged. Do not infer a rule from changed cells alone; check that the same rule reproduces every full example.

## Example 1
Input (6x6):
0 0 0 0 0 2
0 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 0
2 0 0 0 0 0
0 0 0 0 0 0
Output (6x6):
4 4 4 4 4 2
4 1 1 1 1 1
4 4 4 4 4 4
1 1 1 1 1 4
2 4 4 4 4 4
0 0 0 0 0 0
Change audit (18 unchanged): 0->4 at [0:0-4, 1:0, 2:0-5, 3:5, 4:1-5].

## Example 2
Input (5x5):
0 0 0 1 2
0 0 0 1 0
0 1 0 1 0
0 1 0 0 0
2 1 0 0 0
Output (5x5):
0 0 0 1 2
4 4 4 1 4
4 1 4 1 4
4 1 4 4 4
2 1 0 0 0
Change audit (14 unchanged): 0->4 at [1:0-2, 1:4, 2:0, 2:2, 2:4, 3:0, 3:2-4].

## Example 3
Input (6x6):
2 0 0 0 0 0
1 1 1 1 0 0
0 0 0 0 0 0
0 0 0 1 1 1
0 0 0 0 0 2
0 0 0 0 0 0
Output (6x6):
2 4 4 4 4 0
1 1 1 1 4 0
0 0 4 4 4 0
0 0 4 1 1 1
0 0 4 4 4 2
0 0 0 0 0 0
Change audit (24 unchanged): 0->4 at [0:1-4, 1:4, 2:2-4, 3:2, 4:2-4].

## Example 4
Input (10x10):
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 0 0 1 1 0 0 0 1 0
0 1 0 1 1 0 1 0 1 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
0 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
Output (10x10):
0 0 0 1 1 0 0 0 1 2
0 0 0 1 1 0 0 0 1 4
0 0 0 1 1 0 0 0 1 4
4 4 4 1 1 4 4 4 1 4
4 1 4 1 1 4 1 4 1 4
4 1 4 4 4 4 1 4 4 4
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
4 1 0 0 0 0 1 0 0 0
2 1 0 0 0 0 1 0 0 0
Change audit (75 unchanged): 0->4 at [1:9, 2:9, 3:0-2, 3:5-7, 3:9, 4:0, 4:2, 4:5, 4:7, 4:9, 5:0, 5:2-5, 5:7-9, 6:0, 7:0, 8:0].

## Example 5
Input (5x5):
2 1 1 1 2
0 1 0 1 0
0 1 0 1 0
0 1 0 1 0
0 0 0 0 0
Output (5x5):
2 1 1 1 2
4 1 0 1 4
4 1 0 1 4
4 1 0 1 4
4 4 4 4 4
Change audit (14 unchanged): 0->4 at [1:0, 1:4, 2:0, 2:4, 3:0, 3:4, 4:0-4].

## Test
Input (10x10):
2 1 0 0 0 1 0 0 0 2
0 1 0 0 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 1 0 1 0 1 0 1 0 0
0 0 0 1 0 0 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 1 0 1 0 0 0 0

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Solve this independently, without relying on or guessing any prior answer. First identify the objects, colors, and spatial relationships that change in the demonstrations. State a concrete rule that reproduces every training output, then apply it from scratch to the test grid. Check the dimensions and every changed region before returning the grid in <answer> tags, with nothing else inside the tags.

Output: I interpret the 1s as walls and the 2s as endpoints that identify which side of the wall pattern is to be colored. Zeros on that side become 4; zeros in the other region, and all 1s and 2s, stay unchanged.

This accounts for the audits: in Example 1, the selected side is exactly the listed zeros in rows 0–4; row 5 is on the other side. In Example 2, it is the zeros in rows 1–3, while the top and bottom rows are outside the selected region. In Example 3, the staggered horizontal walls select the audited zeros around the central band; the remaining zeros lie on the other side. In Example 4, the selected open regions are exactly the audited zeros around the wall ends; the lower spaces behind the long vertical walls remain unchanged. In Example 5, the exterior around the U-shaped walls is selected, while the central pocket in rows 1–3 stays 0. In each example, the listed 1s and 2s remain as walls and endpoints.

In the test, the 2s lie at opposite ends of the top edge, so the selected side is below that edge. The vertical 1 segments leave openings between their ends, so they do not enclose a separate zero pocket. Thus the zeros below the top row become 4, while the top row and all nonzero cells stay unchanged.

<answer>[[2,1,0,0,0,1,0,0,0,2],[4,1,4,4,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,1,4,1,4,1,4,1,4,4],[4,4,4,1,4,4,4,1,4,4],[4,4,4,1,4,1,4,1,4,4],[4,4,4,1,4,1,4,1,4,4],[4,4,4,1,4,1,4,1,4,4],[4,4,4,1,4,1,4,4,4,4]]</answer>


Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (16x20):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 1 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 2 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 2 0 2 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 1 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 2 0 2 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 4 2 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 2 2 2 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 4 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (9x6):
8 8 8 8 8 8
8 2 8 8 8 8
2 1 2 8 8 8
2 8 8 8 8 8
8 8 8 8 8 8
8 8 8 8 8 8
8 8 2 8 2 8
8 8 8 4 2 8
8 8 2 2 2 8

## Example 2
Input (18x22):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 7 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 2 4 2 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 2 2 0 0 0 1 1 1 1 1 1 1 1 3 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 2 2 2 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 2 8 2 0 0 0 0 0 0 1 1 1 1 4 1 1 1 1 1 1 0
0 2 0 2 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 8 1 1 1 1 7 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (12x11):
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 2 3 2 1
1 1 1 1 1 1 1 1 1 2 1
1 1 1 1 2 1 1 1 1 1 1
1 1 1 2 4 2 1 1 1 1 1
1 1 1 1 2 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 1 1 2 1 1 1
1 2 8 2 1 1 2 7 2 1 1
1 2 1 2 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 1 1 1

## Example 3
Input (16x18):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 3 4 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 3 3 1 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 8 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 2 2 0 0 0 0 2 1 2 0 0 0 0 0 0
0 0 0 2 8 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (6x12):
3 3 3 3 3 2 2 2 3 3 3 3
3 3 3 3 3 3 4 3 3 3 3 3
3 3 3 3 3 2 2 2 3 3 3 3
3 2 1 2 3 3 3 3 2 2 3 3
3 3 2 3 3 3 3 3 2 8 3 3
3 3 3 3 3 3 3 3 3 3 2 3

## Test
Input (26x24):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 7 2 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 2 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 1 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 2 2 0 0 0
0 4 4 4 1 4 4 4 4 4 4 4 4 7 4 4 0 0 0 0 8 2 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 2 2 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 6 4 4 4 4 4 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 4 3 4 4 4 4 4 4 4 4 4 4 4 8 4 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

Solve the task by inferring one precise transformation from the demonstrations. Before deciding, inspect the grids systematically: compare dimensions, colors, connected objects and their bounding boxes; look for repeated motifs, symmetry, reflection, rotation, completion of partial patterns, and changes in object size or position. Do not assume the output is the input with only a small local edit. Derive the rule from the examples, then check that it reproduces every demonstrated output exactly. Apply that same rule to the test. Preserve the full grid and its dimensions unless the examples show a dimension change. Give a brief explanation outside the answer tags, then end with the complete output grid inside <answer></answer> tags as a JSON list of rows, for example: <answer>[[0, 1, 2], [3, 4, 5]]</answer>. Put nothing else inside the tags.

Output: The large color-4 rectangle is the output canvas. Each surrounding pattern of 2s is placed around the matching colored marker inside it.

<answer>[[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],[4,4,4,2,4,4,4,4,4,4,4,4,4,4,4],[4,4,2,1,2,4,4,4,4,4,4,2,7,2,4],[4,4,4,2,4,4,4,4,4,4,4,2,2,4,4],[4,4,4,4,4,4,4,4,2,2,4,4,4,4,4],[4,4,4,4,4,4,4,4,2,6,4,4,4,4,4],[4,2,2,4,4,4,4,4,4,4,2,4,2,2,4],[2,3,2,4,4,4,4,4,4,4,4,4,4,4,2],[2,2,4,4,4,4,4,4,4,4,4,4,4,2,2]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (16x20):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 1 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2 0 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 2 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 2 0 2 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 1 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 2 0 2 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 4 2 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 2 2 2 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 4 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (9x6):
8 8 8 8 8 8
8 2 8 8 8 8
2 1 2 8 8 8
2 8 8 8 8 8
8 8 8 8 8 8
8 8 8 8 8 8
8 8 2 8 2 8
8 8 8 4 2 8
8 8 2 2 2 8

## Example 2
Input (18x22):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 7 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 2 4 2 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 2 2 0 0 0 1 1 1 1 1 1 1 1 3 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 2 2 2 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 2 8 2 0 0 0 0 0 0 1 1 1 1 4 1 1 1 1 1 1 0
0 2 0 2 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 8 1 1 1 1 7 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (12x11):
1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 2 3 2 1
1 1 1 1 1 1 1 1 1 2 1
1 1 1 1 2 1 1 1 1 1 1
1 1 1 2 4 2 1 1 1 1 1
1 1 1 1 2 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 1 1 1 2 1 1 1
1 2 8 2 1 1 2 7 2 1 1
1 2 1 2 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 1 1 1

## Example 3
Input (16x18):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 3 4 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 3 3 1 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 8 3 3 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0
0 0 0 2 2 0 0 0 0 2 1 2 0 0 0 0 0 0
0 0 0 2 8 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (6x12):
3 3 3 3 3 2 2 2 3 3 3 3
3 3 3 3 3 3 4 3 3 3 3 3
3 3 3 3 3 2 2 2 3 3 3 3
3 2 1 2 3 3 3 3 2 2 3 3
3 3 2 3 3 3 3 3 2 8 3 3
3 3 3 3 3 3 3 3 3 3 2 3

## Test
Input (26x24):
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 7 2 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0 0 2 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 1 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 2 2 0 0 0
0 4 4 4 1 4 4 4 4 4 4 4 4 7 4 4 0 0 0 0 8 2 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 2 2 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 6 4 4 4 4 4 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 4 3 4 4 4 4 4 4 4 4 4 4 4 8 4 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

A previous attempt proposed this solution (it may be wrong):
The large color-4 rectangle is the output canvas. Each surrounding pattern of 2s is placed around the matching colored marker inside it.

<answer>[[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],[4,4,4,2,4,4,4,4,4,4,4,4,4,4,4],[4,4,2,1,2,4,4,4,4,4,4,2,7,2,4],[4,4,4,2,4,4,4,4,4,4,4,2,2,4,4],[4,4,4,4,4,4,4,4,2,2,4,4,4,4,4],[4,4,4,4,4,4,4,4,2,6,4,4,4,4,4],[4,2,2,4,4,4,4,4,4,4,2,4,2,2,4],[2,3,2,4,4,4,4,4,4,4,4,4,4,4,2],[2,2,4,4,4,4,4,4,4,4,4,4,4,2,2]]</answer>

Now act as a careful independent verifier, not a copy editor. Infer the rule afresh from the demonstrations, check it against every input/output pair, and inspect whether the proposed grid follows that rule cell by cell. In particular, check repeated motifs and their completion, symmetry/reflection/rotation, object boundaries, colors, and dimensions. Correct the grid if the candidate is inconsistent; if it is consistent, return it unchanged. Briefly explain the rule outside the answer tags. End with the complete output grid inside <answer></answer> tags as a JSON list of rows, with nothing else inside the tags.

Output: The 9×15 color-4 rectangle is the output canvas. Each colored marker inside it receives the surrounding color-2 pattern from the matching external motif, preserving the motif’s relative positions. The proposed grid matches these placements.

<answer>[[4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],[4,4,4,2,4,4,4,4,4,4,4,4,4,4,4],[4,4,2,1,2,4,4,4,4,4,4,2,7,2,4],[4,4,4,2,4,4,4,4,4,4,4,2,2,4,4],[4,4,4,4,4,4,4,4,2,2,4,4,4,4,4],[4,4,4,4,4,4,4,4,2,6,4,4,4,4,4],[4,2,2,4,4,4,4,4,4,4,2,4,2,2,4],[2,3,2,4,4,4,4,4,4,4,4,4,4,4,2],[2,2,4,4,4,4,4,4,4,4,4,4,4,2,2]]</answer>


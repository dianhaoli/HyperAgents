Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (16x16):
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 3 8 8 3 8 8 8 8 8 8 8 8
8 8 8 8 3 3 3 3 8 8 8 8 8 8 8 8
8 8 8 8 3 3 3 3 8 8 8 8 8 8 8 8
8 8 8 8 3 8 8 3 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 6 6 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 1 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8
8 6 6 8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 1 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
Output (4x4):
3 6 6 3
3 3 3 3
3 3 3 3
3 6 6 3
Training change audit (zero-based): dimensions change from 16x16 to 4x4; compare the complete grids above.

## Example 2
Input (16x16):
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 1 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 1 1 1 1 1 2 2 3 2 2 3 2 2 2 2
2 1 2 2 2 1 2 2 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 3 3 3 3 2 2 2 2
2 2 8 8 8 2 2 2 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 3 2 2 3 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 4 4 4 4 4 4 4 4 4 2 2 2 2
2 2 2 2 4 4 4 4 4 4 4 2 2 2 2 2
2 2 2 2 4 4 4 4 4 4 4 2 2 2 2 2
2 2 2 4 4 4 4 4 4 4 4 4 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
Output (3x5):
1 8 8 8 1
1 1 1 1 1
1 8 8 8 1
Training change audit (zero-based): dimensions change from 16x16 to 3x5; compare the complete grids above.

## Example 3
Input (16x16):
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 6 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 6 4
4 4 4 4 1 1 1 1 1 1 4 4 4 4 6 4
4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4
4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4
4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 4 4 2 4 4 4
4 4 3 3 4 4 4 4 4 2 4 4 2 4 4 4
4 4 3 3 4 4 4 4 4 2 4 4 2 4 4 4
4 4 3 3 4 4 4 4 4 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 2 4 4 2 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
Output (5x6):
1 1 1 1 1 1
3 3 1 1 1 6
3 3 1 1 1 6
3 3 1 1 1 6
1 1 1 1 1 1
Training change audit (zero-based): dimensions change from 16x16 to 5x6; compare the complete grids above.

## Test
Input (16x16):
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 4 8 8
8 8 1 8 8 1 8 8 8 8 4 8 8 4 8 8
8 8 1 1 1 1 8 8 8 8 4 4 4 4 8 8
8 8 1 8 8 1 8 8 8 8 4 4 4 4 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 4 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 4 8 8
8 8 8 2 2 2 2 2 2 8 4 8 8 4 8 8
8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 8 8 8 9 9 8 8 8 8 8
8 8 3 3 8 8 8 8 8 9 9 8 8 8 8 8
8 8 8 8 8 8 8 8 8 9 9 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and describe how the changed cells relate to them. Check the proposed rule against every input/output pair, including cells that stay unchanged; reject or revise it if even one pair disagrees. Do not infer a rule from only the endpoints or one example when the other examples constrain which cells change. Then apply the verified rule to the test, checking the grid dimensions and changed regions.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The color-4 object is a 6×4 pattern with two 2×2 gaps; the separate 2×2 color-3 object matches those gaps, so its color fills both. The other objects do not match the gaps.

<answer>[[4,3,3,4],[4,3,3,4],[4,4,4,4],[4,4,4,4],[4,3,3,4],[4,3,3,4]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (16x16):
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 3 8 8 3 8 8 8 8 8 8 8 8
8 8 8 8 3 3 3 3 8 8 8 8 8 8 8 8
8 8 8 8 3 3 3 3 8 8 8 8 8 8 8 8
8 8 8 8 3 8 8 3 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 6 6 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 1 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8
8 6 6 8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 1 1 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
Output (4x4):
3 6 6 3
3 3 3 3
3 3 3 3
3 6 6 3
Training change audit (zero-based): dimensions change from 16x16 to 4x4; compare the complete grids above.

## Example 2
Input (16x16):
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 1 2 2 2 1 2 2 2 2 2 2 2 2 2 2
2 1 1 1 1 1 2 2 3 2 2 3 2 2 2 2
2 1 2 2 2 1 2 2 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 3 3 3 3 2 2 2 2
2 2 8 8 8 2 2 2 3 3 3 3 2 2 2 2
2 2 2 2 2 2 2 2 3 2 2 3 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 4 4 4 4 4 4 4 4 4 2 2 2 2
2 2 2 2 4 4 4 4 4 4 4 2 2 2 2 2
2 2 2 2 4 4 4 4 4 4 4 2 2 2 2 2
2 2 2 4 4 4 4 4 4 4 4 4 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
Output (3x5):
1 8 8 8 1
1 1 1 1 1
1 8 8 8 1
Training change audit (zero-based): dimensions change from 16x16 to 3x5; compare the complete grids above.

## Example 3
Input (16x16):
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 6 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 6 4
4 4 4 4 1 1 1 1 1 1 4 4 4 4 6 4
4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4
4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4
4 4 4 4 4 4 1 1 1 4 4 4 4 4 4 4
4 4 4 4 1 1 1 1 1 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 2 4 4 2 4 4 4
4 4 3 3 4 4 4 4 4 2 4 4 2 4 4 4
4 4 3 3 4 4 4 4 4 2 4 4 2 4 4 4
4 4 3 3 4 4 4 4 4 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 2 4 4 2 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
Output (5x6):
1 1 1 1 1 1
3 3 1 1 1 6
3 3 1 1 1 6
3 3 1 1 1 6
1 1 1 1 1 1
Training change audit (zero-based): dimensions change from 16x16 to 5x6; compare the complete grids above.

## Test
Input (16x16):
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 4 8 8
8 8 1 8 8 1 8 8 8 8 4 8 8 4 8 8
8 8 1 1 1 1 8 8 8 8 4 4 4 4 8 8
8 8 1 8 8 1 8 8 8 8 4 4 4 4 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 4 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 4 8 8
8 8 8 2 2 2 2 2 2 8 4 8 8 4 8 8
8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 8 8 8 9 9 8 8 8 8 8
8 8 3 3 8 8 8 8 8 9 9 8 8 8 8 8
8 8 8 8 8 8 8 8 8 9 9 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and describe how the changed cells relate to them. Check the proposed rule against every input/output pair, including cells that stay unchanged; reject or revise it if even one pair disagrees. Do not infer a rule from only the endpoints or one example when the other examples constrain which cells change. Then apply the verified rule to the test, checking the grid dimensions and changed regions.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Independent verification of a previous candidate: [[4, 3, 3, 4], [4, 3, 3, 4], [4, 4, 4, 4], [4, 4, 4, 4], [4, 3, 3, 4], [4, 3, 3, 4]]
First infer the transformation from the demonstrations and check that it accounts for every input/output pair. Compare the candidate with the test input and that inferred rule; do not copy a demonstration output or accept the candidate merely because it looks plausible. If the candidate fails any check, correct it. Return the verified test grid in the required <answer> tags, with nothing else inside the tags.

Output: <answer>[[4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [4, 4, 4, 4], [4, 3, 3, 4], [4, 3, 3, 4]]</answer>


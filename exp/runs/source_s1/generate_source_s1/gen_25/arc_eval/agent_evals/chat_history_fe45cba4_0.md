Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (8x8):
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
2 7 7 7 7 9 9 9
2 2 2 7 7 7 7 7
2 2 2 7 7 2 2 2
2 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
Output (8x8):
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
7 7 7 7 7 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2

## Example 2
Input (8x8):
7 7 7 7 7 9 9 9
9 7 7 7 7 7 9 9
9 9 7 7 7 9 9 9
9 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
Output (8x8):
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2

## Test
Input (16x16):
7 7 7 7 7 7 7 7 7 7 9 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 9 9 9 9 9 9
8 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
8 8 7 8 7 7 7 7 7 7 7 7 7 7 7 7
8 8 8 8 8 7 7 7 7 7 7 7 7 7 7 7
8 8 7 8 7 7 7 7 7 7 8 8 8 8 8 8
8 7 7 7 7 7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 7 7 7 7 7 7 7 7 8 8
7 7 7 7 7 7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 7 7 7 7 8 8 8 8 8 8
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and describe how the changed cells relate to them. Check the proposed rule against every input/output pair, including cells that stay unchanged; reject or revise it if even one pair disagrees. Do not infer a rule from only the endpoints or one example when the other examples constrain which cells change. Then apply the verified rule to the test, checking the grid dimensions and changed regions.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 9, 9, 9, 9, 9, 9], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (8x8):
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
2 7 7 7 7 9 9 9
2 2 2 7 7 7 7 7
2 2 2 7 7 2 2 2
2 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
Output (8x8):
7 7 7 7 7 9 9 9
7 7 7 7 7 7 9 9
7 7 7 7 7 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2
7 7 7 7 2 2 2 2

## Example 2
Input (8x8):
7 7 7 7 7 9 9 9
9 7 7 7 7 7 9 9
9 9 7 7 7 9 9 9
9 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2
Output (8x8):
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7
7 7 7 7 7 2 2 2
7 7 7 7 7 7 7 2
7 7 7 7 7 7 7 2
7 7 7 7 7 2 2 2

## Test
Input (16x16):
7 7 7 7 7 7 7 7 7 7 9 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 7 9 9 9 9
7 7 7 7 7 7 7 7 7 7 7 9 9 9 9 9
7 7 7 7 7 7 7 7 7 7 9 9 9 9 9 9
8 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
8 8 7 8 7 7 7 7 7 7 7 7 7 7 7 7
8 8 8 8 8 7 7 7 7 7 7 7 7 7 7 7
8 8 7 8 7 7 7 7 7 7 8 8 8 8 8 8
8 7 7 7 7 7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 7 7 7 7 7 7 7 7 8 8
7 7 7 7 7 7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 7 7 7 7 8 8 8 8 8 8
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and describe how the changed cells relate to them. Check the proposed rule against every input/output pair, including cells that stay unchanged; reject or revise it if even one pair disagrees. Do not infer a rule from only the endpoints or one example when the other examples constrain which cells change. Then apply the verified rule to the test, checking the grid dimensions and changed regions.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Make this a fresh, independent solve: do not assume or reuse any earlier proposed rule or grid. Infer a concrete rule from the training pairs, check that it reproduces every demonstrated output, then apply it to the test input. Verify the dimensions and changed cells against that rule before returning the grid in <answer> tags, with nothing else inside the tags.

Output: The color 8 occurs in two separate objects. In both demonstrations, the left occurrence is removed and the right occurrence is filled across the right half of the grid over its existing row range. The single color 9 object stays unchanged. Applying that rule gives:

<answer>[[7,7,7,7,7,7,7,7,7,7,9,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,7,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,9,9,9,9,9,9],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,8,8,8,8,8,8,8,8],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7]]</answer>


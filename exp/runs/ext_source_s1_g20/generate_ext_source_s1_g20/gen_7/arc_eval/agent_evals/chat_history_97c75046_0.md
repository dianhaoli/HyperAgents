Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

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

## Example 2
Input (6x8):
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 0 7
7 7 7 7 7 0 0 7
7 5 7 7 0 0 0 7
Output (6x8):
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 5 7
7 7 7 7 7 7 0 7
7 7 7 7 7 0 0 7
7 7 7 7 0 0 0 7

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

Shape check: the demonstrations consistently imply an output of 10 rows by 16 columns for this test. Use that dimension as a verification constraint; count rows and cells per row before finalizing, and only depart from it if the demonstrated rule requires it.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7], [7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 5, 7, 7, 7, 7, 7]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

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

## Example 2
Input (6x8):
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 0 7
7 7 7 7 7 0 0 7
7 5 7 7 0 0 0 7
Output (6x8):
7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7
7 7 7 7 7 7 5 7
7 7 7 7 7 7 0 7
7 7 7 7 7 0 0 7
7 7 7 7 0 0 0 7

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

Shape check: the demonstrations consistently imply an output of 10 rows by 16 columns for this test. Use that dimension as a verification constraint; count rows and cells per row before finalizing, and only depart from it if the demonstrated rule requires it.
INDEPENDENT SECOND PASS: Ignore any earlier proposed answer. Infer the rule from the demonstrations alone, state the concrete operations internally, and check that they reproduce every demonstrated output before applying them to the test. Verify the final grid dimensions and cell order.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: <answer>[[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,7,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,0,7,7,7,7,7,7,7,7,7],[7,7,7,0,0,0,0,0,7,7,7,7,7,7,7,7],[7,7,0,0,0,0,0,0,0,7,7,7,7,7,7,7],[7,7,0,0,0,0,0,0,0,0,5,7,7,7,7,7]]</answer>


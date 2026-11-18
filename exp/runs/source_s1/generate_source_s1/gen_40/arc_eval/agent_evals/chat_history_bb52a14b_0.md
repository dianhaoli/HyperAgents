Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input. Use audits as evidence, not as a substitute for full grids: before solving the test, check one concrete rule against every cell and output dimension in every training pair. Account for unchanged cells, boundaries, overlaps, and the exact extent and direction of any pattern; reject a rule that only explains the edits or looks visually plausible.

## Example 1
Input (22x22):
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 1 8
0 0 8 0 0 0 0 0 8 1 1 0 1 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 8 1 1 0 0 0 0
0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 8 0 0 0 0 0
0 0 1 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 8 0 0 8 0 0 0 0 0 1 0 0 0 1 0 0 0 0
0 0 0 0 0 1 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 8 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 8 4 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 8 1 1 8 8 1 0 0 0 0 0 0 0 0 8 1 1 0 0
0 0 0 4 1 4 0 0 8 0 0 0 0 0 0 0 0 0 1 0 1 0
0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 8 0 0 8 0 0 0
1 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 8 0 0 0 0 0 8 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 8 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (22x22):
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 8 4 0 0 0 0 0 0 0 0 0 1 8
0 0 8 0 0 0 0 0 8 1 1 0 1 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 4 1 4 0 0 0 0 8 1 1 0 0 0 0
0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 8 0 0 0 0 0
0 0 1 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 8 0 0 8 0 0 0 0 0 1 0 0 0 1 0 0 0 0
0 0 0 0 0 1 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 8 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 8 4 0 0 0 0 0 0 0 0 0 0 0 4 8 4 0 0
0 0 0 8 1 1 8 8 1 0 0 0 0 0 0 0 0 8 1 1 0 0
0 0 0 4 1 4 0 0 8 0 0 0 0 0 0 0 0 4 1 4 1 0
0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 8 0 0 8 0 0 0
1 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 8 0 0 0 0 0 8 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 8 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Change audit (input value -> output value; coordinates are zero-based): 8 changed cell(s); 476 unchanged (value counts: 0: 405, 1: 38, 4: 4, 8: 29): 0->4: 8 cell(s) at (1,8), (1,10), (3,8), (3,10), (11,17), (11,19), (13,17), (13,19)

## Example 2
Input (22x22):
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 8 0 0 0 8 8 0 0
0 0 0 0 1 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8
0 1 0 0 4 8 4 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 8 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 8 1 0 1
0 1 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 8 0
1 8 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 8 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 1 0 0 8 8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0
0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0 0 0
Output (22x22):
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 8 0 0 0 8 8 0 0
0 0 0 0 1 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8
0 1 0 0 4 8 4 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 8 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 8 1 4 1
0 1 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 4 8 4
1 8 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 8 4 4 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 1 0 0 8 8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0
0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0 0 0
Change audit (input value -> output value; coordinates are zero-based): 5 changed cell(s); 479 unchanged (value counts: 0: 418, 1: 32, 4: 5, 8: 24): 0->4: 5 cell(s) at (12,20), (13,19), (13,21), (14,19), (14,20)

## Example 3
Input (22x22):
0 0 0 0 0 1 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 1 8 0
0 8 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0
8 0 1 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 4 8 4 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 8 4 1 0 8
0 1 0 0 0 0 0 0 0 1 0 0 0 0 1 0 1 4 4 4 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 8 1
0 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 1 0 0 0 1 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 8 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 8 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 1 1 1 0 0 0 8 0 0 0 0
Output (22x22):
0 0 0 0 0 1 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 1 8 0
4 8 4 0 0 0 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0
8 4 1 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 1 0 0 0 0 0 0 0 0 0 0 0 0 4 8 4 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 8 4 1 0 8
0 1 0 0 0 0 0 0 0 1 0 0 0 0 1 0 1 4 4 4 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 8 1
0 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 1 0 0 0 1 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 8 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 4 8 4 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 8 4 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 1 1 1 0 0 0 8 0 0 0 0
Change audit (input value -> output value; coordinates are zero-based): 12 changed cell(s); 472 unchanged (value counts: 0: 410, 1: 28, 4: 6, 8: 28): 0->4: 12 cell(s) at (4,0), (4,2), (5,1), (6,0), (6,1), (6,2), (17,14), (17,16), (18,15), (19,14), (19,15), (19,16)

## Test
Input (22x22):
0 0 8 0 0 0 8 0 0 0 0 0 1 0 0 1 0 0 0 0 8 0
0 0 0 1 0 0 1 8 8 1 0 0 0 0 8 8 0 0 0 1 0 0
0 0 8 0 0 8 8 0 0 0 1 8 1 0 0 8 0 0 0 1 0 0
0 8 8 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 1 8 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 8 0 0
0 1 0 0 4 8 4 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8
8 0 0 0 4 8 8 0 8 0 0 0 0 0 8 0 0 1 0 8 1 0
0 0 0 0 4 1 4 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 8 0 0 0 1 1 0 0 1 0 1 0 0 0 0 0 0 0 1 0 8
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 8 8 8 0 0 0 8 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 1 0 0 0 0
1 8 8 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0 8 0
0 8 0 0 8 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 1 0
0 0 8 8 0 0 0 0 0 0 0 0 0 1 0 0 1 0 8 1 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 1 0 8 0 8 1 0 1 0 0 0

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and explain every listed changed cell using one concrete rule that works for every pair. Also check the unchanged cells: do not alter cells merely to complete a shape or extend a pattern beyond the bounds supported by the examples. If dimensions change, account for that explicitly. Reject or revise any rule that cannot explain all demonstrated edits and non-edits. Then apply the verified rule to the test and check its dimensions and bounds.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The rule is to use the existing 3×3 pattern of 4s as a mask. When the same aligned 1/8 arrangement appears elsewhere with zeros at the mask positions, fill only those zeros with 4s.

- **Example 1:** The source block at rows 11–13, columns 3–5 has 4s at its four corners. The matching blocks at rows 1–3, columns 8–10 and rows 11–13, columns 17–19 have the same 1/8 arrangement and zeros at those corners. Filling those eight positions accounts for every listed change.
- **Example 2:** The source block at rows 6–8, columns 4–6 has 4s at offsets (0,1), (1,0), (1,2), (2,0), and (2,1). The matching block at rows 12–14, columns 19–21 has zeros at exactly those five positions, accounting for every change.
- **Example 3:** The source block at rows 6–8, columns 17–19 has 4s at offsets (0,0), (0,2), (1,1), (2,0), (2,1), and (2,2). The matching blocks at rows 4–6, columns 0–2 and rows 17–19, columns 14–16 have zeros at those six positions, accounting for all twelve changes.

In each demonstration the dimensions stay 22×22. Only the mask positions in matching blocks change; all other cells, including the 1s, 8s, and zeros outside those positions, remain unchanged.

In the test, the source block is at rows 8–10, columns 4–6. Its matching 1/8 arrangement is at rows 15–17, columns 12–14, so fill the five mask positions there. The output remains 22×22.

<answer>[[0,0,8,0,0,0,8,0,0,0,0,0,1,0,0,1,0,0,0,0,8,0],[0,0,0,1,0,0,1,8,8,1,0,0,0,0,8,8,0,0,0,1,0,0],[0,0,8,0,0,8,8,0,0,0,1,8,1,0,0,8,0,0,0,1,0,0],[0,8,8,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,8,0,0,0,0,0,0,0,1,8,0,1,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,8,0,0],[0,1,0,0,4,8,4,0,0,0,0,0,0,0,8,0,0,0,0,0,0,8],[8,0,0,0,4,8,8,0,8,0,0,0,0,0,8,0,0,1,0,8,1,0],[0,0,0,0,4,1,4,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0],[0,8,0,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,8],[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0],[0,0,8,8,8,0,0,0,8,1,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,8,4,0,0,1,0,0,0,0],[1,8,8,0,0,0,0,0,0,0,0,0,4,8,8,0,0,0,0,0,8,0],[0,8,0,0,8,1,0,0,0,0,0,0,4,1,4,0,0,0,0,0,8,8],[0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,1,0],[0,0,8,8,0,0,0,0,0,0,0,0,0,1,0,0,1,0,8,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,8,0,1,0,8,0,8,1,0,1,0,0,0,0]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input. Use audits as evidence, not as a substitute for full grids: before solving the test, check one concrete rule against every cell and output dimension in every training pair. Account for unchanged cells, boundaries, overlaps, and the exact extent and direction of any pattern; reject a rule that only explains the edits or looks visually plausible.

## Example 1
Input (22x22):
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 1 8
0 0 8 0 0 0 0 0 8 1 1 0 1 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 8 1 1 0 0 0 0
0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 8 0 0 0 0 0
0 0 1 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 8 0 0 8 0 0 0 0 0 1 0 0 0 1 0 0 0 0
0 0 0 0 0 1 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 8 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 8 4 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 8 1 1 8 8 1 0 0 0 0 0 0 0 0 8 1 1 0 0
0 0 0 4 1 4 0 0 8 0 0 0 0 0 0 0 0 0 1 0 1 0
0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 8 0 0 8 0 0 0
1 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 8 0 0 0 0 0 8 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 8 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Output (22x22):
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 4 8 4 0 0 0 0 0 0 0 0 0 1 8
0 0 8 0 0 0 0 0 8 1 1 0 1 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 4 1 4 0 0 0 0 8 1 1 0 0 0 0
0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 8 0 0 0 0 0
0 0 1 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 8 0 0 8 0 0 0 0 0 1 0 0 0 1 0 0 0 0
0 0 0 0 0 1 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 8 0 0 0 1 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 8 4 0 0 0 0 0 0 0 0 0 0 0 4 8 4 0 0
0 0 0 8 1 1 8 8 1 0 0 0 0 0 0 0 0 8 1 1 0 0
0 0 0 4 1 4 0 0 8 0 0 0 0 0 0 0 0 4 1 4 1 0
0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 8 0 0 8 0 0 0
1 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 8 0 0 0 0 0 8 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 8 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
Change audit (input value -> output value; coordinates are zero-based): 8 changed cell(s); 476 unchanged (value counts: 0: 405, 1: 38, 4: 4, 8: 29): 0->4: 8 cell(s) at (1,8), (1,10), (3,8), (3,10), (11,17), (11,19), (13,17), (13,19)

## Example 2
Input (22x22):
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 8 0 0 0 8 8 0 0
0 0 0 0 1 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8
0 1 0 0 4 8 4 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 8 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 8 1 0 1
0 1 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 8 0
1 8 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 8 0 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 1 0 0 8 8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0
0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0 0 0
Output (22x22):
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 8 0 0 0 8 8 0 0
0 0 0 0 1 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8
0 1 0 0 4 8 4 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 4 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 8 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 1 0 0 0 0 0 8 1 4 1
0 1 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 4 8 4
1 8 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 8 4 4 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 1 0 0 8 8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0
0 0 0 0 1 0 0 0 0 1 0 0 0 1 0 0 0 0 0 1 0 0
0 0 0 1 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0 0 0
Change audit (input value -> output value; coordinates are zero-based): 5 changed cell(s); 479 unchanged (value counts: 0: 418, 1: 32, 4: 5, 8: 24): 0->4: 5 cell(s) at (12,20), (13,19), (13,21), (14,19), (14,20)

## Example 3
Input (22x22):
0 0 0 0 0 1 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 1 8 0
0 8 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0
8 0 1 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 4 8 4 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 8 4 1 0 8
0 1 0 0 0 0 0 0 0 1 0 0 0 0 1 0 1 4 4 4 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 8 1
0 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 1 0 0 0 1 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 8 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 8 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 1 1 1 0 0 0 8 0 0 0 0
Output (22x22):
0 0 0 0 0 1 0 0 0 0 0 0 8 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1
0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 1 8 0
4 8 4 0 0 0 0 0 0 0 8 0 0 0 0 0 0 1 0 0 0 0
8 4 1 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 0 1 0 0 0 0 0 0 0 0 0 0 0 0 4 8 4 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 8 4 1 0 8
0 1 0 0 0 0 0 0 0 1 0 0 0 0 1 0 1 4 4 4 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 8 1
0 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0
0 1 0 0 0 1 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 8 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0 0 4 8 4 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 8 4 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 1 1 1 0 0 0 8 0 0 0 0
Change audit (input value -> output value; coordinates are zero-based): 12 changed cell(s); 472 unchanged (value counts: 0: 410, 1: 28, 4: 6, 8: 28): 0->4: 12 cell(s) at (4,0), (4,2), (5,1), (6,0), (6,1), (6,2), (17,14), (17,16), (18,15), (19,14), (19,15), (19,16)

## Test
Input (22x22):
0 0 8 0 0 0 8 0 0 0 0 0 1 0 0 1 0 0 0 0 8 0
0 0 0 1 0 0 1 8 8 1 0 0 0 0 8 8 0 0 0 1 0 0
0 0 8 0 0 8 8 0 0 0 1 8 1 0 0 8 0 0 0 1 0 0
0 8 8 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 1 8 0 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0 0 0 1 0 0 0 0 8 0 0
0 1 0 0 4 8 4 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8
8 0 0 0 4 8 8 0 8 0 0 0 0 0 8 0 0 1 0 8 1 0
0 0 0 0 4 1 4 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 8 0 0 0 1 1 0 0 1 0 1 0 0 0 0 0 0 0 1 0 8
0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 8 8 8 0 0 0 8 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 1 0 0 0 0
1 8 8 0 0 0 0 0 0 0 0 0 0 8 8 0 0 0 0 0 8 0
0 8 0 0 8 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 8 8
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 1 0
0 0 8 8 0 0 0 0 0 0 0 0 0 1 0 0 1 0 8 1 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 1 0 8 0 8 1 0 1 0 0 0

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and explain every listed changed cell using one concrete rule that works for every pair. Also check the unchanged cells: do not alter cells merely to complete a shape or extend a pattern beyond the bounds supported by the examples. If dimensions change, account for that explicitly. Reject or revise any rule that cannot explain all demonstrated edits and non-edits. Then apply the verified rule to the test and check its dimensions and bounds.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Make this a fresh, independent solve: do not assume or reuse any earlier proposed rule or grid. Infer a concrete rule from the training pairs, check that it reproduces every demonstrated output, then apply it to the test input. Verify the dimensions and changed cells against that rule before returning the grid in <answer> tags, with nothing else inside the tags.

Output: The 4s mark a 3×3 stencil. In each training pair, the stencil’s non-4 cells give an exact arrangement of 1s and 8s; every other matching 3×3 arrangement receives 4s only at the stencil’s positions, and only where those cells are 0. The matching copy locations are (1,8) and (11,17) in Example 1, (12,19) in Example 2, and (4,0) and (17,14) in Example 3. Their stencil positions reproduce every listed change. All other cells remain unchanged; the stencil does not extend beyond those 3×3 windows.

For the test, the stencil at (8,4) matches one other arrangement at (15,12). Its five zero-valued stencil positions become 4; the grid remains 22×22.

<answer>[[0,0,8,0,0,0,8,0,0,0,0,0,1,0,0,1,0,0,0,0,8,0],[0,0,0,1,0,0,1,8,8,1,0,0,0,0,8,8,0,0,0,1,0,0],[0,0,8,0,0,8,8,0,0,0,1,8,1,0,0,8,0,0,0,1,0,0],[0,8,8,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,8,0,0,0,0,0,0,0,1,8,0,1,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,8,0,0],[0,1,0,0,4,8,4,0,0,0,0,0,0,0,8,0,0,0,0,0,0,8],[8,0,0,0,4,8,8,0,8,0,0,0,0,0,8,0,0,1,0,8,1,0],[0,0,0,0,4,1,4,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0],[0,8,0,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,8],[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0],[0,0,8,8,8,0,0,0,8,1,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,4,8,4,0,0,1,0,0,0,0],[1,8,8,0,0,0,0,0,0,0,0,0,4,8,8,0,0,0,0,0,8,0],[0,8,0,0,8,1,0,0,0,0,0,0,4,1,4,0,0,0,0,0,8,8],[0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,1,0],[0,0,8,8,0,0,0,0,0,0,0,0,0,1,0,0,1,0,8,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,8,0,1,0,8,0,8,1,0,1,0,0,0]]</answer>


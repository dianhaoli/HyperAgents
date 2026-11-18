Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (14x22):
0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1
1 8 8 8 8 8 8 8 8 8 8 8 1 2 3 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 4 4 4 4 4 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 4 4 4 4 4 4 3 0 6 6 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 6 6 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 2 3 0 1 2
0 8 8 8 8 8 8 8 8 8 8 8 0 1 2 3 0 1 2 3 0 1
1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
Output (12x11):
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 8 8 8 8 8 8 8 8 8 8
Change audit (input 14x22 -> output 12x11; 8 unchanged cell(s)): 0->4: 5 at (5,3), (5,7), (7,7), (9,7), (10,4); 0->5: 3 at (6,4), (7,3), (8,4); 0->6: 1 at (9,3); 0->8: 10 at (0,0), (0,4), (0,8), (2,0), (4,0), (6,0), (8,0), (10,0), (11,3), (11,7); 0->outside: 36 at (0,12), (0,16), (0,20), (1,15), (1,19), (2,12), (2,16), (2,20), (3,15), (3,19), (4,16), (4,20), (5,15), (5,19), (6,16), (6,20), (7,15), (7,19), (8,16), (8,20), (9,15) (+15 coordinates omitted); 1->0: 6 (+6 coordinates omitted); 1->4: 2 (+2 coordinates omitted); 1->5: 4 (+4 coordinates omitted); 1->8: 11 (+11 coordinates omitted); 1->outside: 38 (+38 coordinates omitted); 2->0: 6 (+6 coordinates omitted); 2->4: 3 (+3 coordinates omitted); 2->5: 5 (+5 coordinates omitted); 2->6: 1 (+1 coordinates omitted); 2->8: 7 (+7 coordinates omitted); 2->outside: 30 (+30 coordinates omitted); 3->0: 6 (+6 coordinates omitted); 3->4: 6 (+6 coordinates omitted); 3->5: 4 (+4 coordinates omitted); 3->6: 2 (+2 coordinates omitted); 3->8: 6 (+6 coordinates omitted); 3->outside: 28 (+28 coordinates omitted); 4->0: 8 (+8 coordinates omitted); 4->8: 2 (+2 coordinates omitted); 4->outside: 12 (+12 coordinates omitted); 5->0: 4 (+4 coordinates omitted); 5->8: 4 (+4 coordinates omitted); 5->outside: 12 (+12 coordinates omitted); 6->outside: 4 (+4 coordinates omitted); 8->0: 12 (+12 coordinates omitted); 8->4: 6 (+6 coordinates omitted); 8->outside: 16 (+16 coordinates omitted)

## Example 2
Input (13x23):
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 4 4 1 2 0 1
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 8 8 4 4 2 0 1 2
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
0 1 2 0 1 3 3 3 3 3 3 3 3 3 8 6 6 6 8 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 8 8 8 8 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 3 3 3 3 3 3 3 3 3 3 3 0 1 2 0 1 2
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1
Output (9x12):
3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 8 6 6 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3
Change audit (input 13x23 -> output 9x12; 13 unchanged cell(s)): 0->3: 14 at (0,0), (0,3), (0,6), (0,9), (1,11), (2,11), (3,0), (4,11), (5,11), (6,0), (7,11), (8,2), (8,8), (8,11); 0->4: 2 at (5,2), (6,3); 0->6: 1 at (4,2); 0->8: 2 at (3,3), (7,2); 0->outside: 43 at (0,12), (0,15), (0,21), (1,20), (2,20), (3,21), (4,20), (5,20), (6,12), (6,15), (6,18), (6,21), (7,14), (7,17), (7,20), (8,14), (8,17), (8,20), (9,0), (9,3), (9,6) (+22 coordinates omitted); 1->0: 14 (+14 coordinates omitted); 1->3: 13 (+13 coordinates omitted); 1->4: 1 (+1 coordinates omitted); 1->6: 2 (+2 coordinates omitted); 1->8: 4 (+4 coordinates omitted); 1->outside: 52 (+52 coordinates omitted); 2->0: 15 (+15 coordinates omitted); 2->3: 9 (+9 coordinates omitted); 2->4: 1 (+1 coordinates omitted); 2->6: 2 (+2 coordinates omitted); 2->8: 5 (+5 coordinates omitted); 2->outside: 48 (+48 coordinates omitted); 3->0: 5 (+5 coordinates omitted); 3->8: 5 (+5 coordinates omitted); 3->outside: 21 (+21 coordinates omitted); 4->outside: 4 (+4 coordinates omitted); 6->outside: 9 (+9 coordinates omitted); 8->outside: 14 (+14 coordinates omitted)

## Example 3
Input (16x23):
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 3 3 3 3 3 3 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 4 4 4 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 3 3 3 3 3 3 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
Output (8x8):
3 3 3 3 3 3 3 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 3 3 3 3 3 3 3
Change audit (input 16x23 -> output 8x8; 19 unchanged cell(s)): 0->3: 8 at (0,0), (0,2), (0,4), (0,6), (2,0), (4,0), (6,0), (7,1); 0->4: 1 at (5,1); 0->8: 2 at (1,1), (3,1); 0->outside: 136 at (0,8), (0,10), (0,12), (0,14), (0,16), (0,18), (0,20), (0,22), (1,11), (1,13), (1,15), (1,17), (1,19), (1,21), (2,10), (2,12), (2,14), (2,16), (2,18), (2,20), (2,22), (3,11), (3,13), (3,15), (3,17), (3,19), (3,21), (4,10), (4,16) (+107 coordinates omitted); 1->3: 8 (+8 coordinates omitted); 1->4: 2 (+2 coordinates omitted); 1->8: 1 (+1 coordinates omitted); 1->outside: 137 (+137 coordinates omitted); 3->4: 3 (+3 coordinates omitted); 3->8: 7 (+7 coordinates omitted); 3->outside: 16 (+16 coordinates omitted); 4->outside: 9 (+9 coordinates omitted); 8->3: 10 (+10 coordinates omitted); 8->4: 3 (+3 coordinates omitted); 8->outside: 6 (+6 coordinates omitted)

## Test
Input (19x27):
2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3
1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 3 1 1 9 9 1 3 1 1
2 3 3 8 3 3 2 3 3 2 3 3 2 3 3 8 3 3 2 3 3 9 9 3 2 3 3
1 2 2 8 2 2 1 2 2 1 2 2 1 2 2 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 1 1 3 1 1 8 1 1 3 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 6 6 6 6 6 6 6 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 6 2 1 2 2 8 2 2 6 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 6 1 3 4 4 4 4 1 6 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 3 2 4 4 4 4 3 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 6 2 1 4 4 4 4 2 6 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 6 1 3 1 1 8 1 1 6 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 6 6 6 6 6 6 6 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 2 2 1 2 2 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 1 1 3 1 1 8 1 1 3 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 3 3 2 3 3 8 3 3 2 3 3 2 3 3 2 3 3
1 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1
2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and describe how the changed cells relate to them. Check the proposed rule against every input/output pair, including cells that stay unchanged; reject or revise it if even one pair disagrees. Do not infer a rule from only the endpoints or one example when the other examples constrain which cells change. Then apply the verified rule to the test, checking the grid dimensions and changed regions.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Output: The large rectangular outline defines the canvas. The repeating background becomes 0 inside it and is discarded outside it. Other objects are moved into the canvas, bottom-left aligned; nested patches are placed bottom-left over the colored interior object. This matches the examples: the 4/5 or 8/6 framed object is placed in the large frame, then the smaller 6 or 4 patch overlays its interior. In the test, the 6 frame is placed bottom-left, its 4 patch keeps its position within that frame, and the 9 patch overlays the bottom-left of the 4 patch.

The resulting canvas is 15×13: the 6 frame occupies rows 7–13 and columns 1–9; the 4 patch occupies rows 9–11 and columns 4–7, with 9 over its bottom-left 2×2.

<answer>[[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 8], [8, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 0, 0, 4, 4, 4, 4, 0, 6, 0, 0, 8], [8, 6, 0, 0, 9, 9, 4, 4, 0, 6, 0, 0, 8], [8, 6, 0, 0, 9, 9, 4, 4, 0, 6, 0, 0, 8], [8, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]</answer>

Input: You are solving an ARC-AGI puzzle. Each grid is a rectangular 2D array of integers 0-9 (each integer is a color). The demonstration pairs below share one hidden transformation rule that maps each input grid to its output grid. Infer the rule and apply it to the test input.

## Example 1
Input (14x22):
0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1
1 8 8 8 8 8 8 8 8 8 8 8 1 2 3 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 4 4 4 4 4 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 5 5 5 5 5 4 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 4 5 5 5 5 5 4 0 1 2 3 0 1 2
0 8 2 3 0 1 2 3 4 4 4 4 4 4 4 3 0 6 6 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 6 6 0 1 2
0 8 2 3 0 1 2 3 0 1 2 8 0 1 2 3 0 1 2 3 0 1
1 8 3 0 1 2 3 0 1 2 3 8 1 2 3 0 1 2 3 0 1 2
0 8 8 8 8 8 8 8 8 8 8 8 0 1 2 3 0 1 2 3 0 1
1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3 0 1 2
Output (12x11):
8 8 8 8 8 8 8 8 8 8 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 0 0 0 0 0 0 0 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 5 5 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 6 6 5 5 5 4 0 0 8
8 4 4 4 4 4 4 4 0 0 8
8 8 8 8 8 8 8 8 8 8 8
Change audit (input 14x22 -> output 12x11; 8 unchanged cell(s)): 0->4: 5 at (5,3), (5,7), (7,7), (9,7), (10,4); 0->5: 3 at (6,4), (7,3), (8,4); 0->6: 1 at (9,3); 0->8: 10 at (0,0), (0,4), (0,8), (2,0), (4,0), (6,0), (8,0), (10,0), (11,3), (11,7); 0->outside: 36 at (0,12), (0,16), (0,20), (1,15), (1,19), (2,12), (2,16), (2,20), (3,15), (3,19), (4,16), (4,20), (5,15), (5,19), (6,16), (6,20), (7,15), (7,19), (8,16), (8,20), (9,15) (+15 coordinates omitted); 1->0: 6 (+6 coordinates omitted); 1->4: 2 (+2 coordinates omitted); 1->5: 4 (+4 coordinates omitted); 1->8: 11 (+11 coordinates omitted); 1->outside: 38 (+38 coordinates omitted); 2->0: 6 (+6 coordinates omitted); 2->4: 3 (+3 coordinates omitted); 2->5: 5 (+5 coordinates omitted); 2->6: 1 (+1 coordinates omitted); 2->8: 7 (+7 coordinates omitted); 2->outside: 30 (+30 coordinates omitted); 3->0: 6 (+6 coordinates omitted); 3->4: 6 (+6 coordinates omitted); 3->5: 4 (+4 coordinates omitted); 3->6: 2 (+2 coordinates omitted); 3->8: 6 (+6 coordinates omitted); 3->outside: 28 (+28 coordinates omitted); 4->0: 8 (+8 coordinates omitted); 4->8: 2 (+2 coordinates omitted); 4->outside: 12 (+12 coordinates omitted); 5->0: 4 (+4 coordinates omitted); 5->8: 4 (+4 coordinates omitted); 5->outside: 12 (+12 coordinates omitted); 6->outside: 4 (+4 coordinates omitted); 8->0: 12 (+12 coordinates omitted); 8->4: 6 (+6 coordinates omitted); 8->outside: 16 (+16 coordinates omitted)

## Example 2
Input (13x23):
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 4 4 1 2 0 1
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 8 8 4 4 2 0 1 2
1 2 0 1 2 0 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
0 1 2 0 1 3 3 3 3 3 3 3 3 3 8 6 6 6 8 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 6 6 6 8 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 8 8 8 8 8 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
0 1 2 0 1 3 0 1 2 0 1 2 0 1 2 0 3 2 0 1 2 0 1
1 2 0 1 2 3 1 2 0 1 2 0 1 2 0 1 3 0 1 2 0 1 2
1 2 0 1 2 3 3 3 3 3 3 3 3 3 3 3 3 0 1 2 0 1 2
0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1 2 0 1
Output (9x12):
3 3 3 3 3 3 3 3 3 3 3 3
3 0 0 0 0 0 0 0 0 0 0 3
3 0 0 0 0 0 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 8 6 6 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 4 4 6 8 0 0 0 0 0 3
3 8 8 8 8 8 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3 3 3
Change audit (input 13x23 -> output 9x12; 13 unchanged cell(s)): 0->3: 14 at (0,0), (0,3), (0,6), (0,9), (1,11), (2,11), (3,0), (4,11), (5,11), (6,0), (7,11), (8,2), (8,8), (8,11); 0->4: 2 at (5,2), (6,3); 0->6: 1 at (4,2); 0->8: 2 at (3,3), (7,2); 0->outside: 43 at (0,12), (0,15), (0,21), (1,20), (2,20), (3,21), (4,20), (5,20), (6,12), (6,15), (6,18), (6,21), (7,14), (7,17), (7,20), (8,14), (8,17), (8,20), (9,0), (9,3), (9,6) (+22 coordinates omitted); 1->0: 14 (+14 coordinates omitted); 1->3: 13 (+13 coordinates omitted); 1->4: 1 (+1 coordinates omitted); 1->6: 2 (+2 coordinates omitted); 1->8: 4 (+4 coordinates omitted); 1->outside: 52 (+52 coordinates omitted); 2->0: 15 (+15 coordinates omitted); 2->3: 9 (+9 coordinates omitted); 2->4: 1 (+1 coordinates omitted); 2->6: 2 (+2 coordinates omitted); 2->8: 5 (+5 coordinates omitted); 2->outside: 48 (+48 coordinates omitted); 3->0: 5 (+5 coordinates omitted); 3->8: 5 (+5 coordinates omitted); 3->outside: 21 (+21 coordinates omitted); 4->outside: 4 (+4 coordinates omitted); 6->outside: 9 (+9 coordinates omitted); 8->outside: 14 (+14 coordinates omitted)

## Example 3
Input (16x23):
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 3 3 3 3 3 3 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 4 4 4 0 1 0 1 0 1 0 1
0 1 3 8 8 8 8 8 8 3 0 1 4 4 4 1 0 1 0 1 0 1 0
1 0 3 8 8 8 8 8 8 3 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 3 3 3 3 3 3 3 3 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1
Output (8x8):
3 3 3 3 3 3 3 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 8 8 8 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 4 4 4 8 8 8 3
3 3 3 3 3 3 3 3
Change audit (input 16x23 -> output 8x8; 19 unchanged cell(s)): 0->3: 8 at (0,0), (0,2), (0,4), (0,6), (2,0), (4,0), (6,0), (7,1); 0->4: 1 at (5,1); 0->8: 2 at (1,1), (3,1); 0->outside: 136 at (0,8), (0,10), (0,12), (0,14), (0,16), (0,18), (0,20), (0,22), (1,11), (1,13), (1,15), (1,17), (1,19), (1,21), (2,10), (2,12), (2,14), (2,16), (2,18), (2,20), (2,22), (3,11), (3,13), (3,15), (3,17), (3,19), (3,21), (4,10), (4,16) (+107 coordinates omitted); 1->3: 8 (+8 coordinates omitted); 1->4: 2 (+2 coordinates omitted); 1->8: 1 (+1 coordinates omitted); 1->outside: 137 (+137 coordinates omitted); 3->4: 3 (+3 coordinates omitted); 3->8: 7 (+7 coordinates omitted); 3->outside: 16 (+16 coordinates omitted); 4->outside: 9 (+9 coordinates omitted); 8->3: 10 (+10 coordinates omitted); 8->4: 3 (+3 coordinates omitted); 8->outside: 6 (+6 coordinates omitted)

## Test
Input (19x27):
2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3
1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 3 1 1 9 9 1 3 1 1
2 3 3 8 3 3 2 3 3 2 3 3 2 3 3 8 3 3 2 3 3 9 9 3 2 3 3
1 2 2 8 2 2 1 2 2 1 2 2 1 2 2 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 1 1 3 1 1 8 1 1 3 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 6 6 6 6 6 6 6 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 6 2 1 2 2 8 2 2 6 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 6 1 3 4 4 4 4 1 6 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 3 2 4 4 4 4 3 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 6 2 1 4 4 4 4 2 6 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 6 1 3 1 1 8 1 1 6 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 6 6 6 6 6 6 6 6 6 3 3 2 3 3 2 3 3
1 2 2 8 2 2 1 2 2 1 2 2 1 2 2 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 8 1 1 3 1 1 3 1 1 3 1 1 8 1 1 3 1 1 3 1 1 3 1 1
2 3 3 8 3 3 2 3 3 2 3 3 2 3 3 8 3 3 2 3 3 2 3 3 2 3 3
1 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 1 2 2 1 2 2 1 2 2
3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1 3 1 1
2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3 2 3 3

Before applying a rule, audit the demonstrations: identify the relevant objects/colors and describe how the changed cells relate to them. Check the proposed rule against every input/output pair, including cells that stay unchanged; reject or revise it if even one pair disagrees. Do not infer a rule from only the endpoints or one example when the other examples constrain which cells change. Then apply the verified rule to the test, checking the grid dimensions and changed regions.

Give the output grid for the test input. End your response with the grid inside <answer></answer> tags as a JSON list of rows, for example:
<answer>[[0, 1, 2], [3, 4, 5]]</answer>
Put nothing else inside the tags.

Make this a fresh, independent solve: do not assume or reuse any earlier proposed rule or grid. Infer a concrete rule from the training pairs, check that it reproduces every demonstrated output, then apply it to the test input. Verify the dimensions and changed cells against that rule before returning the grid in <answer> tags, with nothing else inside the tags.

Output: The demonstrations show nested objects packed into the lower-left of the enclosing frame’s interior: the secondary frame is placed first, then smaller objects are placed in its cavity. This matches all three examples. In the test, the 6 frame fits in the outer 8 frame, with the 4 and 9 shapes packed into the 6 frame’s interior.

<answer>[[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 8], [8, 6, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 0, 0, 4, 4, 4, 4, 0, 6, 0, 0, 8], [8, 6, 0, 0, 4, 4, 4, 4, 0, 6, 0, 0, 8], [8, 6, 9, 9, 4, 4, 4, 4, 0, 6, 0, 0, 8], [8, 6, 9, 9, 0, 0, 0, 0, 0, 6, 0, 0, 8], [8, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]</answer>


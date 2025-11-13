CS 111 Project 5 - README
=============================
DEFINITION OF "BEST"
--------------------
My algorithm defines "best" as the flattest path possible. Meaning the path that 
minimizes elevation changes from one step to the next. This would come in handy for a 
hiking scenario where you want to conserve energy and avoid steep climbs or 
descents. A flatter path is easier to walk and requires less physical effort.


HOW THE ALGORITHM WORKS
------------------------
The algorithm starts at the middle row on the western (left) edge of the map and 
works its way east, one column at a time.

At each step, the algorithm looks at three possible directions:
1. Forward (stay in the same row)
2. Forward-up (move to the row above)
3. Forward-down (move to the row below)

For each of these three options, the algorithm calculates how much the elevation 
would change. Then it picks the option with the smallest elevation change. This 
decision is made at every single step from west to east.

If a direction would go outside the map boundaries (too far up or down), that 
option is ignored.


COST METRIC
-----------
Metric Name: Total Elevation Change

How it's calculated:
The cost metric is the sum of all elevation changes along the entire path. 
For each step in the path, I calculate the absolute difference between the 
current elevation and the next elevation, then add all these differences together.

Formula: Total Cost = |elev1 - elev2| + |elev2 - elev3| + ... + |elevN-1 - elevN|

Why it measures what the algorithm values:
This metric directly measures flatness. A lower total means the path had smaller 
elevation changes throughout, which is exactly what the algorithm tries to achieve 
at each step. The metric is a perfect match for the algorithm's goal of staying 
as flat as possible.


KEY CODE SNIPPET
----------------
Here is the core decision-making logic of my algorithm:

```python
# Calculates elevation change 
best_row = forward_row
forward_elev = grid[forward_row][col + 1]
best_change = abs(forward_elev - current_elevation)  # Start with forward option

# Check forward-up 
if forward_up_row >= 0:
    up_elev = grid[forward_up_row][col + 1]
    up_change = abs(up_elev - current_elevation)
    if up_change < best_change:  # If this is flatter, choose it
        best_change = up_change
        best_row = forward_up_row

# Check forward-down
if forward_down_row < rows:
    down_elev = grid[forward_down_row][col + 1]
    down_change = abs(down_elev - current_elevation)
    if down_change < best_change:  # If this is flatter, choose it
        best_change = down_change
        best_row = forward_down_row

# Move to the row with smallest elevation change
current_row = best_row
```

This code compares the three possible moves and selects whichever one has the 
smallest absolute elevation change, which keeps the path as flat as possible.
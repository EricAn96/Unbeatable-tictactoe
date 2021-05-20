WIN_CONDITIONS = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
comp_tiles = [5]
user_tiles = [1, 6]

computer_pick = None

for condition in WIN_CONDITIONS:
    tiles_taken = user_tiles + comp_tiles
    check = [pick for pick in condition if pick in tiles_taken]
    if len(check) == 1:
        choice = [pick for pick in condition if pick not in check]

print(computer_pick)
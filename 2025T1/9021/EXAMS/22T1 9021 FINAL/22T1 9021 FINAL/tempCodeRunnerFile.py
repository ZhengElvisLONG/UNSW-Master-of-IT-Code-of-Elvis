diffs = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]
    
    if grid[i][j] == '*':
        return 0
    current = grid[i][j]
    max_num = current
    if grid[i][j] == upper_bound:
        return upper_bound
    for dx, dy in diffs:
        a, b = i + dx, j + dy
        if grid[a][b] == grid[i][j] + 1:
            found = explore_from(grid, upper_bound, a, b)
            if found > max_num:
                max_num = found
                if max_num == upper_bound:
                    return max_num
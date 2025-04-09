# 测试用例
grid_1 = (
    '  *   ',
    ' **** ',
    '***** ',
    '******',
    ' **** ',
    '  **  '
)
grid_2 = (' *       ',
 '***   ** ',
 ' *** *** ',
 ' ***  *  ',
 '****     ',
 ' **      '
 )
# 显示原始网格
display(*grid_2)
print("Boundary:")
# 显示最上最左多边形的边界
display_leftmost_topmost_boundary(*grid_2)
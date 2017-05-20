rows = 'ABCDEFGHI'
cols = '123456789'
cols_inverted = cols[::-1]

main_diagonal_unit = [rows[i] + cols[i] for i in range(0, len(rows))]
reverse_diagonal_unit = [rows[i] + cols_inverted[i] for i in range(0, len(rows))]
print(main_diagonal_unit)
print(reverse_diagonal_unit)
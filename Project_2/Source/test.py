from sympy import*

# KB = set()
# #(1, 1)
# KB.add(Not(symbols('P11')))
# KB.add(Not(symbols('W11')))
# KB.add(Not(symbols('S11')))
# KB.add(Not(symbols('B11')))

# #(1, 2)
# KB.add(Not(symbols('P12')))
# KB.add(Not(symbols('W12')))
# KB.add(symbols('S12'))
# KB.add(Not(symbols('B12')))
# KB.add(Or(symbols('W13'), symbols('W22')))
# KB.add(Equivalent(symbols('W13'), And(symbols('S12'), symbols('S14'), symbols('S23'))))
# KB.add(Equivalent(symbols('W22'), And(symbols('S12'), symbols('S23'), symbols('S21'), symbols('S32'))))
# print('P13 va ~P13')
# print(not satisfiable(And(*KB, Not(symbols('P13')))))
# print(not satisfiable(And(*KB, symbols('P13'))))

# print('P22 va ~P22')
# print(not satisfiable(And(*KB, Not(symbols('P22')))))
# print(not satisfiable(And(*KB, symbols('P22'))))
# #(2, 1)
# KB.add(Not(symbols('P21')))
# KB.add(Not(symbols('W21')))
# KB.add(symbols('B21'))
# KB.add(Not(symbols('S21')))
# KB.add(Or(symbols('P22'), symbols('P31')))
# KB.add(Equivalent(symbols('P22'), And(symbols('B12'), symbols('B21'), symbols('B32'), symbols('B23'))))
# KB.add(Equivalent(symbols('P31'), And(symbols('B21'), symbols('B32'), symbols('B41'))))
# print('P31 va ~P31')
# print(not satisfiable(And(*KB, Not(symbols('P31')))))
# print(not satisfiable(And(*KB, symbols('P31'))))

# print('W22 va ~W22')
# print(not satisfiable(And(*KB, Not(symbols('W22')))))
# print(not satisfiable(And(*KB, symbols('W22'))))
temp = [(1, 1), (1, 2)]
l = [(1, 1), (5, 4), (3, 2), (1, 2)]
for t in temp:
    if t in l:
        l.remove(t)
print(l)
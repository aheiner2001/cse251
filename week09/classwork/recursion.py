

# def factorial_rec(n):
#     # base case 
#     if n ==1:
#         return 1
    
#     product = n * (factorial_rec(n-1))
# fac = factorial_rec(5)
# print(fac)

# assert fac == 120

#  n = 5 : product  = 5 * fact(4)
# n = 4 : product = 4 * fact(3)
# n = 3 : product = 3 * fact(2)
# n = 2 : product = 2 * fact(1)
# n = 1 : product = 1
# product = 2 * 1 = 2
# product = 3 * 2 = 6     
# product = 4 * 6 = 24
# product = 5 * 24 = 120  


# with map
def factorial_rec(n, values):
    # base case 
    if n ==1:
        values[n] = 1
        return 1
    

    
    product = n * factorial_rec(n-1,values )
    values[n] = product
    return product

values = {}
fac = factorial_rec(5, values)
print(fac)
print(values)

assert fac == 120

#  n = 5 : product  = 5 * fact(4)
# n = 4 : product = 4 * fact(3)
# n = 3 : product = 3 * fact(2)
# n = 2 : product = 2 * fact(1)
# n = 1 : product = 1
# product = 2 * 1 = 2
# product = 3 * 2 = 6     
# product = 4 * 6 = 24
# product = 5 * 24 = 120  
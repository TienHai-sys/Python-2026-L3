"""Lab Session 1: Python Basics.ipynb"""
# Problem 1
print("Problem 1:")
radius = float(input("Enter circle radius? "))
area = 3.14 * radius ** 2
print("Circle area =", area)

# Problem 2
print("Problem 2:")
celsius = float(input("Enter the temperature in Celsius?"))
fahrenheit = celsius * 9 / 5 + 32
print(celsius, "(C) =", fahrenheit, "(F)")

#Problem 3
print("Problem 3:")
num = int(input("Enter the number? "))
is_prime = True
if num< 2:
  is_prime = False
else:
  for i in range(2, num):
    if num % i == 0:
      is_prime = False
      break

if is_prime:
  print(num, "is a prime number")
else:
  print(num, "is a NOT prime number")
    
# Problem 4
print("Problem 4:")
num = int(input("Enter the number? "))

total = 0
for i in range(1, num):
  if num % i == 0:
    total += i

if total == num:
  print(num, "is a perfect number")
else:
  print(num, "is a NOT perfect number")
    
#Problem 5
print("Problem 5:")
colors = ["White", "Black", "Blue", "Red", "Yellow", "Purple", "Pink", "Gray", "Brown", "Orange"]
favourite = input("Enter your favourite color? ")

if favourite in colors:
  index = colors.index(favourite)
  print("Your color is at index", index, "in my list")
else:
  print("Sorry, I could not find your color")
    
#Problem 6
print("Problem 6:")
range1 = list(range(0, 7))
range2 = list(range(1, 11, 3))
range3 = list(range(5, 0, -1))
range4 = list(range(6, -3, -2))

print("range1:", range1)
print("range2:", range2)
print("range3:", range3)
print("range4:", range4)

# Problem 7
print("Problem 7:")
def remove_dollar_sign(s):
    return s.replace("$", "")
# Example
price = remove_dollar_sign("$100")
print(price)

text = remove_dollar_sign("Total: $50, Tax: $5")
print(text)

# Problem 8
print("Problem 8:")
def extract_even(l):
  even_list = []
  for num in l:
    if num % 2 ==0:
      even_list.append(num)
  return even_list

#Example:
result = extract_even([1, 4, 5, -1, 10])
print(result)

#Problem 9
print("Problem 9:")
def factorial(n):
  result = 1
  for i in range(1, n + 1):
    result *= i
  return result

#Example
print(factorial(5))
print(factorial(0))
print(factorial(3))

# Problem 10
print("Problem 10:")
def get_divisors(n):
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors

#Example:
print(get_divisors(12))

# Problem 11
print("Problem 11:")
import math

x1 = float(input("Enter x1: "))
y1 = float(input("Enter y1: "))
x2 = float(input("Enter x2: "))
y2 = float(input("Enter y2: "))

distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
print("Distance =", distance)

# Problem 12
print("Problem 12:")
def print_pattern(m, n):
    for row in range(m):
        for col in range(n):
            if row == 0 or row == m - 1 or col == 0 or col == n - 1:
                print("*", end=" ")
            else:
                print(" ", end=" ")
        print()

print_pattern(5, 5)

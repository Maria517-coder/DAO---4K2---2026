import random
numeros = set()

todos = [random.randint(1,20) for i in range(10)]
numeros = set(todos)

print(numeros)
print(len(numeros))
print(todos)
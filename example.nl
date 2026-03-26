# Test Import
lyaau utils
lekha("10 + 5 =", utils.sum(10, 5))

# Test Standard Library (math and string)
lekha("Pi is:", math.pi)
lekha("2^3 is:", math.pow(2, 3))

greeting = "Namaste NeLang"
lekha("Uppercase:", string.uppercase(greeting))
lekha("Length:", string.length(greeting))

# Generic Function Blocks
karya test(x):
    yadi x > 5:
        lekha("Greater")
    tyasovaye:
        lekha("Smaller")

test(10)

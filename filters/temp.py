menu = {
    "Baja Taco": 4.25,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}
#print(menu)
value = 0
while True:
    try:
        entered = str(input("Item: ")).title()
        if entered in menu:
            #print(entered)
            value += menu[entered]
        else:
            pass
    except EOFError:
        break

print(value)
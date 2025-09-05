shoppinglist = {}

while True:
    try:
        entered = input("").upper()
        if entered in shoppinglist:
            shoppinglist[entered] += 1
        else:
            shoppinglist[entered] = 1
    except:
        break
for item in shoppinglist:
    print(f'{shoppinglist[item]} {str(item)}')
i = 0
while i < 5:
    if i < 2:
        i += 1
        continue
    print(i)
    if i >= 4:
        break
    i += 1
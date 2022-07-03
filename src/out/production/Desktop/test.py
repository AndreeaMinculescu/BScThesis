list_pos = [1, 2, 3, 1, 0, 5, 2, 5, 6]
count = 0
idx = 1

while idx < len(list_pos):
    flag = "ascend"
    print(idx)
    if list_pos[idx] < list_pos[idx-1]:
        flag = "descend"

    while idx < len(list_pos):
        if flag == "ascend":
            if list_pos[idx] < list_pos[idx-1]:
                break

        else:
            if list_pos[idx] > list_pos[idx-1]:
                break

        idx += 1

    count += 1

print(count)

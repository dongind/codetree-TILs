def put_sushi(x, t, name, sushi_num):
    if not rotate_sushi.get((x - t) % L, False):
        rotate_sushi[(x - t) % L] = {name : 1}

    elif not rotate_sushi[(x - t) % L].get(name, False):
        rotate_sushi[(x - t) % L][name] = 1

    else:
        rotate_sushi[(x - t) % L][name] += 1

    return sushi_num + 1


def enter_sushi(x, name, n, user_num):
    user_list[x] = {"name": name, "count": n}
    return user_num + 1


def leave_sushi(x, user_num):
    user_list.pop(x, None)
    return user_num - 1


def eat_sushi(t, user_num, sushi_num):
    if not user_num or not sushi_num:
        return user_num, sushi_num

    for i in range(L):
        if not user_list.get(i, False):
            continue

        if not rotate_sushi.get((i - t) % L , False):
            continue

        sushi_table = rotate_sushi[(i - t) % L]
        user_name, count = user_list[i]["name"], user_list[i]["count"]
        pop_list = []

        for name in sushi_table.keys():
            if not name == user_name:
                continue

            sushi_num -= sushi_table[name]

            if count > sushi_table[name]:
                user_list[i]["count"] -= sushi_table[name]
                pop_list.append(name)

            elif count == sushi_table[name]:
                user_num = leave_sushi(i, user_num)
                pop_list.append(name)

            else:
                sushi_table[name] -= count
                user_num = leave_sushi(i, user_num)

        for name in pop_list:
            sushi_table.pop(name, None)

    return user_num, sushi_num


L, Q = map(int, input().split())
x_pos = 0
user_num = 0
sushi_num = 0
rotate_sushi = dict()
user_list = dict()
last_t = 0


for _ in range(Q):

    command = input().split()
    camera_flag = False

    while last_t < int(command[1]) and user_num and sushi_num:
        user_num, sushi_num = eat_sushi(last_t, user_num, sushi_num)
        last_t += 1

    if command[0] == "100":
        t, x, name = command[1:]
        sushi_num = put_sushi(int(x), int(t), name, sushi_num)

    if command[0] == "200":
        t, x, name, n = command[1:]
        user_num = enter_sushi(int(x), name, int(n), user_num)

    if command[0] == "300":
        t = command[1]
        camera_flag = True

    user_num, sushi_num = eat_sushi(int(t), user_num, sushi_num)

    if camera_flag:
        print(user_num, sushi_num)

    last_t = int(t) + 1
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

    user_pop_list = []

    for x in user_list.keys():

        if not rotate_sushi.get((x - t) % L, False):
            continue

        sushi_table = rotate_sushi[(x - t) % L]
        user_name, count = user_list[x]["name"], user_list[x]["count"]

        if not sushi_table.get(user_name, False):
            continue

        if count > sushi_table[user_name]:
            user_list[x]["count"] -= sushi_table[user_name]
            sushi_num -= sushi_table[user_name]
            sushi_table.pop(user_name, None)

        elif count == sushi_table[user_name]:
            user_pop_list.append(x)
            sushi_num -= sushi_table[user_name]
            sushi_table.pop(user_name, None)

        else:
            sushi_table[user_name] -= count
            user_pop_list.append(x)

    for user_pos in user_pop_list:
        user_num = leave_sushi(user_pos, user_num)

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
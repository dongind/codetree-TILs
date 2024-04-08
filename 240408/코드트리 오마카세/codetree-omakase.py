def put_sushi(x, t, name, sushi_num):
    rotate_sushi[(x - t) % L].append(name)
    return sushi_num + 1


def enter_sushi(x, name, n, user_num):
    user_list[x] = ({"name": name, "count": n})
    return user_num + 1


def leave_sushi(x, user_num):
    user_list[x] = False
    return user_num - 1


def eat_sushi(t, user_num, sushi_num):
    if not user_num or not sushi_num:
        return user_num, sushi_num

    for i in range(L):
        if not user_list[i]:
            continue
        sushi_table = rotate_sushi[(i - t) % L]
        user_name = user_list[i]["name"]

        for name in sushi_table:
            if name == user_name:
                user_list[i]["count"] -= 1
                sushi_num -= 1
                if not user_list[i]["count"]:
                    user_num = leave_sushi(i, user_num)
        rotate_sushi[(i - t) % L] = list(filter(lambda x: x != user_name, sushi_table))

    return user_num, sushi_num


L, Q = map(int, input().split())
user_num = 0
sushi_num = 0
rotate_sushi = [[] for _ in range(L)]
user_list = [False for _ in range(L)]
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
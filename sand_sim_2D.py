import random

height = 16
width = 32

box = [[0 for _ in range(width)] for _ in range(height)]

def step(l_box):
    n_box = [[0 for _ in range(width)] for _ in range(height)]
    
    for y in range(height - 1, -1, -1):
        for x in range(width):
            if l_box[y][x] == 1:
                if y > 0:
                    if l_box[y - 1][x] == 0:
                        n_box[y - 1][x] = 1
                    else:
                        poses = []
                        if x > 0 and l_box[y - 1][x - 1] == 0 and n_box[y - 1][x - 1] == 0:
                            poses.append(x - 1)
                        if x < width - 1 and l_box[y - 1][x + 1] == 0 and n_box[y - 1][x + 1] == 0:
                            poses.append(x + 1)
                        if (len(poses) == 0):
                            n_box[y][x] = 1
                        else:
                            n_box[y - 1][poses[random.randrange(0, len(poses))]] = 1
                else:
                    n_box[y][x] = 1
    
    return list(n_box)

def output(box):
    for y in range(height):
        for x in range(width):
            if box[height - y - 1][x]:
                print('#',end = '')
            else:
                print('.',end = '')
        print()

box[height - 1][int(width / 2)] = 1
#box[0][int(width / 2)] = 1

while(True):
    box = step(box)
    box[height - 1][int(width / 2)] = 1
    output(box)
    a = input()
    if a == "q":
        break
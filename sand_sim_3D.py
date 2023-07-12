import random
import math

class vec3:
    x = 0
    y = 0
    z = 0
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, a):
        return vec3(self.x + a.x, self.y + a.y, self.z + a.z)
    def __sub__(self, a):
        return vec3(self.x - a.x, self.y - a.y, self.z - a.z)

def rotate_y(c, angle, p):
    sn = math.sin(angle)
    cs = math.cos(angle)
    
    p.x -= c.x
    p.z -= c.z
    
    x_new = p.x * cs - p.z * sn
    z_new = p.x * sn + p.z * cs
    
    p.x = c.x + x_new
    p.z = c.z + z_new
    
    return p

class vec2:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, a):
        return vec3(self.x + a.x, self.y + a.y)
    def __sub__(self, a):
        return vec3(self.x - a.x, self.y - a.y)

w_height = 10
w_width = 10
camera = vec3(0, 0, -5)
camera_angle = vec3(0, 0, 0)

screen = [[0 for _ in range(w_width)] for _ in range(w_height)]

def math_sign(a):
    if a > 0:
        return 1
    if a < 0:
        return -1
    return 0

def abs_ceil(a):
    sign = math_sign(a)
    a = math.ceil(abs(a)) * sign
    return a

def abs_round(a):
    sign = math_sign(a)
    a = round(abs(a)) * sign
    return a

def show_screen():
    for y in range(w_height):
        for x in range(w_width):
            print(screen[y][x], end='')
        print()

def clear_screen():
    for y in range(w_height):
        for x in range(w_width):
            screen[y][x] = '.'
            
def put(p, color):
    if (p.y >= 0 and p.y < w_height and p.x >= 0 and p.x < w_width):
        screen[int(p.y)][int(p.x)] = color

#(p.x + p.y) / (p.y + p.y) * w
#h(1 - (p.x + p.y) / (2p.y))
def render(p):
    p = rotate_y(camera, camera_angle.y, p)
    p = p - camera
    if p.z == 0:
        p.z = 0.00000001
    return vec2(int((p.x + p.z) / (2*p.z) * w_width), int((1 - (p.y + p.z) / (2*p.z)) * w_height))

box_size = vec3(10, 5, 10)

box = [[[0 for _ in range(box_size.x)] for _ in range(box_size.y)] for _ in range(box_size.z)]

# box[z][y][x]

def render_box():
    for z in range(box_size.z):
        for y in range(box_size.y):
            for x in range(box_size.x):
                if box[z][y][x] == 1:
                    pos = render(vec3(x - box_size.x / 2, y - box_size.y / 2, z - box_size.z / 2))
                    put(pos, '#')

def step(l_box):
    n_box = [[[0 for _ in range(box_size.x)] for _ in range(box_size.y)] for _ in range(box_size.z)]
    
    for z in range(box_size.z):
        for y in range(box_size.y):
            for x in range(box_size.x):
                if (l_box[z][y][x] == 1):
                    check_poses = [
                        vec3(x - 1, y - 1, z + 1),
                        vec3(x, y - 1, z + 1),
                        vec3(x + 1, y - 1, z + 1),
                        vec3(x - 1, y - 1, z),
                        vec3(x + 1, y - 1, z),
                        vec3(x - 1, y - 1, z - 1),
                        vec3(x, y - 1, z - 1),
                        vec3(x + 1, y - 1, z - 1)
                    ]
                    found_pos = False
                    if y > 0:
                        for p in check_poses:
                            if p.z >= 0 and p.z < box_size.z and p.x >= 0 and p.x < box_size.z and l_box[p.z][p.y][p.x] == 0 and n_box[p.z][p.y][p.x] == 0:
                                found_pos = True
                                break
                    
                    if (y > 0 and l_box[z][y - 1][x] == 0 and n_box[z][y - 1][x] == 0):
                        n_box[z][y - 1][x] = 1
                    elif found_pos:
                        angle = 0
                        i = 0
                        while True:
                            angle = random.randrange(0, 62832) / 10000
                            ray = vec3(1, -1, 0)
                            ray = rotate_y(vec3(0, 0, 0), angle, ray)
                            ray = vec3(abs_round(ray.x), round(ray.y), abs_round(ray.z))
                            
                            ray = ray + vec3(x, y, z)
                            if ray.x >= 0 and ray.x < box_size.x and ray.z >= 0 and ray.z < box_size.z and l_box[ray.z][ray.y][ray.x] == 0 and n_box[ray.z][ray.y][ray.x] == 0:
                                n_box[ray.z][ray.y][ray.x] = 1
                                break
                            i += 1
                    else:
                        n_box[z][y][x] = 1
    return list(n_box)

box[int(box_size.z / 2)][0][int(box_size.x / 2)] = 1
spawn = True

while (True):
    clear_screen()
    render_box()
    if spawn:
        box[int(box_size.z / 2)][box_size.y - 1][int(box_size.x / 2)] = 1
    spawn = not spawn
    box = step(box)
    show_screen()
    for x in range(box_size.x):
        for z in range(box_size.z):
            print(box[z][0][x], end='')
        print()
    str = input()
    if str == "q":
        break
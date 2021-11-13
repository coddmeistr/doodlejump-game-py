from platform import *


class PlatformManager:
    def __init__(self, base):
        self.base = base

        self.last_platform_height = 0
        self.jumped_platform_height = 0
        self.tracking_platform = None
        self.jumper = None

    def first_platforms_layer(self):
        wnd_w = self.base.resolution.wnd_w
        wnd_h = self.base.resolution.wnd_h

        if self.jumper().jump_time * c.framerate * self.jumper().offsetX >= wnd_w / 2:
            max_platform_distance = self.jumper().JUMP_HEIGHT + 0
        else:
            max_platform_distance = self.jumper().JUMP_HEIGHT + 0

        heights = list()
        for _ in range(random.randint(13, 30)):
            heights.append(random.randint(min(200, max_platform_distance - 1), max_platform_distance))
        heights.append(random.randint(wnd_h, wnd_h + 100))
        maximum_height = max(heights)

        platforms = []
        heights.sort()
        for h in heights:
            p = self.random_platform(0, 0, [100, 0, 0, 0])
            x = random.randint(0, wnd_w - p.width)
            y = wnd_h - h
            p.move(x, y)

            platforms.append(p)

        self.tracking_platform = platforms[-1]
        self.last_platform_height = maximum_height
        return platforms

    def another_platforms(self):
        wnd_w = self.base.resolution.wnd_w
        wnd_h = self.base.resolution.wnd_h

        if self.jumper().jump_time * c.framerate * self.jumper().offsetX >= wnd_w / 2:
            max_platform_distance = self.jumper().JUMP_HEIGHT + 0
        else:
            max_platform_distance = self.jumper().JUMP_HEIGHT + 0

        heights = list()
        for _ in range(random.randint(5, 15)):
            heights.append(random.randint(wnd_h, wnd_h + max_platform_distance))
        maximum_height = max(heights)

        platforms = []
        heights.sort()
        for h in heights:
            x = random.randint(0, wnd_w)
            y = wnd_h - h
            p = self.random_platform(x, y, [80, 5, 5, 5, 5])

            platforms.append(p)

        self.tracking_platform = platforms[-1]
        self.last_platform_height = maximum_height
        return platforms

    def create_saving_platform(self):
        wnd_w = self.base.resolution.wnd_w
        wnd_h = self.base.resolution.wnd_h

        p = self.random_platform(0, 0, [0, 0, 0, 0, 100])
        x = random.randint(0, wnd_w - p.width)
        y = wnd_h - random.randint(0, self.jumped_platform_height) - self.jumper().JUMP_HEIGHT
        p.move(x, y)
        return p

    def create_plato(self):
        wnd_w = self.base.resolution.wnd_w
        wnd_h = self.base.resolution.wnd_h

        platforms = []
        p = self.random_platform(0, 0, [100, 0, 0, 0, 0])
        x = 0
        y = wnd_h - p.height
        p.move(x, y)
        width = p.width

        platforms.append(p)

        for i in range(1, (wnd_w // width) + 1):
            p = self.random_platform(0, 0, [100, 0, 0, 0])
            x = i * p.width
            y = wnd_h - p.height
            p.move(x, y)

            platforms.append(p)

        return platforms

    def random_platform(self, x, y, chances_list):
        # 1. DEFAULT PLATFORM, 2. MOVING PLATFORM 3. FAKE PLATFORM
        chances_sum = 0
        for i in chances_list:
            chances_sum += i
        if chances_sum != 100:
            raise NameError("chances_list EXCEPTION, INVALID CHANCES.")
        loto = []
        for i in range(len(chances_list)):
            for j in range(0, chances_list[i]):
                loto.append(i)
        res = loto[random.randint(0, 99)]
        if res == 0:
            return Platform(x, y, self.base)
        elif res == 1:
            speed = 6
            return MovingPlatform(x, y, speed, self.base)
        elif res == 2:
            return FakePlatform(x, y, self.base)
        elif res == 3:
            return AbsorbPlatform(x, y, self.base)
        elif res == 4:
            return SteinsPlatform(x, y, self.base)

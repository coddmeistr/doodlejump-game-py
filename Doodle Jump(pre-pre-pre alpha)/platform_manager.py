from platform import *


class PlatformManager:
    def __init__(self):
        self.last_platform_height = 0
        self.jumped_platform_height = 0
        self.tracking_platform = None
        self.jumper = None

    def first_platforms_layer(self):
        if self.jumper().jump_time * c.framerate * self.jumper().offsetX >= c.win_width / 2:
            max_platform_distance = self.jumper().JUMP_HEIGHT + 0
        else:
            max_platform_distance = self.jumper().JUMP_HEIGHT + 0

        heights = list()
        for _ in range(random.randint(13, 30)):
            heights.append(random.randint(min(200, max_platform_distance - 1), max_platform_distance))
        heights.append(random.randint(c.win_height, c.win_height + 100))
        maximum_height = max(heights)

        platforms = []
        heights.sort()
        for h in heights:
            p = self.random_platform(0, 0, [100, 0, 0, 0])
            x = random.randint(0, c.win_width - p.width)
            y = c.win_height - h
            p.move(x, y)

            platforms.append(p)

        self.tracking_platform = platforms[-1]
        self.last_platform_height = maximum_height
        return platforms

    def another_platforms(self):
        if self.jumper().jump_time * c.framerate * self.jumper().offsetX >= c.win_width / 2:
            max_platform_distance = self.jumper().JUMP_HEIGHT + 0
        else:
            max_platform_distance = self.jumper().JUMP_HEIGHT + 0

        heights = list()
        for _ in range(random.randint(5, 15)):
            heights.append(random.randint(c.win_height, c.win_height + max_platform_distance))
        maximum_height = max(heights)

        platforms = []
        heights.sort()
        for h in heights:
            p = self.random_platform(0, 0, [0, 0, 0, 0, 100])
            x = random.randint(0, c.win_width - p.width)
            y = c.win_height - h
            p.move(x, y)

            platforms.append(p)

        self.tracking_platform = platforms[-1]
        self.last_platform_height = maximum_height
        return platforms

    def create_saving_platform(self):
        p = self.random_platform(0, 0, [0, 0, 0, 0, 100])
        x = random.randint(0, c.win_width - p.width)
        y = c.win_height - random.randint(0, self.jumped_platform_height) - self.jumper().JUMP_HEIGHT
        p.move(x, y)
        return p

    def create_plato(self):
        platforms = []
        p = self.random_platform(0, 0, [100, 0, 0, 0, 0])
        x = 0
        y = c.win_height - p.height
        p.move(x, y)
        width = p.width

        platforms.append(p)

        for i in range(1, (c.win_width // width) + 1):
            p = self.random_platform(0, 0, [100, 0, 0, 0])
            x = i * p.width
            y = c.win_height - p.height
            p.move(x, y)

            platforms.append(p)

        return platforms

    @staticmethod
    def random_platform(x, y, chances_list):
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
            return Platform(x, y)
        elif res == 1:
            speed = 6
            return MovingPlatform(x, y, speed)
        elif res == 2:
            return FakePlatform(x, y)
        elif res == 3:
            return AbsorbPlatform(x, y)
        elif res == 4:
            return SteinsPlatform(x, y)

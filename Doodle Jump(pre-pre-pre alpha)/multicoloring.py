import pygame
import colors
import weakref


# Class that allows your objects to change colors every tick
# Works with weakref referencing
class Multicolor:
    def __init__(self):
        self.triggering_objects = []

    def add_object(self, obj, left_color=(0, 0, 0), right_color=(255, 255, 255)):
        work_dict = {"object": obj, "left_color": left_color, "right_color": right_color,
                     "original": tuple(obj().color), "current": list(left_color)}

        for i in range(0, 3):
            work_dict[str(i)] = -(left_color[i]-right_color[i])

        obj().color = tuple(work_dict["current"])
        self.triggering_objects.append(work_dict)

    def update(self):
        for work_dict in self.triggering_objects:
            if work_dict["object"]() is None:
                self.triggering_objects.remove(work_dict)
                continue

            new_color = work_dict["current"]
            for i in range(0, 3):
                try:
                    delta = int(work_dict[str(i)] / abs(work_dict[str(i)]))
                except ZeroDivisionError:
                    delta = 0
                new_color[i] += delta
                work_dict[str(i)] -= delta
                if work_dict[str(i)] == 0:
                    if new_color[i] == work_dict["left_color"][i]:
                        work_dict[str(i)] = -(work_dict["left_color"][i] - work_dict["right_color"][i])
                    else:
                        work_dict[str(i)] = work_dict["left_color"][i] - work_dict["right_color"][i]

            work_dict["current"] = new_color
            work_dict["object"]().color = tuple(new_color)

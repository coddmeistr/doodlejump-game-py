import colors
import random


# Game's window settings
win_width = 800  # 800
win_height = 600  # 600
framerate = 60


# Jumper settings
jumper_speedX = 10
jumper_speedY = 6
jump_height = 1000
jump_duration = 1


# menu
font_size = 40
font_better = 'fonts/BeVietnamPro-Light'
font_name = 'Arial'
font_size_trackers = 15
button_text_color = colors.WHITE
button_back_color = colors.BLACK
button_normal_back_color = colors.BLACK
button_hover_back_color = colors.BLUE
button_pressed_back_color = colors.GREEN


# delays(seconds)
after_lost_pause = 5


# platforms
def duration_moving_platforms():
    return (random.random()*1.5)+0.5



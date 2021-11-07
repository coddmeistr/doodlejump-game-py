from MODULES import *


# Game's window settings
win_width = 800  # 800
win_height = 600  # 600
framerate = 60


# Jumper settings
jumper_speedX = 10
jumper_speedY = 6
jump_time = 1
start_speed = 40


# menu
font_size = 40
font_name = 'fonts/arial.ttf'
font_size_trackers = 15
button_text_color = colors.WHITE
button_back_color = colors.BLACK
button_normal_back_color = colors.BLACK
button_hover_back_color = colors.BLUE
button_pressed_back_color = colors.GREEN

slider_normal_back_color = colors.BLUE
slider_hover_back_color = colors.GREEN
slider_pressed_back_color = colors.RED1


# delays(seconds)
after_lost_pause = 5


# platforms
def duration_moving_platforms():
    return (random.random()*1.5)+0.5

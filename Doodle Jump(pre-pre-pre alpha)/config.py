from MODULES import *


# Game's window settings
win_width = 800  # 800
win_height = 600  # 600
start_win_width = 1500
start_win_height = 800
framerate = 60


# Jumper settings
jumper_speedX = 10
jumper_speedY = 6
jump_time = 1       # 1
start_speed = 40    # 40


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
after_lost_pause = 4


# platforms
def duration_moving_platforms():
    return (random.random()*1.5)+0.5


# platforms sizes
s_fake_plat = (58, 32)
s_runic_plat = (58, 42)
s_normal_plat = (58, 34)
# jumper's size
s_jumper = (32, 32)
# menu buttons
s_menu_button_play = (146, 69)
s_menu_button_settings = (10, 10)
s_menu_button_exit = (10, 10)
s_menu_settings_button_sound = (10, 10)
s_menu_settings_button_music = (10, 10)
s_menu_settings_button_difficulty = (10, 10)
s_menu_settings_button_wnd_size = (10, 10)
s_menu_settings_button_back = (10, 10)
# other
s_game_lost_banner = (140, 126)
s_slider_slider = (16, 26)
# animation
s_dust_fall_anim = (58, 50)
s_rotating_gear_anim = (64, 64)
# movies
s_steins_gate_movie = (800, 600)
# backgrounds
s_default_back = (1680, 776)
s_level1_back = (800, 1000)


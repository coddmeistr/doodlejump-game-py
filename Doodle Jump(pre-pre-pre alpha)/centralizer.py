
def get_centralized_params(font_obj, text, border_pixels_w, border_pixels_h):
    text_width, text_height = font_obj.size(text)

    width = text_width + border_pixels_w * 2
    padding_x = border_pixels_w

    height = text_height + border_pixels_h * 2
    padding_y = border_pixels_h

    return text, width, height, padding_x, padding_y

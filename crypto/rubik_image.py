import cv2
import numpy as np

def number_to_np(number):
    # WhiteTop
    if number >= 9 and number <= 17:
        return [243, 243, 243]
    # LeftOrange
    if number >= 27 and number <= 35:
        return [2, 156, 255]
    # FrontGreen
    if number >= 0 and number <= 8:
        return [0, 255, 1]
    # RightRed
    if number >= 36 and number <= 44:
        return [9, 251, 252]
    # BackYellow
    if number >= 45 and number <= 53:
        return [0, 0, 254]
    # BotBlue
    if number >= 18 and number <= 26:
        return [254, 126, 0]


def cube_to_np(cube):
    np_cube = []
    order = ['top', 'left', 'front', 'right', 'back', 'bot']
    for i in order:
        face = []
        for count, j in enumerate(cube[i]):
            if count % 3 == 0:
                layer = []
                layer.append(number_to_np(j))
            elif count % 3 == 1:
                layer.append(number_to_np(j))
            else:
                layer.append(number_to_np(j))
                face.append(layer)
        np_cube.append(face)
    return np_cube

def np_to_pixel(cube_np):
    white = [255,255,255]
    pxiel_cube = np.asarray([[white, white, white, cube_np[0][0][0], cube_np[0][0][1], cube_np[0][0][2], white, white, white, white, white, white],
                       [white, white, white, cube_np[0][1][0], cube_np[0][1][1], cube_np[0][1][2], white, white, white, white, white, white],
                       [white, white, white, cube_np[0][2][0], cube_np[0][2][1], cube_np[0][2][2], white, white, white, white, white, white],
                       [cube_np[1][0][0], cube_np[1][0][1], cube_np[1][0][2], cube_np[2][0][0], cube_np[2][0][1], cube_np[2][0][2], cube_np[3][0][0], cube_np[3][0][1], cube_np[3][0][2], cube_np[4][0][0], cube_np[4][0][1], cube_np[4][0][2]],
                       [cube_np[1][1][0], cube_np[1][1][1], cube_np[1][1][2], cube_np[2][1][0], cube_np[2][1][1], cube_np[2][1][2], cube_np[3][1][0], cube_np[3][1][1], cube_np[3][1][2], cube_np[4][1][0], cube_np[4][1][1], cube_np[4][1][2]],
                       [cube_np[1][2][0], cube_np[1][2][1], cube_np[1][2][2], cube_np[2][2][0], cube_np[2][2][1], cube_np[2][2][2], cube_np[3][2][0], cube_np[3][2][1], cube_np[3][2][2], cube_np[4][2][0], cube_np[4][2][1], cube_np[4][2][2]],
                       [white, white, white, cube_np[5][0][0], cube_np[5][0][1], cube_np[5][0][2], white, white, white, white, white, white],
                       [white, white, white, cube_np[5][1][0], cube_np[5][1][1], cube_np[5][1][2], white, white, white, white, white, white],
                       [white, white, white, cube_np[5][2][0], cube_np[5][2][1], cube_np[5][2][2], white, white, white, white, white, white]])
    return pxiel_cube

def cube_to_pixel(cube):
    cube_np = cube_to_np(cube)
    tiny_cube = np_to_pixel(cube_np)
    big_cube = cv2.resize(tiny_cube,(1200,900), interpolation=cv2.INTER_NEAREST)
    return big_cube
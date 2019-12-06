import copy
import binascii


def row_turn(cube, facelist1, facelist2, row1, row2, face):
    fakecube = copy.deepcopy(cube)
    for x in range(len(facelist1)):
        for y in range(3):
            cube[facelist1[x]][row1[x][y]] = fakecube[facelist2[x]][row2[x][y]]
    # turns face 3 anti-clockwise
    newlist = [2, 5, 8, 1, 4, 7, 0, 3, 6]
    newlist1 = []
    for x in newlist:
        newlist1.append(fakecube[face][x])
    cube[face] = newlist1
    return cube


def cube_turn(cube, direction, mode):
    fakecube = copy.deepcopy(cube)
    if mode == "e":
        if direction == 1:
            facelist1 = ["right", "back", "left", "front"]
            facelist2 = ["front", "right", "back", "left"]
            row1 = [[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2]]
            row2 = [[0, 1, 2], [0, 1, 2], [0, 1, 2], [0, 1, 2]]
            face3 = "top"
            cube = row_turn(cube, facelist1, facelist2, row1, row2, face3)
            # print("TURN " + str(direction) + mode)

        elif direction == 3:
            facelist1 = ["bot", "back", "top", "front"]
            facelist2 = ["front", "bot", "back", "top"]
            row1 = [[2, 5, 8], [6, 3, 0], [2, 5, 8], [2, 5, 8]]
            row2 = [[2, 5, 8], [2, 5, 8], [6, 3, 0], [2, 5, 8]]
            face3 = "right"
            cube = row_turn(cube, facelist1, facelist2, row1, row2, face3)
            # print("TURN " + str(direction) + mode)

        elif direction == 5:
            facelist1 = ["top", "left", "bot", "right"]
            facelist2 = ["right", "top", "left", "bot"]
            row1 = [[6, 7, 8], [8, 5, 2], [2, 1, 0], [0, 3, 6]]
            row2 = [[0, 3, 6], [6, 7, 8], [8, 5, 2], [2, 1, 0]]
            face3 = "front"
            cube = row_turn(cube, facelist1, facelist2, row1, row2, face3)
            # print("TURN " + str(direction) + mode)

        elif direction == 7:
            facelist1 = ["front", "left", "back", "right"]
            facelist2 = ["right", "front", "left", "back"]
            row1 = [[6, 7, 8], [6, 7, 8], [6, 7, 8], [6, 7, 8]]
            row2 = [[6, 7, 8], [6, 7, 8], [6, 7, 8], [6, 7, 8]]
            face3 = "bot"
            cube = row_turn(cube, facelist1, facelist2, row1, row2, face3)
            # print("TURN " + str(direction) + mode)

        elif direction == 9:
            facelist1 = ["front", "top", "back", "bot"]
            facelist2 = ["bot", "front", "top", "back"]
            row1 = [[0, 3, 6], [0, 3, 6], [8, 5, 2], [0, 3, 6]]
            row2 = [[0, 3, 6], [0, 3, 6], [0, 3, 6], [8, 5, 2]]
            face3 = "left"
            cube = row_turn(cube, facelist1, facelist2, row1, row2, face3)
            # print("TURN " + str(direction) + mode)

        elif direction == 11:
            facelist1 = ["top", "right", "bot", "left"]
            facelist2 = ["left", "top", "right", "bot"]
            row1 = [[0, 1, 2], [2, 5, 8], [8, 7, 6], [6, 3, 0]]
            row2 = [[6, 3, 0], [0, 1, 2], [2, 5, 8], [8, 7, 6]]
            face3 = "back"
            cube = row_turn(cube, facelist1, facelist2, row1, row2, face3)
            # print("TURN " + str(direction) + mode)

        else:
            direction = direction + 1
            for x in range(3):
                cube = cube_turn(cube, direction, "e")

    elif mode == "d":
        for x in range(3):
            cube = cube_turn(cube, direction, "e")

    return cube


def cube_print(cubes):
    for cube in cubes:
        print("Front:{}".format(cube["front"]))
        print("Top:{}".format(cube["top"]))
        print("Bottom:{}".format(cube["bot"]))
        print("Left:{}".format(cube["left"]))
        print("Right:{}".format(cube["right"]))
        print("Back:{}".format(cube["back"]))


def padding(text, text_type, mode):
    if text_type == "key":
        amttopad = 12
        if mode == "d":
            text = text + "0"
            timestopad = len(text) % amttopad
            if timestopad != 0:
                for x in range(amttopad - timestopad):
                    text = text + "1"
            return text

    elif text_type == "query":
        amttopad = 54 * 8

    if mode == "e":
        text = text + "1"
        timestopad = len(text) % amttopad
        if timestopad != 0:
            for x in range(amttopad - timestopad):
                text = text + "0"
    elif mode == "d":
        char_index = len(text) - 1
        while char_index >= 0:
            if text[char_index] == "1":
                return text[:char_index]
            char_index -= 1

    return text


def convtobit(text, mode):
    if mode == "e":
        b = text.encode("ascii")
        a = [""]
        for b1 in b:
            c = bin(b1)
            a[0] = a[0] + c[2:]
        return a[0]
    elif mode == "d":
        realtext = "0b" + text[0:7]
        for x in range(1, len(text) // 7):
            realtext = realtext + "0" + text[x * 7:(x + 1) * 7]
        n = int(realtext, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()


def ciphercube(query, key, mode, encryptedcubes=None):
    cipher_bits = ""
    key_bit = convtobit(key, "e")
    cubes = []
    if mode == "e":
        cube = dict()
        faces = ["front", "top", "bot", "left", "right", "back"]
        if query == "TEST":
            for x in range(6):
                inner_cube = []
                for y in range(9):
                    inner_cube.append((9 * x) + y)
                cube[faces[x]] = inner_cube
            for index, key in enumerate(key_bit):
                if key == "1":
                    cube = cube_turn(cube, index % 12, mode)
            cubes.append(cube)

        else:
            query_bit = convtobit(query, mode)
            padded_query = padding(query_bit, "query", "e")
            for x in range(len(padded_query) // (54 * 8)):
                cubebits = padded_query[x * (54 * 8):((x + 1) * (54 * 8))]
                for y in range(6):
                    inner_cube = []
                    for z in range(9):
                        inner_cube.append(cubebits[((9 * y) + z) * 8:((9 * y) + z + 1) * 8])
                    cube[faces[y]] = inner_cube
                for index, key in enumerate(key_bit):
                    if key == "1":
                        cube = cube_turn(cube, index % 12, mode)
                cubes.append(cube)

            for i in cubes:
                for j in i:
                    for k in i[j]:
                        cipher_bits = cipher_bits + k

    elif mode == "d":
        for cube in encryptedcubes:
            for index, key in reversed(list(enumerate(key_bit))):
                if key == "1":
                    cube = cube_turn(cube, index % 12, mode)
            cubes.append(cube)
        if query != "TEST":
            for i in cubes:
                for j in i:
                    for k in i[j]:
                        cipher_bits = cipher_bits + k
            cipher_bits = padding(cipher_bits, "query", "d")
            cipher_bits = convtobit(cipher_bits, mode)
    return cubes, cipher_bits

# def main():
#     testcubes = []
#     key = "hello"
#     #CUBES FOR DISPLAY
#     cube,ciphertext = ciphercube(testcubes,query = "TEST", key = "",mode = "e")
#     cube3,ciphertext3 = ciphercube(testcubes,query = "TEST", key = key,mode = "e")
#     cube_print(cube3)
#     cube4,ciphertext4 = ciphercube(cube3,query = "TEST", key = key,mode = "d")
#     cube_print(cube4)
#
#
#     #CYPHER CUBES
#     plaintext = "KENNETHYOUSUCK"
#     key = "TESTING"
#     cube1,ciphertext1 = ciphercube(query = plaintext, key = key,mode = "e")
#     answer   = ciphercube(query=ciphertext1, key=key, mode="d")
#     answer == plaintext -> This has to be true
#     cube_print(cube1)
#     print(ciphertext1)
#     cube2,ciphertext2 = ciphercube(cube1,query = "KENNETHYOUSUCK", key = key,mode = "d")
#     cube_print(cube2)
#     print(ciphertext2)
#
# if __name__ == "__main__":
#     main()

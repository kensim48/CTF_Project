import copy
import binascii

def row_turn(cube,facelist1,facelist2,row1,row2,face):
    fakecube = copy.deepcopy(cube)
    for x in range(len(facelist1)):
        for y in range(3):
            cube[facelist1[x]][row1[x][y]] = fakecube[facelist2[x]][row2[x][y]]
    #turns face 3 anti-clockwise
    newlist = [2,5,8,1,4,7,0,3,6]
    newlist1 = []
    for x in newlist:
        newlist1.append(fakecube[face][x])
    cube[face] = newlist1
    return cube

def cube_turn(cube,direction,mode):
    fakecube = copy.deepcopy(cube)
    if mode == "e":
        if direction == 1:
            facelist1 = ["right","back","left","front"]
            facelist2 = ["front","right","back","left"]
            row1 = [[0,1,2],[0,1,2],[0,1,2],[0,1,2]]
            row2 = [[0,1,2],[0,1,2],[0,1,2],[0,1,2]]
            face3 = "top"
            cube = row_turn(cube,facelist1,facelist2,row1,row2,face3)
            # print("TURN " + str(direction) + mode)

        elif direction == 3:
            facelist1 = ["bot","back","top","front"]
            facelist2 = ["front","bot","back","top"]
            row1 = [[2,5,8],[6,3,0],[2,5,8],[2,5,8]]
            row2 = [[2,5,8],[2,5,8],[6,3,0],[2,5,8]]
            face3 = "right"
            cube = row_turn(cube,facelist1,facelist2,row1,row2,face3)
            # print("TURN " + str(direction) + mode)
        
        elif direction == 5:
            facelist1 = ["top","left","bot","right"]
            facelist2 = ["right","top","left","bot"]
            row1 = [[6,7,8],[8,5,2],[2,1,0],[0,3,6]]
            row2 = [[0,3,6],[6,7,8],[8,5,2],[2,1,0]]
            face3 = "front"
            cube = row_turn(cube,facelist1,facelist2,row1,row2,face3)
            # print("TURN " + str(direction) + mode)

        elif direction == 7:
            facelist1 = ["front","left","back","right"]
            facelist2 = ["right","front","left","back"]
            row1 = [[6,7,8],[6,7,8],[6,7,8],[6,7,8]]
            row2 = [[6,7,8],[6,7,8],[6,7,8],[6,7,8]]
            face3 = "bot"
            cube = row_turn(cube,facelist1,facelist2,row1,row2,face3)
            # print("TURN " + str(direction) + mode)

        elif direction == 9:
            facelist1 = ["front","top","back","bot"]
            facelist2 = ["bot","front","top","back"]
            row1 = [[0,3,6],[0,3,6],[8,5,2],[0,3,6]]
            row2 = [[0,3,6],[0,3,6],[0,3,6],[8,5,2]]
            face3 = "left"
            cube = row_turn(cube,facelist1,facelist2,row1,row2,face3)
            # print("TURN " + str(direction) + mode)

        elif direction == 11:
            facelist1 = ["top","right","bot","left"]
            facelist2 = ["left","top","right","bot"]
            row1 = [[0,1,2],[2,5,8],[8,7,6],[6,3,0]]
            row2 = [[6,3,0],[0,1,2],[2,5,8],[8,7,6]]
            face3 = "back"
            cube = row_turn(cube,facelist1,facelist2,row1,row2,face3)
            # print("TURN " + str(direction) + mode)

        else:
            direction = direction + 1
            for x in range(3):
                cube = cube_turn(cube,direction,"e")

    elif mode == "d":
        for x in range(3):
            cube = cube_turn(cube,direction,"e")

    
    return cube

def cube_print(cubes):
    for cube in cubes:
        print("Front:{}".format(cube["front"]))
        print("Top:{}".format(cube["top"]))
        print("Bottom:{}".format(cube["bot"]))
        print("Left:{}".format(cube["left"]))
        print("Right:{}".format(cube["right"]))
        print("Back:{}".format(cube["back"]))
        # for i in ["front", "top", "bot", "left", "right", "back"]:
        #     for j in range(0,len(cube[i]),3):
        #         print("{0}: {1}".format(i, cube[i][j:j+3]))
        # print("\n\n")

def paddingkey(text,mode):
    amttopad = 12
    if mode == "d":
        text = text + "0"
        timestopad = len(text)%amttopad
        if timestopad != 0:
            for x in range(amttopad - timestopad):
                text = text + "1"
        return text

    if mode == "e":
        text = text + "1"
        timestopad = len(text)%amttopad
        if timestopad != 0:
            for x in range(amttopad - timestopad):
                text = text + "0"
    return text

def paddingquery(text,mode):
    amttopad = 54*8
    if mode == "e":
        text = text + "1"
        timestopad = len(text)%amttopad
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

def convtobit(text,mode):
    if mode == "e":
        b = text.encode("ascii")
        a =[""]
        for b1 in b:
            c = bin(b1)
            a[0] = a[0] + c[2:]
        return a[0]
    elif mode == "d":
        realtext="0b" + text[0:7]
        for x in range(1,len(text)//7):
           realtext = realtext + "0" + text[x*7:(x+1)*7]
        n = int(realtext, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def bintohex(text,mode):
    if mode == "bintohex":
        text = "1111111111111111"+ text
        hextext = "0x" + hex(int(text,2))[6:]
        return hextext
    
    elif mode == "hextobin":
        value = text[2:]
        value = "ffff" + value
        b = bin(int(value, 16))
        return b[18:]

def changekey(key):
    keybits = ""
    for x in key:
        if x == "A":
            keybits += "100000000000"
        elif x == "B":
            keybits += "010000000000"
        elif x == "C":
            keybits += "001000000000"
        elif x == "D":
            keybits += "000100000000"
        elif x == "E":
            keybits += "000010000000"
        elif x == "F":
            keybits += "000001000000"
        elif x == "G":
            keybits += "000000100000"
        elif x == "H":
            keybits += "000000010000"
        elif x == "I":
            keybits += "000000001000"
        elif x == "J":
            keybits += "000000000100"
        elif x == "K":
            keybits += "000000000010"
        elif x == "L":
            keybits += "000000000001"
        else:
            keybits += "000000000000"
    return keybits

def ciphercube(query,key,mode):
    if mode == "E" or mode=="D":
        mode = "e" if mode=="E" else "d"
    cipher_bits = ""
    key_bit = changekey(key)
    if mode == "e":
        cubes = []
        cube = dict()
        faces = ["front","top","bot","left","right","back"]
        if query == "TEST":
            for x in range(6):
                inner_cube = []
                for y in range(9):
                    inner_cube.append((9*x) + y)
                cube[faces[x]] = inner_cube
            for index,key in enumerate(key_bit):
                    if key == "1":
                        cube = cube_turn(cube,index%12,mode)
            cubes.append(cube)

        else:
            query_bit = convtobit(query,mode)

            print("original query_bit: {0}".format(query_bit))
            
            padded_query = paddingquery(query_bit,"e")
            for x in range(len(padded_query)//(54*8)):
                cubebits = padded_query[x*(54*8):((x+1)*(54*8))]
                for y in range(6):
                    inner_cube = []
                    for z in range(9):
                        inner_cube.append(cubebits[((9*y) + z)*8:((9*y) + z+1)*8])
                    cube[faces[y]] = inner_cube
                for index,key in enumerate(key_bit):
                    if key == "1":
                        cube = cube_turn(cube,index%12,mode)
                newcube = copy.deepcopy(cube)
                cubes.append(newcube)
            for i in cubes:
                for j in i:
                    for k in i[j]:
                        cipher_bits = cipher_bits + k
        cipher = bintohex(cipher_bits,"bintohex")

        

    elif mode == "d":
        cubes = []
        cube = dict()
        faces = ["front","top","bot","left","right","back"]
        query_bit = bintohex(query,"hextobin")
        for x in range(len(query_bit)//(54*8)):
            cubebits = query_bit[x*(54*8):((x+1)*(54*8))]
            for y in range(6):
                inner_cube = []
                for z in range(9):
                    inner_cube.append(cubebits[((9*y) + z)*8:((9*y) + z+1)*8])
                cube[faces[y]] = inner_cube
            newcube = copy.deepcopy(cube)
            cubes.append(newcube)

        encryptedcubes = cubes
        cubes = []  
        for cube in encryptedcubes:
            for index,key in reversed(list(enumerate(key_bit))):
                    if key == "1":
                        cube = cube_turn(cube,index%12,mode)
            newcube = copy.deepcopy(cube)
            cubes.append(newcube)
        if query != "TEST":
            for i in cubes:
                for j in i:
                    for k in i[j]:
                        cipher_bits = cipher_bits + k
            cipher_bits = paddingquery(cipher_bits,"d")
            cipher = convtobit(cipher_bits,mode)
            return encryptedcubes,cipher
    return cubes,cipher

def main():
    plaintext = "CTF{FromtheSpeakGood Singlish Movement red as plum where the joyful grammarian worms I am from nameless noodle stalls with frowny uncles from palm copypaste plantations from the icestoking wilds of Torontonian suburbs}".replace(" ", "")
    key = "ABCDEFGHIJKL"
    #CUBES FOR DISPLAY
    # cube,ciphertext = ciphercube(query = "TEST", key = "",mode = "e")
    # cube_print(cube)
    # cube_turn0 = [cube]
    # cube_turn0[0] = cube_turn(cube[0],0,"e")
    # cube_print(cube_turn0)
    # changekey(key)
    # cube3,ciphertext3 = ciphercube(query = "TEST", key = key,mode = "e")
    # cube_print(cube3)
    # cube4,ciphertext4 = ciphercube(cube3,query = "TEST", key = key,mode = "d")
    # cube_print(cube4)


    #CYPHER CUBES
    # cube1,ciphertext1 = ciphercube(query = plaintext, key = key,mode = "e")
    # cube_print(cube1)
    # print(ciphertext1)
    # cube2,ciphertext2 = ciphercube(query = ciphertext1, key = key,mode = "d")
    # cube_print(cube2)
    # print(ciphertext2)

    cube1,ciphertext1 = ciphercube(query =plaintext, key = "L",mode = "e")
    cube1, new = ciphercube(query=ciphertext1, key="L", mode="d")
    print(new)


if __name__ == "__main__":
    main()
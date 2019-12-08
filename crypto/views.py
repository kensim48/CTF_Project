from rest_framework.response import Response
from rest_framework.views import APIView
from crypto.enigma import enigma
from crypto.rubik import ciphercube
from crypto.rubik_image import cube_to_pixel
import cv2
import os
import binascii
import time


def enigma_check(key):
    # 020301221004ACDGFE
    if len(key)<12:
        message = "Key length too short, not provided for layer 2"
        return False, message
    if not key[:12].isnumeric():
        message = "Incorrect formatting, ensure key for layer 2 looks like this 020301221004ACDGFE ,12 numbers, then even number of characters"
        return False, message
    key_list = [int(key[:2]),int(key[2:4]),int(key[4:6])]
    key_list.sort()
    if key_list != [1,2,3]:
        message = "Incorrect rotor numbers, ensure there is a 01, 02 and 03, in the first 6 characters, i.e. 020301"
        return False, message
    key_pos=[int(key[6:8]),int(key[8:10]),int(key[10:12])]
    for i in key_pos:
        if i < 1 or i > 26:
            message = "Incorrect rotor position, ensure the 7th to 12th characters are numbers between between 1 and 26 i.e. 221004"
            return False, message
    if len(key) >12:
        if len(key[12:]) % 2 != 0:
            message = "Ensure plugboard letters occur in pairs"
            return False, message
        if len(key[12:]) > 4:
            message = "There are only a maximum of 2 pairs for the plugboard"
            return False, message
    plugboard_check = []
    for i in key[12:]:
        if i not in plugboard_check:
            plugboard_check.append(i)
        else:
            message = "Ensure there are no repeating characters in the plugboard section of the key"
            return False, message
    return True, None


class Cipher(APIView):
    def get(self, request):
        cube=None
        response = {}
        try:
            input = request.query_params['input'].upper()
            layer = request.query_params['layer']
            key = request.query_params['key']

            if not layer.isnumeric():
                response["message"] = "Layer must be numeric"
                return Response(response)

            layer = int(layer)
            if layer == 0 or layer == 2:
                mode = request.query_params['mode'].upper()
            else:
                mode = None
            print(layer)
            response["message"] = "Params accepted."
        except:
            response["message"] = "Missing params, using sample URL = 'http://audacia.online:8000/cipher/?input=HELLOWORLD&key=GREYGOO020301221004ACDGFE&mode=e&layer=0'"
            input = "HELLOWORLD"
            mode = 'E'
            key = "GREYGOO020301221004ACDGFE"
            layer = 0

        # if not input.isalpha():
        #     response["message"] = "Input must only be letters"
        #     return Response(response)
        if not key.isalnum():
            response["message"] = "Key must be alphanumeric"
            return Response(response)

        if layer == 0 or layer == 2:
            if not (mode == 'E' or mode == 'D'):
                response["message"] = "Mode must be either 'E' or 'D'"
                return Response(response)
            response["mode"] = "Encryption" if mode == "E" else "Decryption"


        if not layer>=0 and layer<=2:
            response["message"] = "Layer must be between 0 and 2. Check instruction sheet for more info."
            return Response(response)


        response["input"] = input
        response["key"] = key

        if layer == 0:
            keysplit = 0
            for count, i in enumerate(key):
                if i.isdigit():
                    keysplit = count
                    break
            key_2 = key[:keysplit-1]
            key_1 = key[keysplit:]
            enigma_bool, enigma_message = enigma_check(key_1)
            print("key1", key_1, enigma_bool, mode)
            if enigma_bool:
                if mode == "E":
                    layer1, response["final_rotor_positions"] = enigma(input, key_1)
                    throwaway_cube, response["output"] = ciphercube(layer1, key_2, mode)
                    cube, throwaway = ciphercube(query="TEST", key=key_2, mode="e")
                elif mode == "D":
                    cube, layer2 = ciphercube(input, key_2, mode)
                    cube = None
                    response["output"], response["final_rotor_positions"] = enigma(layer2, key_1)
            else:
                response["message"] = enigma_message
        elif layer == 1:
            enigma_bool, enigma_message = enigma_check(key)
            if enigma_bool:
                response["output"], response["final_rotor_positions"] = enigma(input, key)
            else:
                response["message"] = enigma_message
        elif layer == 2:
            cube_throwaway, response["output"] = ciphercube(input, key, mode)
            cube, throwaway = ciphercube(query="TEST", key=key, mode="e")

        # cube = {'front': [0, 1, 2, 3, 4, 5, 6, 7, 8], 'top': [38, 41, 44, 12, 13, 14, 15, 16, 17],
        #         'bot': [18, 19, 20, 21, 22, 23, 27, 30, 33], 'left': [
        #         11, 28, 29, 10, 31, 32, 9, 34, 35], 'right': [36, 37, 26, 39, 40, 25, 42, 43, 24],
        #         'back': [51, 48, 45, 52, 49, 46, 53, 50, 47]}
        # print(cube)
        if cube is not None:
            final_image = cube_to_pixel(cube[0])
            filename = str(binascii.hexlify(os.urandom(16)))[2:-1]
            cv2.imwrite("static/cubes/{}.jpeg".format(filename), final_image)
            background = cv2.imread("static/cubes/{}.jpeg".format(filename))
            overlay = cv2.imread('static/overlay.jpg')
            added_image = cv2.addWeighted(background, 0.7, overlay, 0.3, 0)
            cv2.imwrite("static/cubes/{}.jpeg".format(filename), added_image)
            response["image"] = "http://audacia.online:8000/static/cubes/{}.jpeg".format(filename)

        return Response(response)

class Answer(APIView):
    def get(self, request):
        time.sleep(5)
        response = {}
        try:
            input = request.query_params['input'].upper()
        except:
            response["message"] = "Missing input query, url should look like http://127.0.0.1:8000/answer/?input=THISISMYANSWER"
            return Response(response)
        if input == "CTFFROMTHESPEAKGOODSINGLISHMOVEMENTREDASPLUMWHERETHEJOYFULGRAMMARIANWORMS" or input == "FROMTHESPEAKGOODSINGLISHMOVEMENTREDASPLUMWHERETHEJOYFULGRAMMARIANWORMS":
            response["message"] = "Congrats! You got the flag!"
        elif input == "GYYJILFAGSBNTFVCTZZNZKDOHXWRDXHKXSYPNPSTUZHRSVVZIQDJZXMALCOSVXJYMXZSATTRD" or input == "JILFAGSBNTFVCTZZNZKDOHXWRDXHKXSYPNPSTUZHRSVVZIQDJZXMALCOSVXJYMXZSATTRD":
            response["message"] = "Congrats! You reached the middlepoint!"
        elif input == "8f66cca93323418f4e14ea91ab43a96ad4eb52e2249162bd28964f4bb14ecd09d429d4ab6a452a75ab5a934624ab5626c1990e7d3ad625599b62d538352a52890000000000000000000000000000000000000000000000000000000000000000000000000000000000000000".upper() or input=="0x8f66cca93323418f4e14ea91ab43a96ad4eb52e2249162bd28964f4bb14ecd09d429d4ab6a452a75ab5a934624ab5626c1990e7d3ad625599b62d538352a52890000000000000000000000000000000000000000000000000000000000000000000000000000000000000000":
            response["message"] = "Congrats! You reached the middlepoint! Since you solved it in a way we didn't anticipate, GYYJILFAGSBNTFVCTZZNZKDOHXWRDXHKXSYPNPSTUZHRSVVZIQDJZXMALCOSVXJYMXZSATTRD is the key you should continue using for Enigma."
        else:
            response["message"] = "That was neither the middlepoint nor the flag :("
            print(input)
        return Response(response)
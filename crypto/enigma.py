def plugboard(query, plugboard_list):
    response = ""
    for letter in query:
        response_letter = letter
        for i in plugboard_list:
            if letter == i[0]:
                response_letter = i[1]
                break
            elif letter == i[1]:
                response_letter = i[0]
                break
        response += response_letter
    return response


class Rotor:
    def __init__(self, filename, position=1):
        if position < 1 or position > 26:
            exit()
        self.position = position
        f = open(filename, 'r')
        swap = f.readline().strip().split(',')
        self.swap = []
        for i in swap:
            self.swap.append(int(i))
        notch = f.readline().strip().split(',')
        self.notch = []
        for i in notch:
            self.notch.append(int(i))
        f.close()

    def set_position(self, position):
        if position < 1 or position > 26:
            exit()
        self.position = position

    def increment(self):
        self.position += 1
        if self.position > 26:
            self.position = 1

    def swap_fwd(self, letter):
        pos = ord(letter.lower()) - 97
        pos = (pos + self.position - 1) % 26
        new_pos = self.swap[pos] - 1
        return chr(new_pos + 97).upper()

    def swap_bck(self, letter):
        pos = ord(letter.lower()) - 97
        new_pos = self.swap.index(pos + 1)
        new_pos = (new_pos - (self.position - 1)) % 26
        return chr(new_pos + 97).upper()


class Rotors:
    def __init__(self, rotor1, rotor2, rotor3, key1, key2, key3, reflector):
        self.rotor1, self.rotor2, self.rotor3 = rotor1, rotor2, rotor3
        self.key1, self.key2, self.key3 = key1, key2, key3
        self.reflector = reflector

    def solve(self, query):
        self.rotor1.set_position(self.key1)
        self.rotor2.set_position(self.key2)
        self.rotor3.set_position(self.key3)
        response = ""
        for i in query:
            letter = self.single_letter(i)
            self.increment_rotors()
            response += letter
        rotor_positions = [self.rotor1.position, self.rotor2.position, self.rotor3.position]
        return response, rotor_positions

    def single_letter(self, letter):
        letter = self.rotor1.swap_fwd(
            self.rotor2.swap_fwd(self.rotor3.swap_fwd(letter)))
        letter = self.reflector.swap_fwd(letter)
        return self.rotor3.swap_bck(self.rotor2.swap_bck(self.rotor1.swap_bck(letter)))

    def increment_rotors(self):
        self.rotor3.increment()
        if self.rotor3.position in self.rotor2.notch:
            print(self.rotor3.position)
            self.rotor2.increment()
            if self.rotor2.position in self.rotor1.notch:
                self.rotor1.increment()

def enigma(QUERY, KEY):
    order = [int(KEY[0:2]), int(KEY[2:4]), int(KEY[4:6])]
    rotor_keys = [int(KEY[6:8]), int(KEY[8:10]), int(KEY[10:12])]
    plugboard_list = []

    if len(KEY[12:]) % 2 != 0:
        exit()

    for count, i in enumerate(KEY[12:]):
        if count % 2 == 0:
            mini_list = [i]
        else:
            mini_list.append(i)
            plugboard_list.append(mini_list)

    plugboard_check = []
    for i in plugboard_list:
        for j in i:
            if j in plugboard_check:
                exit()
            plugboard_check.append(j)

    rotor1 = Rotor("crypto/rotors/rotor1.txt")
    rotor2 = Rotor("crypto/rotors/rotor2.txt")
    rotor3 = Rotor("crypto/rotors/rotor3.txt")
    reflector = Rotor("crypto/rotors/reflector.txt")

    rotor_order = []
    for i in order:
        if i == 1:
            rotor_order.append(rotor1)
        elif i == 2:
            rotor_order.append(rotor2)
        elif i == 3:
            rotor_order.append(rotor3)

    rotors = Rotors(rotor_order[0], rotor_order[1], rotor_order[2], rotor_keys[0], rotor_keys[1], rotor_keys[2], reflector)

    query = plugboard(QUERY, plugboard_list)
    query, rotor_positions = rotors.solve(query)
    query = plugboard(query, plugboard_list)
    return query, rotor_positions




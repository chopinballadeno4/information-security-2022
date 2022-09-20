# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by
# Wehrmacht and Luftwaffe, Nazi Germany.
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I": {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

# 반사판
UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    # Reflector
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input


# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]


# Wheels - 신호 통과 구현!!!!!!!!!
def pass_wheels(input, reverse=False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order
    tempinput = input

    if reverse == True:
        for i in range(3):
            idxnum = ord(tempinput) - ord('A')
            tempinput = SETTINGS["WHEELS"][i]["wire"][idxnum]
    elif reverse == False:
        for i in range(2, -1, -1):
            idxnum = ord(tempinput) - ord('A')
            tempinput = SETTINGS["WHEELS"][i]["wire"][idxnum]
    return tempinput


# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]


# Wheel Rotation - 로터 회전 구현!!!!!!!!!
def rotate_wheels():
    # Implement Wheel Rotation Logics
    if SETTINGS["WHEELS"][2]["turn"] == SETTINGS["WHEEL_POS"][2]:
        if SETTINGS["WHEELS"][1]["turn"] == SETTINGS["WHEEL_POS"][1]:
            if SETTINGS["WHEELS"][0]["turn"] == SETTINGS["WHEEL_POS"][0]:
               SETTINGS["WHEEL_POS"][0] = move_idx(SETTINGS["WHEEL_POS"][0])
               SETTINGS["WHEEL_POS"][1] = move_idx(SETTINGS["WHEEL_POS"][1])
               SETTINGS["WHEEL_POS"][2] = move_idx(SETTINGS["WHEEL_POS"][2])
            else:
                SETTINGS["WHEEL_POS"][0] = move_idx(SETTINGS["WHEEL_POS"][0])
        else: # 오른쪽만 일치
            SETTINGS["WHEEL_POS"][1] = move_idx(SETTINGS["WHEEL_POS"][1])
    else: 
        SETTINGS["WHEEL_POS"][2] = move_idx(SETTINGS["WHEEL_POS"][2])


def move_idx(num):
    if num == 26:
        return 1
    else:
        return num + 1


#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Enigma Logics Start
def apply_settings(ukw, wheel, wheel_pos, plugboard):
    # 반사판 설정
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    # 바퀴 순서 세팅 WHEELS = [{wire, turn}]
    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    # Wheel 값 설정 WHEEL_POS = [number]
    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))

    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ") # 암호화 할 코드
ukw_select = input("Set Reflector (A, B, C): ") # Reflector 선택
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ") # Wheel 순서 선택
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ") # Wheel 값
plugboard_setup = input("Plugboard Setup: ") # plug 세팅

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)
    
    print(encoded_ch, end='')

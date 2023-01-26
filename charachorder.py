#!/usr/bin/env python
import serial
import io
import math
import sys

note_names = [
    "RH Thumb 3 Left", # 01
    "RH Thumb 3 Down", # 02
    "RH Thumb 3 Right", # 03
    "RH Thumb 3 Up", # 04
    "RH Thumb 3 Center", # 05
    "RH Thumb 2 Left", # 06
    "RH Thumb 2 Down", # 07
    "RH Thumb 2 Right", # 08
    "RH Thumb 2 Up", # 09
    "RH Thumb 2 Center", # 10
    "RH Thumb 1 Left", # 11
    "RH Thumb 1 Down", # 12
    "RH Thumb 1 Right", # 13
    "RH Thumb 1 Up", # 14
    "RH Thumb 1 Center", # 15
    "RH Pinky Down", # 16
    "RH Pinky Right", # 17
    "RH Pinky Up", # 18
    "RH Pinky Left", # 19
    "RH Pinky Center", # 20
    "RH Ring Secondary Down", # 21
    "RH Ring Secondary Right", # 22
    "RH Ring Secondary Up", # 23
    "RH Ring Secondary Left", # 24
    "RH Ring Secondary Center", # 25
    "RH Ring Primary Down", # 26
    "RH Ring Primary Right", # 27
    "RH Ring Primary Up", # 28
    "RH Ring Primary Left", # 29
    "RH Ring Primary Center", # 30
    "RH Middle Secondary Down", # 31
    "RH Middle Secondary Right", # 32
    "RH Middle Secondary Up", # 33
    "RH Middle Secondary Left", # 34
    "RH Middle Secondary Center", # 35
    "RH Middle Primary Down", # 36
    "RH Middle Primary Right", # 37
    "RH Middle Primary Up", # 38
    "RH Middle Primary Left", # 39
    "RH Middle Primary Center", # 40
    "RH Index Down", # 41
    "RH Index Right", # 42
    "RH Index Up", # 43
    "RH Index Left", # 44
    "RH Index Center", # 45
    "LH Thumb 3 Right", # 46
    "LH Thumb 3 Up", # 47
    "LH Thumb 3 Left", # 48
    "LH Thumb 3 Down", # 49
    "LH Thumb 3 Center", # 50
    "LH Thumb 2 Right", # 51
    "LH Thumb 2 Up", # 52
    "LH Thumb 2 Left", # 53
    "LH Thumb 2 Down", # 54
    "LH Thumb 2 Center", # 55
    "LH Thumb 1 Right", # 56
    "LH Thumb 1 Up", # 57
    "LH Thumb 1 Left", # 58
    "LH Thumb 1 Down", # 59
    "LH Thumb 1 Center", # 60
    "LH Pinky Down", # 61
    "LH Pinky Right", # 62
    "LH Pinky Up", # 63
    "LH Pinky Left", # 64
    "LH Pinky Center", # 65
    "LH Ring Secondary Down", # 66
    "LH Ring Secondary Right", # 67
    "LH Ring Secondary Up", # 68
    "LH Ring Secondary Left", # 69
    "LH Ring Secondary Center", # 70
    "LH Ring Primary Down", # 71
    "LH Ring Primary Right", # 72
    "LH Ring Primary Up", # 73
    "LH Ring Primary Left", # 74
    "LH Ring Primary Center", # 75
    "LH Middle Secondary Down", # 76
    "LH Middle Secondary right", # 77
    "LH Middle Secondary Up", # 78
    "LH Middle Secondary Left", # 79
    "LH Middle Secondary Center", # 80
    "LH Middle Primary Down", # 81
    "LH Middle Primary Right", # 82
    "LH Middle Primary Up", # 83
    "LH Middle Primary Left", # 84
    "LH Middle Primary Center", # 85
    "LH Index Down", # 86
    "LH Index Right", # 87
    "LH Index Up", # 88
    "LH Index Left", # 89
    "LH Index Center" # 90
]

def command(sio, cmd):
    sio.write(cmd + '\r\n')
    sio.flush()
    ready = False
    result = ""
    while not ready:
        line = sio.readline()
        if line == '':
            ready = True
        else:
            result = result + line.rstrip() + "\n"
    return result

# From CharaChorder serial API doc: https://drive.google.com/file/d/1AVIg0iq6csU5MLckxq5jM5cwZrMgmFog/view
def noteId_to_chord(note):
    return ((2*((note-1)%5))+1) * (10**(int((note-1)/5)))

def chord_to_noteId(chord):
    return int(5*int(math.log10(chord)) + (int(chord/(10**int(math.log10(chord)))+1)/2))

def list_notes():
    for i in range(1,91): #note_byte can be an integer value of 1 to 90
        note_chord = noteId_to_chord(i)
        note_byte = chord_to_noteId(note_chord)
        print(""+str(i)+" "+str(note_chord)+" "+note_names[note_byte-1])

# ./charachorder.py set 71 26 74657374   - works!        
# 74657374 = test
def set_key(sio, notes, key):
    print("Setting keys:")
    sum = 0
    for note in notes:
        note = int(note)
        print("Note = " + str(note))
        sum = sum+noteId_to_chord(note)
        print(str(note), noteId_to_chord(note), note_names[note-1])
    chordId = hex(sum)[2:].upper()
    print("Setting " + chordId + " to " + key)
    return command(sio, "SET "+ chordId + " " + key)
        
def main(args):
    with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1))
        if args[0] == "cmd":
            output = command(sio, " ".join(args[1:]))
            print(output)
        elif args[0] == "set":
            output = set_key(sio, args[1:-1], args[-1])
            print(output)
            output = command(sio, "COMMIT")
            print(output)
        elif args[0] == "list":
            list_notes()
if __name__ == "__main__":
    main(sys.argv[1:])


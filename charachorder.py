#!/usr/bin/env python
import serial
import io
import math


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
        print(""+str(i)+" "+str(note_chord)+" "+str(note_byte))

def set_key(sio, chordId, key):
    print("Setting " + chordId + " to " + key)
    return command(sio, "SET "+ chordId + " " + key)
        
def main():
    with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1))
        #output = command(sio, "GET 65DD08B1120")
        # Numshift left = LH Pinky left = 7000000000000 , RH Ring primary up = 500000
        # TODO: key mapped, no output however
        numshiftRingUp = hex(7000000000000 + 500000)[2:].upper()
        #finnishPlus = "2D"  # English -
        letterA = "61"
        #output = set_key(sio, numshiftRingUp, letterA)
        #output = command(sio, "COMMIT")
        print(output)

if __name__ == "__main__":
    #list_notes()
    #print(chord_to_noteId(0x186D2))
    main()


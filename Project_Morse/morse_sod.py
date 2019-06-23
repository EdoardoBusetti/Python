import datetime
import threading
import time
import RPi.GPIO as GPIO
import InternationalMorseCode as ICM

'''Send Morse Code Via Button Click
    This is a Python script for accepting incoming signals 
    (via a physical button that "closes" the circuit), 
    and translating the input into morse code.


Setup for Pi
    The length of time of one "beat" (i.e. a single "dot") 
    can be adjusted via BASE_TIME_SECONDS, which represents seconds.

BASE_TIME_SECONDS = 1.0
    The tolerance can be adjusted via TOLERANCE.
    Exact timing is difficult. On the following line,
    I've stated a tolerance of 1/2 second.
    So instead of pressing the button for 1 sec for a dot 
    or 3 sec for a dash, you're allowed 0.5 - 1.5 sec for a dot,
    and 2.5 - 3.5 sec for a dash.

TOLERANCE = BASE_TIME_SECONDS / 2.0

    Depending on how you have your board setup,
    you may want to adjust the pin numbers throughout the script.

'''







BASE_TIME_SECONDS = 1.0
TOLERANCE = BASE_TIME_SECONDS / 2.0
# Initialize GPIO settings
def initialize_gpio():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([12], GPIO.OUT)  
    GPIO.setup(32, GPIO.IN)
    GPIO.output([12], GPIO.LOW)
    GPIO.add_event_detect(32, GPIO.BOTH, callback=intercept_morse_code)







last_edge = GPIO.LOW
press = datetime.datetime.now()
release = datetime.datetime.now()


# Intercept a rise or fall on pin 31 (button press/release)
def intercept_morse_code(channel):
    global last_edge, press, release

    # Button pressed - determine if start of new letter/word
    if GPIO.input(channel) == GPIO.HIGH and last_edge == GPIO.LOW:
        last_edge = GPIO.HIGH
        press = datetime.datetime.now()
        detect_termination()

    # Button released - determine what the input is
    elif GPIO.input(channel) == GPIO.LOW and last_edge == GPIO.HIGH:
        last_edge = GPIO.LOW
        release = datetime.datetime.now()
        interpret_input()


sequence = ""
letters = []
words = []


# Detect whether most recent button press is start of new letter or word
def detect_termination():
    global sequence

    if sequence == "":
        return

    delta = calc_delta_in_sec(release, press)

    # Check for start of new letter (gap equal to 3 dots)
    if (delta >= ((BASE_TIME_SECONDS * 3) - TOLERANCE)) and (delta <= ((BASE_TIME_SECONDS * 5) + TOLERANCE)):
        process_letter()

    # Check for start of new word (gap equal to 8 dots - but assume anything > 8 dots is valid too)
    elif delta >= ((BASE_TIME_SECONDS * 7) - TOLERANCE):
        process_word()


# Process letter
def process_letter():
    global sequence
    character = ICM.symbols.get(sequence, '')

    if character != '':
        print("Interpreted sequence " + sequence + " as the letter: " + character)
        letters.append(character)
        sequence = ""
        return True
    else:
        print('Invalid sequence: ' + sequence + " (deleting current sequence)")
        sequence = ""
        return False


# Process word
def process_word():
    if process_letter():
        word = ''.join(letters)
        letters[:] = []
        if word == "AR":
            print("\nFine della trasmissione. Questo e' il vostro messaggio: " + ' '.join(words))
            print("\nCancello la precedente trasmissione.Ora e' possibile cominciarne una nuova...\n")
            words[:] = []
        if word == 'SOS' or word =='ES':
            print('Hai Scritto SOS, la porta si apre. Cancello tutte le parole.')
	    GPIO.output(12, GPIO.HIGH)
	    time.sleep(3)
	    GPIO.output(12, GPIO.LOW)
	    words[:] = []
	    sequence = ""
            #Da implementare, connettendo un pin al cavo che fa aprire la porta e mettendolo come autput di questo if
        else:
            words.append(word)


# Interpret button click (press/release) as dot, dash or unrecognized
def interpret_input():
    global sequence

    delta = calc_delta_in_sec(press, release)

    if (delta >= (BASE_TIME_SECONDS - TOLERANCE)) and (delta <= (BASE_TIME_SECONDS + TOLERANCE)):
        sequence += '.'
        print(str(delta) + " : Aggiunto PUNTO alla sequenza:  " + sequence)
    elif (delta >= ((BASE_TIME_SECONDS * 3) - TOLERANCE)) and (delta <= ((BASE_TIME_SECONDS * 3) + TOLERANCE)):
        sequence += '-'
        print(str(delta) + " : Aggiunta LINEA alla sequenza: " + sequence)
    else:
        print(str(delta) + " : Input non riconosciuto!")


def calc_delta_in_sec(time1, time2):
    delta = time2 - time1
    return delta.seconds + (delta.microseconds / 1000000.0)


try:
    initialize_gpio()
    message = raw_input("\nPress any key to exit.\n")


finally:
    GPIO.cleanup()

print("Edo Boss, Ciao Ciao!")


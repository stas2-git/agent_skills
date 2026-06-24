import time
import pyautogui
import pytesseract
import keyboard
from PIL import ImageGrab

# START CONFIG

# Run the included findmousepos.py file for below part, or if you already know what to do, ignore these instructions.
# (x,x) is in reference to the postion of your mouse on your screen displayed from the findmousepos.py script. 
# Find the area of the screen for the below config by running that file in cmd/terminal
# The first number (#) of (x,x) will be the left-to-right (horizontal) position in px
# The second number (#) of (x,x) will be the top-to-bottom (vertical) position in px

# The First # in (x,x) with your mouse positioned on the left of where you want text read from
left = 1240 

# The Second # in (x,x) with your mouse positioned on the bottom of where you want text read from
top = 165 

# Start from the first # in (x,x) on the right side of the area you want text read from and write that number down
# Go to the left side of where you want text read from and write that number down
# Subtract the first number from the second number (of the ones you wrote down) and put that number here
width = 190 

# Start from the second # in (x,x) at the bottom of the area you want text read from and write that number down
# Go to the top of the area you want text read from and write that number down
# Subtract the first number from the second number (of the ones you wrote down) and put that number here
height = 23 

# The text you want read from the screen. This has to be an exact match, try to keep it to 1 line or it might not work
# If script reads text1, it will click on click_pos1 (set in the next set of config items), if it reads text2 it clicks click_pos2
# If it doesn't recognize any text, it will not click anything
text1 = 'correct direction:'
text2 = 'correct direction: anti-'

# Set the positions to click. If you need more, read the included readme.md
click_pos1 = (1280, 340)
click_pos2 = (1380, 340)

#Keyboard key to turn the script on/off
toggle_key = 'space'

wait_time = 3   

# Now you're done! If you know what you are doing, feel free to make any changes to this code you find necessary for
# your own use. If you don't know what you are doing, please feel free to read the included readme.md file that 
# is packaged with this, as it contains information regarding what each part of the code does in simple terms.
# This also includes instructions on how to edit the click events to do what you want to do (i.e add more positions)

# END CONFIG


# Initialize Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Show when tesseract is ran
print("Script initialized!")
print("Waiting for toggle key, please press", toggle_key)
print("You can stop the script by pressing", toggle_key,", or press ctrl+c to exit the script")

# Set the delay before clicking
pyautogui.PAUSE = 1

toggle = False
while True:  
    keyboard.wait(toggle_key) # Wait for toggle_key press
    toggle = not toggle
    print('===========================SCRIPT STATUS===========================')
    print(' ')
    if toggle: # If script is toggled on
        print('===========================SCRIPT STARTED===========================')        
                
    time.sleep(0.2)

    while toggle: # While loop is running
        # Display new event
        print("===========================NEW EVENT===========================")
        print(' ')

        # Check if toggle_key is held down and stops script if it is
        if keyboard.is_pressed(toggle_key):
                toggle = False
                print('===========================SCRIPT STOPPED===========================')
                print(' ')
                print("Waiting for toggle key, please press", toggle_key)
                print("You can stop the script by pressing", toggle_key,", or press ctrl+c at any time to exit the script")
                break  # exit the while loop
        
        # Capture the specified region of the screen
        image = ImageGrab.grab(bbox=(left, top, left + width, top + height))
        print("Image captured from screen!")
        
        # Convert the image to grayscale
        image = image.convert('L')
        print("Image converted to grayscale")

        # Use Tesseract OCR to extract the text from the image
        text = pytesseract.image_to_string(image)
        print("Tesseract extracted image")
        
        # Clean up the text
        text = text.strip().lower()
        print("Text from image cleaned")
        
        # Print the extracted text
        print(f"Extracted text from image: {text}")
        
        # Click in the appropriate position based on the text
        if text == text1:
            pyautogui.click(click_pos1)
            print("Position 1 Clicked!")
            print(' ')
        elif text == text2:
            pyautogui.click(click_pos2)
            print("Position 2 Clicked!")   
            print(' ')
        else:
            print("No text was recognized, nothing was clicked!")
            print(' ')

        # Display end event
        print("===========================EVENT OVER===========================")
        print(' ')
        
        # Wait for a short period before checking again
        time.sleep(wait_time)

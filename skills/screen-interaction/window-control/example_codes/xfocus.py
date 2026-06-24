# Using applescript, sets the focus + foreground on a window by its title
# That works on OSX 12.0.1.
# @author Aurelien Scoubeau <aurelien.scoubeau@gmail.com>
# @edit John Lyu <paleneutron@outlook.com>
import argparse
import subprocess


# find the app or window back and activate it
def xfocus(title):
    apple = """
    set the_title to "%s"
    tell application "System Events"
        repeat with p in every process whose background only is false
            repeat with w in every window of p
                if (name of w) is the_title then
                    tell p
                        set frontmost to true
                        perform action "AXRaise" of w
                    end tell
                end if
            end repeat
        end repeat
    end tell
    """ % (title, )
    p = subprocess.Popen('osascript',
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    p.communicate(apple.encode())[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Utility to activate a window by title, for OSX')
    parser.add_argument('title', help='Title of the window to activate')
    args = vars(parser.parse_args())
    title = args['title']
    xfocus(title)
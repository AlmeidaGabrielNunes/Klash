# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *



def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message):
  background = pygame.Surface(screen.get_size())
  background = background.convert()
  background.fill((0,0,0))
  "Print a message in a box in the middle of the screen"
  screen.blit(background, (0,0))
  fontobject = pygame.font.Font(None,30)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 300,
                    (screen.get_height() / 2) - 12,
                    600,49), 1)
  print message
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 298, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + string.join(current_string,""))
  while 1:
    inkey = get_key()
    print inkey
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
      pygame.display.flip()
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")

    if inkey>=256 and inkey<=265:
      if (inkey==256):
        current_string.append('0')
      elif (inkey==257):
        current_string.append('1')
      elif (inkey==258):
        current_string.append('2')
      elif (inkey==259):
        current_string.append('3')
      elif (inkey==260):
        current_string.append('4')
      elif (inkey==261):
        current_string.append('5')
      elif (inkey==262):
        current_string.append('6')
      elif (inkey==263):
        current_string.append('7')
      elif (inkey==264):
        current_string.append('8')
      elif (inkey==265):
        current_string.append('9')

      
    elif inkey <= 127 and inkey <>8:
      
      current_string.append(chr(inkey))
      


    display_box(screen, question + ": " + string.join(current_string,""))
    print current_string
  return string.join(current_string,"")

def main():
  screen = pygame.display.set_mode((1280, 720))
  print ask(screen, "Name") + " was entered"


if __name__ == '__main__': main()

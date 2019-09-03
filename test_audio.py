import pygame
pygame.mixer.init()
pygame.mixer.music.load("temple-bell.mp3")
print("You should hear a bell sound.")
pygame.mixer.music.play()
while pygame.mixer.music.get_busy() == True:
    continue
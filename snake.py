# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 10:29:17 2023

@author: SHIRSENDU MALI
"""

# snake.py: A Python-made game where a Snake chases a Fruit to eat and survive.


import pygame
from random import randint
from math import sqrt

# Initializing 'pygame'
pygame.init()


# Setting colors
black = (0, 0, 0)  # Background color
white = (255, 255, 255)  # Color of 'points' text
yellow = (254, 221, 0)  # Color of the Snake
green = (48, 183, 0)  # Color of the Fruit
red = (255, 0, 0)  # Color of 'Game Over!' text

# Setting width and height for the display area
width = 800
height = 600

# Creating game display
game_display = pygame.display.set_mode((width, height))

# Setting the title for the game
pygame.display.set_caption("The Hungry Snake")
pygame.display.update()

game_font = pygame.font.SysFont("arial", 28)

# To keep track of time so that the program can update frames with respect to time
clock = pygame.time.Clock()


# Function to draw the Snake onto the display
def draw_snake(display, color, s_list, size):
    for temp in s_list:
        x = temp[0]
        y = temp[1]
        pygame.draw.rect(display, color, [x, y, size, size])


# Function to show text onto the display
def display_text(text, color, x, y):
    resultant_text = game_font.render(text, True, color)
    # Placing the text onto x and y coordinates of the display
    game_display.blit(resultant_text, [x, y])


# Main function which contains game logic
def main():
    # Required variables for the game
    game_over = False
    game_exit = False
    x = 450  # Let 450 be the Snake's position along x-axis
    y = 300  # Let 300 be the Snake's position along y-axis
    size = 15  # Size of the Snake
    # Frames Per Second (the higher the fps, the smoother the gameplay)
    fps = 30
    velocity = 10  # Initial velocity of the Snake
    vx = 0  # Velocity of the Snake along x-axis
    vy = 0  # Velocity of the Snake along y-axis
    # Randomly generating the Fruit's position along x-axis
    fruit_x = randint(50, (width - 50))
    # Randomly generating the Fruit's position along y-axis
    fruit_y = randint(50, (height - 50))
    points = 0  # Total points scored
    points_string = ""  # String that will be drawn onto the display
    snake_list = []  # List that will contain appended coordinates
    snake_length = 1

    # Reading 'high-score.txt' file for manipulating highscore
    with open("high-score.txt", "r") as file:
        high_score = int(file.read())

    points_string = "Points: " + \
        str(points) + "    Best Record: " + str(high_score)

    # GAME LOGIC
    # Game continues to run until 'game_exit' becomes True
    while not game_exit:
        # If game is over,
        # then display "Game Over! Press ENTER to restart.".
        if game_over == True:
            # After game is over, updating the highscore
            with open("high-score.txt", "w") as file:
                file.write(str(high_score))

            game_display.fill(black)
            display_text("Game Over! Press ENTER to restart.", red, 8, 8)

            # Game exit logic
            for event in pygame.event.get():
                # Quitting the game
                if event.type == pygame.QUIT:
                    game_exit = True
                # Game will restart if ENTER key is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        main()  # Restarting the game
        else:
            for event in pygame.event.get():
                # If we mistakenly close the application, the game will also quit
                if event.type == pygame.QUIT:
                    game_exit = True

                # When keyboard button is pressed
                if event.type == pygame.KEYDOWN:
                    # When RIGHT ARROW is pressed, Snake moves to the right
                    if event.key == pygame.K_RIGHT:
                        vx = velocity
                        vy = 0
                    # When LEFT ARROW is pressed, Snake moves to the left
                    if event.key == pygame.K_LEFT:
                        vx = - velocity
                        vy = 0
                    # When UP ARROW is pressed, Snake moves to the up
                    if event.key == pygame.K_UP:
                        vx = 0
                        vy = - velocity
                    # When DOWN ARROW is pressed, Snake moves to the down
                    if event.key == pygame.K_DOWN:
                        vx = 0
                        vy = velocity

            x = x + vx
            y = y + vy

            # Calculating distance between the Snake and the Fruit
            dist = sqrt((x - fruit_x)**2 + (y - fruit_y)**2)

            # If the Snake and the Fruit come close to a distance of 10 units or lesser,
            # then the Snake eats the Fruit and player scores 1 point.
            if dist <= 12:
                points += 10  # 10 point is scored
                points_string = "Points: " + \
                    str(points) + "    Best Record: " + str(high_score)
                # Resetting the Fruit's position each time after the Snake eats it
                fruit_x = randint(50, (width - 50))
                fruit_y = randint(50, (height - 50))

                # Increasing the length of the Snake after it eats a Fruit
                snake_length += 5

                if points > high_score:
                    high_score = points

            game_display.fill(black)  # Filling the display area

            # Displaying the points scored
            display_text(points_string, white, 8, 8)

            # Drawing the Fruit
            pygame.draw.rect(game_display, green, [
                             fruit_x, fruit_y, size, size])

            # Since the beginning of the game, the Snake should have atleast its head as its whole body.
            # So we are providing that head in this step.
            head = []
            # Appending the initial x-axis coordinate of the Snake
            head.append(x)
            # Appending the initial y-axis coordinate of the Snake
            head.append(y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                # Deleting the first element (a list containing x, y coordinates)
                # So that the Snake's end portion will move accordingly
                del snake_list[0]

            # Game Over logic (if crashes to itself)
            # Here head is the last element
            # Logic: If the head's coordinate matches to the remaining body's coordinate(s),
            #        then the Snake will collide with itself and then the game will be over.
            # Excluding head from the list 'snake_list' by slicing
            if head in snake_list[:-1]:
                game_over = True

            # Game Over logic (if crashes to the walls)
            if x > (width - 4) or x < 4 or y > (height - 4) or y < 4:
                game_over = True

            # Drawing the Snake
            draw_snake(game_display, yellow, snake_list, size)

        pygame.display.update()  # Updating the display area
        clock.tick(fps)

    pygame.quit()
    quit()  # Exiting the game


# Driver code
main()

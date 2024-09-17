#IMPORTING MODULES
import pygame
from pynput import mouse

#------------------------
#Set up the drawing window
pygame.init()
width = 350
height = 350
background_color = 255, 255, 255
screen = pygame.display.set_mode((width, height))

#importing images
highlight = pygame.image.load("highlight.png")
gameboard_image = pygame.image.load("ultimate_gameboard.png")
x_image = pygame.image.load("ultimate_x.png")
o_image = pygame.image.load("ultimate_o.png")
big_o = pygame.image.load("o.png")
big_x = pygame.image.load("x.png")
screen.fill("white")
screen.blit(gameboard_image, (3, 1))
player_turn = 0
move_done = True
player1 = input("Player 1 name: ")
player2 = input("Player 2 name: ")
moves = []
big_square = []
x_range = []
y_range = []
yellow_move = [0, 350, 0, 350]
y_check = [
    70, 20, 100, 50, 137, 80, 173, 124, 200, 152, 240, 180, 278, 225, 303, 255,
    350, 282
]
x_check = [
    50, 25, 78, 53, 115, 82, 152, 124, 181, 153, 217, 183, 254, 225, 280, 254,
    350, 283
]
#gameboard is 300 pixels wide
#x lines are 115 and 217
#y lines are 137 and 240


def update_board(x, y):
    global gameboard, player_turn, moves, yellow_move
    for i in range(0, len(y_check), 2):
        if y < y_check[i]:
            marker_y = y_check[i + 1]
            moves.append(y_check[i + 1])
            i = i / 2
            if i < 3:
                big = [0, 1, 2]
            elif i < 6:
                big = [3, 4, 5]
            else:
                big = [6, 7, 8]
            if i % 3 == 0:
                highlight_y = 12
                small = [0, 1, 2]
            elif i % 3 == 1:
                highlight_y = 111
                small = [3, 4, 5]
            else:
                highlight_y = 214
                small = [6, 7, 8]
            break
    for i in range(0, len(x_check), 2):
        if x < x_check[i]:
            marker_x = x_check[i + 1]
            moves.append(x_check[i + 1])
            i = i / 2
            if i < 3:
                big = big[0]
            elif i < 6:
                big = big[1]
            else:
                big = big[2]
            if i % 3 == 0:
                highlight_x = 12
                small = small[0]
            elif i % 3 == 1:
                highlight_x = 116
                small = small[1]
            else:
                highlight_x = 218
                small = small[2]
            break

    check = move_check(marker_x, marker_y, highlight_x, highlight_y)

    if gameboard[big][small] == 0 and check == True:
        player_turn += 1
        gameboard[big][small] = (player_turn % 2) + 1
        score_check()
        screen.fill("white")
        if gameboard[small][0] < 3:
            screen.blit(highlight, (highlight_x, highlight_y))
        else:
            yellow_move[0] = 0
            yellow_move[1] = 350
            yellow_move[2] = 0
            yellow_move[3] = 350
    else:
        print("Please choose a valid square")
        moves.pop()
        moves.pop()

    pygame.display.update()
    redraw_board()


#making user click print shapes
def on_click(x, y, button, pressed):
    global player_turn, gameboard
    if pressed == False:
        print((x, y))
        update_board(x, y)


listener = mouse.Listener(on_click=on_click)
listener.start()

#https://pythonhosted.org/pynput/mouse.html#controlling-the-mouse

#creating the logic
gameboard = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
big_gameboard = [0, 0, 0, 0, 0, 0, 0, 0, 0]

running = True


def move_check(x, y, yellow_x, yellow_y):
    if yellow_move[0] <= x <= yellow_move[1] and yellow_move[
            2] <= y <= yellow_move[3]:
        yellow_move[0] = yellow_x
        yellow_move[1] = yellow_x + 103
        yellow_move[2] = yellow_y
        yellow_move[3] = yellow_y + 102
        return True


def lock_grid(grid, locked_num):
    if grid % 3 == 0:
        x = 10
    elif grid % 3 == 1:
        x = 115
    else:
        x = 227

    if grid < 3:
        y = 10
    elif grid < 6:
        y = 117
    else:
        y = 220

    for i in range(9):
        gameboard[grid][i] = locked_num

    if locked_num == 4:
        screen.blit(big_x, (x, y))
    else:
        screen.blit(big_o, (x, y))

    big_square.extend((x, y, locked_num))
    big_gameboard[grid] = locked_num


def redraw_board():
    counter = 0
    for i in range(0, len(moves), 2):
        x = moves[i + 1]
        y = moves[i]
        if counter % 2 == 0:
            screen.blit(x_image, (x, y))
        else:
            screen.blit(o_image, (x, y))
        counter += 1

    for i in range(0, len(big_square), 3):
        if big_square[i + 2] == 4:
            screen.blit(big_x, (big_square[i], big_square[i + 1]))
        else:
            screen.blit(big_o, (big_square[i], big_square[i + 1]))


def score_check():
  for i in range(9):
      #diagonal check
      temp = []
      temp.append(gameboard[i][0])
      temp.append(gameboard[i][4])
      temp.append(gameboard[i][8])
      if temp[0] == temp[1] == temp[2] and len(
              temp) == 3 and 0 < temp[0] < 3:
          if temp[0] == 2:
              lock_grid(i, 4)
          else:
              lock_grid(i, 3)
          pygame.display.flip()
          return
      temp = []
      temp.append(gameboard[i][2])
      temp.append(gameboard[i][4])
      temp.append(gameboard[i][6])
      if temp[0] == temp[1] == temp[2] and len(temp) == 3 and 0 < temp[0] < 3:
        if temp[0] == 2:
          lock_grid(i, 4)
        else:
          lock_grid(i, 3)
        pygame.display.flip()
        return
      #horizontal check
      for j in range(0, 7, 3):
        temp = []
        temp.append(gameboard[i][j])
        temp.append(gameboard[i][j + 1])
        temp.append(gameboard[i][j + 2])
        if temp[0] == temp[1] == temp[2] and len(temp) == 3 and 0 < temp[0] < 3:
          if temp[0] == 2:
            lock_grid(i, 4)
          else:
            lock_grid(i, 3)
            pygame.display.flip()
          return
        #vertical check
      for j in range(3):
          temp = []
          temp.append(gameboard[i][j])
          temp.append(gameboard[i][j + 3])
          temp.append(gameboard[i][j + 6])
          if temp[0] == temp[1] == temp[2] and len(temp) == 3 and 0 < temp[0] < 3:
            if temp[0] == 2:
              lock_grid(i, 4)
            else:
              lock_grid(i, 3)
            pygame.display.flip()
            return
  big_score_check()


#same function but for the bigger board not the tiny ones


def big_score_check():
    global running
    temp = []
    temp.append(big_gameboard[0])
    temp.append(big_gameboard[4])
    temp.append(big_gameboard[8])
    if temp[0] == temp[1] == temp[2] and len(temp) == 3 and 2 < temp[0]:
        if temp[0] == 4:
            print(f'{player1} is the winner!')
        else:
            print(f'{player2} is the winner!')
        pygame.display.flip()
        running = False
        return
    temp = []
    temp.append(big_gameboard[2])
    temp.append(big_gameboard[4])
    temp.append(big_gameboard[6])
    if temp[0] == temp[1] == temp[2] and len(temp) == 3 and 2 < temp[0]:
        if temp[0] == 4:
            print(f'{player1} is the winner!')
        else:
            print(f'{player2} is the winner!')
        pygame.display.flip()
        running = False
        return
    #horizontal check
    for j in range(0, 7, 3):
        temp = []
        temp.append(big_gameboard[j])
        temp.append(big_gameboard[j + 1])
        temp.append(big_gameboard[j + 2])
        if temp[0] == temp[1] == temp[2] and len(temp) == 3 and 2 < temp[0]:
            if temp[0] == 4:
                print(f'{player1} is the winner!')
            else:
                print(f'{player2} is the winner!')
            pygame.display.flip()
            running = False
            return
    #vertical check
    for j in range(3):
        temp = []
        temp.append(big_gameboard[j])
        temp.append(big_gameboard[j + 3])
        temp.append(big_gameboard[j + 6])
        if temp[0] == temp[1] == temp[2] and len(temp) == 3 and 2 < temp[0]:
            if temp[0] == 4:
                print(f'{player1} is the winner!')
            else:
                print(f'{player2} is the winner!')
            pygame.display.flip()
            running = False
            return


#updating screen
while running:
    screen.blit(gameboard_image, (3, 1))
    pygame.display.flip()
    score_check()

#while not running:
#  answer = input("play again? y/n   ")
#  if answer == "y":
#    running = True
#  else:
#    break

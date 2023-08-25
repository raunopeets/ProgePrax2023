import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen size
screen = pygame.display.set_mode((800, 600))

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set font
font = pygame.font.Font(None, 36)

# Set questions and answers
questions = ["2X + 3 = 9, Mis on X?", "Kelle nimeliseks taheti kool muuta aastal 2022?", "Kuidas importida pygame'i?", "Millises kuulsas viktoriini mängus osales Kristjan Vällik?", "Mis on õpetaja Ene Soolepa hüüdnimi?"]
answers = ["3", "Kalju Aigro", "import pygame", "Kuldvillak", "Sollu"]


# Set grid size
grid_width = 20
grid_height = 10

# Set cell size
cell_width = 40
cell_height = 40

# Set player position
player_x = 0
player_y = 0

# Set question positions
question_positions = []
for i in range(len(questions)):
    x = random.randint(0, grid_width - 1)
    y = random.randint(0, grid_height - 1)
    question_positions.append((x, y))

# Set current question index
current_question_index = 0

# Set game over flag
game_over = False

# Set win flag
win = False

# Set text input flag
text_input = False

# Set text input string
text_input_string = ""

player_out = False

# Game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if text_input:
                if event.key == pygame.K_RETURN:
                    if text_input_string.lower() == answers[current_question_index].lower():
                        current_question_index += 1
                        if current_question_index >= len(questions):
                            win = True
                    else:
                        game_over = True
                    text_input_string = ""
                    text_input = False
                elif event.key == pygame.K_BACKSPACE:
                    text_input_string = text_input_string[:-1]
                else:
                    text_input_string += event.unicode
            else:
                if player_out:
                    game_over = True
                    break
                if event.key == pygame.K_LEFT:
                    player_x -= 1
                    if player_x < 0:
                        player_x=0
                elif event.key == pygame.K_RIGHT:
                    player_x += 1
                    if player_x >= grid_width:
                        player_x=grid_width-1
                elif event.key == pygame.K_UP:
                    player_y -= 1
                    if player_y < 0:
                        player_y=0
                elif event.key == pygame.K_DOWN:
                    player_y += 1
                    if player_y >= grid_height and (not win or player_x > 0):
                        player_y=grid_height-1

                elif event.key == pygame.K_RETURN:
                    if (player_x, player_y) in question_positions:
                        index = question_positions.index((player_x, player_y))
                        if index == current_question_index:
                            text_input_string = ""
                            text_input = True

    # Draw walls.
    rect=(0,0,2,grid_height*cell_height)
    pygame.draw.rect(screen,BLACK,rect)
    rect=(grid_width*cell_width-2,0,2,grid_height*cell_height)
    pygame.draw.rect(screen,BLACK,rect)

    rect=(0,0,grid_width*cell_width-2,2)
    pygame.draw.rect(screen,BLACK,rect)
    rect=(0,grid_height*cell_height,grid_width*cell_width, 2)
    pygame.draw.rect(screen,BLACK,rect)

    # Draw exit.
    if win:
        rect=(0,grid_height*cell_height,cell_width,2)
        pygame.draw.rect(screen,WHITE,rect)
    else:
        # Draw questions that have not been answered yet.
        position=question_positions[current_question_index]
        x,y=position
        text=font.render("?",True,BLACK)
        screen.blit(text,(x*cell_width+cell_width/2-text.get_width()/2,y*cell_height+cell_height/2-text.get_height()/2))

    # Draw player.
    rect=(player_x*cell_width+cell_width/4,player_y*cell_height+cell_height/4,cell_width/2,cell_height/2)
    pygame.draw.ellipse(screen,RED,rect)

    # Draw current question and answer box if necessary.
    if current_question_index<len(questions) and text_input:
        question_text=font.render(questions[current_question_index],True,BLACK)
        screen.blit(question_text,(screen.get_width()/2-question_text.get_width()/2,grid_height*cell_height+10))
        answer_text=font.render(text_input_string,True,BLACK)
        screen.blit(answer_text,(screen.get_width()/2-answer_text.get_width()/2,grid_height*cell_height+50))

    if player_y == grid_height:
        player_out = True

    # Update screen
    pygame.display.flip()

    # Clear screen
    screen.fill(WHITE)

# Show end screen
if win:
    text = font.render("Palju õnne! Sa läbisid mängu edukalt :)", True, GREEN)
else:
    text = font.render("Sa kaotasid :(", True, RED)
screen.blit(text, (screen.get_width() / 2 - text.get_width() / 2, screen.get_height() / 2 - text.get_height() / 2))
pygame.display.flip()

# Wait for user to close window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
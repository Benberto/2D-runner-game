import pygame
from pygame.locals import *
from sys import exit
from random import randint
import sys


def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
          pygame.quit()
          sys.exit()


def display_score():
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  score_surf = test_font.render(f'Score: {current_time}', False, (64,64,64))
  score_rect = score_surf.get_rect(center = (400, 20))
  screen.blit(score_surf, score_rect)
  return current_time

def obstacle_movement(obstacle_list):
      if obstacle_list:
          for obstacle_rect in obstacle_list:
              obstacle_rect.x -= 5 

              if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
              else: screen.blit(fly_surf, obstacle_rect)

          obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

          return obstacle_list
      else: return []

def collisions(player,obstacles):
  if obstacles:
      for obstacle_rect in obstacles:
          if player.colliderect(obstacle_rect):
            pygame.mixer.Sound.play(game_over)
            return False
          
  return True

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
pygame.mixer.init()

jump_sound = pygame.mixer.Sound('audio/jump.wav')
jump_sound.set_volume(0.1)
game_over = pygame.mixer.Sound('audio/GameOver.wav')
game_over.set_volume(0.3)
start_game = pygame.mixer.Sound('audio/Retro_Game_Sounds_SFX_92.wav')
start_game.set_volume(0.3)

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/Sky2.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
x=0

# Background loop



# score_surf = test_font.render('Score: ', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400, 20))
# Obstacles
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []



pygame.mixer.music.set_volume(0.03)





player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

# intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))
game_name = test_font.render('Pixel Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))
game_message = test_font.render('Press space to Start!', False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400, 340))
 
# timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1600)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,100)

while True:
    rel_x = x % sky_surface.get_rect().width
    screen.blit(sky_surface, (rel_x - sky_surface.get_rect().width, 0))
    if rel_x > 0:
      screen.blit(sky_surface, (rel_x, 0))
    x -= .6
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
        if game_active:
          if event.type == pygame.MOUSEBUTTONDOWN:
              if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                player_gravity = -20
                # pygame.mixer.music.stop()
                pygame.mixer.Sound.play(jump_sound)
                
      
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                  player_gravity = -20
                  # pygame.mixer.music.stop()
                  pygame.mixer.Sound.play(jump_sound)
                   
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active= True
                pygame.mixer.Sound.play(start_game)
                background_music = pygame.mixer.music.load('audio/music.wav')
                pygame.mixer.music.play(-1)
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
              if randint(0,2):
                obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100),300)))
              else: 
                obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

      

    
          

    if game_active:
        # screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
      

          
      # pygame.draw.rect(screen, '#c0e8ec', score_rect)
      # pygame.draw.rect(screen, '#c0e8ec', score_rect,10)
      # screen.blit(score_surf, score_rect)
        score = display_score()

      # snail_rect.left -=4
      # if snail_rect.right <= 0: snail_rect.left = 800
      # screen.blit(snail_surf, snail_rect)

      # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf,player_rect)

      # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collisions
        game_active = collisions(player_rect,obstacle_rect_list)
      

    else:
      screen.fill((94,124,162))
      screen.blit(player_stand,player_stand_rect)
      obstacle_rect_list.clear()
      player_rect.midbottom = (80,300)
      player_gravity = 0

      score_message = test_font.render(f'Your score: {score}', False,(111,196,169))
      score_message_rect = score_message.get_rect(center = (400,330))
      screen.blit(game_name,game_name_rect)
      

      if score == 0:
           screen.blit(game_message,game_message_rect)
      else: screen.blit(score_message,score_message_rect) and pygame.mixer.music.stop()


    pygame.display.update()
    clock.tick(60) 
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:07:58 2020

@author: Radwane
"""

import pygame as pg
import sys
import random

pg.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=512)
pg.init()
s_w=576
s_h=1024
screen=pg.display.set_mode((s_w,s_h))
clock=pg.time.Clock()
floor_x=0


#loading and scaling images 
bg_d=pg.image.load('images/background-day.png').convert()
bg_d=pg.transform.scale2x(bg_d)
floor=pg.image.load('images/base.png').convert()
floor=pg.transform.scale2x(floor)

bird_df=pg.image.load('images/redbird-downflap.png').convert_alpha()
bird_df=pg.transform.scale2x(bird_df)
bird_mf=pg.image.load('images/redbird-midflap.png').convert_alpha()
bird_mf=pg.transform.scale2x(bird_mf)
bird_uf=pg.image.load('images/redbird-upflap.png').convert_alpha()
bird_uf=pg.transform.scale2x(bird_uf)
bird_an=[bird_df,bird_mf,bird_uf]
bird_ind=0
bird=bird_an[bird_ind]
bird_rect=bird.get_rect(center=(100,s_h/2))
pipe=pg.image.load('images/pipe-green.png').convert()
pipe=pg.transform.scale2x(pipe)
flap=pg.USEREVENT+1
pg.time.set_timer(flap,200)
game_over=pg.transform.scale2x(pg.image.load('images/gameover.png')).convert_alpha()
game_over_rect=game_over.get_rect(center=(s_w/2,s_h/2))

#Sounds
flap_sound=pg.mixer.Sound('sound/sfx_wing.wav')
die =pg.mixer.Sound('sound/sfx_hit.wav')
score_sound=pg.mixer.Sound('sound/sfx_point.wav')
#moving the floor
def move_floor():
    screen.blit(floor,(floor_x,900))
    screen.blit(floor,(floor_x+s_w,900))

#game gravity and bird movement
gravity=0.25
bird_move=0

#the pipes
pipe_list=[]
pipe_event=pg.USEREVENT
pg.time.set_timer(pipe_event,1200)
def create_pipe():
    rand_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe.get_rect(midtop=(700,rand_pipe_pos))
    top_pipe=pipe.get_rect(midbottom=(700,rand_pipe_pos-300))
    return bottom_pipe,top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx-=5
    return pipes
def draw_pipes(pipes):
    for one in pipes:
        if one.bottom>=s_h:
            screen.blit(pipe,one)
        else:
            flip_pipe=pg.transform.flip(pipe,False, True)
            screen.blit(flip_pipe,one)
pipe_height =[400,600,800]

#Collisions 
def check_collision(pipes):
    for one in pipes:
        if bird_rect.colliderect(one):
            die.play()
            return False
            
    if bird_rect.top<=-100 or bird_rect.bottom>=900:
        die.play()
        return False
    return True

#rotating the bird
def rotate_bird(bird):
   new_bird=pg.transform.rotozoom(bird,-bird_move*3,1) 
   return new_bird

def bird_ani():
    n_bird=bird_an[bird_ind]
    n_bird_rect=n_bird.get_rect(center=(100,bird_rect.centery))
    return n_bird,n_bird_rect

#score and text
s=0
hs=0

        
        
g_font=pg.font.Font('04B_19.TTF',40)
def score_dis_on():
    score_s=g_font.render(str(s), True,(255,255,255))
    score_rect=score_s.get_rect(center=(288,100))
    screen.blit(score_s,score_rect)
def score_dis_off():
    score_s=g_font.render(f'Score : {str(s)}', True,(255,255,255))
    score_rect=score_s.get_rect(center=(288,100))
    screen.blit(score_s,score_rect)
def high_score_dis():
    high_score_s=g_font.render(f'High score : {str(hs)}', True,(255,255,255))
    high_score_rect=high_score_s.get_rect(center=(288,850))
    screen.blit(high_score_s,high_score_rect)


#the main game loop
game=True

while True:
    #Event loop: 
    for event in pg.event.get():
        #Exit strategy
        if event.type==pg.QUIT:
            pg.quit()
            sys.exit()
        #user input
        if event.type==pg.KEYDOWN:
            if event.key==pg.K_SPACE and game:
                bird_move=0
                bird_move-=10
                
                flap_sound.play()
            if event.key==pg.K_SPACE and game==False:
                game=True
                pipe_list.clear()
                bird_rect.center= (100,s_h/2)
                bird_move=0
                s=0
        #generating pipes every 1.2 seconds
        if event.type ==pipe_event:
            pipe_list.extend(create_pipe())
            
            
        if event.type ==flap:
            if bird_ind<2:
                bird_ind+=1
            else:
                bird_ind=0
            bird,bird_rect=bird_ani()
    
    #outputing the images:
    #background
    screen.blit(bg_d,(0,0))
    #moving floor
    floor_x-=1
    move_floor()
    if floor_x<=-s_w:
        floor_x=0
    if game:
        #bird moving
        bird_move+=gravity
        rot_bird=rotate_bird(bird)
        bird_rect.centery +=bird_move
        screen.blit(rot_bird,bird_rect)
        #pipes
        pipe_list=move_pipe(pipe_list)
        draw_pipes(pipe_list)
        game=check_collision(pipe_list)
        for one in pipe_list:
            if  bird_rect.centerx == one.centerx:
                score_sound.play()
                s+=1
                break 
                   
        if s>hs:
           hs=s
            
        score_dis_on()
    else:
         screen.blit(game_over,game_over_rect)
         score_dis_off()
         high_score_dis()
        
    #updating the display
    pg.display.update()
    
    #setting the FPS (framerate)
    clock.tick(120)
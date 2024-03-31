#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Ars
#
# Created:     21.03.2024
# Copyright:   (c) Ars 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from ursina import *

app = Ursina()
window.color = color.gray

player = Entity(model='sphere', position=(0, 0.5, 0), scale=0.5, collider='sphere')
ground = Entity(model='cube', position=(0, 0, 0), scale=(10, 0.1, 10), color=color.red, collider='box')

blok = Entity(model='cube', position=(13, 0.2, 0), scale=(0.3, 0.3, 10), color=color.pink, collider='box')
blok_2 = Entity(model='cube', position=(0, 0.2, 19), scale=(10, 0.3, 0.3), color=color.pink, collider='box')
blok_3 = Entity(model='cube', position=(20, 0.2, 0), scale=(0.3, 0.3, 10), color=color.pink, collider='box')
blok_4 = Entity(model='cube', position=(0, 0.2, 25), scale=(10, 0.3, 0.3), color=color.pink, collider='box')

pivot = Entity()
DirectionalLight(parent=pivot, y=0, z=0, shadows=True, rotation=(50, 0, 0))

camera.position = (0, 10, -20)
camera.rotation=(27, 0, 0)

jump_force = 1
gravity = 0.005
jump_velocity = 0.01

player.on_ground = False

original_position = Vec3(0, 0.5, 0)
fall_time = 0.0
fall_duration = 3.0

jump_timer = 0.0
game_over = False

direction = 1
direction_2 = 1
direction_3 = 1
direction_4 = 1

def update():
    global fall_time, jump_timer, jump_velocity, direction, direction_2, direction_3, direction_4, game_over

    blok.x += 0.003 * direction
    blok_2.z -= 0.003 * direction_2
    blok_3.x += 0.003 * direction_3
    blok_4.z -= 0.003 * direction_4

    if abs(blok.x) > 13:
        direction *= -1
    if abs(blok_2.z) > 19:
        direction_2 *= -1
    if abs(blok_3.x) > 20:
        direction_3 *= -1
    if abs(blok_4.z) > 25:
        direction_4 *= -1

    if player.x > 5 or player.x < -5 or player.z > 5 or player.z < -5:
        if fall_time < fall_duration:
            player.y -= 0.01
            fall_time += time.dt
        else:
            player.position = original_position
            fall_time = 0.0
            game_over = True
        return

    if player.on_ground:
        if held_keys['d']:
            player.x += 0.003
        if held_keys['a']:
            player.x -= 0.003
        if held_keys['w']:
            player.z += 0.003
        if held_keys['s']:
            player.z -= 0.003
    else:
        if player.y > 0:
            player.y -= gravity
            if held_keys['d']:
                player.x += 0.003
            if held_keys['a']:
                player.x -= 0.003
            if held_keys['w']:
                player.z += 0.003
            if held_keys['s']:
                player.z -= 0.003
        else:
            player.on_ground = True

    if player.intersects(ground).hit:
        player.on_ground = True

    if player.intersects(blok).hit or player.intersects(blok_2).hit or player.intersects(blok_3).hit or player.intersects(blok_4).hit:
        game_over = True

    if held_keys['space'] and player.on_ground:
        player.on_ground = False
        jump_timer = 0.0
        jump_velocity = 0.01

    if not player.on_ground:
        jump_timer += time.dt

        if jump_timer < 0.4:
            player.y += jump_velocity
            jump_velocity += 0.001 * time.dt

    if game_over:
        player.position = original_position
        fall_time = 0
        game_over = False

app.run()
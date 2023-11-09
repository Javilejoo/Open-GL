import pygame
from pygame.locals import *
from OpenGL.GL import *
from gl import Renderer
from shaders import *
from obj import Obj


width = 960
height = 540

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, unlit_shader)

obj = Obj("models/dittoo.obj", "textures/ditto.png")

obj.model.position.z -= 10
obj.model.position.y -= 2

obj.model.scale.x = 2
obj.model.scale.y = 2
obj.model.scale.z = 2

rend.scene.append(obj.model)
rend.target = obj.model.position


isRunning = True
while isRunning:
    deltaTime = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_SPACE:
                rend.toggleFilledMode()
            elif event.key == pygame.K_0:
                rend.setShaders(vertex_shader, unlit_shader)
            elif event.key == pygame.K_1:
                rend.setShaders(fat_vertex_shader, trip_shader)
            elif event.key == pygame.K_2:
                rend.setShaders(vertex_shader, rainbow_shader)
            elif event.key == pygame.K_3:
                rend.setShaders(vertex_shader,color_wave_shader)
            elif event.key == pygame.K_4:
                rend.setShaders(vertex_shader, cel_shading)
            elif event.key == pygame.K_5:
                rend.setShaders(vertex_shader, shader_rayX)
            elif event.key == pygame.K_6:
                rend.setShaders(vertices, unlit_shader)
            elif event.key == pygame.K_8:
                rend.setShaders(vertex_shader, toon_shader)
            elif event.key == pygame.K_9:
                rend.setShaders(vertex_shader, gourad_shader)




        
    if keys[K_d]:
        rend.camPosition.x += 5 * deltaTime
    elif keys[K_a]:
        rend.camPosition.x -= 5 * deltaTime
        
    if keys[K_w]:
        rend.camPosition.y -= 5 * deltaTime
    elif keys[K_s]:
        rend.camPosition.y += 5 * deltaTime

    if keys[K_q]:
        rend.camPosition.z += 5 * deltaTime
    elif keys[K_e]:
        rend.camPosition.z -= 5 * deltaTime

    if keys[K_UP] :
        if rend.fatness < 1.0:
            rend.fatness += 1 * deltaTime
    elif keys[K_DOWN]:
        if rend.fatness > 0.0:
            rend.fatness -= 1 * deltaTime
    
    if keys[K_RIGHT]:
        if rend.fatness < 1.0:
            rend.fatness += 1.0 * deltaTime

    elif keys[K_LEFT]:
        if rend.fatness > 0.0:
            rend.fatness -= 1.0 * deltaTime

    obj.model.rotation.y += 45 * deltaTime * 2
    
    rend.elapsedTime +=  deltaTime
    
    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()

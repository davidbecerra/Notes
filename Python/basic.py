"""
A basic pymunk Physics simulation of a single ball and a V shaped floor.
  Pygame is used to render the graphics.
  Features: The ball can be moved by grabbing it with the left mouse button.
  Clicking the A-button will toggle whether the ball attaches to floors on
  contact.
"""
import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk.pygame_util import draw

import sys
import math

# Global Vars
g_width, g_height = 400, 400
g_bgcolor = Color(55, 55, 55) #RGB

# Collision Types
COLLTYPE_FLOOR = 0
COLLTYPE_BALL = 1

# Display Text
g_text = """ESC or Q: Quit
R: reset simulation
A: Toggle floor-ball attachment on collision"""

def create_floor(space):
  """Creates the floor for the simulation space. Adds floor object to space."""
  ## Compute endpoints of each line segment that composes the floor
  angle = 60 # angle in degrees
  dx = g_width * 0.25
  x0, y0 = (0, g_height * 0.60)
  x1, y1 = (x0 + dx, y0)
  dy = dx * math.tan(angle * math.pi / 180.0)
  x2, y2 = (x1 + dx, y1 - dy)
  x3, y3 = (x2 + dx, y0)
  x4, y4 = (g_width, y0)
  ## Create the line segments in pymunk
  floor = [pymunk.Segment(space.static_body, (x0, y0), (x1, y1), 5),
          pymunk.Segment(space.static_body, (x1, y1), (x2, y2), 5),
          pymunk.Segment(space.static_body, (x2, y2), (x3, y3), 5),
          pymunk.Segment(space.static_body, (x3, y3), (x4, y4), 5)
        ]
  ## Define properties for each segment
  for segment in floor:
    segment.friction = 1.0
    segment.color = THECOLORS["red"]
    segment.collision_type = COLLTYPE_FLOOR
  ## Add floor to pymunk space
  space.add(floor)
  return

def create_ball(space):
  """
  Creates a single ball dropped onto the floor. Does not add ball to space.
  Instead, it returns the ball body and shape
  """
  mass = 10
  radius = 30
  moment = pymunk.moment_for_circle(mass, 0, radius, offset=(0,0))
  ball_body = pymunk.Body(mass, moment)
  ball_shape = pymunk.Circle(ball_body, radius)

  ball_shape.color = THECOLORS["green"]
  ball_shape.collision_type = COLLTYPE_BALL
  ball_body.position = (200, g_height * 0.8)
  ball_body.start_position = pymunk.Vec2d(ball_body.position)
  ball_body.is_attached = False
  # ball_body.elasticity = 1.0
  space.add(ball_body, ball_shape)
  return
  # return ball_body, ball_shape

def reset_objects(space):
  """
  Resets body to initial position with no motion or forces
  Removes all constraints in space (i.e. joints, springs, motors)
  """
  for body in space.bodies:
    body.position = pymunk.Vec2d(body.start_position)
    body.reset_forces()
    body.velocity = (0,0)
    body.angular_velocity = 0
    body.is_attached = False
  space.remove(space.constraints)
  return

def render_text(screen):
  """Attaches the onscreen text in g_text that will be drawn on the screen to screen"""
  font = pygame.font.SysFont("Arial", 16)
  font.set_bold(True)
  y_text = 5
  for line in g_text.splitlines():
    text = font.render(line, 1, THECOLORS["white"])
    screen.blit(text, (5,y_text))
    y_text += 20

def ball_attach(space, arbiter):
  """
  Collision Handler between floor and ball.

  Creates a spring at the point of contact. There will only be one active spring
  attachment point per ball.
  Returns True so Pymunk performs normal collision physics b/w the colliding objects
  """
  floor, ball = arbiter.shapes
  if ball.body.is_attached: return True
  contact_point = arbiter.contacts[0].position
  floor_anchor = contact_point
  ball_anchor = ball.body.world_to_local(contact_point)
  joint = pymunk.DampedSpring(floor.body, ball.body, floor_anchor, ball_anchor,
              2, 100, 10) # spring rest length, stiffness, damping - adjust accordingly
  space.add(joint)
  ball.body.is_attached = True  
  return True

def main():
  ### Allows quick conversion b/w pygame coordinates and pymunk coordinates
  def toPygame(p):
      return int(p.x), int(g_height - p.y)
  def toPymunk(p): 
      return toPygame(p)

  ### Pygame init
  pygame.init()
  screen = pygame.display.set_mode((g_width, g_height), RESIZABLE)
  clock = pygame.time.Clock()
  screen.fill(g_bgcolor)

  ### Physics
  space = pymunk.Space()
  space.gravity = (0.0, -900.0) 
  # Create physics bodies (floor, ball, mouse)
  create_floor(space)
  create_ball(space)
  mouse_body = pymunk.Body()
  mouse_selected = None # object mouse is currently holding

  # space.add_collision_handler(COLLTYPE_FLOOR, COLLTYPE_BALL, begin = ball_attach)
  collisions_on = False

  ### Main loop
  while True:
    ## Handle events like keyboard clicks
    for event in pygame.event.get():
      # Quitting simulation (clicking ESC or Q)
      if event.type == QUIT or \
        event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
          pygame.display.quit()
          sys.exit(0)
      # Clicking R - reset simulation
      elif event.type == KEYDOWN and event.key == K_r:
        reset_objects(space)
      # Clicking A - toggle floor-ball attachment on collision
      elif event.type == KEYDOWN and event.key == K_a:
        if collisions_on: # Turn OFF floor-ball attachment
          space.remove(space.constraints)
          for body in space.bodies:
            body.is_attached = False
          space.remove_collision_handler(COLLTYPE_FLOOR, COLLTYPE_BALL)
        else:             # Turn ON floor-ball attachment
          space.add_collision_handler(COLLTYPE_FLOOR, COLLTYPE_BALL, begin = ball_attach)
        collisions_on = not collisions_on
      # Left Mouse button (Hold) - grab ball object
      elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        p = toPymunk(pymunk.Vec2d(event.pos))
        shape = space.point_query_first(p)
        if shape and shape.collision_type == COLLTYPE_BALL: 
          shape.body.position = toPymunk(pymunk.Vec2d(pygame.mouse.get_pos()))
          shape.body.reset_forces()
          shape.body.velocity = (0,0)
          shape.body.angular_velocity = 0
          shape.body.sleep() # turn off ball physics; just move with mouse
          mouse_selected = shape
      #Left Mouse button (Release) - release ball object
      elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        if mouse_selected:
          mouse_selected.body.activate() # wake up object
          mouse_selected = None

    ### Clear screen
    screen.fill(g_bgcolor)

    ### Draw
    pymunk.pygame_util.draw(screen, space)
    render_text(screen)

    ### Update physics
    mouse_p = pygame.mouse.get_pos()
    mouse_body.position = toPymunk(pymunk.Vec2d(mouse_p))
    if mouse_selected:
      mouse_selected.body.position = mouse_body.position
    frame_rate = 30 # frames per second
    dt = 1. / frame_rate
    space.step(dt)

    ### Flip screen
    pygame.display.flip()
    clock.tick(frame_rate)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
  return

if __name__ == '__main__':
  main()
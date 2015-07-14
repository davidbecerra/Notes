"""
A basic pymunk Physics simulation of a single ball and a V shaped floor.
  Pygame is used to render the graphics.
  Features: The ball can be moved by grabbing it with the left mouse button.
  Clicking the A-button will toggle whether the ball attaches to floors on
  contact. Clicking the arrow keys increases/decreases the ball's mass or the 
  spring's stiffness. The spring will break if the tension is too high.
"""
import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk.pygame_util import draw

import sys
import math

# Collision Types
COLLTYPE_FLOOR = 0
COLLTYPE_BALL = 1

### Global Vars #####################
g_width, g_height = 800, 600
g_bgcolor = Color(255, 255, 255) #RGB
g_start_mass = 10.0
g_start_stiffness = 100.0
# Display Text
g_text = """ESC or Q: Quit
R: reset simulation
A: Toggle floor-ball attachment on collision

Mass of ball: {0}
Spring stiffness: {1}
"""
g_display_mass = g_start_mass
g_stiffness = g_start_stiffness
g_collisions_on = False
#####################################

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
  """Creates a single ball dropped onto the floor."""
  mass = g_start_mass
  radius = 20
  moment = pymunk.moment_for_circle(mass, 0, radius, offset=(0,0))
  ball_body = pymunk.Body(mass, moment)
  ball_shape = pymunk.Circle(ball_body, radius)

  ball_shape.color = THECOLORS["green"]
  ball_shape.collision_type = COLLTYPE_BALL
  ball_shape.friction = 0.94
  ball_body.position = (g_width * 0.3, g_height * 0.8)
  ball_body.start_position = pymunk.Vec2d(ball_body.position)
  ball_body.is_attached = False
  space.add(ball_body, ball_shape)
  return

def reset_objects(space):
  """
  Resets body to initial position with no motion or forces
  Removes all constraints in space (i.e. joints, springs, motors)
  Resets global mass and stiffness variables for onscreen display
  """
  for body in space.bodies:
    body.position = pymunk.Vec2d(body.start_position)
    body.reset_forces()
    body.velocity = (0,0)
    body.angular_velocity = 0
    body.is_attached = False
    body.mass = g_start_mass
    moment = pymunk.moment_for_circle(body.mass, 0, 20)
    body.moment = moment
  global g_display_mass, g_stiffness
  g_display_mass = g_start_mass
  g_stiffness = g_start_stiffness
  space.remove(space.constraints)
  return

def render_text(screen):
  """Attaches the onscreen text in g_text that will be drawn on the screen to screen"""
  font = pygame.font.SysFont("Arial", 16)
  font.set_bold(True)
  y_text = 5
  for line in g_text.format(g_display_mass, g_stiffness).splitlines():
    text = font.render(line, 1, THECOLORS["black"])
    screen.blit(text, (5,y_text))
    y_text += 20

  color = THECOLORS["green"] if g_collisions_on else THECOLORS["red"]
  msg = "Spring Collisions: On" if g_collisions_on else "Spring Collisions: Off"
  text = font.render(msg, 1, color)
  screen.blit(text, (5, y_text))

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
              2, g_start_stiffness, 10) # spring rest length, stiffness, damping - adjust accordingly
  joint.max_force = 500.0
  space.add(joint)
  ball.body.is_attached = True  
  return True

def change_mass(shape, delta):
  """
  Alters the mass of shape.body. Assumes that shape is a pymunk.Circle.
  Recalculates the correct moment of inertia given the new mass. Mass not allowed
  to go below 0.
  """
  if shape.body.mass + delta <= 0.0: return
  shape.body.mass += delta
  global g_display_mass
  g_display_mass = shape.body.mass 
  shape.body.moment = pymunk.moment_for_circle(shape.body.mass, 0, shape.radius)
  return

def check_spring(space):
  """
  Check the tension in the spring attachment. If it's above the max force
  allowed, then break (i.e. remove) the spring.
  """
  for spring in space.constraints:
    if abs(spring.impulse) > spring.max_force:
      space.remove(spring)
      spring.b.is_attached = False
      print "Spring Broke with impulse: ", spring.impulse
      print "Max Force: ", spring.max_force
    break

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

  global g_collisions_on

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
        if g_collisions_on: # Turn OFF floor-ball attachment
          space.remove(space.constraints)
          for body in space.bodies:
            body.is_attached = False
          space.remove_collision_handler(COLLTYPE_FLOOR, COLLTYPE_BALL)
        else:             # Turn ON floor-ball attachment
          space.add_collision_handler(COLLTYPE_FLOOR, COLLTYPE_BALL, pre_solve = ball_attach)
        g_collisions_on = not g_collisions_on
      # Clicking Left/Right arrow keys - increases/decreases mass of ball by 10
      elif event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_LEFT):
        for shape in space.shapes:
          if shape.collision_type == COLLTYPE_BALL:
            delta = 10 if event.key == K_RIGHT else -10
            change_mass(shape, delta)
            break
      # Up/Down arrow keys - increase/decrease spring stiffness
      elif event.type == KEYDOWN and (event.key == K_UP or event.key == K_DOWN):
        for constraint in space.constraints:
          delta = 50 if event.key == K_UP else -50
          if constraint.stiffness + delta <= 0.0: continue
          constraint.stiffness += delta
          constraint.max_force = constraint.stiffness * 5.0
          global g_stiffness
          g_stiffness = constraint.stiffness
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
    # Check spring tension
    if g_collisions_on:
      check_spring(space)
    frame_rate = 60 # frames per second
    dt = 1. / frame_rate
    space.step(dt)

    ### Flip screen
    pygame.display.flip()
    clock.tick(frame_rate)
    pygame.display.set_caption("fps: " + str(clock.get_fps()))
  return

if __name__ == '__main__':
  main()
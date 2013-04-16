import pyglet, random, math
from game import load, resources, player

# Set up a window
game_window = pyglet.window.Window(800, 600)

#Set up a batch for all of the drawings
main_batch = pyglet.graphics.Batch()

#Set up the two top labels
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="Draw me things", 
                                x=400, y=575, anchor_x='center', batch=main_batch)

#Initialize the player sprite
player_ship = player.Player(x=400, y=300, batch=main_batch)

#Make three asteroids so we have something to shoot at 
asteroids = load.asteroids(3, player_ship.position, main_batch)

#Store all of the objects that update each frame in a list
game_objects = [player_ship] + asteroids

#Make 5 lives in the top right corner
playerLives = load.player_lives(5, main_batch)

#take in events
game_window.push_handlers(player_ship.key_handler)

@game_window.event
def on_draw():
    game_window.clear()
    
    #draw everything in the batch
    main_batch.draw()

def update(dt):
	to_add = []

	for obj in game_objects:
		obj.update(dt)
		#to_add.extend(obj.new_object)
		#obj.new_object = []

	'''Check for all collision detection. If they collide, handle them, then remove'''
	for i in xrange(len(game_objects)):
		for j in xrange(i+1, len(game_objects)):
			obj_1 = game_objects[i]
			obj_2 = game_objects[j]

			#check if collision
			if not obj_1.dead and not obj_2.dead:
				if obj_1.collides_with(obj_2):
					obj_1.handle_collision_with(obj_2)
					obj_2.handle_collision_with(obj_1)
	for to_remove in [obj for obj in game_objects if obj.dead]:
		to_remove.delete()
		game_objects.remove(to_remove)

		#game_objects.extend(to_add)

if __name__ == "__main__":
	#clock at 120 fps
	pyglet.clock.schedule_interval(update, 1/120.0)

	# Tell pyglet to do its thing
	pyglet.app.run()

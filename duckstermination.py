# Bryce Ogden
# Duckstermination
# Final Game

# Shoot gun by pressing spacebar
# Turn gun by pressing left and right arrow keys
# (directions also in game)

from livewires import games, color
import random, math

games.init(screen_width = 900, screen_height = 600, fps = 50)

class Wrap(games.Sprite):
    """ A sprite that wraps around the screen """
    def update(self):
        """ Wrap sprite around screen """
        if self.left > games.screen.width:
            self.right = 0
            
        if self.right < 0:
            self.left = games.screen.width

    def die(self):
        """ Destroy self """
        self.destroy()
        
class Collide(games.Sprite):
    """ A Wrap that can collide with another object """
    def update(self):
        """ Check for overlapping sprites """
        super(Collide, self).update()
							
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.die()
            self.die()               

    def die(self):
        """ Destroy self and then quack """
        duck_quack = games.load_sound("quack.wav")
        duck_quack.play()
        self.destroy()
        
        # add a new duck
        ## this is cool because they are spontaneously spawning from the grass with
        ## the death of a comrade
        x = random.randrange(games.screen.width)
        y = random.randrange(400)
        size = random.choice([Duck.Duck1, Duck.Duck2, Duck.Duck3, Duck.Shadow_duck])
        new_duck = Duck(x = x, y = y, size = size)
        games.screen.add(new_duck)

class Duck(Wrap):
    """ Ducks that float across the screen """
    Duck1 = 1
    Duck2 = 2
    Duck3 = 3
    Shadow_duck = 4
    images = {Duck1  : games.load_image("duck1.png"),
              Duck2 : games.load_image("duck2.png"),
              Duck3  : games.load_image("Untitled-1.png"),
              Shadow_duck : games.load_image("shadow_duck.png") }

    SPEED = 2
    POINTS = 50
    
    total = 0

    def __init__(self, x, y, size):
        """ Initialize duck sprite """
        Duck.total += 2
        super(Duck, self).__init__(
            image = Duck.images[size],
            x = x, y = y,
            dx = random.choice([3.25, 2]) * Duck.SPEED) #* random.random()/size) 
            #dy = random.choice([1, -1]) * Duck.SPEED * random.random()/size)
        
        self.size = size
        
    def die(self):
        """ Destroy duck """
        Duck.total -= 1

        super(Duck, self).die()

        
class Gun(games.Sprite):
    """ The player's gun """
    image = games.load_image("minigun.png")
    ROTATION_STEP = 2
    VELOCITY_STEP = 0.02
    BULLET_DELAY = 25

    def __init__(self, x, y):
        """ Initialize gun sprite """
        super(Gun, self).__init__(image = Gun.image, x = x, y = y)
        self.bullet_wait = 0
        self.is_collideable = False
        
    	self.score = games.Text(value = 0, size = 30, color = color.black,
							top = 5, right = games.screen.width - 15,
							is_collideable = False)
    	games.screen.add(self.score)

    def update(self):
        """ Rotate and fire bullets based on keys pressed """
        super(Gun, self).update()
        
        # rotate based on left and right arrow keys
        if games.keyboard.is_pressed(games.K_LEFT):
            self.angle -= Gun.ROTATION_STEP        
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.angle += Gun.ROTATION_STEP

        # if waiting until the gun can fire next, decrease wait
        if self.bullet_wait > 0:
            self.bullet_wait -= 1
            
        # fire bullet if spacebar pressed and bullet wait is over  
        if games.keyboard.is_pressed(games.K_SPACE) and self.bullet_wait == 0:
            new_bullet = Bullet(self.x, self.y, self.angle, self.score)
            games.screen.add(new_bullet)
            self.bullet_wait = Gun.BULLET_DELAY

class Bullet(Collide):
    """ A bullet shot by the player's gun """
    image = games.load_image("minigun_bullet.png")
    sound = games.load_sound("gunshot.wav")
    BUFFER = 180
    VELOCITY_FACTOR = 7
    LIFETIME = 80

    def __init__(self, gun_x, gun_y, gun_angle, score):
        """ Initialize bullet sprite """
        Bullet.sound.play()
        
        # convert to radians
        angle = gun_angle * math.pi / 180  

        # calculate bullet's starting position 
        buffer_x = Bullet.BUFFER * math.sin(angle)
        buffer_y = Bullet.BUFFER * -math.cos(angle)
        x = gun_x + buffer_x
        y = gun_y + buffer_y

        # calculate bullet's velocity components
        dx = Bullet.VELOCITY_FACTOR * math.sin(angle)
        dy = Bullet.VELOCITY_FACTOR * -math.cos(angle)

        # create the bullet
        super(Bullet, self).__init__(image = Bullet.image,
                                      x = x, y = y,
                                      dx = dx, dy = dy)
        
        # rotate image in relation to gun's angle
        self.angle = gun_angle
        self.lifetime = Bullet.LIFETIME
        self.score = score

    def update(self):
        """ Move the bullet """
        
        # add 50 points if you hit a duck with a bullet
        if self.overlapping_sprites:
        	self.score.value += 1
        	for sprite in self.overlapping_sprites:
        		sprite.die()
        	self.die()
        
        # if 20 ducks have been killed, you win
		if self.score.value == 20:
			end_message = games.Message(value = "Good job!",
										size = 90,
										color = color.blue,
										x = games.screen.width/2,
										y = games.screen.height/2,
										lifetime = 3 * games.screen.fps,
										after_death = games.screen.quit)
			games.screen.add(end_message)

        # if lifetime is up, destroy the bullet   
        self.lifetime -= 1
        if self.lifetime == 0:
            self.destroy()


def main():
	# background
	wall_image = games.load_image("field_background.bmp", transparent = False)
	games.screen.background = wall_image
	
	# when game starts, play sound
	yahoo_sound = games.load_sound("yahoo.wav")
	yahoo_sound.play()
	
	# begin message
	start_message = games.Message(value = "Kill 20 ducks!",
								  size = 90,
								  color = color.blue,
								  x = games.screen.width/2,
								  y = games.screen.height/2,
								  lifetime = games.screen.fps)
	games.screen.add(start_message)
	
	directions_spacebar = games.Message(value = "Spacebar to shoot!",
										size = 25,
										color = color.green,
										is_collideable = False,
										x = games.screen.width/4,
										y = games.screen.height - 20,
										lifetime = 500)
	games.screen.add(directions_spacebar)
	
	directions_turning = games.Message(value = "Turn with <- and -> arrow keys!",
									   size = 25,
									   color = color.green,
									   is_collideable = False,
									   x = games.screen.width - 225,
									   y = games.screen.height - 20,
									   lifetime = 500)
	games.screen.add(directions_turning)
	
	# create 4 ducks
	for i in range(2):
		x = random.randrange(games.screen.width)
		y = random.randrange(400)
		size = random.choice([Duck.Duck1, Duck.Duck2, Duck.Duck3, Duck.Shadow_duck])
		new_duck = Duck(x = x, y = y, size = size)
		games.screen.add(new_duck)
	
	# add the gun	
	the_gun = Gun(x = games.screen.width/2, y = games.screen.height)
	games.screen.add(the_gun)

	games.mouse.is_visible = False

	games.screen.event_grab = True
	games.screen.mainloop()


main()

### image credits ###
# background image : http://puckettpages.com/wp-content/uploads/
#					 bright-blue-sky-above-a-grass-field-with-tall-grass.jpg
# duck 1 image : http://www.floraltrims.com/media/RichardB247.jpg
# duck 2 image : http://techtran.uoregon.edu/files/techtran/FlyingDuck.jpg
# duck 3 image : http://www.animalphotos.biz/wp-content/uploads/2012/06/
#				 Colorful-Mallard-Duck-Flight.jpg
# shadow duck image : http://getitstickit.com/images/watermarked/1/detailed/2/
#					  tmp_7EMgty.jpg
# gun image : http://www.navweaps.com/Weapons/WNUS_30-cal_GAU17_minigun_pic.jpg
# bullet image : http://i.istockimg.com/file_thumbview_approve/1096341/2/
#				 stock-photo-1096341-bullet-chain.jpg
# yahoo sound : soundbible.com
# duck quack sound : soundbible.com
# bullet sound : soundbible.com


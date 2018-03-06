import pygame
import sys
from pygame.locals import DOUBLEBUF,KEYDOWN,K_ESCAPE,FULLSCREEN,K_s
import random

screen = pygame.display.set_mode((640,480), DOUBLEBUF)

clock=pygame.time.Clock()


class Enemylaser(pygame.sprite.Sprite):
	def __init__(self,x,y,group):
		super(Enemylaser,self).__init__()
		self.add(group)
		sheet=pygame.image.load("laser.png").convert_alpha()
		self.image=pygame.Surface((128,32),pygame.SRCALPHA).convert_alpha()
		self.image.blit(sheet,dest = (0,0),area=(0,0,128,32))
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		
	def update(self):
		x,y=self.rect.center
		x-=20
		if x<100:
			self.kill()
		self.rect.center=(x,y)
class explosion(pygame.sprite.Sprite):
	def __init__(self,x,y,group):
		super(explosion,self).__init__()
		self.add(group)
		sheet=pygame.image.load("x.png").convert_alpha()
		self.images=[]
		self.index=0
		for i in range(0,1536,96):
			img=pygame.Surface((96,96),pygame.SRCALPHA).convert_alpha()
			img.blit(sheet,dest=(0,0), area=(i,0,i+96,96))
			self.images.append(img)
		self.image=self.images[-1]
		self.rect=self.image.get_rect()
		self.rect.center=x,y
	def update(self):
		self.image=self.images[self.index]
		self.index+=1
		self.index=len(self.images)-1
		if self.index==0:
			self.kill()	
		
		
		
		
class Enemy(pygame.sprite.Sprite):
	def __init__(self,x,y,fighter,group,fire_group):
		super(Enemy,self).__init__()
		self.image=pygame.image.load("s.png").convert_alpha()
		self.rect=self.image.get_rect()
		self.rect.center=(x,y)
		self.add(group)
		self.fighter=fighter
		self.velocity=0
		self.main_laser_counter=0
		self.fire_group=fire_group
		self.laser=False
	def update(self):
		f_x,f_y=self.fighter.rect.center
		s_x,s_y=self.rect.center
		if s_y>f_y:
			self.velocity= -1
			self.main_laser_counter=0
		elif s_y<f_y:
			self.velocity=1
			self.main_laser_counter=0
		else:
			self.velocity= 0
			if self.main_laser_counter !=10:
				self.main_laser_counter+=1
				
		if not (self.laser and self.laser.alive()):
			if self.main_laser_counter==10:
				self.laser=Enemylaser(s_x-110,s_y,self.fire_group)
			
			
				
			
		s_y+=self.velocity
		self.rect.center=s_x,s_y

class ship(pygame.sprite.Sprite):
	def __init__(self,x,y,group):
		super(ship,self).__init__()
		self.image=pygame.image.load("ship.png").convert_alpha()
		self.good=pygame.image.load("ship.png").convert_alpha()
		self.hit=pygame.image.load("ship-hit.png").convert_alpha()
		self.image=self.good
		self.rect = self.image.get_rect()
		self.rect.center=(x,y)
		self.add(group)
		self.impacted=False
		self.energy=100
		self.all=group
	def impact(self):
		self.impacted=True
		self.energy-=10
	def update(self):
		x,y=pygame.mouse.get_pos()
		self.rect.center=(x,y)
		if self.impacted:
			self.image=self.hit
			self.impacted=False
			print("got hit "+str(self.energy))
		else:
			self.image=self.good
		self.rect.center=(x,y)
		if self.energy<0:
			self.kill()
			explosion(x,y,self.all)
	

class MySprite(pygame.sprite.Sprite):
	def __init__(self,x,y,vel,group):
		super(MySprite, self).__init__()
		self.image = pygame.Surface((3,3))
		self.image.fill((255,255,255))
		self.rect = self.image.get_rect()
		self.rect.center=(x,y)
		self.add(group)
		self.vel=vel
		self.col=0
		
	def update(self):
		self.col+= 20
		self.col%= 255
		x,y = self.rect.center
		
		if x>640:
			x=0
		
		x += self.vel	
		self.rect.center = x,y

all_sprites=pygame.sprite.Group()
enemy_fire=pygame.sprite.Group()

background =pygame.Surface((640,480))

for i in range(100):
	x= random.randint(0,640)
	y=random.randint(0,480)
	MySprite(x,y,5,all_sprites)
for i in range(50):
	x= random.randint(0,640)
	y=random.randint(0,480)
	MySprite(x,y,15,all_sprites)
for i in range(25):
	x= random.randint(0,640)
	y=random.randint(0,480)
	MySprite(x,y,25,all_sprites)
	

fighter=ship(320,240,all_sprites)


Enemy(600,240,fighter,all_sprites,[all_sprites,enemy_fire])

while True :
    
		clock.tick(20)

		for event in pygame.event.get():
			 if event.type == KEYDOWN: #pressing_key
				if event.key == K_ESCAPE:
					print ("thanks for playing")
					sys.exit(0)
		collided = pygame.sprite.spritecollideany(fighter,enemy_fire)
		
		if(collided):
			collided.kill()
			fighter.impact()	 				
		all_sprites.clear(screen,background)
		all_sprites.update()
		all_sprites.draw(screen)		       
	

		pygame.display.flip()
	
raw_input()


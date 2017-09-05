

from visual import *
from visual.graph import *

animscene = display(title='Sun and the earth simulation ',x=0,y=0)

mass_list = [0] # Creating a mass list with 0 items

mass_list.append(1.989e30) # Sun   obj = 1
mass_list.append(5.972e24) # Earth obj = 2

xyz = len(mass_list)-1  #Required for the counter

obj = 1			#Sun

body_list = [0] # Start body list.
velocity_list = [0] # Start velocity list.

# Set up body obj = 1.
x = 0	#Setting up the x co-ordinate as 0
y = 0	#y co-ordinate
z = 0	#z co-ordinate
rad = 696.3e6   #Radius
col = color.yellow	#Adding yellow color to the object

body_list.append(sphere(radius = rad,
                      pos = (x,y,z),
                      color=col,
                      make_trail = False))		#Change this to make trail visible
vx = 0	
vy = 0
vz = 0
velocity_list.append(vector(vx,vy,vz))
    
# Set up body obj = 2.
x = 147.1e9			#Distance to the earth
y = 0				#0
z = 0				#0
rad = 6.371e6		#radiua
col1 = color.blue	#Earth is also known as the blue planet
body_list.append(sphere(radius = rad, 
                      pos = (x,y,z),
                      color= col1,	#Makes it look like Earth
                      make_trail = True))		#Change this to make the trail visible 

angularmomentum = 149.6e9**2 * 2*3.14159 * mass_list[2] / (365.25*24*3600)
vx = 0
vy = angularmomentum/(147.1e9*mass_list[2])
vz = 0
velocity_list.append(vector(vx,vy,vz))

force_list = [0]
obj = 1
while obj <= xyz:
    force_list.append(vector(0,0,0))
    obj = obj + 1

t = 0
dt = 100
G = 6.67e-11 # Graviational constant.

while True: # Begin motion loop.

    rate(5000)			#Randomly from solved examples
	

    obj = 1
    while obj <= xyz:
        force_list[obj] = vector(0,0,0)
        obj = obj + 1

    obj = 1
    while obj <=xyz:
        
        obj2 = obj + 1
        while obj2 <= xyz:
		
            r = body_list[obj].pos - body_list[obj2].pos
            rmag = mag(r)	#For the gravitation formula	
            rhat = r/rmag	#For the gravitation formula
			
            # Calculate force on obj.
            force_list[obj] = force_list[obj] - G*mass_list[obj]*mass_list[obj2]/rmag**2 * rhat
            force_list[obj2] = force_list[obj2] - force_list[obj]		

            obj2 = obj2 + 1
        velocity_list[obj] = velocity_list[obj] + force_list[obj]/mass_list[obj] * dt # Update body obj velocity.
        body_list[obj].pos = body_list[obj].pos + velocity_list[obj]*dt # Update body obj position.
        obj = obj + 1
    t = t + dt

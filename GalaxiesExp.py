
from __future__ import division
from math import fsum
from random import gauss
from visual import *
import numpy as np


# Gravitational constant in N * m^2 / kg^2
G = 6.673e-11

# Solar mass in kg (assume average stellar mass)
SOLAR_MASS = 2.000e30

# Precalculated bounds to solar mass
MIN_SOLAR_MASS = SOLAR_MASS * 0.5
MAX_SOLAR_MASS = SOLAR_MASS * 250
AVG_SOLAR_MASS = SOLAR_MASS * 3.0

# Scale distances for galactic scales
DIST_SCALE = 1e20

# Galactic parameters
MAX_ORBITAL_RADIUS = DIST_SCALE * 10
MIN_ORBITAL_RADIUS = DIST_SCALE * 0.15
GALAXY_THICKNESS = DIST_SCALE * 0.5
NUM_STARS_MILKY_WAY = 500
NUM_STARS_ANDROMEDA = 500

# Graphical constants here
STAR_RADIUS = 0.025

dt = 1e17

# Limit x between lower and upper
def clamp(x, lower, upper):
    return max(min(x, upper), lower)


# Return the force due to gravity on an object
def gravity(mass1, mass2, radius):
    return G * mass1 * mass2 / radius / radius


# Return the acceleration due to gravity on an object.
def g_accel(mass, radius):
    # Limit minimum radius to avoid flinging out too many particles
    radius = max(radius, MIN_ORBITAL_RADIUS)
    return G * mass / radius / radius

class Star(object):
    def __init__(self, mass, radius, pos, vel, color):
        self.obj = sphere(pos=pos / DIST_SCALE, radius=radius, color=color)
        self.mass = mass
        self.vel = vel
        self._pos = pos

    # Externally use scaled version for physics, use normalized version for graphics
    # Make sure _pos = obj.pos * DIST_SCALE is always true
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self.obj.pos = value / DIST_SCALE
        self._pos = value

    def __str__(self):
        return "Mass: " + str(self.mass) + "\nPos: " + str(self.pos) + \
            "\nVel: " + str(self.vel)


class Galaxy(object):
    def __init__(self, num_stars, pos, vel, radius, thickness, color):
        self.pos = pos
        self.vel = vel
        self.radius = radius

        # Gaussian (normal) distributions ftw!
        sigma_mass = AVG_SOLAR_MASS / 3.0
        masses = [clamp(gauss(mu=AVG_SOLAR_MASS, sigma=sigma_mass), MIN_SOLAR_MASS, MAX_SOLAR_MASS)
            for i in xrange(num_stars)]

        # Galaxy mass is sum of all stars
        self.mass = fsum(masses)

        # Gaussian distribution of positions
        sigma_x = radius * 0.1
        sigma_y = thickness * 1.00
        sigma_z = radius * 0.1

        # Generate list of all positions
        positions = []
        for i in xrange(num_stars):
            pos = vector(
                clamp(gauss(mu=0, sigma=sigma_x), -radius, radius),
                clamp(gauss(mu=0, sigma=sigma_y), -thickness, thickness),
                clamp(gauss(mu=0, sigma=sigma_z), -radius, radius)
            )

            # Limit radius to avoid particles shooting to nowhere
            if pos.mag < MIN_ORBITAL_RADIUS:
                pos.mag = MIN_ORBITAL_RADIUS

            positions.append(pos)

        def calc_orbital_velocity(center_mass, radius):
            return sqrt(G * center_mass / radius)

        # Generate list of all stars
        stars = []
        up = vector(0.0, 1.0, 0.0)
        for i in xrange(num_stars):
            # Find normalized vector along direction of travel
            absolute_pos = positions[i] + self.pos
            relative_pos = positions[i]
            vec = relative_pos.cross(up).norm()
            relative_vel = vec * calc_orbital_velocity(self.mass, relative_pos.mag)
            absolute_vel = relative_vel + vel

            stars.append(Star(
                mass=masses[i],
                radius=STAR_RADIUS,
                pos=absolute_pos,
                # From a = v^2/r = Gm/r^2 w we have v = sqrt(G * m / r)
                vel=absolute_vel,
                color=color
            ))

        self.stars = np.array(stars)


# Calculate acceleration on an object caused by galaxy
def accel(obj, galaxy):
    r_galaxy = galaxy.pos - obj.pos
    # We have a = F / m = G * m_center / r ^2
    return r_galaxy.norm() * g_accel(galaxy.mass, r_galaxy.mag)


def main():
    t = 0
    milky_way = Galaxy(
        num_stars=NUM_STARS_MILKY_WAY,
        pos=vector(3, 0, 0) * DIST_SCALE,
        vel=vector(0, 5, 0),
        radius=MAX_ORBITAL_RADIUS,
        thickness=GALAXY_THICKNESS,
        color=color.white
    )
    andromeda = Galaxy(
        num_stars=NUM_STARS_ANDROMEDA,
        pos=vector(-3, 0, 0) * DIST_SCALE,
        vel=vector(0, 0, 0),
        radius=MAX_ORBITAL_RADIUS,
        thickness=GALAXY_THICKNESS,
        color=color.red
    )

    while 1:
        rate(70)

        for i in xrange(len(milky_way.stars)):
            star = milky_way.stars[i]
            star.vel += accel(star, andromeda) * dt
            star.vel += accel(star, milky_way) * dt
            star.pos += star.vel * dt

        andromeda_mask = np.zeros(len(andromeda.stars))

        for star in andromeda.stars:
            star.vel += accel(star, milky_way) * dt
            star.vel += accel(star, andromeda) * dt
            star.pos += star.vel * dt

        milky_way.vel += accel(milky_way, andromeda) * dt
        milky_way.pos += milky_way.vel * dt

        andromeda.vel += accel(andromeda, milky_way) * dt
        andromeda.pos += andromeda.vel * dt

        t += dt


if __name__ == '__main__':
    main()


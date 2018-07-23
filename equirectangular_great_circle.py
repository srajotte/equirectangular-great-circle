#!python3

import numpy as np
import matplotlib.pyplot as plt

def X_rotation_matrix(angle):
	""" Generated 3D rotation matrix. 
	    angle : degrees."""
	Ry = np.zeros((3,3))
	angle = np.deg2rad(angle)
	Ry[0,0] = 1.0
	Ry[1,1] = Ry[-1,-1] = np.cos(angle)
	Ry[1,-1] = -np.sin(angle)
	Ry[-1,1] = np.sin(angle)
	return Ry

def circle_coordinates(samples):
	coord = np.zeros((samples,3))
	angle = np.linspace(-np.pi, np.pi, samples)
	coord[:,0] = np.cos(angle)
	coord[:,1] = np.sin(angle)
	return coord

def great_circle_coordinates(angle, samples=1000):
	circle = circle_coordinates(samples)
	Ry = X_rotation_matrix(angle)
	great_circle = (Ry @ circle.T).T
	return great_circle

def cartesian_to_spherical(cartesian):
	X = cartesian[:,0]
	Y = cartesian[:,1]
	Z = cartesian[:,2]

	rho = np.sqrt(X**2 + Y**2 + Z**2)
	theta = np.arccos(Z / rho)
	phi = np.arctan2(Y, X)
	return np.vstack((rho,theta,phi)).T

def spherical_to_equirectangular(spherical):
	rho = spherical[:,0]
	theta = spherical[:,1]
	phi = spherical[:,2]
	
	altitude = np.rad2deg(theta) - 90.0
	lattitude = np.rad2deg(phi)
	return np.vstack((lattitude, altitude)).T

def equirectangular_great_circle(angle, samples=100):
	great_circle = great_circle_coordinates(angle, samples=samples)
	spherical_great_circle = cartesian_to_spherical(great_circle)
	equirect_great_circle = spherical_to_equirectangular(spherical_great_circle)
	return equirect_great_circle

def main():
	N_samples = 1001
	angles = list(range(0, 90+1, 15)) + [85, 89]
	angles.sort()
	gc = (equirectangular_great_circle(a, samples=N_samples) for a in angles)

	plt.figure()
	for a, xy in zip(angles, gc):
		plt.plot(xy[:,0], xy[:,1], label=str(a) + '°')
	plt.xlim(-180, 180)
	plt.ylim(-90, 90)
	plt.xticks(np.arange(-180.0,181.0, step=45.0))
	plt.yticks(np.arange(-90.0,91.0, step=30.0))
	plt.xlabel('Longitude [degree]')
	plt.ylabel('Lattitude [degree]')
	plt.grid()
	plt.legend(ncol=2)

	plt.savefig('equirectangular_great_circle.png', dpi=200)
	plt.show()

if __name__ == '__main__':
	main()
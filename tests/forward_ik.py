
from os import path as os_path
from sys import path as sys_path

FILE_DIRECTORY = os_path.dirname(os_path.realpath(__file__))

sys_path.append( os_path.join(FILE_DIRECTORY, "..") )

from src import Vector2, Segment2D

sys_path.pop()

def run_2d_test():
	pass

if __name__ == '__main__':
	run_2d_test()
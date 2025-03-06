#include "Room.h"

Room::Room(int coord_x, int coord_y, int size_, int bestiary_ref, int tokens)
{
	active = 0;
	top_left_x = coord_x;
	top_left_y = coord_y;
	size = size_;

	defender_nbr = 0;
	defenders_idx = {};
}
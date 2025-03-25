#pragma once
#include <vector>

using namespace std;

class Room
{
public: //For test purposes, to be modified
	//True if a fight is currently on, False otherwise
	int active;

	int top_left_x, top_left_y;
	int size;

	int tokens;

	unsigned int defender_nbr;

public:
	Room(int coord_x, int coord_y, int size_, int bestiary_ref, int tokens_);

	void Get_hitbox(int& x, int& y, int& size_) const { x = top_left_x; y = top_left_y; size_ = size; };
};


#pragma once
#include <vector>
#include <array>

#include "Object.h"

class Chunk
{
private:

	int x, y;

	bool active;

	std::vector<BasicObject*> props;

	std::array<int, 256> tiles;

	Chunk* leftNeighboor;
	Chunk* rightNeighboor;
	Chunk* upperNeighboor;
	Chunk* lowerNeighboor;

public:

	Chunk(int x, int y);

	bool isActive() { return active; }

	void setActive(bool state) { active = state; }

	int getTile(int x_, int y_) { return tiles[y_ * 16 + x_]; }

	void putTile(int x_, int y_, int value) { tiles[y_ * 16 + x_] = value; } //Not optimal (slow)

	void setNeighboors(Chunk* left, Chunk* upper, Chunk* right, Chunk* lower) {
		leftNeighboor = left; upperNeighboor = upper; rightNeighboor = right; lowerNeighboor = lower;
	}

	//WIP...
};
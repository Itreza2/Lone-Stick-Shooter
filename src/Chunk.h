#pragma once
#include <vector>
#include <array>
#include <iostream>

#include "Object.h"

class Chunk
{
private:

	int x, y;

	bool active;

	std::vector<BasicObject*> props;

	std::array<int, 256> tilesType;

	std::array<int, 256> tiles;

	Chunk* leftNeighboor;
	Chunk* rightNeighboor;
	Chunk* upperNeighboor;
	Chunk* lowerNeighboor;

public:

	Chunk(int x, int y);

	bool isActive() { return active; }

	void setActive(bool state) { active = state; }

	int getPosX() { return x; }

	int getPosY() { return y; }

	int getTile(int x_, int y_) { return tiles[y_ * 16 + x_]; }

	int getTileType(int x_, int y_) { return tilesType[y_ * 16 + x_]; }

	std::vector<BasicObject*> getAllObjects();

	void putTile(int x_, int y_, int type, int value) { tilesType[y_ * 16 + x_] = type; tiles[y_ * 16 + x_] = value; } //Not optimal (slow)

	void setNeighboors(Chunk* left, Chunk* upper, Chunk* right, Chunk* lower) {
		leftNeighboor = left; upperNeighboor = upper; rightNeighboor = right; lowerNeighboor = lower;
	}

	void spawnProp(BasicObject* prop) { props.push_back(prop); }

	/**
	* @brief update, delete and spawn all the objects on the chunk
	*/
	void update();

	//WIP...
};
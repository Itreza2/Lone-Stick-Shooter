#include "Chunk.h"

Chunk::Chunk(int x, int y)
{
	this->x = x;
	this->y = y;

	active = false;

	leftNeighboor = nullptr;
	upperNeighboor = nullptr;
	rightNeighboor = nullptr;
	lowerNeighboor = nullptr;

	props = {};

	tilesType = std::array<int, 256>();
	tilesType.fill(1);

	tiles = std::array<int, 256>();
	tiles.fill(rand() % 256);
}

std::vector<BasicObject*> Chunk::getAllObjects()
{
	std::vector<BasicObject*> res = {};
	res.insert(res.end(), props.begin(), props.end());

	return res;
}
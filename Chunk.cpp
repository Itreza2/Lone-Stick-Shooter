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

	tiles = std::array<int, 256>();
	tiles.fill(2);
}
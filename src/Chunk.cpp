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
	characters = {};

	tilesType = std::array<int, 256>();
	tilesType.fill(0);

	tiles = std::array<int, 256>();
	tiles.fill(0);
}

std::vector<BasicObject*> Chunk::getAllObjects()
{
	std::vector<BasicObject*> res = {};
	res.insert(res.end(), props.begin(), props.end());
	res.insert(res.end(), characters.begin(), characters.end());

	return res;
}

void Chunk::update()
{
	for (int i = 0; i < props.size(); i++) {
		if (props[i]->update()) {
			props.erase(props.begin() + i);
		}
	}
	for (int i = 0; i < characters.size(); i++) {
		if (characters[i]->update()) {
			characters.erase(characters.begin() + i);
		}
	}
}
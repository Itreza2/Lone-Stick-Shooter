#include "Chunk.h"

bool Chunk::gridCollision(SDL_Rect hBox)
{
	Chunk* chunk = this;
	int gridX, gridY;
	for (int column = (hBox.x - x) / 32; column <= (hBox.x - x + hBox.w) / 32; column++) {
		for (int row = (hBox.y - y) / 32; row <= (hBox.y - y + hBox.h) / 32; row++) {
			gridX = column;
			gridY = row;

			if (gridX < 0) {
				if (leftNeighboor == nullptr)
					return true;
				else {
					gridX = 15 + column;
					if (gridY < 0) {
						if (leftNeighboor->upperNeighboor == nullptr)
							return true;
						else {
							chunk = leftNeighboor->upperNeighboor;
							gridY = 15 + gridY;
						}
					} else if (gridY > 15) {
						if (leftNeighboor->lowerNeighboor == nullptr)
							return true;
						else {
							chunk = leftNeighboor->upperNeighboor;
							gridY = gridY - 16;
						}
					} else chunk = leftNeighboor;
				}
			} else if (gridX > 15) {
				if (rightNeighboor == nullptr)
					return true;
				else {
					gridX = gridX - 16;
					if (gridY < 0) {
						if (rightNeighboor->upperNeighboor == nullptr)
							return true;
						else {
							chunk = rightNeighboor->upperNeighboor;
							gridY = 15 + gridY;
						}
					} else if (gridY > 15) {
						if (rightNeighboor->lowerNeighboor == nullptr)
							return true;
						else {
							chunk = rightNeighboor->upperNeighboor;
							gridY = gridY - 16;
						}
					} else chunk = rightNeighboor;
				}
			} else if (gridY < 0) {
				if (upperNeighboor == nullptr)
					return true;
				else {
					chunk = upperNeighboor;
					gridY = 15 + gridY;
				}
			} else if (gridY > 15) {
				if (lowerNeighboor == nullptr)
					return true;
				else {
					chunk = lowerNeighboor;
					gridY = gridY - 16;
				}
			}
			if (chunk->tilesType[gridY * 16 + gridX] != 1)
				return true;
		}
	}
	return false;
}

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
	for (int i = 0; i < props.size(); i++) { // Props (unmovable)
		if (props[i]->update()) {
			props.erase(props.begin() + i);
		}
	}
	for (int i = 0; i < characters.size(); i++) { // Characters
		if (characters[i]->update()) {
			characters.erase(characters.begin() + i);
		}
		else {
			if (gridCollision(characters[i]->getGroundHitBox()))
				characters[i]->revert();
			for (BasicObject* prop : props) {
				if (characters[i]->collision(prop->getHitbox()))
					characters[i]->revert();
			}
			if (characters[i]->getHitbox().x < x) {
				leftNeighboor->characters.push_back(std::move(characters[i]));
				characters.erase(characters.begin() + i);
			}
			else if (characters[i]->getHitbox().x > x + 32 * 16) {
				rightNeighboor->characters.push_back(std::move(characters[i]));
				characters.erase(characters.begin() + i);
			}
			else if (characters[i]->getHitbox().y < y) {
				upperNeighboor->characters.push_back(std::move(characters[i]));
				characters.erase(characters.begin() + i);
			}
			else if (characters[i]->getHitbox().y > y + 32 * 16) {
				lowerNeighboor->characters.push_back(std::move(characters[i]));
				characters.erase(characters.begin() + i);
			}
		}
	}
}
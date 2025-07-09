#include "Level.h"

void Level::initChunks()
{
	Chunk* left;
	Chunk* upper;
	Chunk* right;
	Chunk* lower;

	for (int i = 0; i < chunks.size(); i++) {
		chunks.at(i) = std::make_unique<Chunk>((i / 10) * 512 , (i % 10) * 512);
	}
	for (int i = 0; i < chunks.size(); i++) {
		left = nullptr;
		if (i % 10 != 0)
			left = chunks.at((i / 10) * 10 + (i % 10 - 1)).get();
		right = nullptr;
		if (i % 10 != 9)
			right = chunks.at((i / 10) * 10 + (i % 10 + 1)).get();
		upper = nullptr;
		if (i / 10 != 0)
			upper = chunks.at((i / 10 - 1) * 10 + (i % 10)).get();
		lower = nullptr;
		if (i / 10 != 9)
			lower = chunks.at((i / 10 + 1) * 10 + (i % 10)).get();

		chunks.at((i / 10) * 10 + i % 10)->setNeighboors(left, upper, right, lower);
	}
}

void Level::spawnProp(BasicObject* prop)
{
	chunks[(prop->getHitbox().x / (16 * 32)) * 10 + (prop->getHitbox().y / (16 * 32))]->spawnProp(prop);
}

Level::Level()
{
	chunks = std::array<std::unique_ptr<Chunk>, 100>();
	initChunks();

	spawnProp(new BasicObject(2700, 2700, BasicObject::loadModel("tree1")));
}
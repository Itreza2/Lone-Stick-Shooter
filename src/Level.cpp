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
		upper = nullptr;
		if (i % 10 != 0)
			upper = chunks.at((i / 10) * 10 + (i % 10 - 1)).get();
		lower = nullptr;
		if (i % 10 != 9)
			lower = chunks.at((i / 10) * 10 + (i % 10 + 1)).get();
		left = nullptr;
		if (i / 10 != 0)
			left = chunks.at((i / 10 - 1) * 10 + (i % 10)).get();
		right = nullptr;
		if (i / 10 != 9)
			right = chunks.at((i / 10 + 1) * 10 + (i % 10)).get();

		chunks.at((i / 10) * 10 + i % 10)->setNeighboors(left, upper, right, lower);
	}
}

void Level::spawnText(Text* text)
{
	chunks[(text->getBox().x / (16 * 32)) * 10 + (text->getBox().y / (16 * 32))]->spawnText(text);
}

void Level::spawnProp(BasicObject* prop)
{
	chunks[(prop->getHitbox().x / (16 * 32)) * 10 + (prop->getHitbox().y / (16 * 32))]->spawnProp(prop);
}

void Level::spawnCharacter(Character* character)
{
	chunks[(character->getHitbox().x / (16 * 32)) * 10 + (character->getHitbox().y / (16 * 32))]->spawnCharacter(character);
}

Level::Level()
{
	chunks = std::array<std::unique_ptr<Chunk>, 100>();
	initChunks();

	//Test spawns (to be removed)
	spawnProp(new BasicObject(2900, 2710, BasicObject::loadModel("tree2")));
	spawnProp(new BasicObject(2700, 2800, BasicObject::loadModel("tree1")));
	spawnProp(new BasicObject(2900, 2900, BasicObject::loadModel("portal1")));
	spawnProp(new BasicObject(3000, 3000, BasicObject::loadModel("column")));

	spawnText(new Text(2850, 2850, "The quick brown fox jumped over the lazy dog",
		AssetsManager::getManager()->getFont("futuraL"), {0, 0xff, 0xff, 0}, { 0xff, 0xff, 0, 0 }));

	for (int i = 0; i < chunks.size(); i++) {
		for (int x = 0; x < 16; x++) {
			for (int y = 0; y < 16; y++) {
				if (!x || !y)
					chunks[i]->putTile(x, y, 2, (rand() % 13));
				else
					chunks[i]->putTile(x, y, 1, (rand() % 255));
			}
		}
	}
}

void Level::update()
{
	for (int i = 0; i < chunks.size(); i++) {
		chunks[i]->update();
	}
}
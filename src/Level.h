#pragma once
#include <memory>
#include <array>
#include <fstream>
#include <string>

#include "AssetsManager.h"
#include "Chunk.h"
#include "Player.h"
#include "Text.h"

class Level
{
private:

	std::array<std::unique_ptr<Chunk>, 100> chunks;

	std::array<int, 50> rooms;

	int firstX, firstY;

	//[ Methods ]//

	void initChunks();

	void generateLayer();

	void generateFloor();

	void hallwaysFloor(int roomIdx);

	void roomsFloor(int roomIdx);

	void generateWalls();

	void populate();

public:

	void spawnText(Text* text);

	void spawnProp(BasicObject* prop);

	void spawnCharacter(Character* character);

	Level();

	Chunk* getChunk(int x, int y) { return chunks.at(x * 10 + y).get(); }

	/**
	* @brief update all the chunks of the level
	*/
	void update();
};


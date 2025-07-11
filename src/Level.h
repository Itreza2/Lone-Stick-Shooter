#pragma once
#include <memory>
#include <array>

#include "Chunk.h"
#include "Player.h"

class Level
{
private:

	std::array<std::unique_ptr<Chunk>, 100> chunks;

	void initChunks();

public:

	void spawnProp(BasicObject* prop);

	void spawnCharacter(Character* character);

	Level();

	Chunk* getChunk(int x, int y) { return chunks.at(y * 10 + x).get(); }

	/**
	* @brief update all the chunks of the level
	*/
	void update();
};


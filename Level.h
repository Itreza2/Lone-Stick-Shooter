#pragma once
#include <memory>
#include <array>

#include "Chunk.h"

class Level
{
private:

	std::array<std::unique_ptr<Chunk>, 100> chunks;

	void initChunks();

	void spawnProp(BasicObject* prop);

public:

	Level();

	Chunk* getChunk(int x, int y) { return chunks.at(y * 10 + x).get(); }
};


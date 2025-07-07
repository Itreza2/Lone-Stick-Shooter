#pragma once
#include <memory>
#include <array>

#include "Chunk.h"

class Level
{
private:

	std::array<std::unique_ptr<Chunk>, 100> chunks;

	void initChunks();

public:

	Level();
};


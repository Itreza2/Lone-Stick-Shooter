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

void Level::generateLayer()
{
	int x, y;
	int nextX, nextY;
	int posFound;
	int iterCpt;//If the current layout is unsolvable, the process must be terminated and restarted

	int gen_unfinished = 1;
	while (gen_unfinished) {
		gen_unfinished = 0;

		for (int i = 0; i < rooms.size(); i++) {
			rooms.at(i) = 0;
		}
		x = rand() % 5; y = rand() % 5;
		rooms.at((x * 5 + y) * 2) = 1;
		rooms.at((x * 5 + y) * 2 + 1) = 1;

		for (int i = 0; i < 4; i++) {
			posFound = 0; iterCpt = 0;
			while (!posFound) {
				iterCpt++;
				nextX = x; nextY = y;
				if (rand() % 2) {
					if (rand() % 2) nextX++;
					else nextX--;
				}
				else {
					if (rand() % 2) nextY++;
					else nextY--;
				}
				if (nextX >= 0 && nextX < 5 && nextY >= 0 && nextY < 5) {
					if (rooms.at((nextX * 5 + nextY) * 2) == 0 ||
						(rooms.at((nextX * 5 + nextY) * 2) == 1 && rooms.at((nextX * 5 + nextY) * 2 + 1) > 2)) {
						posFound = 1;
					}
				} if (iterCpt > 10) { posFound = 1; gen_unfinished = 1; }
			}
			x = nextX; y = nextY;
			if (i == 0) { //The first room after the spawn can only lead to another combat room to avoid shortcuts
				firstX = x;
				firstY = y;
			}
			if (i == 3) { //End of the level
				rooms.at((x * 5 + y) * 2) = 1;
				rooms.at((x * 5 + y) * 2 + 1) = 2;
			}
			else { // Combat room
				rooms.at((x * 5 + y) * 2) = rand() % 2 + 2;
				rooms.at((x * 5 + y) * 2 + 1) = 0;

				//Generation of special rooms (shop, chest...)
				if (rand() % 2) {
					if (rand() % 2) nextX++;
					else nextX--;
				}
				else {
					if (rand() % 2) nextY++;
					else nextY--;
				}
				if (nextX >= 0 && nextX < 5 && nextY >= 0 && nextY < 5) {
					if (rooms.at((nextX * 5 + nextY) * 2) == 0) {
						rooms.at((nextX * 5 + nextY) * 2) = 1;
						rooms.at((nextX * 5 + nextY) * 2 + 1) = 3;
					}
				}
			}
		}
	}
}

void Level::generateFloor()
{
	for (int i = 0; i < 25; i++) {
		if (rooms.at((i) * 2) != 0){

			//Corridors connecting rooms
			hallwaysFloor(i);

			//Rooms
			roomsFloor(i);
		}
	}
}

void Level::hallwaysFloor(int roomIdx)
{
	int type;

	if (roomIdx % 5 < 4) { // Horizontal
		if (rooms.at((roomIdx + 1) * 2) != 0 && 1) {
			for (int x = 0; x < 31; x++) {
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 17 + x) / 16, ((roomIdx / 5) * 31 + 15) / 16)
					->putTile(((roomIdx % 5) * 31 + 17 + x) % 16, ((roomIdx / 5) * 31 + 15) % 16, 1, (type / 8 * 16 + type % 8));
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 17 + x) / 16, ((roomIdx / 5) * 31 + 16) / 16)
					->putTile(((roomIdx % 5) * 31 + 17 + x) % 16, ((roomIdx / 5) * 31 + 16) % 16, 1, ((8 + type / 8) * 16 + type % 8));
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 17 + x) / 16, ((roomIdx / 5) * 31 + 17) / 16)
					->putTile(((roomIdx % 5) * 31 + 17 + x) % 16, ((roomIdx / 5) * 31 + 17) % 16, 1, ((8 + type / 8) * 16 + type % 8));
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 17 + x) / 16, ((roomIdx / 5) * 31 + 18) / 16)
					->putTile(((roomIdx % 5) * 31 + 17 + x) % 16, ((roomIdx / 5) * 31 + 18) % 16, 1, ((8 + type / 8) * 16 + type % 8));
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 17 + x) / 16, ((roomIdx / 5) * 31 + 19) / 16)
					->putTile(((roomIdx % 5) * 31 + 17 + x) % 16, ((roomIdx / 5) * 31 + 19) % 16, 1, (type / 8 * 16 + type % 8));
			}
		}
	} if (roomIdx / 5 < 4) { // Vertical
		if (rooms.at((roomIdx + 5) * 2) != 0 && 1) {
			for (int y = 0; y < 31; y++) {
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 15) / 16, ((roomIdx / 5) * 31 + 17 + y) / 16)
					->putTile(((roomIdx % 5) * 31 + 15) % 16, ((roomIdx / 5) * 31 + 17 + y) % 16, 1, (type / 8 * 16 + type % 8));
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 16) / 16, ((roomIdx / 5) * 31 + 17 + y) / 16)
					->putTile(((roomIdx % 5) * 31 + 16) % 16, ((roomIdx / 5) * 31 + 17 + y) % 16, 1, ((8 + type / 8) * 16 + type % 8));
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 17) / 16, ((roomIdx / 5) * 31 + 17 + y) / 16)
					->putTile(((roomIdx % 5) * 31 + 17) % 16, ((roomIdx / 5) * 31 + 17 + y) % 16, 1, ((8 + type / 8) * 16 + type % 8));
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 18) / 16, ((roomIdx / 5) * 31 + 17 + y) / 16)
					->putTile(((roomIdx % 5) * 31 + 18) % 16, ((roomIdx / 5) * 31 + 17 + y) % 16, 1, ((8 + type / 8) * 16 + type % 8));
				type = rand() % 63 + 1;
				getChunk(((roomIdx % 5) * 31 + 19) / 16, ((roomIdx / 5) * 31 + 17 + y) / 16)
					->putTile(((roomIdx % 5) * 31 + 19) % 16, ((roomIdx / 5) * 31 + 17 + y) % 16, 1, (type / 8 * 16 + type % 8));
			}
		}
	}
}

void Level::roomsFloor(int roomIdx)
{
	std::ifstream sketch;
	std::string line;
	int type;
	int offset = 15 - rooms.at(roomIdx * 2) * 3;
	int width = 5 + rooms.at(roomIdx * 2) * 6;

	if (rooms.at(roomIdx * 2) == 1) 
		sketch.open(std::string("rsc/rooms/1.txt"));
	else if (rooms.at(roomIdx * 2) == 2) 
		sketch.open(std::string("rsc/rooms/2/" + std::to_string(rand() % 7) + ".txt"));
	else if (rooms.at(roomIdx * 2) == 3)
		sketch.open(std::string("rsc/rooms/3/" + std::to_string(rand() % 4) + ".txt"));

	for (int y = 0; y < width; y++) {
		std::getline(sketch, line);
		for (int x = 0; x < width; x++) {

			type = rand() % 63 + 1;
			if (line[x] == '1')
				type = (type / 8 * 16 + type % 8);
			if (line[x] == '2') {
				type = (type / 8 * 16 + type % 8 + 8);

				//Plant props spawn
				if (!(rand() % 12)) {
					spawnProp(new BasicObject((x + offset + (roomIdx % 5) * 31) * 32 + 16, (y + offset + (roomIdx / 5) * 31) * 32 + 16,
						BasicObject::loadModel(std::string("tree") + std::to_string(rand() % 2 + 1))));
				}
			}
			if (line[x] == '3')
				type = ((type / 8 + 8) * 16 + type % 8);
			if (line[x] == '4')
				type = ((type / 8 + 8) * 16 + type % 8 + 8);

			if (line[x] != '0') {
				getChunk(((roomIdx % 5) * 31 + offset + x) / 16, ((roomIdx / 5) * 31 + offset + y) / 16)
					->putTile(((roomIdx % 5) * 31 + offset + x) % 16, ((roomIdx / 5) * 31 + offset + y) % 16, 1, type);
			} else {
				getChunk(((roomIdx % 5) * 31 + offset + x) / 16, ((roomIdx / 5) * 31 + offset + y) / 16)
					->putTile(((roomIdx % 5) * 31 + offset + x) % 16, ((roomIdx / 5) * 31 + offset + y) % 16, 0, 0);
			}
		}
	}
}

void Level::generateWalls()
{
	bool wall;

	for (int x = 1; x < 31 * 5; x++) {
		for (int y = 1; y < 31 * 5; y++) {
			wall = false;

			if (getChunk((x) / 16, (y) / 16)->getTileType(x % 16, y % 16) == 0) {
				for (int i = -1; i <= 1; i++) {
					for (int j = -1; j <= 1; j++) {
						if (getChunk((x + i) / 16, (y + j) / 16)->getTileType((x + i) % 16, (y + j) % 16) == 1)
							wall = true;
					}
				}
			}
			if (wall)
				getChunk(x / 16, y / 16)->putTile(x % 16, y % 16, 2, rand() %13 + 1);
		}
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
	rooms = std::array<int, 50>();

	firstX = 0; firstY = 0;

	initChunks();
	generateLayer();
	generateFloor();
	generateWalls();
}

void Level::update()
{
	for (int i = 0; i < chunks.size(); i++) {
		chunks[i]->update();
	}
}
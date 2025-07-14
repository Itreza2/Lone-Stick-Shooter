#include <iostream>

#include "Window.h"
#include "Level.h"
#include "Keyboard.h"

int main(int argc, char** argv)
{
	srand(time(NULL));


	Window window = Window();
	Level* level = new Level();
	Player* player1 = new Player(PLAYER_1_, 2870, 2820, BasicObject::loadModel("player1"));
	window.setLevel(level, player1, nullptr);
	level->spawnCharacter(player1);
	Uint32 lastRefresh = 0;
	Uint32 currentTick;

	bool exit = false;
	while (!exit) {
		exit = Keyboard::getKeyboard()->catchEvents();

		level->update();

		currentTick = SDL_GetTicks();
		if (currentTick - lastRefresh > 16) {
			window.refresh();
			lastRefresh = currentTick;
		}

	}
	return EXIT_SUCCESS;
}
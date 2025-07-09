#include <iostream>

#include "Window.h"
#include "Level.h"
#include "Keyboard.h"

int main(int argc, char** argv)
{
	srand(time(NULL));

	Window window = Window();
	Level* level = new Level();
	window.setLevel(level, 1);

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
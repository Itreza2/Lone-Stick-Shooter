#include "Events.h"

Events::Events()
{
	mapping = (unsigned int*)malloc(sizeof(unsigned int) * 5);
	if (mapping != NULL) {
		mapping[0] = SDL_SCANCODE_RIGHT;
		mapping[1] = SDL_SCANCODE_LEFT;
		mapping[2] = SDL_SCANCODE_UP;
		mapping[3] = SDL_SCANCODE_DOWN;
		mapping[4] = SDL_SCANCODE_R;
	}
	is_pressed = (unsigned char*)malloc(sizeof(unsigned char) * 5);
	if (is_pressed != NULL) {
		for (int i = 0; i < 5; i++) is_pressed[i] = 0;
	}
}

int Events::catch_events()
{
	while (SDL_PollEvent(&event)) {
		if (event.type == SDL_QUIT) {
			return 1;
		} if (event.type == SDL_KEYDOWN) {
			for (int i = 0; i < 5; i++) {
				if (mapping[i] == event.key.keysym.scancode) is_pressed[i] = 1;
			}
		} if (event.type == SDL_KEYUP) {
			if (event.key.keysym.scancode == SDL_SCANCODE_ESCAPE) {
				return 1;
			}
			for (int i = 0; i < 5; i++) {
				if (mapping[i] == event.key.keysym.scancode) is_pressed[i] = 0;
			}
		}
	}
	return 0;
}
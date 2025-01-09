#include <SDL.h>
#include <SDL_image.h>
#include <SDL_ttf.h>
#include <cstdlib>
#include <iostream>

#include "Character.h"
#include "Camera.h"
#include "Events.h"
#include "World.h"
#include "Sprite_lib.h"

using namespace std;

#define RES_W 1920
#define RES_H 1080

int main(int argc, char** argv) {
	SDL_Init(SDL_INIT_VIDEO);
	IMG_Init(IMG_INIT_PNG);
	TTF_Init();

	srand(time(NULL));

	SDL_Window* win = SDL_CreateWindow("title", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, RES_W, RES_H, SDL_WINDOW_FULLSCREEN);
	SDL_Renderer* render = SDL_CreateRenderer(win, -1, SDL_RENDERER_ACCELERATED);

	//Organisation provisoire, à des fins de test
	int* wall_map = (int*)malloc(sizeof(int) * (static_cast<unsigned long long>(175) * 175));
	if (wall_map == NULL) {
		cout << "Echec allocation wall_map" << endl;
		return 1;
	}
	for (int i = 0; i < 175 * 175; i++) wall_map[i] = rand() % 255;

	Sprite_lib sprites = Sprite_lib();

	SDL_Rect rect = { 0, 0, 960, 540 };

	Events evt_handler = Events();

	Player car = Player(960, 540, &evt_handler);

	World map = World(&car.car);

	int err = 0;
	Camera cam = Camera(&car.car, &map, &sprites, rect, 768, 432, err);

	int quit = 0;
	Uint32 fps_lim = SDL_GetTicks();
	Uint32 current_time;
	while (! quit) {
		quit = evt_handler.catch_events();
		car.read_inputs();
		car.car.update_pos();

		current_time = SDL_GetTicks();
		if ((fps_lim - current_time) > (1000 / 60)) {
			cam.draw_frame(render);
			fps_lim = SDL_GetTicks();
		}
	}

	SDL_DestroyRenderer(render);
	SDL_DestroyWindow(win);
	SDL_Quit();

	return 0;
}
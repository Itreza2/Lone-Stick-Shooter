#include <SDL.h>
#include <SDL_image.h>
#include <SDL_ttf.h>
#include <cstdlib>
#include <iostream>

#include "Character.h"
#include "Camera.h"
#include "Events.h"
#include "World.h"
#include "Weapon.h"
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

	SDL_Rect rect = { 0, 0, 1920, 1080 };

	Events evt_handler = Events();

	Player car = Player(&sprites, 0, 960, 540, &evt_handler);

	World map = World(&car);

	int err = 0;
	Camera cam = Camera(&car, &map, &sprites, rect, 768, 432, err);

	int quit = 0;

	Uint32 last_anim_tick = SDL_GetTicks(); //I don't really know where to put that...
	Uint32 fps_lim = SDL_GetTicks();
	Uint32 current_time;
	while (! quit) {
		quit = evt_handler.catch_events();
		car.read_inputs();
		car.update_pos();

		if (car.is_shooting) {
			int x, y, a, b, c, dir, n;
			float deg;

			car.Get_pos(x, y);
			car.Get_anim(a, b, c, dir, deg);
			n = 0;
			vector<Bullet*> res = car.weapon->shoot(y, x, deg, dir, n);
			for (int i = 0; i < n; i++) {
				map.proj_idx.push_back(res[i]);
				map.proj_nb++;
			}
		}

		int nb_erased = 0;
		for (int i = 0; i < map.proj_nb; i++) {
			if (map.proj_idx[i-nb_erased]->update_pos()) {
				map.proj_idx.erase(map.proj_idx.begin() + (i - nb_erased));
				map.proj_nb--;
			}
		}
		map.check_collision();

		current_time = SDL_GetTicks();
		if ((current_time - fps_lim) > (1000 / 60)) {
			SDL_RenderClear(render);
			cam.draw_frame(render);
			SDL_RenderPresent(render);
			fps_lim = SDL_GetTicks();
		}
		if ((current_time - last_anim_tick) > (100)) {
			for (int i = 0; i < map.char_nb; i++) {
				map.char_idx[i]->update_anim();
			}
			for (int i = 0; i < map.proj_nb; i++) {
				map.proj_idx[i]->update_anim();
			}
			last_anim_tick = SDL_GetTicks();
		}
	}

	SDL_DestroyRenderer(render);
	SDL_DestroyWindow(win);
	SDL_Quit();

	return 0;
}
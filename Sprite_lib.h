#pragma once
#include <SDL.h>
#include <SDL_image.h>
#include <iostream>

using namespace std;

class Sprite_lib
{
public: //temporary

	SDL_Surface* floor_sheet;

	SDL_Surface* wall_sheet;

	SDL_Surface* prop_sheet;

	SDL_Surface* void_sheet;

	SDL_Surface* player_sheet;

	Sprite_lib();
};


#pragma once
#include <iostream>

#include <SDL.h>
#include <SDL_ttf.h>

using namespace std;

class Text
{
private:

	Uint32 spawn_time;

	Uint32 time_to_live;

	int pos_x, pos_y;

	SDL_Rect rect;

public:

	//The surface is public for convenience sake
	SDL_Surface* surface;

public:

	Text(TTF_Font* font, const SDL_Color color, const char* content, int x, int y, int ttl = 0);

	~Text() { SDL_FreeSurface(surface); }

	bool should_be_erased();

	SDL_Rect* get_rect(int camera_x, int camera_y);
};


#pragma once
#include <SDL_ttf.h>
#include <string>

#include "SuperSurface.h"

/**
* @brief a rendered text with a solid or glowing color and coordinates
*/
class Text
{
private:

	int x, y;

	Uint32 spawnTick;

	time_t ttl;

	std::string content;

	TTF_Font* font;

	SDL_Color color1, color2;

	time_t glowFrequency;

	SuperSurface* surface;

	//[ Methods ]//

public:

	Text(int x, int y, std::string content, TTF_Font* font, SDL_Color color1, SDL_Color color2, time_t freq = 2000, time_t ttl = 0);

	Text(int x, int y, std::string content, TTF_Font* font, SDL_Color color, time_t ttl = 0) :
		Text(x, y, content, font, color, color, 0, ttl) {}

	Text(int x, int y, std::string content, TTF_Font* font, time_t ttl = 0) :
		Text(x, y, content, font, (SDL_Color)0, (SDL_Color)0, 0, ttl) {}

	SDL_Rect getBox() { return {x - surface->w / 2, y - surface->h / 2, surface->w, surface->h}; }

	bool shouldBeErased();

	SuperSurface* getSurface();
};
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

	Uint32 color1, color2;

	time_t glowFrequency;

	SuperSurface* surface;

	//[ Methods ]//

	SDL_Color convertColor(Uint32 color);

	SDL_Color currentColor(); // Very badly done, should be remade but better

public:

	Text(int x, int y, time_t ttl, std::string content, TTF_Font* font, Uint32 color1, Uint32 color2, time_t freq = 2000);

	Text(int x, int y, time_t ttl, std::string content, TTF_Font* font, Uint32 color) :
		Text(x, y, ttl, content, font, color, color, 0) {}

	Text(int x, int y, time_t ttl, std::string content, TTF_Font* font) :
		Text(x, y, ttl, content, font, 0, 0, 0) {}

	SDL_Rect getBox() { return {x - surface->getWidth() / 2, y - surface->getHeight() / 2, surface->getWidth(), surface->getHeight()}; }

	bool shouldBeErased();

	SuperSurface* getSurface();
};
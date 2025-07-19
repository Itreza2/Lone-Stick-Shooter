#include "Text.h"

Text::Text(int x, int y, std::string content, TTF_Font* font, SDL_Color color1, SDL_Color color2, time_t freq, time_t ttl)
{
	this->x = x;
	this->y = y;
	this->content = content;
	this->font = font;
	this->color1 = color1;
	this->color2 = color2;
	glowFrequency = freq;
	this->ttl = ttl;

	SDL_Surface* surfaceUnknown = TTF_RenderUTF8_Solid(font, content.c_str(), color1);
	SDL_Surface* surfaceRGBA = SDL_CreateRGBSurfaceWithFormat(0, surfaceUnknown->w, surfaceUnknown->h, 32, SDL_PIXELFORMAT_RGBA8888);
	SDL_BlitSurface(surfaceUnknown, NULL, surfaceRGBA, NULL);
	SDL_FreeSurface(surfaceUnknown);
	surface = new SuperSurface(std::move(*surfaceRGBA));
	
	spawnTick = SDL_GetTicks();
}

bool Text::shouldBeErased()
{
	if (SDL_GetTicks() - spawnTick > ttl && ttl)
		return true;
	return false;
}

SuperSurface* Text::getSurface()
{
	if (glowFrequency) {
		// To be implemented...
	}
	return surface;
}
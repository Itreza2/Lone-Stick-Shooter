#include "Text.h"

SDL_Color Text::convertColor(Uint32 color)
{
	SDL_Color temp = { 0, 0, 0, 0xff };
	temp.r = (unsigned char)(color >> 16 & 0xff);
	temp.g = (unsigned char)(color >> 8 & 0xff);
	temp.b = (unsigned char)(color & 0xff);

	return temp;
}

SDL_Color Text::currentColor()
{
	Uint32 currentTick = SDL_GetTicks();

	unsigned char r1 = (unsigned char)(color1 >> 16 & 0xff);
	unsigned char g1 = (unsigned char)(color1 >> 8 & 0xff);
	unsigned char b1 = (unsigned char)(color1 & 0xff);
	unsigned char r2 = (unsigned char)(color2 >> 16 & 0xff);
	unsigned char g2 = (unsigned char)(color2 >> 8 & 0xff);
	unsigned char b2 = (unsigned char)(color2 & 0xff);
	unsigned char r = r1;
	unsigned char g = g1;
	unsigned char b = b1;
	int temp;

	if (r1 != r2) {
		if (r1 < r2) {
			temp = (currentTick / glowFrequency) % (2 * (r2 - r1));
			if (temp > (r2 - r1))
				temp = 2 * (r2 - r1) - temp;
			r = r1 + temp;
		}
		else {
			temp = r2 - (currentTick / glowFrequency % (2 * (r1 - r2)));
			if (temp > (r2 - r1)) temp = 2 * (r2 - r1) - temp;
			r = r2 - temp;
		}
	}
	if (b1 != b2) {
		if (b1 < b2) {
			temp = (currentTick / glowFrequency) % (2 * (b2 - b1));
			if (temp > (b2 - b1))
				temp = 2 * (b2 - b1) - temp;
			b = b1 + temp;
		}
		else {
			temp = b2 - (currentTick / glowFrequency % (2 * (b1 - b2)));
			if (temp > (b2 - b1)) temp = 2 * (b2 - b1) - temp;
			b = b2 - temp;
		}
	}
	if (g1 != g2) {
		if (g1 < g2) {
			temp = (currentTick / glowFrequency) % (2 * (g2 - g1));
			if (temp > (g2 - g1))
				temp = 2 * (g2 - g1) - temp;
			g = g1 + temp;
		}
		else {
			temp = g2 - (currentTick / glowFrequency % (2 * (g1 - g2)));
			if (temp > (g2 - g1)) temp = 2 * (g2 - g1) - temp;
			g = g2 - temp;
		}
	}
	return { r, b, g, 0xff };
}

Text::Text(int x, int y, time_t ttl, std::string content, TTF_Font* font, Uint32 color1, Uint32 color2, time_t freq)
{
	this->x = x;
	this->y = y;
	this->content = content;
	this->font = font;
	this->color1 = color1;
	this->color2 = color2;
	glowFrequency = freq;
	this->ttl = ttl;

	SDL_Surface* surfaceUnknown = TTF_RenderUTF8_Solid(font, content.c_str(), convertColor(color1));
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

		//Text generation
		SDL_Surface* surfaceUnknown = TTF_RenderUTF8_Solid(font, content.c_str(), currentColor());
		SDL_Surface* surfaceRGBA = SDL_CreateRGBSurfaceWithFormat(0, surfaceUnknown->w, surfaceUnknown->h, 32, SDL_PIXELFORMAT_RGBA8888);
		SDL_BlitSurface(surfaceUnknown, NULL, surfaceRGBA, NULL);
		SDL_FreeSurface(surfaceUnknown);

		delete surface;
		surface = new SuperSurface(std::move(*surfaceRGBA));
	}
	return surface;
}
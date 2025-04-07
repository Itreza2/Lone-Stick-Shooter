#include "text.h"

Text::Text(TTF_Font* font, const SDL_Color color, const char* content, int x, int y, int ttl)
{
	spawn_time = SDL_GetTicks();
	time_to_live = ttl;

	surface = TTF_RenderUTF8_Solid(font, content, color);
	
	pos_x = x - surface->w * 0.5;
	pos_y = y - surface->h * 0.5;
}

bool Text::should_be_erased()
{
	if (SDL_GetTicks() - spawn_time > time_to_live && time_to_live) {
		return true;
	}
	else return false;
}

SDL_Rect* Text::get_rect(int camera_x, int camera_y)
{
	rect = { pos_x - camera_y, pos_y - camera_x,
					 surface->w, surface->h };
	return &rect;
}
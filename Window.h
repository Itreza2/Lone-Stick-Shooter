#pragma once
#include <SDL.h>
#include <SDL_image.h>
#include <SDL_ttf.h>

#include "AssetsManager.h"

class Window
{
private:

	SDL_Window* window;

	SDL_Renderer* renderer;

public:

	Window();

};


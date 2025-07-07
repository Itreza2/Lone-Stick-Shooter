#pragma once
#include <SDL.h>
#include <SDL_image.h>
#include <SDL_ttf.h>

#include "AssetsManager.h"
#include "Level.h"
#include "Camera.h"

class Window
{
private:

	SDL_Window* window;

	SDL_Renderer* renderer;

	Level* currentLevel;

	Camera* camera1;

	Camera* camera2;

public:

	Window();
	
	void refresh();

	void setLevel(Level* level, int nbPlayers = 1);
};


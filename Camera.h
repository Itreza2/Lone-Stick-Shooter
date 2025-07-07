#pragma once
#include <SDL.h>

#include "AssetsManager.h"
#include "Level.h"

class Camera
{
private:

	//[Position]//

	int x, y;

	Level* world;

	//[Rendering stuff]//

	SDL_Renderer* renderer;

	SDL_Rect rect;

	SDL_Texture* bg;		//Layer 0

	SDL_Texture* floor;		//Layer 1

	SDL_Surface* iso;		//Layer 2

	SDL_Texture* hud;		//Layer 3

	//[Methods]//

	void captureFloor();

public:

	Camera(SDL_Renderer* renderer, SDL_Rect rect,  Level* level);

	void render();
};


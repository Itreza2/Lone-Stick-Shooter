#include "Window.h"

Window::Window()
{
	SDL_Init(SDL_INIT_VIDEO);
	IMG_Init(IMG_INIT_PNG);
	TTF_Init();

	window = SDL_CreateWindow("Lone Stick Shooter", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 960, 540, NULL);
	renderer = SDL_CreateRenderer(window, -1, (SDL_RENDERER_ACCELERATED | SDL_RENDERER_TARGETTEXTURE));

	AssetsManager::getManager()->loadGroup("rsc\\assets\\loaders\\biome1.load", renderer);

	currentLevel = nullptr;

	camera1 = nullptr;
	camera2 = nullptr;
}

void Window::refresh()
{
	SDL_RenderClear(renderer);
	
	if (camera1 != nullptr)
		camera1->render();
	if (camera2 != nullptr)
		camera2->render();

	SDL_RenderPresent(renderer);
}

void Window::setLevel(Level* level, int nbPlayers)
{
	currentLevel = level;

	if (camera1 != nullptr) delete camera1;
	if (camera2 != nullptr) delete camera2;

	if (nbPlayers == 1) {
		camera1 = new Camera(renderer, { 0, 0, 960, 540 }, currentLevel);
		camera2 = nullptr;
	}
	else {
		camera1 = new Camera(renderer, { 0, 0, 430, 540 }, currentLevel);
		camera2 = new Camera(renderer, { 430, 0, 430, 540 }, currentLevel);
	}
}
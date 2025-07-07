#include "Camera.h"

void Camera::captureFloor()
{
	SDL_Texture* texture = AssetsManager::getManager()->getTexture("floor1");
	Chunk* chunk;
	SDL_Rect src, dst;

	SDL_SetRenderTarget(renderer, floor);

	for (int i = x / (32 * 16); i <= (x + rect.w) / (32 * 16) + 1; i++) {
		for (int j = y / (32 * 16); j <= (y + rect.h) / (32 * 16) + 1; j++) {
			chunk = world->getChunk(i, j);

			for (int column = 0; column < 16; column++) {
				for (int row = 0; row < 16; row++) {
					
					if (chunk->getTileType(column, row) == 1) {
						src = { (chunk->getTile(column, row) % 16) * 32, (chunk->getTile(column, row) / 16) * 32, 32, 32 };
						dst = { chunk->getPosX() - x + 32 * column, chunk->getPosY() - y + 32 * row, 32, 32 };

						SDL_RenderCopy(renderer, texture, &src, &dst);
					}
				}
			}
		}
	}
	SDL_SetRenderTarget(renderer, NULL);
}

Camera::Camera(SDL_Renderer* renderer, SDL_Rect rect, Level* level)
{
	this->renderer = renderer;
	this->rect = rect;

	world = level;

	x = 2600;
	y = 2600;

	bg = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
	floor = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
	iso = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	hud = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
}

void Camera::render()
{
	captureFloor();

	SDL_RenderCopy(renderer, floor, NULL, &rect);
}
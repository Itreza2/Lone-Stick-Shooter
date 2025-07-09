#include "Camera.h"

void Camera::captureFloor()
{
	SDL_Texture* texture = AssetsManager::getManager()->getTexture("floor1");
	Chunk* chunk;
	SDL_Rect src, dst;

	SDL_SetRenderTarget(renderer, floor);
	SDL_RenderCopy(renderer, texBlank, NULL, NULL); //Erase the previous frame with a quick Bit-BLT

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

void Camera::captureObjects()
{
	SuperSurface* surface;
	Chunk* chunk;
	SDL_Rect src;
	std::vector<BasicObject*> objects;

	for (int i = x / (32 * 16); i <= (x + rect.w) / (32 * 16) + 1; i++) {
		for (int j = y / (32 * 16); j <= (y + rect.h) / (32 * 16) + 1; j++) {
			chunk = world->getChunk(i, j);

			objects = chunk->getAllObjects();
			for (BasicObject* object : objects) {
				surface = AssetsManager::getManager()->getSheet(object->getSheet());
				src = object->getFrame();

				surface->printIso(&src, object->getHitbox().x - x, object->getHitbox().y - y, iso, hmap);
			}
		}
	}
}

Camera::Camera(SDL_Renderer* renderer, SDL_Rect rect, Level* level)
{
	this->renderer = renderer;
	this->rect = rect;

	world = level;

	x = 2600;
	y = 2600;

	hmap = (unsigned int*)malloc((rect.w * rect.h) * sizeof(unsigned int));
	if (hmap) {
		for (int i = 0; i < rect.w * rect.h; i++) hmap[i] = 0;
	} //Else... oh god it's not an arduino chip wth care ?

	bg = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
	floor = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
	iso = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	hud = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);

	surfBlank = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	texBlank = SDL_CreateTextureFromSurface(renderer, surfBlank);  //Default surface's alpha is 0 when texture's is 255 for some reason...
}

void Camera::render()
{
	for (int i = 0; i < rect.w * rect.h; i++) hmap[i] = 0;
	SDL_BlitSurface(surfBlank, NULL, iso, NULL);

	captureFloor();
	captureObjects();

	SDL_Texture* temp = SDL_CreateTextureFromSurface(renderer, iso);

	SDL_RenderCopy(renderer, floor, NULL, &rect);
	SDL_RenderCopy(renderer, temp, NULL, &rect);
}
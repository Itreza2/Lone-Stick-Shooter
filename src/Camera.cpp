#include "Camera.h"

void Camera::captureFloor()
{
	SDL_Texture* texture = AssetsManager::getManager()->getTexture("floor1");
	SuperSurface* surface = AssetsManager::getManager()->getSheet("walls1");
	Chunk* chunk;
	SDL_Rect src, dst;

	SDL_SetRenderTarget(renderer, floor);
	SDL_RenderCopy(renderer, texBlank, NULL, NULL); //Erase the previous frame with a quick Bit-BLT

	for (int i = x / (32 * 16); i <= (x + rect.w) / (32 * 16); i++) {
		for (int j = y / (32 * 16); j <= (y + rect.h + 50) / (32 * 16); j++) {
			chunk = world->getChunk(j, i);

			for (int column = 0; column < 16; column++) {
				for (int row = 0; row < 16; row++) {
					
					if (chunk->getTileType(column, row) == 1) { //Floor tiles
						src = { (chunk->getTile(column, row) % 16) * 32, (chunk->getTile(column, row) / 16) * 32, 32, 32 };
						dst = { chunk->getPosX() - x + 32 * column, chunk->getPosY() - y + 32 * row, 32, 32 };

						SDL_RenderCopy(renderer, texture, &src, &dst);
					}
					else if (chunk->getTileType(column, row) == 2) { //Wall tiles (Body and top)
						if (chunk->getTile(column, row)) {
							src = { 32 * chunk->getTile(column, row), 32, 32, 20 };
							surface->printIso(&src, chunk->getPosX() + 32 * column - x, chunk->getPosY() + 32 * row + 12  - y, iso, hmap);
							
							src = { 32 * chunk->getTile(column, row), 0, 32, 32 };
							surface->printIso(&src, chunk->getPosX() + 32 * column - x, chunk->getPosY() + 32 * row - 20 - y, iso, hmap,
								false, 20, false);
						}
						else { //Doors
							src = { 0, 0, 32, 70 };

							surface->printIso(&src, chunk->getPosX() + 32 * column - x, chunk->getPosY() + 32 * row - 38 - y, iso, hmap);
						}
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

	for (int i = x / (32 * 16) - 1; i <= (x + rect.w) / (32 * 16) + 1; i++) {
		for (int j = y / (32 * 16) - 1; j <= (y + rect.h) / (32 * 16) + 1; j++) {
			chunk = world->getChunk(j, i);

			objects = chunk->getAllObjects();
			for (BasicObject* object : objects) {
				surface = AssetsManager::getManager()->getSheet(object->getSheet());
				src = object->getFrame();

				surface->printIso(&src, object->getHitbox().x + (object->getHitbox().w / 2) + object->getOffsetX() - x,
					object->getHitbox().y + (object->getHitbox().h / 2) + object->getOffsetY() - y, iso, hmap, object->fliped(), object->getElevation());
			}
		}
	}
}

void Camera::captureTexts()
{
	SuperSurface* surface;
	Chunk* chunk;
	std::vector<Text*> texts;

	for (int i = x / (32 * 16) - 1; i <= (x + rect.w) / (32 * 16) + 1; i++) {
		for (int j = y / (32 * 16) - 1; j <= (y + rect.h) / (32 * 16) + 1; j++) {
			chunk = world->getChunk(j, i);

			texts = chunk->getTexts();
			for (Text* text : texts) {
				surface = text->getSurface();

				surface->printIso(nullptr, text->getBox().x - x,
					text->getBox().y - y, iso, hmap, false, 100);
			}
		}
	}
}

void Camera::renderShadows()
{
	Uint32* pixels = (Uint32*)shadow->pixels;
	int dstX, dstY;

	for (int i = 0; i < rect.w * (rect.h * 1.25); i++) {
		if (hmap[i]) {
			dstY = i / rect.w - hmap[i] * 0.35;
			dstX = i % rect.w;

			if (dstX >= 0 && dstX < rect.w && dstY >= 0 && dstY < rect.h) {
				if (hmap[dstY * rect.w + dstX] < hmap[i])
					pixels[dstY * rect.w + dstX] = SDL_MapRGBA(shadow->format, 0, 0, 0, 50);
			}
			if (dstX >= 0 && dstX < rect.w && dstY > 0 && dstY <= rect.h) {
				if (hmap[(dstY - 1) * rect.w + dstX] < hmap[i])
					pixels[(dstY - 1) * rect.w + dstX] = SDL_MapRGBA(shadow->format, 0, 0, 0, 50);
			}
		}
	}
}

Camera::Camera(SDL_Renderer* renderer, SDL_Rect rect, Level* level, Player* target)
{
	this->renderer = renderer;
	this->rect = rect;
	this->target = target;
	world = level;

	x = target->getHitbox().x - rect.w / 2;
	y = target->getHitbox().y - rect.h / 2;

	hmap = (unsigned int*)malloc((rect.w * (rect.h * 1.25)) * sizeof(unsigned int));
	if (hmap) {
		for (int i = 0; i < rect.w * (rect.h * 1.25); i++) hmap[i] = 0;
	} //Else... oh god it's not an arduino chip wth care ?

	bg = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
	floor = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
	shadow = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	iso = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	hud = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);

	surfBlank = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	texBlank = SDL_CreateTextureFromSurface(renderer, surfBlank);  //Default surface's alpha is 0 when texture's is 255 for some reason...
}

void Camera::render()
{
	x = target->getHitbox().x + target->getHitbox().w / 2 - rect.w / 2;
	y = target->getHitbox().y + target->getHitbox().h / 2 - rect.h / 2;

	for (int i = 0; i < rect.w * (rect.h * 1.25); i++) hmap[i] = 0;

	SDL_FreeSurface(iso);
	iso = SDL_DuplicateSurface(surfBlank);
	SDL_FreeSurface(shadow);
	shadow = SDL_DuplicateSurface(surfBlank);

	captureFloor();
	captureObjects();
	captureTexts();
	renderShadows();


	SDL_RenderCopy(renderer, floor, NULL, &rect);

	SDL_Texture* temp = SDL_CreateTextureFromSurface(renderer, iso);
	SDL_RenderCopy(renderer, temp, NULL, &rect);
	SDL_DestroyTexture(temp);

	temp = SDL_CreateTextureFromSurface(renderer, shadow);
	SDL_RenderCopy(renderer, temp, NULL, &rect);
	SDL_DestroyTexture(temp);
}
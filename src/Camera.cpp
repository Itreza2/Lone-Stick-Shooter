#include "Camera.h"

void Camera::updateBackground()
{
	SuperSurface* surface = AssetsManager::getManager()->getSheet("sky1");

	for (int i = x / 4 - 512 + (int)(SDL_GetTicks() * 0.02) % 512; i < x / 4 + rect.w; i += 512) {
		for (int j = y / 4 - 512; j < y / 4 + rect.h; j += 512) {
			surface->blit(NULL, i - x / 4, j - y / 4, bg);
		}
	}
}

void Camera::captureFloor()
{
	SDL_Texture* texture = AssetsManager::getManager()->getTexture("floor1");
	SDL_Texture* textureWater = AssetsManager::getManager()->getTexture("water");
	SuperSurface* surface = AssetsManager::getManager()->getSheet("walls1");
	Chunk* chunk;
	SDL_Rect src, dst;
	int currentWaterTile = SDL_GetTicks() / 100 % 40;

	SDL_DestroyTexture(floor);
	floor = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
	SDL_SetTextureBlendMode(floor, SDL_BLENDMODE_BLEND);

	for (int i = x / (32 * 16); i <= (x + rect.w) / (32 * 16); i++) {
		for (int j = y / (32 * 16); j <= (y + rect.h + 50) / (32 * 16); j++) {
			if (i >= 0 && i < 10 && j >= 0 && j < 10) {
				chunk = world->getChunk(i, j);

				for (int column = 0; column < 16; column++) {
					for (int row = 0; row < 16; row++) {

						if (chunk->getTileType(column, row) == 1) { //Floor tiles
							SDL_SetRenderTarget(renderer, floor);

							src = { (chunk->getTile(column, row) % 16) * 32, (chunk->getTile(column, row) / 16) * 32, 32, 32 };
							dst = { chunk->getPosX() - x + 32 * column, chunk->getPosY() - y + 32 * row, 32, 32 };

							SDL_RenderCopy(renderer, texture, &src, &dst);
						}
						else if (chunk->getTileType(column, row) == 2) { //Wall tiles (Body and top)
							SDL_SetRenderTarget(renderer, floor);

							if (chunk->getTile(column, row)) {
								src = { 32 * chunk->getTile(column, row), 32, 32, 20 };
								surface->printIso(&src, chunk->getPosX() + 32 * column - x, chunk->getPosY() + 32 * row + 12 - y, iso, hmap);

								src = { 32 * chunk->getTile(column, row), 0, 32, 32 };
								surface->printIso(&src, chunk->getPosX() + 32 * column - x, chunk->getPosY() + 32 * row - 20 - y, iso, hmap,
									false, 20, false);
							}
							else { //Doors
								src = { 0, 0, 32, 70 };

								surface->printIso(&src, chunk->getPosX() + 32 * column - x, chunk->getPosY() + 32 * row - 38 - y, iso, hmap);
							}
						}
						else { //Void : backgroud water tile
							SDL_SetRenderTarget(renderer, water);

							src = { currentWaterTile * 128 + (column % 4 * 32), (row % 4 * 32), 32, 32 };
							dst = { chunk->getPosX() - x + 32 * column, chunk->getPosY() - y + 32 * row, 32, 32 };

							SDL_RenderCopy(renderer, textureWater, &src, &dst);
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
			if (i >= 0 && i < 10 && j >= 0 && j < 10) {
				chunk = world->getChunk(i, j);

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
}

void Camera::captureTexts()
{
	SuperSurface* surface;
	Chunk* chunk;
	std::vector<Text*> texts;

	for (int i = x / (32 * 16) - 1; i <= (x + rect.w) / (32 * 16) + 1; i++) {
		for (int j = y / (32 * 16) - 1; j <= (y + rect.h) / (32 * 16) + 1; j++) {
			if (i >= 0 && i < 10 && j >= 0 && j < 10) {
				chunk = world->getChunk(i, j);

				texts = chunk->getTexts();
				for (Text* text : texts) {
					surface = text->getSurface();

					surface->printIso(nullptr, text->getBox().x - x,
						text->getBox().y - y, iso, hmap, false, 10000);
				}
			}
		}
	}
}

void Camera::renderShadows()
{
	Uint32* pixels = (Uint32*)shadow->pixels;
	Uint32* pixelsIso = (Uint32*)iso->pixels;
	Uint32* pixelsBg = (Uint32*)bg->pixels;
	int dstX, dstY;

	for (int i = 0; i < rect.w * (rect.h * 1.25); i++) {
		if (hmap[i]) {

			//Shadows
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
			//Reflection on water
			dstY = i / rect.w + 2 * hmap[i];
			dstX = i % rect.w;
			if (dstX >= 0 && dstX < rect.w && dstY >= 0 && dstY < rect.h) {
				pixelsBg[dstY * rect.w + dstX + (SDL_GetTicks() / 100 + dstY / 4) % 3 - 1] = pixelsIso[(dstY - 2 * hmap[i]) * rect.w + dstX];
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

	bg = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	water = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
	floor = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);
	shadow = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	iso = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	hud = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, rect.w, rect.h);

	SDL_SetTextureBlendMode(water, SDL_BLENDMODE_BLEND);
	SDL_SetTextureAlphaMod(water, 150);

	surfBlank = SDL_CreateRGBSurfaceWithFormat(0, rect.w, rect.h, 32, SDL_PIXELFORMAT_RGBA8888);
	texBlank = SDL_CreateTextureFromSurface(renderer, surfBlank);  //Default surface's alpha is 0 when texture's is 255 for some reason...
}

void Camera::render()
{
	x = target->getHitbox().x + target->getHitbox().w / 2 - rect.w / 2;
	y = target->getHitbox().y + target->getHitbox().h / 2 - rect.h / 2;

	for (int i = 0; i < rect.w * (rect.h * 1.25); i++) hmap[i] = 0;

	SDL_FreeSurface(bg);
	bg = SDL_DuplicateSurface(surfBlank);
	SDL_FreeSurface(iso);
	iso = SDL_DuplicateSurface(surfBlank);
	SDL_FreeSurface(shadow);
	shadow = SDL_DuplicateSurface(surfBlank);

	updateBackground();
	captureFloor();
	captureObjects();
	captureTexts();
	renderShadows();


	SDL_Texture* temp = SDL_CreateTextureFromSurface(renderer, bg);
	SDL_RenderCopy(renderer, temp, NULL, &rect);
	SDL_DestroyTexture(temp);

	SDL_RenderCopy(renderer, water, NULL, &rect);

	SDL_RenderCopy(renderer, floor, NULL, &rect);

	temp = SDL_CreateTextureFromSurface(renderer, iso);
	SDL_RenderCopy(renderer, temp, NULL, &rect);
	SDL_DestroyTexture(temp);

	temp = SDL_CreateTextureFromSurface(renderer, shadow);
	SDL_RenderCopy(renderer, temp, NULL, &rect);
	SDL_DestroyTexture(temp);
}
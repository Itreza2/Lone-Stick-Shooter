#include "SuperSurface.h"

void SuperSurface::printIso(SDL_Rect* source, int x, int y, SDL_Surface* dest, unsigned int* hmap, 
	bool flip, unsigned int height, bool vertical)
{	
	SDL_Rect* src = source;
	if (source == nullptr) {
		src = new SDL_Rect();
		*src = {0, 0, w, h};
	}
	Uint32* srcPixels = (Uint32*)pixels;
	Uint32* destPixels = (Uint32*)dest->pixels;
	unsigned int pixHeight = height;

	for (int i = src->x; i < src->x + src->w; i++) {
		for (int j = src->y; j < src->y + src->h; j++) {
			if (vertical)
				pixHeight = src->h - j + height - 1;

			if ((x + i) >= 0 && (x + i) < dest->w && (y + j) >= 0 && (y + j) < dest->h) {
				if (pixHeight > hmap[(y + j) * dest->w + (x + i)] && 1) {
					hmap[(y + j) * dest->w + (x + i)] = pixHeight;

					if (flip)
						destPixels[(y + j) * dest->w + (x + i)] = srcPixels[j * w + (2 * src->x + src->w - 1 - i)];
					else
						destPixels[(y + j) * dest->w + (x + i)] = srcPixels[j * w + i];
				}
			}
		}
	}
	if (source == nullptr)
		free(src);
}

void SuperSurface::printRot(SDL_Rect* source, int x, int y, int angle, SDL_Surface* dest, unsigned int* hmap, 
	bool flip, unsigned int height)
{
	SDL_Rect* src = source;
	if (source == nullptr) {
		src = new SDL_Rect();
		*src = { 0, 0, w, h };
	}
	Uint32* srcPixels = (Uint32*)pixels;
	Uint32* destPixels = (Uint32*)dest->pixels;
	unsigned int pixHeight = height;
	unsigned int l;
	int srcX, srcY;

	if (src->w > src->h) l = src->w;
	else l = src->h;
	if (l % 2) l++;

	for (int i = 0; i < l; i++) {
		for (int j = 0; j < l; j++) {

			if ((x - l / 2 + i) >= 0 && (x - l / 2 + i) < dest->w && (y - l / 2 + j) >= 0 && (y - l / 2 + j) < dest->h) {
				if (hmap[(y - l / 2 + j) * dest->w + (x - l / 2 + i)] < height) {

					//Search of the relevent source pixel
					srcX = (i - (l / 2)) * cos(angle) + (j - (l / 2)) * sin(angle) + (l / 2);
					srcY = (i - (l / 2)) * (-sin(angle)) + (j - (l / 2)) * cos(angle) + (l / 2);
					if (flip) srcX = src->w - srcX - 1;

					if (srcX >= 0 && srcX < src->w and srcY >= 0 && srcY < src->h && 1) {
						hmap[(y - l / 2 + j) * dest->w + (x - l / 2 + i)] = height;
						destPixels[(y - l / 2 + j) * dest->w + (x - l / 2 + i)] = srcPixels[(src->y + srcY) * w + src->x + srcX];
					}
				}
			}
		}
	}
	if (source == nullptr)
		free(src);
}
#include "SuperSurface.h"

void SuperSurface::printIso(int x, int y, SDL_Surface* dest, unsigned int* hmap, bool flip, unsigned int height, bool vertical)
{
	Uint32* srcPixels = (Uint32*)pixels;
	Uint32* destPixels = (Uint32*)dest->pixels;
	unsigned int pixHeight = height;

	for (int i = 0; i < w; i++) {
		for (int j = 0; j < h; j++) {
			if (vertical)
				pixHeight = h - j + height - 1;

			if ((x + i) >= 0 && (x + i) < dest->w && (y + j) >= 0 && (y + j) < dest->h) {
				if (pixHeight > hmap[(y + j) * dest->w + (x + i)] && 1) {
					hmap[(y + j) * dest->w + (x + i)] = pixHeight;

					if (flip)
						destPixels[(y + j) * dest->w + (x + i)] = srcPixels[j * w + (w - 1 - i)];
					else
						destPixels[(y + j) * dest->w + (x + i)] = srcPixels[j * w + i];
				}
			}
		}
	}
}

void SuperSurface::printRot(int x, int y, int angle, SDL_Surface* dest, unsigned int* hmap, bool flip, unsigned int height)
{
	Uint32* srcPixels = (Uint32*)pixels;
	Uint32* destPixels = (Uint32*)dest->pixels;
	unsigned int pixHeight = height;
	unsigned int l;
	int srcX, srcY;

	if (w > h) l = w;
	else l = h;
	if (l % 2) l++;

	for (int i = 0; i < l; i++) {
		for (int j = 0; j < l; j++) {

			if ((x - l / 2 + i) >= 0 && (x - l / 2 + i) < dest->w && (y - l / 2 + j) >= 0 && (y - l / 2 + j) < dest->h) {
				if (hmap[(y - l / 2 + j) * dest->w + (x - l / 2 + i)] < height) {

					//Search of the relevent source pixel
					srcX = (i - (l / 2)) * cos(angle) + (j - (l / 2)) * sin(angle) + (l / 2);
					srcY = (i - (l / 2)) * (-sin(angle)) + (j - (l / 2)) * cos(angle) + (l / 2);
					if (flip) srcX = w - srcX - 1;

					if (srcX >= 0 && srcX < w and srcY >= 0 && srcY < h && 1) {
						hmap[(y - l / 2 + j) * dest->w + (x - l / 2 + i)] = height;
						destPixels[(y - l / 2 + j) * dest->w + (x - l / 2 + i)] = srcPixels[srcY * w + srcX];
					}
				}
			}
		}
	}
}
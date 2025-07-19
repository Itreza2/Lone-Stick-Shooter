#pragma once
#include <SDL.h>

/*
TODO :
-> prevent overwriting with a transparent pixel
*/

/**
* @brief an extention of the SDL Surface that provide methods for rotation and "isometric" rendering
* /!\ These methods do not perform optimised bit-BLT as the ones of the SDL librairy, and may be a bit slow /!\
*/
struct SuperSurface : public SDL_Surface
{
	SuperSurface(const SDL_Surface& surface) : SDL_Surface(surface) {}

	SuperSurface(SDL_Surface&& surface) : SDL_Surface(surface) {}

	//~SuperSurface() { SDL_FreeSurface(this); }

	/**
	* @brief print itself on an other Surface, taking into account a height map (a pixel is only printed if
	* its height is superior to the one of the pixel it overwrite)
	* @param source the rectangle within the surface that will be printed (if nullptr, the whole surface)
	* @param x the position on the x axis of the destination surface where the top-left pixel will be printed
	* @param y the position on the y axis of the destination surface where the top-left pixel will be printed
	* @param dest the Surface on which the print will be performed
	* @param hmap a height map containing the current height of every pixel of the destination Surface
	* @param flip print the surface with a vertical flip
	* @param height the height of the lowest row of pixels of the printed Surface
	* @param vertical if true, every row of pixel of the printed surface will be higher by one than the row below
	*/
	void printIso(SDL_Rect* source, int x, int y, SDL_Surface* dest, unsigned int* hmap,
		bool flip = false, unsigned int height = 1, bool vertical = true);

	/**
	* @brief print itself on an other surface with a rotation, taking into account a height map (a pixel is
	* only printed if its height is superior to the one of the pixel it overwrite)
	* @param source the rectangle within the surface that will be printed (if nullptr, the whole surface)
	* @param x the position on the x axis of the destination surface of the center of the print
	* @param y the position on the y axis of the destination surface of the center of the print
	* @param angle the angle (in rad) of the rotation
	* @param dest the Surface on which the print will be performed
	* @param hmap a height map containing the current height of every pixel of the destination Surface
	* @param flip print the surface with a vertical flip
	* @param height the height of the lowest row of pixels of the printed Surface
	*/
	void printRot(SDL_Rect* source, int x, int y, int angle, SDL_Surface* dest, unsigned int* hmap, 
		bool flip = false, unsigned int height = 1);
};
#pragma once
#include <SDL.h>
#include <cmath>
#include <iostream>

#include "Character.h"
#include "World.h"
#include "Sprite_lib.h"

class Camera
{
private:

	//The character tracked by the camera
	Character* target;

	//The offset of the camera from the position of @m target on the x and y axis
	int offset_x;
	int offset_y;

	//x and y coordinates of the top left corner of the camera
	int top_left_x;
	int top_left_y;

	//The world object containing every drawable entity
	World* map;

	Sprite_lib* sprites;

	//The part of the window where the camera must be rendered
	SDL_Rect render_rect;

	//A SDL surface on witch the camera is drawing
	SDL_Surface* surface;

	//Represent the height of every pixel drawn on @m surface, used for the isometric rendering
	unsigned int* h_map;

	//Number of pixels covered by the camera on the x and y axis
	unsigned int width;
	unsigned int height;

	/*
	@brief draw the floor at the current camera's position using a given sprite sheet
	it is assumed that the member surface is locked when calling this method.
	@param sprite_sheet a pointer toward a surface containing the sprite sheet of the tile set
	(Must be locked beforehand !)
	@return 0 on success, otherwise 1 (no exeption currently that being said)
	*/
	int draw_floor();

	/*
	@brief called by draw_floor, draw a given wall
	@param x the x position of the wall to draw on the @m World arrays
	@param y the y position of the wall to draw on the @m World arrays
	*/
	void draw_wall(int x, int y, Uint32* pixels, Uint32* pixels_w);

	/*
	*/
	void draw_props();

	/*
	*/
	void draw_character(int char_idx, Uint32* pixels);

public:

	/*
	@brief <todo>
	@param target_ The character tracked by the camera
	@param render_rect_ The part of the window where the camera must be rendered
	@param width_ the width in pixels of the area covered by the camera
	@param height_ the width in pixels of the area covered by the camera
	@param err a int where the error code is to be stored. It can be 0 if everything is successfull or
	1 in the case of a malloc faillure
	*/
	Camera(Character* target_, World* map_, Sprite_lib* sprites_, SDL_Rect render_rect_, unsigned int width_, unsigned int height_, int& err);

	/*
	@brief draw on the window the current state of the covered area
	@param draw_frame the renderer where camera is to be rendered
	*/
	void draw_frame(SDL_Renderer* render);
};


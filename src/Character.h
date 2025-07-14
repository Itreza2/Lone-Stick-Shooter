#pragma once

#include "Object.h"

class Character : public BasicObject
{
private:

	int relXGHBox, relYGHBox;

	int wGHBox, hGHBox;

public:

	Character(int x, int y, ryml::Tree model);

	SDL_Rect getGroundHitBox() { return {(int)(x + relXGHBox), (int)(y + relYGHBox), wGHBox, hGHBox}; }

	virtual bool update();

	virtual void animate();

	virtual void behavior() {}

	virtual bool collision(const SDL_Rect& rect); //Take the ground hbox instead

};
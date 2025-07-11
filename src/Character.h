#pragma once

#include "Object.h"

class Character : public BasicObject
{
public:

	Character(int x, int y, ryml::Tree model) : BasicObject(x, y, model) {}

	virtual bool update();

	virtual void animate();

	virtual void behavior() {}

};
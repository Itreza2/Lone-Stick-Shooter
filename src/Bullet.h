#pragma once

#include "Object.h"

class Bullet : public BasicObject
{
public:

	Bullet(int x, int y, ryml::Tree model) : BasicObject(x, y, model) {}

};
#include "Object.h"

ryml::Tree BasicObject::loadModel(std::string model)
{
	//Load the model yaml file
	std::ifstream file(("rsc/templates/" + model + ".yml").c_str());
	if (!file.is_open());
	//TODO exception if file does not open
	std::string content{ std::istreambuf_iterator<char>(file), std::istreambuf_iterator<char>() };
	
	return ryml::parse_in_arena(ryml::to_csubstr(content));
}

BasicObject::BasicObject(int x, int y, ryml::Tree model)
{
	this->x = x;
	this->y = y;
	currentAnim = 0;
	currentFrame = 0;
	animLengths = {};

	vX << model["velocity"][0];
	vY << model["velocity"][1];
	w << model["hitbox"][0];
	h << model["hitbox"][1];
	e << model["elevation"];
	sheet << model["sheet"];
	sX << model["spriteCoordinates"][0];
	sY << model["spriteCoordinates"][1];
	sW << model["spriteShape"][0];
	sH << model["spriteShape"][1];

	int nbrAnim;
	unsigned int lenght;
	nbrAnim << model["animNbr"];
	for (int i = 0; i < nbrAnim; i++) {
		lenght << model["animLenghts"][i];
		animLengths.push_back(lenght);
	}
}

bool BasicObject::update()
{
	//Circle through the same animation indefinitely and doesn't move
	if (SDL_GetTicks() - lastFrame > 200)
		animate();
	return false;
}

void BasicObject::animate()
{
	currentFrame++;
	if (currentFrame >= animLengths[0])
		currentFrame = 0;
}

bool BasicObject::collision(const BasicObject& obj)
{
	int x1, x2, y1, y2, w1, h1;
	if (x < obj.x) {
		x1 = x; x2 = obj.x; w1 = w;
	} else {
		x1 = obj.x; x2 = x; w1 = obj.w;
	}
	if (y < obj.y) {
		y1 = y; y2 = obj.y; h1 = h;
	} else {
		y1 = obj.y; y2 = y; h1 = obj.h;
	}
	if (x2 - x1 < w1 && y2 - y1 < h1)
		return true;
	else
		return false;
}
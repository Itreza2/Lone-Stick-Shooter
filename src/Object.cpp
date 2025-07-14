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
	this->x = (float)x;
	this->y = (float)y;
	prevX = x;
	prevY = y;
	flip = false;
	currentAnim = 0;
	currentFrame = 0;
	animLengths = {};
	model["hitPoints"] >> maxHp;
	hp = maxHp;
	model["velocityMax"][0] >> maxVx;
	model["velocityMax"][1] >> maxVy;
	model["velocity"][0] >> vX;
	model["velocity"][1] >> vY;
	model["hitbox"][0] >> w;
	model["hitbox"][1] >> h;
	model["elevation"] >> e;
	model["sheet"] >> sheet;
	model["spriteCoordinates"][0] >> sX;
	model["spriteCoordinates"][1] >> sY;
	model["spriteShape"][0] >> sW;
	model["spriteShape"][1] >> sH;
	model["spriteOffset"][0] >> sOffsetX;
	model["spriteOffset"][1] >> sOffsetY;

	int nbrAnim;
	unsigned int lenght;
	model["animNb"] >> nbrAnim;
	for (int i = 0; i < nbrAnim; i++) {
		model["animLenghts"][i] >> lenght;
		animLengths.push_back(lenght);
	}
}

bool BasicObject::update()
{
	//Circle through the same animation indefinitely and doesn't move
	if (SDL_GetTicks() - lastFrame > 200) {
		animate();
		lastFrame = SDL_GetTicks();
	}
	if (hp == 0 && maxHp > 0)
		return true;
	return false;
}

void BasicObject::animate()
{
	currentFrame++;
	if (currentFrame >= animLengths[0])
		currentFrame = 0;
}

bool BasicObject::collision(BasicObject& obj)
{
	if ((w == 1 && h == 1) || (obj.w == 1 && obj.h == 1))
		return false;  //Object without hitbox
	else {
		return collision({ (int)obj.x, (int)obj.y, (int)obj.w, (int)obj.h });
	}
}

bool BasicObject::collision(const SDL_Rect& rect)
{
	int x1, x2, y1, y2, w1, h1;
	if (x < rect.x) {
		x1 = (int)x; x2 = rect.x; w1 = w;
	}
	else {
		x1 = rect.x; x2 = (int)x; w1 = rect.w;
	}
	if (y < rect.y) {
		y1 = (int)y; y2 = rect.y; h1 = h;
	}
	else {
		y1 = rect.y; y2 = (int)y; h1 = rect.h;
	}
	if (x2 - x1 < w1 && y2 - y1 < h1)
		return true;
	else
		return false;
}
#include "Character.h"

Character::Character(int x, int y, ryml::Tree model) : BasicObject(x, y, model) {
	model["groundBoxRelative"][0] >> relXGHBox;
	model["groundBoxRelative"][1] >> relYGHBox;
	model["groundBoxSize"][0] >> wGHBox;
	model["groundBoxSize"][1] >> hGHBox;
}

bool Character::update()
{
	Uint32 currentTick = SDL_GetTicks();
	
	prevX = x;
	prevY = y;
	if (vX)
		x += (static_cast<float>(currentTick) - lastUpdate) / 1000 * vX;
	if (vY)
		y += (static_cast<float>(currentTick) - lastUpdate) / 1000 * vY;
	lastUpdate = currentTick;

	behavior();

	if (currentTick - lastFrame > 150) {
		animate();
		lastFrame = currentTick;
	}
	if (hp == 0 && maxHp > 0)
		return true;
	return false;
}

void Character::animate()
{
	if (!vX && !vY)
		currentAnim = 0;
	else
		currentAnim = 1;

	currentFrame++;
	if (currentFrame >= animLengths[currentAnim])
		currentFrame = 0;
}

bool Character::collision(const SDL_Rect& rect)
{
	if ((rect.w == 1 && rect.h == 1))
		return false;
	else {
		int x1, x2, y1, y2, w1, h1;
		if ((x + relXGHBox) < rect.x) {
			x1 = (int)(x + relXGHBox); x2 = rect.x; w1 = wGHBox;
		}
		else {
			x1 = rect.x; x2 = (int)(x + relXGHBox); w1 = rect.w;
		}
		if ((y + relYGHBox) < rect.y) {
			y1 = (int)(y + relYGHBox); y2 = rect.y; h1 = hGHBox;
		}
		else {
			y1 = rect.y; y2 = (int)(y + relYGHBox); h1 = rect.h;
		}
		if (x2 - x1 < w1 && y2 - y1 < h1)
			return true;
		else
			return false;
	}
}
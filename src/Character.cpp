#include "Character.h"

bool Character::update()
{
	Uint32 currentTick = SDL_GetTicks();

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
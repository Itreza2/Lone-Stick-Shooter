#include "Player.h"

void Player::behavior()
{
	Keyboard* keyboard = Keyboard::getKeyboard();

	if (keyboard->keyDown(KEY_UP, (Caller_)type) && keyboard->keyDown(KEY_LEFT, (Caller_)type)) {
		vX = -maxVx * 0.71; //0.71 = cos(pi / 4), we spare ourselves a computation
		vY = -maxVy * 0.71;
		flip = true;
	} else if (keyboard->keyDown(KEY_UP, (Caller_)type) && keyboard->keyDown(KEY_RIGTH, (Caller_)type)) {
		vX = maxVx * 0.71;
		vY = -maxVy * 0.71;
		flip = false;
	} else if (keyboard->keyDown(KEY_DOWN, (Caller_)type) && keyboard->keyDown(KEY_LEFT, (Caller_)type)) {
		vX = -maxVx * 0.71;
		vY = maxVy * 0.71;
		flip = true;
	} else if (keyboard->keyDown(KEY_DOWN, (Caller_)type) && keyboard->keyDown(KEY_RIGTH, (Caller_)type)) {
		vX = maxVx * 0.71;
		vY = maxVy * 0.71;
		flip = false;
	} else if (keyboard->keyDown(KEY_LEFT, (Caller_)type)) {
		vX = -maxVx;
		vY = 0;
		flip = true;
	} else if (keyboard->keyDown(KEY_RIGTH, (Caller_)type)) {
		vX = maxVx;
		vY = 0;
		flip = false;
	} else if (keyboard->keyDown(KEY_UP, (Caller_)type)) {
		vX = 0;
		vY = -maxVy;
	} else if (keyboard->keyDown(KEY_DOWN, (Caller_)type)) {
		vX = 0;
		vY = maxVy;
	} else {
		vX = 0;
		vY = 0;
	}
}
#pragma once

#include "Character.h"
#include "Keyboard.h"

enum PlayerType_ { //Equivalent to the Caller_ enum of Keyboard.h but more restrictive
	PLAYER_1_ = 1,
	PLAYER_2_ = 2
};

class Player : public Character
{
private:

	PlayerType_ type;

public:

	Player(PlayerType_ type, int x, int y, ryml::Tree model) : Character(x, y, model) { this->type = type; }

	virtual void behavior();

};
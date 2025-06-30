#pragma once
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <SDL.h>

/*
TODO :
-> User defined keymap
*/

enum Key_ {
	KEY_EXIT = 0,
	KEY_UP = 1,
	KEY_DOWN = 2,
	KEY_RIGTH = 3,
	KEY_LEFT = 4,
	KEY_SHOOT = 5,
	KEY_POWER = 6,
	KEY_CONTEXT = 7,
	KEY_TOGGLE = 8,
	KEY_UNUSED1 = 9,
	KEY_UNUSED2 = 10,
	KEY_ANY = 11
};

enum Caller_ {
	MAIN,
	PLAYER_1,
	PLAYER_2
};

class Keyboard
{
private:

	static Keyboard* instance;

	std::vector<unsigned int> keyMapping;

	std::vector<bool> isPressed;

	SDL_Event event;

	Keyboard();

	void applyMapping();

public:

	static Keyboard* getKeyboard();

	bool catchEvents();

	bool keyDown(Key_ keyName, Caller_ caller = MAIN);
};

Keyboard* Keyboard::instance = nullptr;
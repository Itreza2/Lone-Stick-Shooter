#include "Keyboard.h"

Keyboard::Keyboard()
{
	keyMapping = {};
	isPressed = {};

	applyMapping();
}

void Keyboard::applyMapping()
{
	//TODO : user defined keymap

	std::ifstream file ("rsc/tools/keymapDEFAULT");
	std::string line;
	
	if (file.is_open()) {
		while (std::getline(file, line)) {
			keyMapping.push_back(std::stoi(line));
			isPressed.push_back(false);
		}
	}

}

Keyboard* Keyboard::getKeyboard()
{

	if (instance == nullptr) {
		instance = new Keyboard();
	}
	return instance;
}

bool Keyboard::catchEvents()
{
	while (SDL_PollEvent(&event)) {
		if (event.type == SDL_QUIT) {
			return true;
		} if (event.type == SDL_KEYDOWN) {
			for (int i = 0; i < 21; i++) {
				if (keyMapping[i] == event.key.keysym.scancode)
					isPressed[i] = true;
			}
		} if (event.type == SDL_KEYUP) {
			for (int i = 0; i < 21; i++) {
				if (keyMapping[i] == event.key.keysym.scancode)
					isPressed[i] = false;
			}
		}
	}
	return false;
}

bool Keyboard::keyDown(Key_ keyName, Caller_ caller)
{
	if (caller == MAIN) {
		switch (keyName) {
		case (KEY_EXIT):
			return isPressed[0];
			break;
		case (KEY_ANY):
			for (unsigned int i = 1; i <= 10; i++) {
				if (isPressed[keyName] || isPressed[keyName + 10])
					return true;
			} return false;
			break;
		default:
			return isPressed[keyName] || isPressed[keyName + 10];
		};
	}
	if (caller == PLAYER_1 && keyName != KEY_EXIT && keyName != KEY_ANY)
		return isPressed[keyName];
	if (caller == PLAYER_2 && keyName != KEY_EXIT && keyName != KEY_ANY)
		return isPressed[keyName + 10];
	return false; //should never be called
}
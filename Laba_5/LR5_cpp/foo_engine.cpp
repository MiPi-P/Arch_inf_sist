#include "foo_engine.h"
#include <iostream>

void FooEngine::forward(float value)
{
    std::cout << "ROBOT: Forward " << value << " cm" << std::endl;
}

void FooEngine::left(float value)
{
    std::cout << "ROBOT: Left " << value << " degrees" << std::endl;
}

void FooEngine::right(float value)
{
    std::cout << "ROBOT: Right " << value << " degrees" << std::endl;
}

void FooEngine::stop()
{
    std::cout << "ROBOT: Stop" << std::endl;
}
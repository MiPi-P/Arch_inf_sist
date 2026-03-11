#pragma once
#include "engine.h"
#include <iostream>

class FooEngine : public AEngine
{
public:
    void forward(int time) override {
        std::cout << "Forward " << time << std::endl;
    }

    void left(int time) override {
        std::cout << "Left " << time << std::endl;
    }

    void right(int time) override {
        std::cout << "Right " << time << std::endl;
    }

    void stop() override {
        std::cout << "Stop" << std::endl;
    }
};
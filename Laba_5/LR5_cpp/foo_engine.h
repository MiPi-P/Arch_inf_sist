#pragma once
#include "engine.h"

class FooEngine : public AEngine
{
public:
    void forward(float value) override;
    void left(float value) override;
    void right(float value) override;
    void stop() override;
};

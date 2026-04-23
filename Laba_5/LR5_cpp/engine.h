#pragma once

class AEngine
{
public:
    virtual ~AEngine() = default;

    virtual void forward(float value) = 0;
    virtual void left(float value) = 0;
    virtual void right(float value) = 0;
    virtual void stop() = 0;
};
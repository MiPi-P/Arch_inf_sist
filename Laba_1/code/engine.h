#pragma once

class AEngine
{
public:
    virtual void forward(int time) = 0;
    virtual void left(int time) = 0;
    virtual void right(int time) = 0;
    virtual void stop() = 0;
};
#pragma once
#include <string>

class AReceiver
{
public:
    virtual std::string receive() = 0;
};
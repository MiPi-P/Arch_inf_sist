#include "receiver.h"
#include <iostream>

class FooReceiver : public AReceiver
{
public:
    std::string receive() override {
        std::string cmd;
        std::getline(std::cin, cmd);
        return cmd;
    }
};
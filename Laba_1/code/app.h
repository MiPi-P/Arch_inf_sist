#pragma once
#include "receiver.h"
#include "engine.h"

class App
{
private:
    AReceiver& receiver;
    AEngine& engine;

public:

    App(AReceiver& r, AEngine& e);

    void run();
};
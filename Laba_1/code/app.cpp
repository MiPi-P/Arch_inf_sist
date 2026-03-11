#include "app.h"
#include <sstream>

App::App(AReceiver& r, AEngine& e) : receiver(r), engine(e) {}

void App::run()
{
    while(true)
    {
        std::string cmd = receiver.receive();

        std::stringstream ss(cmd);
        std::string action;
        int time;

        ss >> action >> time;

        if(action == "forward")
            engine.forward(time);

        else if(action == "left")
            engine.left(time);

        else if(action == "right")
            engine.right(time);

        else if(action == "stop")
            engine.stop();
    }
}
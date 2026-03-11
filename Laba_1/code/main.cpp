#include "app.h"
#include "foo_receiver.h"
#include "foo_engine.h"

int main() {
    FooReceiver receiver;
    FooEngine engine;

    App app(receiver, engine);

    app.run();

    return 0;
}
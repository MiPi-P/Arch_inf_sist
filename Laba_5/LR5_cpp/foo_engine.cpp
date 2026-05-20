#include "foo_engine.h"
#include <iostream>
#include <cstdint>
#include <thread>
#include <chrono>

#ifdef __linux__

#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/gpio.h>

void gpio_write(const char *dev_name, int offset, uint8_t value)
{
    struct gpiohandle_request rq;
    struct gpiohandle_data data;
    int fd, ret;

    fd = open(dev_name, O_RDONLY);
    if (fd < 0) {
        std::cout << "GPIO open error: " << strerror(errno) << std::endl;
        return;
    }

    memset(&rq, 0, sizeof(rq));
    rq.lineoffsets[0] = offset;
    rq.flags = GPIOHANDLE_REQUEST_OUTPUT;
    rq.lines = 1;
    rq.default_values[0] = value;

    ret = ioctl(fd, GPIO_GET_LINEHANDLE_IOCTL, &rq);
    close(fd);

    if (ret == -1) {
        std::cout << "GPIO ioctl error: " << strerror(errno) << std::endl;
        return;
    }

    memset(&data, 0, sizeof(data));
    data.values[0] = value;

    ret = ioctl(rq.fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &data);
    if (ret == -1) {
        std::cout << "GPIO set error: " << strerror(errno) << std::endl;
    }

    close(rq.fd);
}

#endif

void FooEngine::stop()
{
    std::cout << "ROBOT: Stop" << std::endl;

#ifdef __linux__
    gpio_write("/dev/gpiochip0", 12, 0);
    gpio_write("/dev/gpiochip0", 13, 0);
    gpio_write("/dev/gpiochip0", 20, 0);
    gpio_write("/dev/gpiochip0", 21, 0);

    gpio_write("/dev/gpiochip0", 6, 0);   // ENA
    gpio_write("/dev/gpiochip0", 26, 0);  // ENB
#endif
}

void FooEngine::forward(float time)
{
    std::cout << "ROBOT: Forward " << time << " sec" << std::endl;

#ifdef __linux__
    gpio_write("/dev/gpiochip0", 6, 1);   // ENA
    gpio_write("/dev/gpiochip0", 26, 1);  // ENB

    gpio_write("/dev/gpiochip0", 12, 1);
    gpio_write("/dev/gpiochip0", 13, 0);
    gpio_write("/dev/gpiochip0", 20, 0);
    gpio_write("/dev/gpiochip0", 21, 1);

    std::this_thread::sleep_for(std::chrono::milliseconds((int)(time * 1000)));
    stop();
#endif
}

void FooEngine::left(float time)
{
    std::cout << "ROBOT: Left " << time << " sec" << std::endl;

#ifdef __linux__
    gpio_write("/dev/gpiochip0", 26, 1);  // ENB

    gpio_write("/dev/gpiochip0", 20, 0);
    gpio_write("/dev/gpiochip0", 21, 1);

    std::this_thread::sleep_for(std::chrono::milliseconds((int)(time * 1000)));
    stop();
#endif
}

void FooEngine::right(float time)
{
    std::cout << "ROBOT: Right " << time << " sec" << std::endl;

#ifdef __linux__
    gpio_write("/dev/gpiochip0", 6, 1);   // ENA

    gpio_write("/dev/gpiochip0", 12, 1);
    gpio_write("/dev/gpiochip0", 13, 0);

    std::this_thread::sleep_for(std::chrono::milliseconds((int)(time * 1000)));
    stop();
#endif
}

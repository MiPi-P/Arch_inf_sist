#include "foo_engine.h"
#include <iostream>
#include <cstdint>

#ifdef __linux__

#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>
#include <sys/ioctl.h>
#include <linux/gpio.h>

// ===== GPIO =====
void gpio_write(const char *dev_name, int offset, uint8_t value)
{
    struct gpiohandle_request rq;
    struct gpiohandle_data data;
    int fd, ret;

    fd = open(dev_name, O_RDONLY);
    if (fd < 0) return;

    rq.lineoffsets[0] = offset;
    rq.flags = GPIOHANDLE_REQUEST_OUTPUT;
    rq.lines = 1;

    ret = ioctl(fd, GPIO_GET_LINEHANDLE_IOCTL, &rq);
    close(fd);

    if (ret == -1) return;

    data.values[0] = value;
    ioctl(rq.fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &data);

    close(rq.fd);
}

#endif

// ===== ВПЕРЁД =====
void FooEngine::forward(float time)
{
    std::cout << "ROBOT: Forward " << time << " sec" << std::endl;

#ifdef __linux__
    gpio_write("/dev/gpiochip0", 12, 1);
    gpio_write("/dev/gpiochip0", 13, 0);
    gpio_write("/dev/gpiochip0", 20, 0);
    gpio_write("/dev/gpiochip0", 21, 1);
#endif
}

// ===== ВЛЕВО =====
void FooEngine::left(float time)
{
    std::cout << "ROBOT: Left " << time << " sec" << std::endl;

#ifdef __linux__
    gpio_write("/dev/gpiochip0", 20, 0);
    gpio_write("/dev/gpiochip0", 21, 1);
#endif
}

// ===== ВПРАВО =====
void FooEngine::right(float time)
{
    std::cout << "ROBOT: Right " << time << " sec" << std::endl;

#ifdef __linux__
    gpio_write("/dev/gpiochip0", 12, 1);
    gpio_write("/dev/gpiochip0", 13, 0);
#endif
}

// ===== СТОП =====
void FooEngine::stop()
{
    std::cout << "ROBOT: Stop" << std::endl;

#ifdef __linux__
    gpio_write("/dev/gpiochip0", 12, 0);
    gpio_write("/dev/gpiochip0", 13, 0);
    gpio_write("/dev/gpiochip0", 20, 0);
    gpio_write("/dev/gpiochip0", 21, 0);
#endif
}
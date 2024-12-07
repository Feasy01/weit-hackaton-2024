#include <Arduino.h>

#include "actuator.hpp"

int move_up(Servo actuator)
{
    int pos = actuator.read();

    if (pos < 90)
    {
        for (pos; pos <= 90; pos += 1)
        {
            actuator.write(pos);
            delay(10);
        }
    } 
    else if (pos > 90)
    {
        for (pos; pos >= 90; pos -= 1)
        {
            actuator.write(pos);
            delay(10);
        }
    }
    
    return 0;
}

int move_down(Servo actuator)
{
    int pos = actuator.read();

    if (pos > 0)
    {
        for (pos; pos >= 0; pos -= 1)
        {
            actuator.write(pos);
            delay(10);
        }
    }
    return 0;
}

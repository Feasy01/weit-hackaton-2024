#include <Arduino.h>
#include "HX711.h"

const int BED_ID = 1;
const int NUMBER_OF_PRESS_SENSORS = 3;

const int pinout[NUMBER_OF_PRESS_SENSORS][2] = { // DOUT, SCK
    {13, 12},
    {8, 7},
    {6, 5}};

HX711 press_sensors[NUMBER_OF_PRESS_SENSORS];

void setup()
{
  Serial.begin(9600);

  for (int i = 0; i < NUMBER_OF_PRESS_SENSORS; i++)
  {
    press_sensors[i].begin(pinout[i][0], pinout[i][1]);
    press_sensors[i].tare();
  }
}

void loop()
{
  int raw_values[NUMBER_OF_PRESS_SENSORS];
  int values[NUMBER_OF_PRESS_SENSORS];

  for (int i = 0; i < NUMBER_OF_PRESS_SENSORS; i++)
  {
    if (!press_sensors[i].wait_ready_timeout(1000))
    {
      Serial.println("HX711 of id " + String(i) + " not found.");
      return;
    }
    raw_values[i] = abs(press_sensors[i].get_value(5)); // get_units
    Serial.print("HX711 of id " + String(i) + " reading: " + String(raw_values[i]) + "\n");
  }

  // save to values in format: 0 for min of all sensors, 1 for next min, 2 for next min, etc.
  for (int i = 0; i < NUMBER_OF_PRESS_SENSORS; i++)
  {
    int current_min_index = 0;
    for (int j = 0; j < NUMBER_OF_PRESS_SENSORS; j++)
    {
      if (raw_values[j] < raw_values[current_min_index])
      {
        current_min_index = j;
      }
    }
    values[current_min_index] = i + 1;
    raw_values[current_min_index] = INT32_MAX;
  }

  // print "Sensor x: y" for each sensor
  for (int i = 0; i < NUMBER_OF_PRESS_SENSORS; i++)
  {
    Serial.print("-> Sensor " + String(i) + ": " + String(values[i]) + "\n");
  }

  // if (scale.wait_ready_timeout(1000))
  // {
  //   long reading = scale.get_value(5);
  //   Serial.print("HX711 reading: ");
  //   Serial.println(reading);
  // }
  // else
  // {
  //   Serial.println("HX711 not found.");
  // }

  delay(1500);
}
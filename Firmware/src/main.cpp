#include <Arduino.h>
#include "HX711.h"
#include "actuator.hpp"

const int BED_ID = 1;
const int NUMBER_OF_PRESS_SENSORS = 3;

const int pinout[NUMBER_OF_PRESS_SENSORS][2] = { // DOUT, SCK
    {13, 12},
    {8, 7},
    {6, 5}};

const int actuator_pins[NUMBER_OF_PRESS_SENSORS] = {9, 10, 11};

HX711 press_sensors[NUMBER_OF_PRESS_SENSORS];
Servo actuators[NUMBER_OF_PRESS_SENSORS];

void setup()
{
  Serial.begin(9600);

  for (int i = 0; i < NUMBER_OF_PRESS_SENSORS; i++)
  {
    press_sensors[i].begin(pinout[i][0], pinout[i][1]);
    press_sensors[i].tare();
    actuators[i].attach(actuator_pins[i]);
    actuators[i].write(0);
  }
}

void loop()
{
  int raw_values[NUMBER_OF_PRESS_SENSORS];
  int values[NUMBER_OF_PRESS_SENSORS];
  int index_of_max_part = -1;

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
    index_of_max_part = current_min_index;
  }

  // print "Sensor x: y" for each sensor
  for (int i = 0; i < NUMBER_OF_PRESS_SENSORS; i++)
  {
    Serial.print("-> Sensor " + String(i) + ": " + String(values[i]) + "\n");
  }

  // print "Max part: x" for the sensor with the highest value
  Serial.print("-> Max part index: " + String(index_of_max_part) + "\n");

  int first_neighbor_of_max_part = index_of_max_part - 1;
  int second_neighbor_of_max_part = index_of_max_part + 1;

  if (first_neighbor_of_max_part < 0)
  {
    first_neighbor_of_max_part = -1;
  }

  if (second_neighbor_of_max_part >= NUMBER_OF_PRESS_SENSORS)
  {
    second_neighbor_of_max_part = -1;
  }

  // print "First neighbor: x" for the sensor with the second highest value
  if (first_neighbor_of_max_part != -1)
  {
    Serial.print("-> First neighbor: " + String(first_neighbor_of_max_part) + "\n");
  }
  else
  {
    Serial.print("-> First neighbor: None\n");
  }

  // print "Second neighbor: x" for the sensor with the third highest value
  if (second_neighbor_of_max_part != -1)
  {
    Serial.print("-> Second neighbor: " + String(second_neighbor_of_max_part) + "\n");
  }
  else
  {
    Serial.print("-> Second neighbor: None\n");
  }

  int neighbors[2] = {first_neighbor_of_max_part, second_neighbor_of_max_part};

  // move up the actuators of the neighbors
  for (int i = 0; i < 2; i++)
  {
    if (neighbors[i] != -1)
    {
      move_up(actuators[neighbors[i]]);
    }
  }

  // move down the rest of the actuators
  for (int i = 0; i < NUMBER_OF_PRESS_SENSORS; i++)
  {
    if (i != first_neighbor_of_max_part && i != second_neighbor_of_max_part)
    {
      move_down(actuators[i]);
    }
  }

  delay(5000);
}
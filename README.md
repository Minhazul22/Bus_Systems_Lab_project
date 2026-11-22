# Distance Sensor Characterization & Selection

**Comparing an ultrasonic sensor and an infrared PSD sensor using
Arduino and Python.**

A hands-on embedded-systems project focused on measuring, analyzing and
comparing two distance sensors:

-   **MaxBotix XL-MaxSonar-EZ MB1360** --- ultrasonic
-   **Sharp GP2Y0A21YK0F** --- infrared PSD

**Course:** Laboratory N2, HAW Hamburg · **Team:** Omar Ebrahem &
Minhazul Islam · **Date:** November 2026

## Project overview
![Distance sensor project overview](images/A)
Both sensors were tested over a target-distance range of 20--80 cm.
Their analog outputs were measured with a multimeter and oscilloscope,
then acquired using an Arduino Nano. Python was used to log and analyze
the ADC data.

The project covered the complete measurement process: sensor
characterization, data acquisition, noise analysis, digital filtering
and sensor selection.

## Hardware & tools

-   Arduino Nano (10-bit ADC)
-   MaxBotix MB1360 ultrasonic sensor
-   Sharp GP2Y0A21YK0F PSD sensor
-   Multimeter and oscilloscope
-   Arduino/C++ and Python
-   USB serial communication

## System architecture & workflow

The diagram below shows the sensor connections, Arduino acquisition path
and Python-based logging and analysis workflow.

![Distance sensor system architecture and workflow](images/Distance%20Sensor%20System%20Workflow.png)

*Both sensors share the Arduino Nano's 5 V supply and ground. The Nano
reads the MB1360 on A0 and the Sharp sensor on A1, then streams the
10-bit ADC readings to Python over USB serial at 115200 baud.*

## What was implemented

-   Set up and connected two analog distance sensors.
-   Measured sensor output at ten distances between 20 and 80 cm.
-   Compared measured characteristic curves with datasheet values.
-   Investigated signal behavior using an oscilloscope.
-   Acquired sensor readings through the Arduino ADC.
-   Logged data and generated time-series plots and histograms in
    Python.
-   Calculated mean, median, standard deviation and peak-to-peak
    variation.
-   Applied a five-sample median filter to reduce measurement spikes.
-   Compared both sensors against customer requirements.

## Key results

At 40 cm, 500 raw samples were collected from each sensor.

  Measurement                           MB1360           Sharp
  ----------------------------- -------------- ---------------
  Mean                            26.39 counts   228.55 counts
  Median                             21 counts      221 counts
  Raw standard deviation                 17.40           27.88
  Filtered standard deviation         **0.65**        **1.82**

The median filter substantially reduced short-term variation in the
recorded data.

The experiments also revealed time-dependent signal excursions and
possible interference through the shared supply and ground. This was a
plausible explanation, not a confirmed cause.

## Sensor comparison & conclusion

The Sharp sensor was the **provisional choice** because its specified
range covers 20--80 cm. The MB1360 reports no closer than 25 cm, so it
cannot cover the full required range.

However, the measurements did not demonstrate that either system meets
the customer requirements:

-   Resolution: 0.5 cm
-   Precision: 1 cm
-   Accuracy: 2 cm

The Sharp measurements deviated significantly from its datasheet
characteristic. Further testing with a defined reference target, proper
supply decoupling and calibration is needed before claiming compliance.

## Technologies

`Arduino` · `C++` · `Python` · `ADC` · `Serial Communication` ·
`Signal Processing` · `Data Analysis` · `Oscilloscope`

## Repository structure

``` text
├── README.md
├── arduino/
├── python/
├── data/
└── report/
```

*Suggested structure: include only folders and files that are actually
part of the repository.*

## References

-   MaxBotix XL-MaxSonar-EZ MB1360 datasheet
-   Sharp GP2Y0A21YK0F datasheet
-   HAW Hamburg, Laboratory N2 instructions, Winter Semester 2026/2027

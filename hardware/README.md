# Hardware

## Components

* Pi Pico (RP2040) - https://thepihut.com/products/raspberry-pi-pico
* Grove GPS Air530 - https://thepihut.com/products/grove-gps-air530
* Micro-USB male to USB-C female adapter
* Toggle switch with LED
* Project box

## Soldered connections

| Pico | GPS Air530 |
|------|----------|
| GP0 (UART Tx) | Rx |
| GP1 (UART Rx) | Tx |
| 3v3 |  3v3 |
| Gnd |  Gnd |

| Pico | Switch |
|------|--------|
| VSys | Vcc |
| GP22 | out |
| Gnd | Gnd |

*Note that the switch is connected to VSys on the Pico so we don't overload the Pico's input. My LED is rated for 12V but lights up with the 3.3V that Vsys provides.*

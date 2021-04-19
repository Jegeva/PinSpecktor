# PinSpector

Mass, a posteriori manipulation tool in kicad

Allows you to change local characteristics on multiple
Pins, Nets & Footprints at the same time.

This is designed for Kicad 5.x w/ Python3 & wxPhoenix

If that is a pain for you check

https://github.com/Jegeva/kicad-master-docker


## Thingies it does

For exemple, this can be usefull to


- hide value on all capacitors or on all transistors
- set paste retraction ratio to -30% on the odd pins of IC3


Cause you didn't put them wide enough and it burns on your last pototype :
- change the trace with on all traces in GND* to a specific width<sup>1</sup>
- change the trace with on all traces in GND* to the new rule width<sup>1</sup>


Cause you fuxed your impedance calculation :
- change the trace with on all traces in nets ADDR_.* to a specific width on a specific layer<sup>1</sup>


## Caveat emptor

This is free software, as-is, it may halt and catch fire,
damage your retina and cause high blood pressure.

Merge & pull requests accepted



<sup>1</sup>Yes, after the fact and (possibly) violating DRC but setting that straight is your job

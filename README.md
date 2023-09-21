# NanoControl v2
A scalable system for controlling Nanoleaf replicas based on the Adafruit Macropad.

---

This was originally a Christmas gift for my brother. I'd thrown together a set of hand-made NanoLeaf clones in almost no time and written the code even faster. It ran on a Raspberry Pi Zero W and was just... awful.

It was only controllable through a Google Assistant integration setup through IFTTT, and WHEN it worked, it was great. However, my code was pretty bad and broke all the time.

Eventually, I got annoyed with fixing it all the time and abandoned it, because I'm a bad person.

Now, I've rewritten just about everything in C++ for the Adafruit Macropad, and importantly, the RP2040. 

The code could *probably* be run on something else, but the code presently uses both cores of the RP2040. Core 0 controls the keypad, and core 1 controls the animations for the leaves.

This is still very incomplete, but the code is a million times less awful than the original was, it will function, basically forever, and doesn't try to be an IoT device for no reason.
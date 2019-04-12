# dmx-hackathon
Frank


Fix run non-root

add in /etc/udev/rules.d -> 51-velleman-dmx.rules

\\\
SUBSYSTEM=="usb", ATTRS{idVendor}=="10cf", ATTRS{idProduct}=="8062", MODE="0666"
\\\

# dmx-hackathon
Frank


Fix run non-root

add in /etc/udev/rules.d -> 51-velleman-dmx.rules

\\\
SUBSYSTEM=="usb", ATTRS{idVendor}=="10cf", ATTRS{idProduct}=="8062", MODE="0666"
\\\

### How to install OLA on a Raspberry Pi:
* Go to `/etc/apt/`
* Edit (with correct permissions) `sources.list` and add the following line:
    `deb [trusted=yes] http://apt.openlighting.org/raspbian wheezy main`
Do an `apt update`
And `apt install ola`
Then run `olad -l 3`, and go to `<pi_ip_address>:9090`.


### How to install OLA on a Raspberry Pi:
Go to `/etc/apt/`
Edit (with correct permissions) `sources.list` and add the following line:

`deb [trusted=yes] http://apt.openlighting.org/raspbian wheezy main`


Do an `apt update`

And `apt install ola`
Then run `olad -l 3`, and go to `<pi_ip_address>:9090`.


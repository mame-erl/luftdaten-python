# python-sck

Python 3 program to query data from a Smart Citizen Kit using their API and feed it to the [luftdaten.info](http://luftdaten.info/) sensor network.

Based on the work from [corny](https://github.com/corny/luftdaten-python)


## Dependencies

    apt install python3-numpy python3-requests python3-yaml


## Configuration

Copy the `config.yml.default` to `config.yml` and adjust the settings.


## Add Linux SystemD service

First, add a new service user.

	sudo adduser --system --no-create-home --disabled-login --group sckdaemon

Then, add a SystemD service.

	cd /etc/systemd/system
	sudo nano sckdaemon.service

Paste the specified contents - maybe adjust your paths.

	[Unit]
	Description=SCKdaemon
	Wants=network-online.target
	After=network-online.target
	StartLimitIntervalSec=500
	StartLimitBurst=5
	
	[Service]
	User=sckdaemon
	WorkingDirectoy=/home/pi/Dev/luftdaten-python/
	ExecStart=/home/pi/Dev/luftdaten-python/main.py
	Restart=on-failure
	RestartSec=30s
	
	[Install]
	WantedBy=multi-user.target

Enable in SystemD and check status.

	sudo systemctl enable sckdaemon.service
	sudo systemctl daemon-reload 
	sudo systemctl start sckdaemon.service 
	sudo systemctl status sckdaemon.service 
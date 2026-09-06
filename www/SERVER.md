# To enable server on startup:
```ino
# /etc/systemd/system/hostinfo.service

[Unit]
Description=Host info web server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=arduino
WorkingDirectory=/home/arduino/www
ExecStart=/usr/bin/python3 /home/arduino/www/server.py
Environment=PYTHONUNBUFFERED=1
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

```

Then run:
```bash
pkill -f server.py
sudo systemctl daemon-reload
sudo systemctl enable --now hostinfo
```
To confirm everything is working:
```bash
systemctl status hostinfo
```

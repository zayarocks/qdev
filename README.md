# Uno Q 
## Setup
Install [Arduino App Lab](https://docs.arduino.cc/software/app-lab/).
Set a network name and password.

```bash
ssh arduino@LOCAL_NETWORK_NAME.local
```


## Customization

Add the following to the bottom of .bashrc to load the repo's custom server configuration:
```bash
source ~/.bashrc.local
```

Now preview the banner:
```bash
python3 ./rainbow_motd.py
```

## Web Server
To run the basic HTML page:
```
python3 -m http.server 8000 --bind 0.0.0.0
```

Goto: [http://s3cr3t.local:8000]

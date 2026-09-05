# Uno Q 
## Setup
Install [Arduino App Lab](https://docs.arduino.cc/software/app-lab/).
Set a network name and password.

## SSH
```bash
ssh arduino@[NETWORK_NAME].local
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




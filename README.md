# How install 

## version

    Python 3.8.10
    pip 20.0.2

## Run

python3 -m venv venv
source venv/bin/activate
pip install -r versioning/pip_requirements.txt


# How to Install MQTT 

```
$ sudo apt-get install mosquitto

$ sudo apt-get install mosquitto-clients
```

## Test

```
$ mosquitto_pub -m "Mensagem" -t "test"
$ mosquitto_sub -t "test"
```

## Creating user and security passwords in MQTT

```
$ sudo mosquitto_passwd -c /etc/mosquitto/passwd udesc

$ sudo vim /etc/mosquitto/conf.d/default.conf

```
allow_anonymous false
password_file /etc/mosquitto/passwd

```
sudo systemctl restart mosquitto
```

```
$ mosquitto_sub -t "/teste" -u "udesc" -P "udesc"

$ mosquitto_pub -t "/teste" -m "mensagem" -u "udesc" -P "udesc"
```
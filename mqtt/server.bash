#!/bin/bash

mosquitto_sub -t "IDAtual" -u "udesc" -P "udesc" -h "localhost"
mosquitto_sub -t "StopCronometr" -u "udesc" -P "udesc" -h "localhost"
mosquitto_pub -t "ProximoID" -m "7" -u "udesc" -P "udesc" -h "localhost"
mosquitto_pub -t "TempoDecorrido" -m "timestamp" -u "udesc" -P "udesc" -h "localhost"
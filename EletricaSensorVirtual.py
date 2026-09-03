#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:53:35 2026

@author: fabiolicht
"""

import paho.mqtt.client as mqtt
import time
import json
import numpy as np
import random

BROKER_ADDRESS = "test.mosquitto.org"
PORT = 1883
TOPIC = "telemetria/motor_01/eletrica"

FREQ_REDE = 60.0
TAXA_AMOSTRAGEM = 1000.0

def gerar_amostra(t):
    # Onda fundamental 60Hz + ruído
    tensao = 220 * np.sqrt(2) * np.sin(2 * np.pi * FREQ_REDE * t) + random.gauss(0, 2.0)
    corrente = 15 * np.sqrt(2) * np.sin(2 * np.pi * FREQ_REDE * t) + random.gauss(0, 0.5)
    
    # Simula a injeção de uma falha grave (5º harmônico) a cada 5 segundos
    if int(t) % 10 >= 5: 
        tensao += 40 * np.sin(2 * np.pi * (5 * FREQ_REDE) * t)
        
    return round(tensao, 2), round(corrente, 2)

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Sensor_ESP32_Virtual")
    client.connect(BROKER_ADDRESS, PORT)
    client.loop_start()
    print(f"Sensor Virtual INICIADO. Publicando no tópico: {TOPIC}")
    
    t = 0.0
    passo = 1.0 / TAXA_AMOSTRAGEM
    
    try:
        while True:
            v, i = gerar_amostra(t)
            payload = {"tensao_v": v, "corrente_a": i}
            
            client.publish(TOPIC, json.dumps(payload))
            t += passo
            
            # Pequeno atraso para não sobrecarregar a rede pública instantaneamente
            time.sleep(0.001) 
            
    except KeyboardInterrupt:
        print("\nSensor Virtual desligado.")
        client.loop_stop()
        client.disconnect()
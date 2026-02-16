#!/bin/bash

while true; do
    revan=$(python3 revan.py)
    
    # Verifica o código de saída do Python
    if [ $? -ne 0 ]; then
        echo "O script revan.py encontrou um erro. Tentando novamente em breve..."
        sleep 5  # Espera 5 segundos antes de tentar de novo
    fi
done

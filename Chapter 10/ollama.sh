#!/bin/bash
echo "Starting ollama from docker, port 11434"
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# Use nvidia gpu with docker
# docker run -d --rm --gpus all \
#--device /dev/nvidia0:/dev/nvidia0   \
#--device /dev/nvidiactl:/dev/nvidiactl   \
#--device /dev/nvidia-uvm:/dev/nvidia-uvm   \
#--device /dev/nvidia-uvm-tools:/dev/nvidia-uvm-tools   \
#-v /usr/share/ollama:/root/.ollama:z -p 11434:11434 --name ollama ollama/ollama
echo "Pulling cogito:8b model"
docker exec -it ollama ollama pull cogito:8b
echo "Pulling gemma3n:e4b model"
docker exec -it ollama ollama pull gemma3n:e4b
echo "Pulling granite3.3:8b model"
docker exec -it ollama ollama pull granite3.3:8b
echo "Pulling qwen3:4b model"
docker exec -it ollama ollama pull qwen3:4b
echo "Now you can run the local jupyter notebook"
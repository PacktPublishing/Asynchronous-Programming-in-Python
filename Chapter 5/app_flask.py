import io
import json
import base64
import logging
from functools import lru_cache
import requests
from PIL import Image
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
OLLAMA_URL = 'http://127.0.0.1:11434'
POKEMON_URL = 'https://pokeapi.co'
MODEL_ID = 'llava'
headers = {'Content-Type': 'application/json'}

@lru_cache
def get_image(file):
    img_bytes = io.BytesIO()
    img = Image.open(file)
    img.save(img_bytes, 'PNG')
    base64_string = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    return base64_string

def analyze(base64):
    data = json.dumps({
            'model': MODEL_ID,
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': 'What is name of this pokemon?'
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/png;base64,{base64}'
                            }
                        }
                    ]
                }
            ],
            'max_tokens': 100,
    })
    response = requests.post(f'{OLLAMA_URL}/v1/chat/completions', data=data
                             , timeout=10,headers=headers)
    return response.json()

@lru_cache
def get_pokemon(pokemon_id):
    url = f'{POKEMON_URL}/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url, timeout=10, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Failed to get pokemon: {response.status_code}')
                        
def evaluate_response(id, img, pokemon, identification):
    name = str(pokemon.get('name')).lower()
    desc = str(identification.get('choices')[0]['message']['content']).lower()
    return {
        'id':id
        , 'image': img
        , 'name': name
        , 'model_identification':desc
        , 'ok': name in desc}

@app.route('/classify', methods=['POST'])
def classify():
    try:
        pokemon_id = request.args.get('id')
        pokemon = get_pokemon(pokemon_id)
        base64_img = get_image(request.files['image'])
        analysis = analyze(base64_img)
        r = evaluate_response(pokemon_id, base64_img, pokemon, analysis)
        return json.dumps(r), 200 if r.get('ok') == True else 418
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

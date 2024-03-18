from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Exemple d'endpoint qui interagit avec l'API externe de Pôle emploi
@app.route('/pole_emploi')
def pole_emploi():
    # Ici, tu ferais l'appel à l'API Pôle emploi
    # et retournerais la réponse. Par exemple :
    # response = requests.get('URL DE L API POLE EMPLOI', params=request.args)
    # return jsonify(response.json())
    return jsonify({"message": "Ceci est un exemple avec l'API Pôle emploi."})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

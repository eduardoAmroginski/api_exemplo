from flask import Flask, request, jsonify

app = Flask(__name__)

LISTA_PRODUTOS = []

@app.route("/api/produtos", methods=["POST"])
def cadastrar():
    dados = request.get_json()
    
    if not dados or "nome" not in dados or "preco" not in dados:
        return jsonify({
            "erro": "DADOS_INCOMPLETOS",
            "mensagem": "Os campos 'nome' e 'preco' são obrigatórios."
        }), 400

    novo_item = {
        "id" : len(LISTA_PRODUTOS) + 1,
        "nome" : dados["nome"],
        "preco" : dados["preco"]
    }

    LISTA_PRODUTOS.append(novo_item)

    return jsonify(novo_item), 201


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/produtos", methods=["POST"])
def adicionar_produto():
    dados = request.get_json()
    nome = dados.get("nome")

    return jsonify({
        "status" : "sucesso",
        "mensagem": f"Produto {nome} recebido!"
        }), 201


if __name__ == "__main__":
    app.run(debug=True)
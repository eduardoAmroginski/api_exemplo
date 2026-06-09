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


@app.route("/api/produtos", methods=["GET"])
def listar_produtos():
    id_produto = request.args.get("id")
    
    if not LISTA_PRODUTOS:
        return jsonify({"mensagem": "Nenhum produto cadastrado"}), 200
    
    if id_produto:
        for produto in LISTA_PRODUTOS:
            if int(produto.get("id")) == int(id_produto):
                return jsonify(produto), 200
                
        return jsonify({"erro": "NOT_FOUND", "mensagem": "Produto não encontrado"}), 404

    return jsonify(LISTA_PRODUTOS), 200


if __name__ == "__main__":
    app.run(debug=True)
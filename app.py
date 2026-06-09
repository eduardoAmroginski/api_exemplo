# Importa as ferramentas necessárias do Flask
# Flask: a classe principal para criar o servidor
# request: para acessar dados enviados pelo usuário (JSON, parâmetros da URL, etc.)
# jsonify: para converter dicionários Python em respostas no formato JSON
from flask import Flask, request, jsonify

# Inicializa a aplicação Flask
app = Flask(__name__)

# "Banco de dados" em memória. Como é uma lista, se o servidor reiniciar, os dados somem.
LISTA_PRODUTOS = []

PROXIMO_ID = 1  # Variável global para controlar os IDs

# ==========================================
# CREATE: CADASTRAR PRODUTO (Método POST)
# ==========================================
@app.route("/api/produtos", methods=["POST"])
def cadastrar():
    global PROXIMO_ID
    # Pega o corpo da requisição em formato JSON e transforma num dicionário Python
    dados = request.get_json()
    
    # Validação: verifica se enviaram o JSON e se os campos obrigatórios estão presentes
    if not dados or "nome" not in dados or "preco" not in dados:
        return jsonify({
            "erro": "DADOS_INCOMPLETOS",
            "mensagem": "Os campos 'nome' e 'preco' são obrigatórios."
        }), 400 # Retorna 400 (Bad Request) indicando que o cliente enviou dados inválidos


    novo_item = {
        "id" : PROXIMO_ID,
        "nome" : dados["nome"],
        "preco" : dados["preco"]
    }

    # Adiciona o novo produto na nossa lista
    LISTA_PRODUTOS.append(novo_item)
    PROXIMO_ID += 1  # Prepara o ID para o próximo produto que for cadastrado

    # Retorna o item criado e o status 201 (Created), que é o padrão para sucesso em POST
    return jsonify(novo_item), 201


# ==========================================
# READ: LISTAR PRODUTOS (Método GET)
# ==========================================
@app.route("/api/produtos", methods=["GET"])
def listar_produtos():
    # Tenta capturar um parâmetro 'id' passado na URL (ex: /api/produtos?id=1)
    id_produto = request.args.get("id")
    
    # Se a lista estiver vazia, retorna uma mensagem amigável com status 200 (OK)
    if not LISTA_PRODUTOS:
        return jsonify({"mensagem": "Nenhum produto cadastrado"}), 200
    
    # Se o usuário passou um ID na URL, vamos procurar esse produto específico
    if id_produto:
        for produto in LISTA_PRODUTOS:
            # Converte ambos para inteiro (int) para garantir que a comparação funcione
            if int(produto.get("id")) == int(id_produto):
                return jsonify(produto), 200 # Encontrou? Retorna o produto
                
        # Se o loop terminar e não achar, retorna 404 (Not Found)
        return jsonify({"erro": "NOT_FOUND", "mensagem": "Produto não encontrado"}), 404

    # Se nenhum ID foi passado na URL, retorna a lista com todos os produtos
    return jsonify(LISTA_PRODUTOS), 200


# ==========================================
# UPDATE TOTAL: ATUALIZAR TUDO (Método PUT)
# ==========================================
# A URL agora espera o ID no próprio caminho (ex: /api/produtos/2)
@app.route("/api/produtos/<int:id>", methods=["PUT"])
def atualizar_total(id):
    # Pega os dados novos enviados pelo usuário
    dados_novos = request.get_json()

    # O enumerate nos dá a posição do item na lista (index) e o próprio item (produto)
    for index, produto in enumerate(LISTA_PRODUTOS):
        if int(produto.get("id")) == int(id):
            # O PUT substitui o objeto inteiro pelos dados novos na posição encontrada
            # Atenção: Se 'dados_novos' não tiver o 'id', ele será perdido!
            LISTA_PRODUTOS[index] = dados_novos
            return jsonify(LISTA_PRODUTOS[index]), 200
        
    # Se não encontrar o ID, retorna 404
    return jsonify({"erro": "NOT_FOUND", "mensagem": "Produto não encontrado"}), 404


# ==========================================
# UPDATE PARCIAL: ATUALIZAR PARTE (Método PATCH)
# ==========================================
@app.route("/api/produtos/<int:id>", methods=["PATCH"])
def atualizar_parcial(id):
    dados = request.get_json()

    for produto in LISTA_PRODUTOS:
        if produto["id"] == id:
            # O PATCH atualiza apenas os campos que vieram na requisição
            if "preco" in dados:
                produto["preco"] = dados["preco"] # Atualiza só o preço se ele existir
            if "nome" in dados:
                produto["nome"] = dados["nome"]   # Atualiza só o nome se ele existir

            # Preserva os outros campos (como o ID) e retorna o produto atualizado
            return jsonify(produto), 200

    return jsonify({"erro": "NOT_FOUND", "mensagem": "Produto não encontrado"}), 404


# ==========================================
# DELETE: APAGAR PRODUTO (Método DELETE)
# ==========================================
@app.route("/api/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    
    # Percorre a lista para achar a posição (index) do produto que queremos apagar
    for index, produto in enumerate(LISTA_PRODUTOS):
        if produto["id"] == id:
            # pop() remove o item da lista na posição (index) especificada
            LISTA_PRODUTOS.pop(index)
            return jsonify({"mensagem" : "Apagado"}), 200
    
    # Se não encontrar para apagar, avisa que não existe
    return jsonify({"erro": "NOT_FOUND", "mensagem": "Produto não encontrado"}), 404


# ==========================================
# INICIALIZAÇÃO DO SERVIDOR
# ==========================================
# Garante que o servidor só inicie se este arquivo for executado diretamente
if __name__ == "__main__":
    # debug=True permite ver erros no navegador e reinicia o servidor ao salvar o arquivo
    app.run(debug=True)
from flask import Flask, request, jsonify
from datetime import datetime
import json, os

app = Flask(__name__)
DADOS_FILE = "dados.json"

def carregar_dados():
    if not os.path.exists(DADOS_FILE):
        return {}
    with open(DADOS_FILE, "r") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(DADOS_FILE, "w") as f:
        json.dump(dados, f)

@app.route("/status/<token>", methods=["GET"])
def get_status(token):
    dados = carregar_dados()
    if token not in dados:
        dados[token] = {"comando": "livre", "lucro": 0, "status": "aguardando", "atualizado": ""}
        salvar_dados(dados)
    return jsonify(dados[token])

@app.route("/atualizar/<token>", methods=["POST"])
def atualizar(token):
    dados = carregar_dados()
    body = request.get_json()
    if token not in dados:
        dados[token] = {}
    dados[token]["lucro"]      = body.get("lucro", 0)
    dados[token]["status"]     = body.get("status", "aguardando")
    dados[token]["adx"]        = body.get("adx", 0)
    dados[token]["rsi"]        = body.get("rsi", 0)
    dados[token]["atr"]        = body.get("atr", 0)
    dados[token]["atualizado"] = datetime.now().strftime("%H:%M:%S")
    if "comando" not in dados[token]:
        dados[token]["comando"] = "livre"
    salvar_dados(dados)
    return jsonify({"ok": True})

@app.route("/comando/<token>/<acao>", methods=["POST"])
def comando(token, acao):
    dados = carregar_dados()
    if token not in dados:
        dados[token] = {}
    dados[token]["comando"] = acao
    salvar_dados(dados)
    from flask import redirect
    return redirect("/painel/" + token)

@app.route("/painel/<token>")
def painel(token):
    dados = carregar_dados()
    u = dados.get(token, {})
    lucro     = u.get("lucro", 0)
    status    = u.get("status", "---")
    adx       = u.get("adx", 0)
    rsi       = u.get("rsi", 0)
    atr       = u.get("atr", 0)
    atualizado= u.get("atualizado", "---")
    comando   = u.get("comando", "livre")
    cor_lucro = "#00c864" if lucro >= 0 else "#dc3c3c"
    cor_cmd   = "#00c864" if comando == "livre" else "#dc3c3c"
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta http-equiv="refresh" content="10">
      <title>BullRunnPrime</title>
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: #14141e; color: white; font-family: 'Segoe UI', sans-serif; padding: 20px; }}
        h1 {{ text-align: center; color: #b4c8ff; font-size: 1.3em; margin-bottom: 20px; letter-spacing: 2px; }}
        .card {{ background: #1e1e2e; border-radius: 12px; padding: 16px; margin-bottom: 12px; border: 1px solid #3c5090; }}
        .row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #2a2a3e; }}
        .row:last-child {{ border-bottom: none; }}
        .label {{ color: #8ca0c8; font-size: 0.9em; }}
        .value {{ font-weight: bold; font-size: 0.9em; }}
        .btn {{ width: 100%; padding: 16px; border: none; border-radius: 12px; font-size: 1.1em; font-weight: bold; cursor: pointer; margin-top: 10px; }}
        .btn-parar {{ background: #dc3c3c; color: white; }}
        .btn-liberar {{ background: #00c864; color: white; }}
        .atualizado {{ text-align: center; color: #506080; font-size: 0.75em; margin-top: 16px; }}
      </style>
    </head>
    <body>
      <h1>🤖 BULLRUNN PRIME</h1>
      <div class="card">
        <div class="row"><span class="label">Status</span><span class="value">{status.upper()}</span></div>
        <div class="row"><span class="label">Lucro do dia</span><span class="value" style="color:{cor_lucro}">R$ {lucro:.2f}</span></div>
        <div class="row"><span class="label">ADX</span><span class="value">{adx:.1f}</span></div>
        <div class="row"><span class="label">RSI</span><span class="value">{rsi:.1f}</span></div>
        <div class="row"><span class="label">ATR</span><span class="value">{atr:.1f}</span></div>
        <div class="row"><span class="label">Comando atual</span><span class="value" style="color:{cor_cmd}">{comando.upper()}</span></div>
      </div>
      <form method="post" action="/comando/{token}/parar">
        <button class="btn btn-parar">⛔ PARAR E FECHAR POSIÇÃO</button>
      </form>
      <form method="post" action="/comando/{token}/livre">
        <button class="btn btn-liberar" style="margin-top:10px">✅ LIBERAR PARA OPERAR</button>
      </form>
      <p class="atualizado">Atualizado às {atualizado} · Página recarrega a cada 10s</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

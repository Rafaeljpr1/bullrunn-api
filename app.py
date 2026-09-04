from flask import Flask, request, jsonify, redirect
from datetime import datetime
import json, os

app = Flask(__name__)
DADOS_FILE = "dados.json"

LOGO_B64 = "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"

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
    return redirect(f"/painel/{token}")

@app.route("/painel/<token>")
def painel(token):
    dados = carregar_dados()
    u = dados.get(token, {})
    lucro      = u.get("lucro", 0)
    status     = u.get("status", "---")
    adx        = u.get("adx", 0)
    rsi        = u.get("rsi", 0)
    atr        = u.get("atr", 0)
    atualizado = u.get("atualizado", "---")
    comando    = u.get("comando", "livre")

    cor_lucro = "#00c864" if lucro >= 0 else "#dc3c3c"
    cor_cmd   = "#00c864" if comando == "livre" else "#dc3c3c"

    status_map = {
        "comprado":       ("#00c864", "COMPRADO"),
        "vendido":        ("#dc3c3c", "VENDIDO"),
        "aguardando":     ("#f0c800", "AGUARDANDO"),
        "aguard_ignicao": ("#ff5050", "AGUARD. IGNICAO"),
        "ignicao_ativa":  ("#ff5050", "IGNICAO ATIVA"),
        "encerrado":      ("#888888", "ENCERRADO"),
    }
    cor_status, status_txt = status_map.get(status, ("#ffffff", status.upper()))

    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <meta http-equiv="refresh" content="10">
      <title>BullRunn Prime</title>
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: #0a0a12; color: white; font-family: 'Segoe UI', sans-serif; padding: 20px; }}
        .logo-container {{
          display: flex; flex-direction: column; align-items: center;
          margin-bottom: 18px;
        }}
        .logo-container img {{
          height: 90px; width: auto; border-radius: 50%;
          border: 2px solid #c9a84c;
          box-shadow: 0 0 18px rgba(201,168,76,0.4);
          margin-bottom: 8px;
        }}
        .logo-title {{
          color: #c9a84c; font-size: 1.1em; font-weight: bold;
          letter-spacing: 3px; text-transform: uppercase;
        }}
        .logo-sub {{
          color: #7a6030; font-size: 0.65em; letter-spacing: 2px;
          margin-top: 2px;
        }}
        .card {{
          background: #1a1a28; border-radius: 12px; padding: 16px;
          margin-bottom: 12px; border: 1px solid #3a3060;
        }}
        .row {{
          display: flex; justify-content: space-between;
          padding: 8px 0; border-bottom: 1px solid #242438;
        }}
        .row:last-child {{ border-bottom: none; }}
        .label {{ color: #8888aa; font-size: 0.85em; }}
        .value {{ font-weight: bold; font-size: 0.85em; }}
        .btn {{
          width: 100%; padding: 16px; border: none; border-radius: 12px;
          font-size: 1em; font-weight: bold; cursor: pointer; margin-top: 10px;
          letter-spacing: 1px;
        }}
        .btn-parar {{ background: #dc3c3c; color: white; }}
        .btn-liberar {{ background: #00a854; color: white; }}
        .footer {{
          text-align: center; color: #3a3060; font-size: 0.7em;
          margin-top: 18px;
        }}
      </style>
    </head>
    <body>
      <div class="logo-container">
        <img src="data:image/jpeg;base64,{LOGO_B64}" alt="BullRunn Logo">
        <div class="logo-title">BullRunn Prime</div>
        <div class="logo-sub">ESTRATEGIA &bull; TECNOLOGIA &bull; RESULTADOS</div>
      </div>
      <div class="card">
        <div class="row">
          <span class="label">Status</span>
          <span class="value" style="color:{cor_status}">{status_txt}</span>
        </div>
        <div class="row">
          <span class="label">Lucro do dia</span>
          <span class="value" style="color:{cor_lucro}">R$ {lucro:.2f}</span>
        </div>
        <div class="row">
          <span class="label">ADX</span>
          <span class="value">{adx:.1f}</span>
        </div>
        <div class="row">
          <span class="label">RSI</span>
          <span class="value">{rsi:.1f}</span>
        </div>
        <div class="row">
          <span class="label">ATR</span>
          <span class="value">{atr:.1f}</span>
        </div>
        <div class="row">
          <span class="label">Controle remoto</span>
          <span class="value" style="color:{cor_cmd}">{comando.upper()}</span>
        </div>
      </div>
      <form method="post" action="/comando/{token}/parar">
        <button class="btn btn-parar">PARAR E FECHAR POSICAO</button>
      </form>
      <form method="post" action="/comando/{token}/livre">
        <button class="btn btn-liberar">LIBERAR PARA OPERAR</button>
      </form>
      <p class="footer">Atualizado as {atualizado} &bull; Recarrega a cada 10s &bull; v2.0.9</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

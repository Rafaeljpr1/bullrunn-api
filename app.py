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
          height: 110px; width: auto; border-radius: 50%;
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

import asyncio
import json
import random
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

dashboard_state = {
    "total_pnl_percent": 12.0,
    "total_pnl_inr": 24780.00,
    "trades_24h": [
        {"symbol": "BTC/INR", "type": "Buy", "time": "09:45 AM", "price": 5432100, "pnl": 6518.52, "status": "green"},
        {"symbol": "ETH/INR", "type": "Sell", "time": "08:15 AM", "price": 298450, "pnl": -4320.10, "status": "red"},
        {"symbol": "SOL/INR", "type": "Buy", "time": "08:15 AM", "price": 10800, "pnl": 1240.30, "status": "green"}
    ],
    "active_trades": [
        {"symbol": "BTC/INR", "side": "Long", "size": "0.10 BTC", "entry": 5410000, "current": 5432100, "pnl": 2210.00},
        {"symbol": "ETH/INR", "side": "Long", "size": "2.0 ETH", "entry": 296800, "current": 298450, "pnl": 3300.00}
    ]
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Trading Terminal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0b0e14; font-family: sans-serif; color: #e2e8f0; }
        .neon-glow-green { box-shadow: 0 0 15px rgba(34, 197, 94, 0.25); border: 1px solid rgba(34, 197, 94, 0.4); }
        .card-bg { background: #131722; border: 1px solid #1e232d; }
    </style>
</head>
<body class="flex justify-center items-center min-h-screen p-2 sm:p-4">
    <div class="w-full max-w-md card-bg rounded-3xl p-5 flex flex-col justify-between h-[840px] shadow-2xl relative overflow-hidden">
        <div>
            <div class="flex justify-between items-center mb-5">
                <div>
                    <span class="text-xs text-gray-400 font-medium">Quantum Terminal</span>
                    <h2 class="text-lg font-bold text-white">Hi, Trader</h2>
                </div>
                <button class="p-2 rounded-full bg-slate-800 text-gray-300">⚙️</button>
            </div>
            <div class="neon-glow-green bg-gradient-to-r from-emerald-950/40 to-slate-900 rounded-2xl p-5 mb-5 flex justify-between items-center">
                <div>
                    <span class="text-xs text-emerald-400 font-semibold tracking-wide uppercase">Total P&L</span>
                    <div class="text-2xl font-black text-emerald-400 mt-1" id="pnl-header">+12% (₹24,780)</div>
                </div>
                <div class="bg-emerald-500/20 text-emerald-400 p-2.5 rounded-full text-lg font-bold">↗</div>
            </div>
            <div class="mb-5">
                <div class="flex justify-between items-center mb-3">
                    <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Trade History (24h)</span>
                    <span class="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded">Auto-Clean Active</span>
                </div>
                <div id="trade-history" class="space-y-2.5 max-h-[220px] overflow-y-auto pr-1"></div>
            </div>
            <div>
                <span class="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-3">Active Live Trades</span>
                <div id="active-trades" class="space-y-2.5"></div>
            </div>
        </div>
        <div class="bg-slate-900/90 backdrop-blur border-t border-slate-800 -mx-5 -mb-5 p-3 flex justify-around items-center">
            <button class="flex flex-col items-center text-emerald-400"><span class="text-base">🏠</span><span class="text-[10px] font-bold">Home</span></button>
            <button class="flex flex-col items-center text-gray-500"><span class="text-base">📊</span><span class="text-[10px]">Markets</span></button>
            <button class="flex flex-col items-center text-gray-500"><span class="text-base">💼</span><span class="text-[10px]">Capital</span></button>
            <button class="flex flex-col items-center text-gray-500"><span class="text-base">⚡</span><span class="text-[10px]">Strategy</span></button>
            <button class="flex flex-col items-center text-gray-500"><span class="text-base">🚨</span><span class="text-[10px]">System</span></button>
        </div>
    </div>
    <script>
        const ws = new WebSocket(`ws://${location.host}/ws`);
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            document.getElementById('pnl-header').innerText = `+${data.total_pnl_percent.toFixed(1)}% (₹${data.total_pnl_inr.toLocaleString('en-IN')})`;
            
            document.getElementById('trade-history').innerHTML = data.trades_24h.map(t => `
                <div class="card-bg rounded-xl p-3 flex justify-between items-center border-l-4 ${t.status === 'green' ? 'border-l-emerald-500' : 'border-l-rose-500'}">
                    <div>
                        <div class="text-sm font-bold text-white">${t.symbol} <span class="text-xs font-normal ${t.type === 'Buy' ? 'text-emerald-400' : 'text-rose-400'}">${t.type}</span></div>
                        <div class="text-[11px] text-gray-500">${t.time} @ ₹${t.price.toLocaleString('en-IN')}</div>
                    </div>
                    <div class="text-sm font-extrabold ${t.pnl >= 0 ? 'text-emerald-400' : 'text-rose-400'}">${t.pnl >= 0 ? '+' : ''}₹${t.pnl.toLocaleString('en-IN')}</div>
                </div>
            `).join('');

            document.getElementById('active-trades').innerHTML = data.active_trades.map(a => `
                <div class="card-bg rounded-xl p-3 border border-slate-800">
                    <div class="flex justify-between items-center mb-1.5">
                        <span class="text-sm font-bold text-white">${a.symbol} <span class="text-xs text-emerald-400 bg-emerald-950 px-1.5 py-0.5 rounded">${a.side}</span></span>
                        <span class="text-[11px] bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded-full font-bold">● Live</span>
                    </div>
                    <div class="flex justify-between text-[11px] text-gray-400">
                        <span>Size: ${a.size}</span>
                        <span>Entry: ₹${a.entry.toLocaleString('en-IN')}</span>
                        <span class="text-emerald-400 font-bold">P&L: +₹${a.pnl.toLocaleString('en-IN')}</span>
                    </div>
                </div>
            `).join('');
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def get_dashboard():
    return HTMLResponse(content=HTML_TEMPLATE)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            for trade in dashboard_state["active_trades"]:
                delta = random.randint(-200, 300)
                trade["current"] += delta
                trade["pnl"] += delta * 0.1
            await websocket.send_text(json.dumps(dashboard_state))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
      

# app/websockets.py
from fastapi import WebSocket
from typing import Dict, List
import json
from datetime import datetime
import pytz

COLOMBIA_TZ = pytz.timezone('America/Bogota')

class ConnectionManager:
    def __init__(self):
        # bar_id → lista de websockets activos
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, bar_id: int):
        await websocket.accept()
        if bar_id not in self.active_connections:
            self.active_connections[bar_id] = []
        self.active_connections[bar_id].append(websocket)

    def disconnect(self, websocket: WebSocket, bar_id: int):
        if bar_id in self.active_connections:
            self.active_connections[bar_id] = [
                conn for conn in self.active_connections[bar_id] if conn != websocket
            ]
            if not self.active_connections[bar_id]:
                del self.active_connections[bar_id]

    async def broadcast(self, message: dict, bar_id: int):
        if bar_id not in self.active_connections:
            return
        dead_connections = []
        for connection in self.active_connections[bar_id]:
            try:
                await connection.send_text(json.dumps(message, default=str))
            except Exception:
                dead_connections.append(connection)
        # Limpiar conexiones muertas
        for conn in dead_connections:
            self.active_connections[bar_id].remove(conn)

# Instancia global
manager = ConnectionManager()

# === FUNCIÓN HELPER PRO (esto es lo que hace todo fácil) ===
async def notify_bar(bar_id: int, event_type: str, data: dict = None):
    """
    Envía una notificación en tiempo real a todos los conectados al bar.
    
    Uso:
        await notify_bar(bar_id=5, event_type="nueva_factura", data={...})
    """
    if data is None:
        data = {}
    
    message = {
        "type": event_type,
        "data": data,
        "timestamp": datetime.now(COLOMBIA_TZ).isoformat()
    }
    
    await manager.broadcast(message, bar_id=bar_id)
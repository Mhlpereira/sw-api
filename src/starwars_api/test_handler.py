import os
import redis
import socket

def lambda_handler(event, context):
    redis_url = os.getenv("REDIS_URL", "redis://172.31.82.138:6379")
    
    # Extrai host e porta da URL
    host = redis_url.split("://")[1].split(":")[0]
    port = int(redis_url.split(":")[-1].replace("/0", ""))
    
    try:
        # Teste 1: Conexão TCP pura
        with socket.create_connection((host, port), timeout=5) as s:
            s.send(b"PING\r\n")
            response = s.recv(1024)
            tcp_ok = b"PONG" in response
        
        # Teste 2: Cliente Redis
        r = redis.Redis.from_url(redis_url, socket_timeout=5)
        redis_ok = r.ping()
        
        return {
            "tcp_test": "success" if tcp_ok else "fail",
            "redis_test": "success" if redis_ok else "fail",
            "host_port": f"{host}:{port}"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "type": type(e).__name__,
            "host_port": f"{host}:{port}"
        }
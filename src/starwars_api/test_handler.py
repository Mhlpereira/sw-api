import socket

def lambda_handler(event, context):
    try:
        with socket.create_connection(('172.31.82.138', 6379), timeout=5):
            return {"status": "TCP connection OK"}
    except Exception as e:
        return {"error": str(e)}
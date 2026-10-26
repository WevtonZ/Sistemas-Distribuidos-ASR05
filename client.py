from socket  import *
from constCS import CLIENT_HOST, PORT #-
import json

def execute(data, operations):
    client_socket = socket(AF_INET, SOCK_STREAM)

    try:
        client_socket.connect((CLIENT_HOST, PORT))

        payload = {
            "dados": data,
            "operacoes": operations
        }

        client_socket.sendall(json.dumps(payload).encode("utf-8"))
        resposta_bytes = client_socket.recv(4096)
        if resposta_bytes:
            return json.loads(resposta_bytes.decode("utf-8"))
        else:
            print("n tem dados no servidor")
            return None
    except Exception as e:
        print(f"deu o erro {e}")
        return None
    finally:
        client_socket.close()


if __name__ == "__main__":
    data = [10, 20, 30, 30, 45, 50] # dados
    # essas sao todas as operacoes que sao validas no servidor.
    operations = [
        "soma",
        "desvio_padrao_variancia",
        "z_score",
        "converter_base"
    ]

    ans = execute(data, operations)
    print(json.dumps(ans, indent=4, ensure_ascii=False))
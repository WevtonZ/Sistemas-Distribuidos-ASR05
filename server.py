from socket  import *
from constCS import SERVER_HOST, PORT
import json, statistics

"""
	pelo visto eh 3 dessas aspas duplas

	o que eu tenho eh um negócio pra fazer operações em números inteiros. Decidi olhar alguma
	biblioteca pra ver o que eu poderia usar e achei essa statistics. além disso vou usar essas
	atividades pra aprender a usar json já que é o padrão para as coisas da industria.

	ok o que a gente tem como operações é:
	
	1. soma -> retorna a soma de todos os valores do vetor.
	2. desvio_padrao_variancia -> calcula a variancia e desvio padrão do vetor.
	3. z_score -> padroniza os valores do vetor calculando o desvio padrão em relação à média.
	4. converter_base -> converte os valores do vetor para outra base

	eu escolhi um monte de operação aleatória pra atividade.

	demorei um dia inteiro pra conseguir fazer esse negocio pq toda hora dava erro no socket, erro nas conta
	erro nos if, erro no erro, sou um pessimo programador
"""

def processar(req):
	data = req.get('dados', [])
	op = req.get('operacoes', [])

	resultados = {}
	# print(data)

	if not data:
		return {"status": "erro", "mensagem": 'nao tem dados pra processar'}

	for o in op:
		if o == "soma":
			resultados["soma"] = sum(data) # só soma tudo

		elif o == "desvio_padrao_variancia":
			if len(data) > 1:
				x = statistics.pvariance(data)
				y = statistics.pstdev(data)

				resultados["desvio_padrao_variancia"] = {
					"variancia": round(x, 4),
					"desvio_padrao": round(y, 4)
				}
			else:
				resultados["desvio_padrao_variancia"] = "pelos menos dois numeros"

		elif o == "z_score":
			if len(data) > 1:
				media = statistics.mean(data)
				stdev = statistics.stdev(data)

				if stdev != 0:
					z_scores = [round((x-media)/stdev, 4) for x in data]
					resultados["z_score"] = z_scores
				else:
					resultados["z_score"] = "desvio padrao = 0"
			else:
				resultados["z_score"] = "pelo menos dois numeros"

		elif o == "converter_base":
			# só entra se o valor for inteiro ou float que pode ser convertido pra inteiro
			inteiros = []
			for x in data:
				if isinstance(x, (int, float)) and float(x).is_integer():
					inteiros.append(int(x))

			resultados["converter_base"] = {
				str(x): {
					"binario": bin(x),
					"hexadecimal": hex(x)
				} for x in inteiros
			}
		else:
			resultados[o] = "digita algo que ta no conjunto de operacoes"

	return {"status": "sucesso", "resultados": resultados}
		

def init_server():
	server_socket = socket(AF_INET, SOCK_STREAM)
	server_socket.bind((SERVER_HOST, PORT))
	server_socket.listen(5)
	try:
		while True:
			conn, addr = server_socket.accept() # esperar alguem aceitar a conexao
			try:
				data = conn.recv(4096)
				if data:
					req = json.loads(data.decode('utf-8'))
					res = processar(req)

					conn.sendall(json.dumps(res).encode('utf-8'))
					
			except Exception as e:
				print(f"Erro ao processar requisição {e}")
			finally:
				conn.close() # fechar a conexao
	except KeyboardInterrupt:
		print("encerrando servidor com ctrel+C")
	finally:
		server_socket.close()
		print("\nFechando socket e liberando porta")

if __name__ == '__main__':
	init_server()
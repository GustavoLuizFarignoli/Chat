import socket
import threading

SERVIDOR = input('Digite o IP do servidor: ')
PORTA = int(input('Digite a porta: '))

usuario = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Criamos o socket TCP
try:
    nickname = input('Informe seu nome: ') # Usuário escolhe seu apelido
    usuario.connect((SERVIDOR, PORTA)) # Faz a conexão com o servidor
    print(f'Conexão feita com perfeição: {SERVIDOR}:{PORTA}') 
except:
    print('ERRO!!!') # avisando caso tenha dado erro na conexão

def recMensagem(): # está fução é responsável por receber as mensagens que o servidor mandou
    while True: 
        try:
            menssagem = usuario.recv(2048).decode('utf-8')
            if menssagem =='getUser':
                usuario.send(nickname.encode('utf-8'))
            else:
                print(menssagem)
        except:
            print('ERRO!!')

def mandaMensagem(): # está função é responsável por enviar a mensagem para o servidor que ira mandar para os outros usuários
    while True:
        usuario.send(input('').encode('utf-8'))


thread1 = threading.Thread(target=recMensagem,args=())
thread2 = threading.Thread(target=mandaMensagem,args=())

thread1.start()
thread2.start()

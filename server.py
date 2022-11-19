import socket
import threading

HOST = (input('Digite o host: ')) 
PORTA = int(input('Digite a porta: ')) 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # criamos o socket TCP
sock.bind((HOST, PORTA)) # fizemos bind do servidor
sock.listen() # o servidor entrou em modo de escuta
print(f"Servidor está vivo em {HOST}:{PORTA}")

usuarios = [] #lista com todos os usuários conectados e seus ips e portas
nicknames = [] #lista que contém o nickname que os usuários escolhem quando entram no chat
# ao invés de fazer um dicionário estamos fazendo duas listas e cruzamos ela quando precisamos, como adicionamos em ambas as listas ao mesmo tempo podemos cruzamos os indices iguais

def broadcast(message): # como o metodo TCP não possui broadcast essa função funciona atráves de diversos unicasts, ou seja percorro todos os usuários e mando mensagem para ele
    for usuario in usuarios:
        usuario.send(message)

def msgCliente(usuario): # este metódo fica esperando para ver se o usuário mandou alguma mensagem
    while True:
        try:
            recebeMsgUsuario = usuario.recv(2048).decode('utf-8')
            broadcast(f'{nicknames[usuarios.index(usuario)]}: {recebeMsgUsuario}'.encode('utf-8'))
        except:
            usuarioSaiu = usuarios.index(usuario) # pegamos o ip do usuário que saiu
            usuario.close() # fechamos a conexão do qual o ip é igual ao ip do usuário que saiu
            usuarios.remove(usuarios[usuarioSaiu]) # removes o usuário que saiu da lista dos usuários conectados
            usuarioSaiuNickname = nicknames[usuarioSaiu] 
            print(f'{usuarioSaiuNickname} Saiu do chat...') # printamos no servidor que o usuário saiu
            broadcast(f'{usuarioSaiuNickname} Nos abandonou...'.encode('utf-8')) # avisamos a todos os usuários que alguém saiu do chat
            nicknames.remove(usuarioSaiuNickname) # depois de termos printado podemos remover o nickname das arrays também
            break

def iniciarConexao():
    while True:
        try:
            usuario, addr = sock.accept()
            print(f'Conexão feita: {str(addr)}')
            usuarios.append(usuario) # Aqui colocamos as informações da conexão na lista usuários
            usuario.send('getUser'.encode('utf-8')) # Aqui é quando pedimos para o usuário escolher o seu apelido, estamos decodificando em ascii
            nickname = usuario.recv(2048).decode('utf-8') # Aqui recebemos o nome do usuário e decodificamos ele com um buffer total é de 2048 bytes, estamos decodificando em ascii
            nicknames.append(nickname) # Aqui colocamos o apelido recebido na lista de apelidos
            broadcast(f'{nickname} Acabou de entrar no chat!'.encode('utf-8')) # chamamos o metodo de broadcast para avisar a todos os usuários que alguém entrou
            user_thead = threading.Thread(target=msgCliente,args=(usuario,))
            user_thead.start() #criamos uma thread para ficar ouvindo este cliete que acabou de se conectar
        except:
            pass
    

iniciarConexao() # começamos o código para inciar a criar conexões



        
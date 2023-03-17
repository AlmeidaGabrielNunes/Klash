# -*- coding: cp1252 -*-

## Cabeçalho de Importação
import pygame
import pygame._view
import socket
import inputbox
import sys
import time
import random
import os
import py2exe
from pygame.locals import *

## Classes
largura_texto = 0
PORT = 0
pag = 0
manual_a = pygame.image.load("data/manual1.png")
manual_b = pygame.image.load("data/manual2.png")

historias_personagens = [pygame.image.load("data/hist_" + str(x) + ".png") for x in range (5)]

reada = pygame.image.load("data/reada.png")
readb = pygame.image.load("data/readb.png")
readc = pygame.image.load("data/readc.png")
reada_fim = pygame.image.load("data/reada_fim.png")
readb_fim = pygame.image.load("data/readb_fim.png")

tipos_nomes = ["" for x in range (3)]
tipos_imagem = [pygame.image.load("data/icon-espada.png") for x in range (3)]

tipos_nomes[0] = "Força"
tipos_nomes[1] = "Habilidade"
tipos_nomes[2] = "Magia"

derrota = pygame.image.load("data/derrota.png")




class seletor:
    img = pygame.image.load("data/seletor.png")
    img.set_colorkey((0,0,0))
    x = 480
    y = 500
    y_max = 600
    y_min = 500

    def move(self):
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            if self.y<self.y_max:
                pygame.mixer.Sound.play(som)
                self.y += 50                
        if key[pygame.K_UP] :
            if self.y>self.y_min:
                pygame.mixer.Sound.play(som)
                self.y -= 50
                


    def blit(self):
        screen.blit(self.img, (self.x, self.y))


class avatar:
    vida = 20
    tipo = 0
    ataque = 1
    defesa = 1
    nome = ""
    imagem = pygame.image.load("data/logo-b.png")
    nome_golpes = ["" for x in range (3)]
    descricao_golpes = ["" for x in range (3)]
    efeito_golpes = ["" for x in range (3)]
    custo_golpes =  ["" for x in range (3)]
    recursos =   [0 for x in range (3)]
    



class adversario:
    vida = 20
    nome = ""
    imagem = pygame.image.load("data/logo-b.png")
    nome_golpes = ["" for x in range (3)]
    golpes = [0 for x in range(3)]
    

fullscreen = False
apertou = False
op_desafio = ''


## FUNÇÕES

mini_console = ""

def handling():
    global running, tela, tipo_socket, tipo_conexao, personagem, personagem_escolhido, turno, pegar_recursos, pag, jogardenovo, resp_again, apertou
    global golpe_selecionado, fullscreen
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            key = pygame.key.get_pressed()
            if tela==0:
                seletor_menu.move()
            elif tela ==2:
                seletor_conexao.move()
            elif tela==4:
                seletor_personagem.move()
            elif tela==5:
                seletor_golpe.move()
            elif tela==6 or tela==7:
                seletor_partida.move()

            if (key[pygame.K_LALT] or key[pygame.K_RALT]) and key[pygame.K_RETURN]:
                if (fullscreen):
                    pygame.display.set_mode((1280,720))
                    fullscreen = False
                else:
                    pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
                    fullscreen = True
            elif key[pygame.K_BACKSPACE]:
                if tela==1:
                    tela=0
            elif key[pygame.K_SPACE] or key[pygame.K_RETURN]:
                if tela==0:
                    if seletor_menu.y == 600:
                        running = False
                    elif seletor_menu.y == 550:
                        tela = 1
                        pag = 0
                    elif seletor_menu.y == 500:
                        tela = 2
                elif tela == 2:
                    if seletor_conexao.y == 600:
                        tela = 0
                        seletor_conexao.y = 450
                    elif seletor_conexao.y == 500:
                        tipo_conexao = 1
                        turno = False
                        tela = 3
                    elif seletor_conexao.y == 550:
                        tipo_conexao = 0
                        turno = True
                        pegar_recursos = True
                        tela = 3
                elif tela == 3:
                    tela = 4
                elif tela==4:
                    if seletor_personagem.y == 70:
                        personagem = 1
                    elif seletor_personagem.y == 120:
                        personagem = 2
                    elif seletor_personagem.y == 170:
                        personagem = 3
                    elif seletor_personagem.y == 220:
                        personagem = 4
                    elif seletor_personagem.y == 270:
                        personagem = 5
                    personagem_escolhido = True
                elif tela == 5:
                    golpe_selecionado = True
                    if(seletor_golpe.y <> 450):
                        pygame.mixer.Sound.play(atk_som)
                elif tela ==6 or tela ==7:
                    if seletor_partida.y == 400: 
                        jogardenovo = 's'
                    elif seletor_partida.y == 450:
                        jogardenovo = 'n'
                    resp_again = True
            elif key[pygame.K_LEFT]:
                if tela == 1:
                    if pag> -6:
                        pag = pag-1
            elif key[pygame.K_RIGHT]:
                if tela == 1:
                    if pag< 2:
                        pag = pag+1
            if key[pygame.K_LEFT] or key[pygame.K_RIGHT]:
                if tela == 2:
                    if seletor_conexao.y == 450:
                        if tipo_socket=="UDP":
                            tipo_socket = "TCP"
                        else:
                            tipo_socket = "UDP"
            if key[pygame.K_ESCAPE] or (key[pygame.K_LALT] and key[pygame.K_F4]) :
                running = False


def texto(pilha, tamanho, cor, x, y, fonte=None):
    font = pygame.font.SysFont(fonte, tamanho)
    tex = font.render(pilha, 1, cor)
    
    
    screen.blit(tex, (x,y))


def texto_centralizado(pilha, tamanho, cor, x, y, fonte=None):
    font = pygame.font.SysFont(fonte, tamanho)
    tex = font.render(pilha, 1, cor)
    largura = font.size(pilha)[0]
    
    screen.blit(tex, (640-largura/2,y))



def criar_sockets(protocolo, tipo_conexao):
        global emissor_udp, receptor_udp, emissor_tcp, receptor_tcp, HOST, PORT, background, kx, con
        if(protocolo == "UDP"):

            emissor_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            receptor_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        
            if (tipo_conexao == 0): ##SERVIDOR
               
                ip_servidor = socket.gethostbyname(socket.gethostname())

                HOST = ''
                if (PORT == 0):
                    PORT=int(inputbox.ask(screen, 'Porta desejada (0 é aleatória)'))
                if (PORT == 0):
                    PORT = random.randint(1024,49150)
                    
                receptor_udp.bind(('', PORT))


                

                texto("SEU IP E PORTA:", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 500)
                texto(ip_servidor + ':' + str(PORT), 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 550)
                
                pygame.display.flip()
                handling()
                

                

            elif (tipo_conexao == 1): ## CLIENTE

                HOST = inputbox.ask(screen, 'Servidor')
                PORT = inputbox.ask(screen, 'Porta')
                
                

                
                receptor_udp.bind(('', int(PORT)+1))
               
                



                                




def conectar(protocolo, tipo_conexao, mensagem):
    global emissor_udp, receptor_udp, emissor_tcp, receptor_tcp, HOST, PORT, cliente, kx, con
    msg= "raw"
    if(protocolo=="UDP"):
        if(tipo_conexao==1):
            while(msg=="raw"):
                emissor_udp.sendto(str(mensagem), (HOST, int(PORT)))               
                msg, kx = receptor_udp.recvfrom(1024)
                


                        
                    
        elif(tipo_conexao==0):
            
            while(msg=="raw"):
                
                msg, cliente = receptor_udp.recvfrom(1024)
                
            emissor_udp.sendto(str(mensagem),(cliente[0], PORT+1))


    return msg;
                        
    
    


## Inicialização
pygame.init()
pygame.mixer.init()

running = True
font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()
pygame.mixer.music.load("data/mfBGM1.mid")
#pygame.mixer.music.play()
som = pygame.mixer.Sound("data/Effect11.wav")
atk_som = pygame.mixer.Sound("data/ataque.wav")

tipo_socket = "UDP"
dados_preenchidos = False
conexao_feita = False
personagem_escolhido = False
jogador = [0]*20
oponente = [0]*20
recursos = [0]*3
paralisado = False
primeira_conexao = True
## MULTIMIDIA

turnbox_player = pygame.image.load("data/turn_pl.png")
turnbox_oponente = pygame.image.load("data/turn_op.png")

musica_char = True






## BANCO DE DADOS - PERSONAGENS

tipos = [0 for x in range(10)]
nomes = [" " for x in range (5)]
nome_golpes = [["" for x in range (4)] for x in range (10)]
descricao_golpes = [["" for x in range (4)] for x in range (10)]
efeito_golpes = [["" for x in range (4)] for x in range (10)]
custo_golpes = [["" for x in range (4)] for x in range (10)]


imagens_personagens = [pygame.image.load("data/logo-b.png")]*5










#Aléxia, a Arqueira Dourada

nomes[0] = "Aléxia"
imagens_personagens[0] = pygame.image.load("data/alexia.png")
tipos[0] = 1

nome_golpes[0][0] = "Chuva de Flechas"
descricao_golpes [0][0] = "Dispara várias flechas causando 2 de dano físico."
custo_golpes[0][0] = "010"
efeito_golpes [0][0] = "02"

nome_golpes[0][1] = "Flecha Congelate"
descricao_golpes [0][1] = "Deixa o adversário paralisado por uma rodada."
custo_golpes[0][1] = "001"
efeito_golpes [0][1] = "60"

nome_golpes[0][2] = "Oração do Sol"
descricao_golpes [0][2] = " Aléxia recebe proteção de Apolo e recebe mais 2 de defesa."
custo_golpes[0][2] = "121"
efeito_golpes [0][2] = "12"

nome_golpes[0][3] = "Benção do Sol"
descricao_golpes [0][3] = " Aléxia recebe 3 recursos aleatórios"
custo_golpes[0][3] = "001"
efeito_golpes [0][3] = "73"

#Runab, a Assassina

nomes[1] = "Runab"
imagens_personagens[1] = pygame.image.load("data/runab.png")
tipos[1] = 1

nome_golpes[1][0] = "Ataque com Adaga"
descricao_golpes [1][0] = "Desfere 2 golpes físicos, causando 3 de dano."
custo_golpes[1][0] = "110"
efeito_golpes [1][0] = "02"

nome_golpes[1][1] = "Apunhalar"
descricao_golpes [1][1] = "Runab aparece atrás da personagem e faz um ataque com adaga mais poderoso. Causa 4 de dano."
custo_golpes[1][1] = "120"
efeito_golpes [1][1] = "04"

nome_golpes[1][2] = "Veneno"
descricao_golpes [1][2] = "Diminui em 4 pontos a defesa do adversário."
custo_golpes[1][2] = "122"
efeito_golpes [1][2] = "44"

nome_golpes[1][3] = "Descanso"
descricao_golpes [1][3] = "Runab se esonde da batalha e recupera 2 de vida."
custo_golpes[1][3] = "011"
efeito_golpes [1][3] = "32"

#Roran, o Dragoniano

nomes[2] = "Roran"
imagens_personagens[2] = pygame.image.load("data/roran.png")
tipos[2] = 0

nome_golpes[2][0] = "Investida"
descricao_golpes [2][0] = "Desfere uma sequencia de golpes em alta velocidade causando 3 de dano."
custo_golpes[2][0] = "200"
efeito_golpes [2][0] = "03"

nome_golpes[2][1] = "Divindade Dragoniana"
descricao_golpes [2][1] = "Aumenta um recurso aleatório em 5."
custo_golpes[2][1] = "200"
efeito_golpes [2][1] = "75"

nome_golpes[2][2] = "Mutilar"
descricao_golpes [2][2] = "Roran ganha garras de dragão aumento em 5 seu ataque."
custo_golpes[2][2] = "222"
efeito_golpes [2][2] = "25"

nome_golpes[2][3] = "Voar"
descricao_golpes [2][3] = "Roran aumenta sua defesa em 2."
custo_golpes[2][3] = "201"
efeito_golpes [2][3] = "12"

#Ariane, a Espadachim Protetora

nomes[3] = "Ariane"
imagens_personagens[3] = pygame.image.load("data/ariana.png")
tipos[3] = 0

nome_golpes[3][0] = "Aniquilar Fonte"
descricao_golpes [3][0] = "Ariane ataca os pontos de chakra do adversário, diminuindo em 3 um dos recursos do adversário."
custo_golpes[3][0] = "200"
efeito_golpes [3][0] = "83"

nome_golpes[3][1] = "Oração da Lua"
descricao_golpes [3][1] = "Ariane reza para Diana aumentar as marés e deixar sua espada mais forte, aumentando seu ataque em 3."
custo_golpes[3][1] = "211"
efeito_golpes [3][1] = "23"

nome_golpes[3][2] = "Estocada"
descricao_golpes [3][2] = "Ariane avança para cima do adversário com sua espada, causando 5 de dano."
custo_golpes[3][2] = "300"
efeito_golpes [3][2] = "05"

nome_golpes[3][3] = "Maré Pesada"
descricao_golpes [3][3] = "Ariane invoca ondas para deixar o adversário paralisado por uma rodada."
custo_golpes[3][3] = "001"
efeito_golpes [3][3] = "60"

#Kdevil, o Demônio de Fogo

nomes[4] = "Kdevil"
imagens_personagens[4] = pygame.image.load("data/kdevil.png")
tipos[4] = 2

nome_golpes[4][0] = "Chamas da Saúde"
descricao_golpes [4][0] = "Aumenta 3 de vida."
custo_golpes[4][0] = "002"
efeito_golpes [4][0] = "33"

nome_golpes[4][1] = "Bola de Fogo"
descricao_golpes [4][1] = "Lança uma bola de fogo que causa 3 de dano."
custo_golpes[4][1] = "002"
efeito_golpes [4][1] = "03"

nome_golpes[4][2] = "Explosão de Fogo"
descricao_golpes [4][2] = "Gera uma explosão que causa um alto dano de 7 pontos"
custo_golpes[4][2] = "104"
efeito_golpes [4][2] = "07"

nome_golpes[4][3] = "Incendiar"
descricao_golpes [4][3] = "O adversário começa a pegar fogo e tem sua defesa reduzida em 2"
custo_golpes[4][3] = "011"
efeito_golpes [4][3] = "42"




###

###Recursos Golpe
# FORÇA/HABILIDADE/MAGIA
# 0 / 1 / 2

###Golpe
# TIPO/PODER
# 0: Dano
# 1: + Def
# 2: + Atk
# 3: + Vida
# 4: - Def
# 5: - Atk
# 6: Paralisar
# 7: + Recurso
# 8: - Recurso

# Seletores (p/Menus)
seletor_menu = seletor()
seletor_conexao = seletor()
seletor_conexao.y = 500
seletor_conexao.y_min = 500
seletor_personagem = seletor()
seletor_personagem.x = 100
seletor_personagem.y = 70
seletor_personagem.y_min = 70
seletor_personagem.y_max = 270
seletor_golpe = seletor()
seletor_golpe.y = 250
seletor_golpe.img = pygame.image.load("data/seletor_p.png")
seletor_golpe.x = 520
seletor_golpe.y_min = 250
seletor_golpe.y_max = 450
seletor_partida = seletor()
seletor_partida.y  = 400
seletor_partida.y_min = 400
seletor_partida.y_max = 450

# Variáveis de controle booleano

golpe_selecionado = False
golpe_executado = False
testar_golpe = ""



## Tela
window = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Klash")

screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
logo = pygame.image.load("data/logo-b.png")

background = background.convert()
background.fill((0,0,0))
screen.blit(background, (0,0))
pygame.display.flip()
msg = "0"

inicio = True


icone_vida = pygame.image.load("data/icon-coracao.png")
icone_espada = pygame.image.load("data/icon-espada.png")
icone_escudo = pygame.image.load("data/icon-escudo.png")
icone_magia = pygame.image.load("data/icon-estrela.png")
icone_forca = pygame.image.load("data/icon-forca.png")
icone_habilidade = pygame.image.load("data/icon-determ.png")

tipos_imagem[0] = icone_forca
tipos_imagem[1] = icone_habilidade
tipos_imagem[2] = icone_magia

personagem = 0

## Menu

tela = 0


historia_a = pygame.image.load("data/pag-1.png")

## Loop de Jogo
while(running):
    clock.tick(60)
    resp_again = False
    handling()
    
    ### MENU
    if(tela==0) :
        screen.blit(background, (0,0))
        screen.blit(logo, (0,0))
        texto_centralizado("INICIAR!", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 500)
        texto_centralizado("SOBRE", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 550)
        texto_centralizado("SAIR", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 600)
        seletor_menu.blit()
        jogardenovo = ''
        op_desafio = ''

    if (tela==1) :
        
        if(pag==0) :
            screen.blit(background, (0,0))
            texto_centralizado("KLASH", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 100)
            texto_centralizado("---", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 150)
            texto_centralizado("Ana Paula Uehara", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 200)
            texto_centralizado("Gabriel Almeida", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 250)
            texto_centralizado("Hamilton Santos", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 300)
            texto_centralizado("Letícia Custódio", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 350)
            texto_centralizado("Python e PyGame", 30, (255,255,255), (pygame.Surface.get_width(screen)/2), 450)
            texto_centralizado("Música: Kevin MacLeod", 30, (255,255,255), (pygame.Surface.get_width(screen)/2), 480)
            texto_centralizado("Inputbox: Timothy Downs", 30, (255,255,255), (pygame.Surface.get_width(screen)/2), 500)


            screen.blit(readc, (pygame.Surface.get_width(screen)/2 - 243, 660))
            texto_centralizado("Pressione BACKSPACE para voltar", 30, (255,255,255), (pygame.Surface.get_width(screen)/2), 550)

        elif(pag==-1) :
            screen.blit(background, (0,0))
            screen.blit(historia_a, (0,0))
            screen.blit(readb, (pygame.Surface.get_width(screen)/2 - 243, 660))

        elif(pag==1):
            screen.blit(background, (0,0))
            screen.blit(manual_a, (0,0))
            screen.blit(reada, (pygame.Surface.get_width(screen)/2 - 243, 660))

        elif(pag==2):
            screen.blit(background, (0,0))
            screen.blit(manual_b, (0,0))
            screen.blit(reada_fim, (pygame.Surface.get_width(screen)/2 - 243, 660))

        elif(pag<-1):
            screen.blit(background, (0,0))
            screen.blit(imagens_personagens[-pag-2], (0,0))
            texto(nomes[-pag-2], 60, (255,255,255), 450, 15)
            screen.blit(historias_personagens[-pag-2], (450,50))
            texto(tipos_nomes[tipos[-pag-2]], 60, (255,255,255), 90, 615)
            screen.blit(tipos_imagem[tipos[-pag-2]], (5,600))
            if pag == -6:
                screen.blit(readb_fim, (pygame.Surface.get_width(screen)/2 - 243, 660))
            else:
                screen.blit(readb, (pygame.Surface.get_width(screen)/2 - 243, 660))
            
            
                        


    ### MENU DE CONEXÃO
    if(tela==2) :
        screen.blit(background, (0,0))
        screen.blit(logo, (0,0))
        
        texto_centralizado("CLIENTE", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 500)
        texto_centralizado("SERVIDOR", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 550)
        texto_centralizado("VOLTAR", 60, (255,255,255), (pygame.Surface.get_width(screen)/2), 600)
        seletor_conexao.blit()


    ### CRIAÇÃO DE SOCKET
    if(tela==3) :
        screen.blit(background, (0,0))

        criar_sockets(tipo_socket, tipo_conexao)
        inicio = True
        if tipo_conexao == 1:
            tela = 4


        
             


    ### SELEÇÃO DE PERSONAGENS
    if(tela==4) :

        if(musica_char):
            pygame.mixer.music.load("data/char_song.mp3")
            pygame.mixer.music.play(-1)
            musica_char = False

        jogardenovo = ''
        op_desafio = ''
        screen.blit(background, (0,0))
        texto("SELEÇÃO DE PERSONAGENS", 60, (255,255,255), (pygame.Surface.get_width(screen)/2 - 40), 8, "calibri")
        texto("Aléxia, a Arqueira Dourada", 60, (255,255,255), 160, 70)
        texto("Runab, a Assassina", 60, (255,255,255), 160, 120)
        texto("Roran, o Dragoniano", 60, (255,255,255), 160, 170)
        texto("Ariane, a Espadachim Protetora", 60, (255,255,255), 160, 220)
        texto("Kdevil, o Demônio de Fogo", 60, (255,255,255), 160, 270)
        screen.blit(imagens_personagens[seletor_personagem.y/50-1], (870, 150))
        seletor_personagem.blit()
        
        if(personagem_escolhido):
            personagem_adversario = conectar(tipo_socket, tipo_conexao, personagem)            
            pygame.mixer.music.stop()        
            pygame.mixer.music.load("data/battle_song.mp3")
            tela = 5
            



    ### INGAME
    if(tela==5) :
            
            screen.blit(background, (0,0))
            if(inicio):
                pygame.mixer.music.play(-1)
                player = avatar()
                oponente = adversario()
                player.nome = nomes[personagem-1]
                oponente.nome = nomes[int(personagem_adversario)-1]
                player.imagem = imagens_personagens[personagem-1]
                oponente.imagem = imagens_personagens[int(personagem_adversario)-1]
                player.tipo = tipos[personagem-1]
                player.nome_golpes = nome_golpes[personagem-1]
                player.descricao_golpes = descricao_golpes[personagem-1]
                player.custo_golpes = custo_golpes[personagem-1]
                player.efeito_golpes = efeito_golpes[personagem-1]

                
                inicio = False

            texto_centralizado(player.nome + " X " + oponente.nome, 35, (255,255,255), 600, 5)
            screen.blit(player.imagem, (0, 40))
            screen.blit(oponente.imagem, (870, 40))
            screen.blit(icone_vida, (15, 640))
            texto(str(player.vida), 40, (255,255,255), 80, 670)
            screen.blit(icone_espada, (150, 640))
            texto(str(player.ataque), 40, (255,255,255), 195, 670)
            screen.blit(icone_escudo, (230, 640))
            texto(str(player.defesa), 40, (255,255,255), 275, 670)
            screen.blit(icone_vida, (1130, 640))
            texto(str(oponente.vida), 40, (255,255,255), 1195, 670)
            screen.blit(icone_forca, (510, 500))
            texto(str(player.recursos[0]), 40, (255,255,255), 535, 560)
            screen.blit(icone_habilidade, (590, 500))
            texto(str(player.recursos[1]), 40, (255,255,255), 615, 560)
            screen.blit(icone_magia, (670, 500))
            texto(str(player.recursos[2]), 40, (255,255,255), 695, 560)

            if oponente.vida == 0:
                player.vida = -1
                tela = 7

            if player.vida == 0:
                tela = 6
            
            if player.vida > 0:
                
                    
                if(turno):
                    screen.blit(turnbox_player, (565, 50))
                    if(pegar_recursos):
                        player.recursos[player.tipo] += 1
                        player.recursos[random.randint(0,2)] += 1
                        pegar_recursos = False
                    if(paralisado == False):
                        texto(player.nome_golpes[0] + " (" + player.custo_golpes[0][0] + "/" + player.custo_golpes[0][1] + "/" + player.custo_golpes[0][2] + ")", 30, (255, 255, 255), 565, 250)
                        texto(player.nome_golpes[1] + " (" + player.custo_golpes[1][0] + "/" + player.custo_golpes[1][1] + "/" + player.custo_golpes[1][2] + ")", 30, (255, 255, 255), 565, 300)
                        texto(player.nome_golpes[2] + " (" + player.custo_golpes[2][0] + "/" + player.custo_golpes[2][1] + "/" + player.custo_golpes[2][2] + ")", 30, (255, 255, 255), 565, 350)
                        texto(player.nome_golpes[3] + " (" + player.custo_golpes[3][0] + "/" + player.custo_golpes[3][1] + "/" + player.custo_golpes[3][2] + ")", 30, (255, 255, 255), 565, 400)
                        texto("Passar o turno", 30, (255, 255, 255), 565, 450)

                        texto("> " + mini_console, 20, (255,255,255), 430, 640)
                        if(seletor_golpe.y < 450):
                            texto(player.descricao_golpes[seletor_golpe.y/50-5], 20, (255,255,255), 430, 680)
                        else:
                            texto("Passar o turno e aguardar mais recursos", 20, (255,255,255), 430, 680)
                    
                        seletor_golpe.blit()

                        if(golpe_selecionado):
                            if(golpe_executado<> True and paralisado <> True):
                                if(seletor_golpe.y <450):
                                    testar_golpe = player.custo_golpes[seletor_golpe.y/50-5]
                                    executar_golpe = player.efeito_golpes[seletor_golpe.y/50-5]
                                else:
                                    testar_golpe = "000"
                                    executar_golpe = "00"
                                if int(testar_golpe[0]) > player.recursos[0] or int(testar_golpe[1]) > player.recursos[1] or int(testar_golpe[2]) > player.recursos[2]:
                                    texto("Movimento inválido! Sem recursos suficientes.", 20, (255,255,255), 430, 600)
                                    pygame.display.flip()
                                    time.sleep(2)
                                    golpe_selecionado = False
                                else:
                                    player.recursos[0] += -int(testar_golpe[0])
                                    player.recursos[1] += -int(testar_golpe[1])
                                    player.recursos[2] += -int(testar_golpe[2])

                                    

                                    if executar_golpe[0] == "0" and executar_golpe[1]<>"0":
                                        x = int(executar_golpe[1])
                                        x += random.randint(0, player.ataque)
                                        executar_golpe = executar_golpe[0] + str(x)
                                    elif executar_golpe[0] == "1":
                                        player.defesa += int(executar_golpe[1])
                                    elif executar_golpe[0] == "2":
                                        player.ataque += int(executar_golpe[1])
                                    elif executar_golpe[0] == "3":
                                        player.vida += int(executar_golpe[1])
                                    elif executar_golpe[0] == "7":
                                        player.recursos[random.randint(0,2)] += int(executar_golpe[1])

                                    if player.ataque > 9:
                                        player.ataque = 9
                                    if player.defesa > 9:
                                        player.defesa = 9
                                    if player.vida > 99:
                                        player.vida = 99
                                        
                                    golpe_executado = True
                                    
                                    
                                    if(player.vida <10):
                                        controle = "0"
                                    else:
                                        controle = ""
                                    x = conectar(tipo_socket, tipo_conexao, executar_golpe + controle + str(player.vida))

                                    oponente.vida = int(conectar(tipo_socket, tipo_conexao, "a"))
                                    ## Envia o golpe e a vida
                                    ## inverte turno
                                    turno = False

                    elif(paralisado == True):
                        texto("Você está paralisado. Aguarde o próximo turno.", 20, (255,255,255), 565, 640)
                        pygame.display.flip()
                        time.sleep(4)
                        if(player.vida <10):
                            controle = "0"
                        else:
                            controle = ""
                        x = conectar(tipo_socket, tipo_conexao, "00" + controle + str(player.vida))
                        oponente.vida = int(conectar(tipo_socket, tipo_conexao, "a"))
                        paralisado = False
                        turno = False
                                
                                        
                                    


                                

                    
                    


                else:
                    screen.blit(turnbox_oponente, (565, 50))
                    golpe_executado = False
                    pygame.display.flip()
                    acao = conectar(tipo_socket, tipo_conexao, "")
                    
                    x = 0
                    if acao[0] == "0":
                        x = int(acao[1])
                        x += -random.randint(0, player.defesa)
                        if x>0:
                            if player.vida >= x:
                                player.vida += -x
                            else:
                                player.vida = 0
                            mini_console = "Você foi atacado. Total de dano: " + str(x)
                        else:
                            if acao[1] <> "0":
                                mini_console = "Você foi atacado, mas não sofreu dano! Boa defesa!"
                            else:
                                mini_console = "Seu adversário não se moveu."
                    elif acao[0] == "4":
                        if player.defesa >= int(acao[1]):
                            player.defesa += -int(acao[1])
                        else:
                            player.defesa = 0
                        mini_console = "A sua defesa foi reduzida em " + acao[1] + " pontos."
                    elif acao[0] == "5":
                        if player.ataque >= int(acao[1]):
                            player.ataque += -int(acao[1])
                        else:
                            player.ataque = 0
                        mini_console = "O seu ataque foi reduzido em " + acao[1] + " pontos."
                    elif acao[0] == "6":
                        paralisado = True
                    elif acao[0] == "8":
                        x = random.randint(0,2)
                        if player.recursos[x] >= int(acao[1]):
                            player.recursos[x] += - int(acao[1])
                        else:
                            player.recursos[x] = 0
                        mini_console = "Você perdeu " + acao[1] + " de um recurso."
                    else:
                        mini_console = "Seu adversário não te atacou diretamente... Ele deve estar tramando algo."
                    
                    oponente.vida = int(acao[2] + acao[3])

                    if(player.vida <10):
                        controle = "0"
                    else:
                        controle = ""
                    x = conectar(tipo_socket, tipo_conexao, controle + str(player.vida))
                    
                    turno = True
                    pegar_recursos = True
                    golpe_selecionado = False
                    golpe_executado = False
                
            
                ## Recebe o golpe, executa as ações, envia vida
                ## inverte turno


    if (tela == 6):

        #Zerando variáveis
        personagem_escolhido = False
        golpe_selecionado = False
        golpe_executado = False
        oponente.vida = 20
        player.vida = 20
        player.ataque = 1
        player.defesa = 1
        player.recursos[0] = 0
        player.recursos[1] = 0
        player.recursos[2] = 0
        inicio = True
        mini_console = ""
        musica_char = True
        
        screen.blit(background, (0,0))
        screen.blit(player.imagem, (0, 100))
        screen.blit(oponente.imagem, (870, 100))
        screen.blit(derrota, (0,100))
        seletor_partida.blit()
        texto_centralizado("DERROTA", 60, (255,255,255), 565, 10, "calibri")
        texto_centralizado("Jogar de novo?", 50, (255,255,255), 5, 200, "calibri")
        texto_centralizado("Sim", 50, (255,255,255), 5, 400, "calibri")
        texto_centralizado("Não", 50, (255,255,255), 5, 450, "calibri")
        if(resp_again):
            op_desafio = conectar(tipo_socket, tipo_conexao, jogardenovo)
        if op_desafio == 's' and jogardenovo == 's':
            tela = 4
            pygame.mixer.music.stop()
        elif op_desafio == 'n' or jogardenovo == 'n':
            tela = 0
            pygame.mixer.music.stop()
        


    if (tela == 7) :

        #Zerando variáveis
        personagem_escolhido = False
        golpe_selecionado = False
        golpe_executado = False
        inicio = True
        oponente.vida = 20
        player.vida = 20
        player.ataque = 1
        player.defesa = 1
        player.recursos[0] = 0
        player.recursos[1] = 0
        player.recursos[2] = 0
        mini_console = ""
        musica_char = True
        
        
        screen.blit(background, (0,0))
        screen.blit(player.imagem, (0, 100))
        screen.blit(oponente.imagem, (870, 100))
        screen.blit(derrota, (870,100))
        seletor_partida.blit()
        texto_centralizado("VITÓRIA", 60, (255,255,255), 565, 10, "calibri")
        texto_centralizado("Jogar de novo?", 50, (255,255,255), 5, 200, "calibri")
        texto_centralizado("Sim", 50, (255,255,255), 5, 400, "calibri")
        texto_centralizado("Não", 50, (255,255,255), 5, 450, "calibri")
        if(resp_again):
            op_desafio = conectar(tipo_socket, tipo_conexao, jogardenovo)
        if op_desafio == 's' and jogardenovo == 's':
            tela = 4
            pygame.mixer.music.stop()
        elif op_desafio == 'n' or jogardenovo == 'n':
            tela = 0
            pygame.mixer.music.stop()









                
            
            

    
    pygame.display.flip()

pygame.mixer.music.stop()
pygame.display.quit()

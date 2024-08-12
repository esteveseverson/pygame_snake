import pygame as pg
import random

# Inicializar o Pygame
pg.init()
pg.display.set_caption('Snake Python')

# Definições de cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO_CLARO = (255, 99, 71)
AZUL_CIELO = (135, 206, 250)
VERDE_CLARO = (144, 238, 144)

# Configurações da tela
LARGURA, ALTURA = 800, 600
TELA = pg.display.set_mode((LARGURA, ALTURA))
RELOGIO = pg.time.Clock()

# Parâmetros do jogo
TAMANHO_QUADRADO = 20

class Cobra:
    def __init__(self):
        self.x = LARGURA / 2
        self.y = ALTURA / 2
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.tamanho = 1
        self.pixels = []
        self.direcao_atual = None  # Começar parado

    def atualizar(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        
        # Atualiza a posição da cobra
        self.pixels.append([self.x, self.y])
        if len(self.pixels) > self.tamanho:
            del self.pixels[0]

    def mudar_direcao(self, tecla):
        if tecla == pg.K_DOWN or tecla == pg.K_s:
            if self.direcao_atual != 'UP':
                self.velocidade_x = 0
                self.velocidade_y = TAMANHO_QUADRADO
                self.direcao_atual = 'DOWN'
        elif tecla == pg.K_UP or tecla == pg.K_w:
            if self.direcao_atual != 'DOWN':
                self.velocidade_x = 0
                self.velocidade_y = -TAMANHO_QUADRADO
                self.direcao_atual = 'UP'
        elif tecla == pg.K_RIGHT or tecla == pg.K_d:
            if self.direcao_atual != 'LEFT':
                self.velocidade_x = TAMANHO_QUADRADO
                self.velocidade_y = 0
                self.direcao_atual = 'RIGHT'
        elif tecla == pg.K_LEFT or tecla == pg.K_a:
            if self.direcao_atual != 'RIGHT':
                self.velocidade_x = -TAMANHO_QUADRADO
                self.velocidade_y = 0
                self.direcao_atual = 'LEFT'

    def verificar_colisao(self):
        # Verifica se a cobra colidiu com as paredes
        if self.x < 20 or self.x >= LARGURA - 20 or self.y < 20 or self.y >= ALTURA - 20:
            return True
        
        #Verifica se a cobra colidiu com ela mesma
        if [self.x, self.y] in self.pixels[:-1]:
            return True
        return False

    def desenhar(self):
        for pixel in self.pixels:
            pg.draw.rect(TELA, VERDE, [pixel[0], pixel[1], TAMANHO_QUADRADO, TAMANHO_QUADRADO])

class Comida:
    def __init__(self):
        self.x, self.y = self.gerar_comida()

    def gerar_comida(self):
        comida_x = round(random.randrange(20, LARGURA - TAMANHO_QUADRADO - 20) / float(TAMANHO_QUADRADO)) * float(TAMANHO_QUADRADO)
        comida_y = round(random.randrange(20, ALTURA - TAMANHO_QUADRADO - 20) / float(TAMANHO_QUADRADO)) * float(TAMANHO_QUADRADO)
        return comida_x, comida_y

    def desenhar(self):
        pg.draw.rect(TELA, VERMELHO, [self.x, self.y, TAMANHO_QUADRADO, TAMANHO_QUADRADO])

class Jogo:
    def __init__(self):
        self.cobra = Cobra()
        self.comida = Comida()
        self.pontuacao = 0
        self.fim_jogo = False
        self.velocidade_jogo = 15 
        self.contador_comidas = 0

    def desenhar_pontuacao(self):
        fonte = pg.font.SysFont('Helvetica', 27)
        texto = fonte.render(f'Pontos: {self.pontuacao}', True, VERMELHO_CLARO)
        TELA.blit(texto, [1, 1])

    def desenhar_bordas(self):
        # Desenhar retângulo nas extremidades
        pg.draw.rect(TELA, BRANCO, [0, 0, LARGURA, 20])
        pg.draw.rect(TELA, BRANCO, [0, ALTURA - 20, LARGURA, 20])
        pg.draw.rect(TELA, BRANCO, [0, 0, 20, ALTURA])
        pg.draw.rect(TELA, BRANCO, [LARGURA - 20, 0, 20, ALTURA])

    def mostrar_mensagem(self, mensagem):
        fonte = pg.font.SysFont('Helvetica', 50)
        texto = fonte.render(mensagem, True, VERMELHO_CLARO)
        largura_texto = texto.get_width()
        altura_texto = texto.get_height()
        x = (LARGURA - largura_texto) / 2
        y = (ALTURA - altura_texto) / 2
        TELA.blit(texto, [x, y])
        pg.display.update()  # Atualiza a tela para exibir a mensagem

    def aumentar_velocidade(self):
        self.contador_comidas += 1
        if self.contador_comidas % 3 == 0:
            self.velocidade_jogo += 1

    def rodar(self):
        while not self.fim_jogo:
            TELA.fill(PRETO)

            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    self.fim_jogo = True
                elif evento.type == pg.KEYDOWN:
                    self.cobra.mudar_direcao(evento.key)

            self.cobra.atualizar()
            
            if self.cobra.verificar_colisao():
                self.fim_jogo = True

            # Verifica se a cobra comeu a comida
            if self.cobra.x == self.comida.x and self.cobra.y == self.comida.y:
                self.cobra.tamanho += 1
                self.comida = Comida()  # Gera nova comida
                self.pontuacao += 1
                self.aumentar_velocidade()  # Aumenta a velocidade do jogo a cada 3 comidas

            self.desenhar_bordas()
            self.cobra.desenhar()
            self.comida.desenhar()
            self.desenhar_pontuacao()

            pg.display.update()
            RELOGIO.tick(self.velocidade_jogo)

        # Mostrar a mensagem de Game Over
        self.mostrar_mensagem(f'Você perdeu, você fez {self.pontuacao} pontos.')
        pg.time.wait(3000)  # Espera por 3 segundos antes de fechar o jogo

class TelaInicial:
    def __init__(self):
        self.fonte = pg.font.SysFont('Helvetica', 50)
        self.espaco_vertical = 100
        self.raio_botao = 80  # Aumentar o raio para garantir que o texto se encaixe melhor

    def desenhar_botao(self, texto, posicao, cor_fundo, cor_texto):
        fonte = pg.font.SysFont('Helvetica', 40)
        texto_renderizado = fonte.render(texto, True, cor_texto)
        largura_texto = texto_renderizado.get_width()
        altura_texto = texto_renderizado.get_height()
        
        # Desenho do botão redondo
        x, y = posicao
        centro_x = x
        centro_y = y
        
        # Desenha o círculo de fundo
        pg.draw.circle(TELA, cor_fundo, (centro_x, centro_y), self.raio_botao)
        # Desenha a borda do círculo
        pg.draw.circle(TELA, cor_texto, (centro_x, centro_y), self.raio_botao, 2)
        
        # Posiciona o texto no centro do botão
        texto_x = centro_x - largura_texto // 2
        texto_y = centro_y - altura_texto // 2
        TELA.blit(texto_renderizado, (texto_x, texto_y))

    def mostrar_tela(self):
        clicou = False
        while not clicou:
            TELA.fill(AZUL_CIELO)
            
            posicao_mouse = pg.mouse.get_pos()
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    pg.quit()
                    return 'sair'
                elif evento.type == pg.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.botao_jogar.collidepoint(posicao_mouse):
                        clicou = True
                        return 'iniciar'
                    elif self.botao_sair.collidepoint(posicao_mouse):
                        pg.quit()
                        return 'sair'
            
            # Atualiza as posições dos botões
            self.botao_jogar = pg.Rect((LARGURA // 2 - self.raio_botao, ALTURA // 2 - 60 - self.espaco_vertical // 2), (self.raio_botao * 2, self.raio_botao * 2))
            self.botao_sair = pg.Rect((LARGURA // 2 - self.raio_botao, ALTURA // 2 + self.espaco_vertical // 2), (self.raio_botao * 2, self.raio_botao * 2))
            
            # Desenha os botões na tela
            self.desenhar_botao('Iniciar', (LARGURA // 2, ALTURA // 2 - 30 - self.espaco_vertical // 2), VERDE_CLARO, PRETO)
            self.desenhar_botao('Sair', (LARGURA // 2, ALTURA // 2 + 30 + self.espaco_vertical // 2), VERDE_CLARO, PRETO)
            
            pg.display.update()

# Executar a Tela Inicial
tela_inicial = TelaInicial()
opcao = tela_inicial.mostrar_tela()

if opcao == 'iniciar':
    jogo = Jogo()
    jogo.rodar()

pg.quit()

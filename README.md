# Neon Snake Game - Documentação Completa

## Visão Geral

Neon Snake é um jogo estilo arcade inspirado no clássico "Snake" com uma estética visual neon moderna. O jogador controla uma cobra que deve comer alimentos para crescer enquanto evita colisões com as paredes, bordas da tela e seu próprio corpo. O jogo apresenta efeitos visuais avançados, sistema de pontuação, diferentes tipos de comida e mecânicas de jogo dinâmicas.



## Características Principais

- **Estética Neon**: Design visual com cores vibrantes e efeitos de brilho
- **Efeitos Visuais**: Partículas, pulsação, gradientes e vinhetas
- **Sistema de Pontuação**: Placar de recordes persistente salvo em arquivo JSON
- **Mecânicas Avançadas**: Diferentes tipos de comida com efeitos variados
- **Paredes Dinâmicas**: Adição e remoção de obstáculos durante o jogo
- **Controles Responsivos**: Movimentação fluida com as setas do teclado
- **Sistema de Pausa**: Capacidade de pausar o jogo com a tecla ESC
- **Controle de Música**: Opção para ativar/desativar a música de fundo

## Requisitos Técnicos

- Python 3.x
- Pygame (biblioteca)
- Arquivos de áudio:
  - `comer.wav` - Som ao comer alimento
  - `criarparede.wav` - Som ao criar parede
  - `destruirparede.wav` - Som ao destruir parede
  - `musicabackgroundmusic.mp3` - Música de fundo

## Instalação

1. Certifique-se de ter Python 3.x instalado
2. Instale a biblioteca Pygame:
   ```
   pip install pygame
   ```
3. Baixe todos os arquivos de áudio necessários
4. Execute o jogo:
   ```
   python neon_snake.py
   ```

## Estrutura do Código

### Configurações Iniciais
- Inicialização do Pygame e mixer de áudio
- Definição de constantes (tamanho da tela, grid, cores)
- Carregamento de fontes e configuração de display

### Classes e Objetos
- `Particle`: Classe para efeitos de partículas
- Superfície de vinheta para efeitos visuais nas bordas

### Estados do Jogo
- `MENU`: Tela inicial com placar e botão de início
- `PLAYING`: Estado ativo de jogo
- `GAME_OVER`: Tela de fim de jogo
- `GETTING_NAME`: Entrada de nome para novo recorde
- `PAUSED`: Jogo pausado

### Funções Principais

#### Funções de Desenho
- `draw_grid`: Desenha linhas de grade
- `draw_element_with_glow`: Desenha elementos com efeito de brilho
- `draw_snake`: Renderiza a cobra com gradiente de cor
- `draw_food`: Desenha alimentos com efeitos pulsantes
- `draw_walls`: Renderiza paredes com efeito de brilho
- `draw_text_with_shadow`: Texto com sombra para melhor legibilidade
- `draw_button`: Botões interativos com efeito hover
- `draw_scoreboard`: Placar de recordes com estilo visual

#### Funções de Partículas
- `add_particles`: Adiciona partículas em uma posição
- `update_particles`: Atualiza estado das partículas
- `draw_particles`: Renderiza partículas na tela

#### Funções de Lógica
- `get_valid_spawn_position`: Encontra posição válida para novos elementos
- `spawn_food`: Gera novo alimento no jogo
- `reset_game_state`: Reinicia variáveis do jogo
- `move_snake`: Atualiza posição da cobra
- `add_wall`: Adiciona nova parede
- `remove_random_wall`: Remove parede aleatória
- `check_collisions`: Verifica colisões da cobra
- `toggle_music`: Ativa/desativa música de fundo

#### Funções de Placar
- `load_scoreboard`: Carrega placar do arquivo
- `save_scoreboard`: Salva placar em arquivo
- `add_score`: Adiciona nova pontuação ao placar

### Mecânicas de Jogo

#### Tipos de Comida
- **Azul**: Aumenta o tamanho da cobra, adiciona pontos e acelera o jogo
- **Vermelha**: Ação aleatória (adicionar ou remover parede)

#### Paredes
- Adicionadas automaticamente a cada 3 pontos
- Podem ser adicionadas/removidas ao comer comida vermelha

#### Pontuação
- Aumenta ao comer comida azul
- Placar de recordes persistente entre sessões
- Entrada de nome para novos recordes

#### Controles
- **Setas**: Movimentação da cobra
- **ESC**: Pausar/continuar jogo
- **ENTER**: Confirmar nome para novo recorde

## Loop Principal do Jogo

1. **Tratamento de Eventos**: Processa entradas do usuário
2. **Lógica do Jogo**: Atualiza estado do jogo conforme o estado atual
3. **Renderização**: Desenha elementos na tela
4. **Atualização da Tela**: Atualiza o display
5. **Controle de FPS**: Mantém taxa de quadros consistente

## Efeitos Visuais

- **Partículas**: Efeitos ao comer, criar/destruir paredes e colisões
- **Pulsação**: Elementos com tamanho/brilho variável
- **Gradiente**: Corpo da cobra com degradê de cor
- **Vinheta**: Escurecimento nas bordas da tela
- **Hover**: Efeitos ao passar o mouse sobre botões
- **Sombras**: Textos com sombra para melhor legibilidade

## Sistema de Arquivos

- `neon_snake_scoreboard.json`: Armazena placar de recordes

## Personalização

O código permite fácil personalização de:
- Cores e efeitos visuais
- Tamanho da tela e grid
- Velocidade inicial e incremento
- Dificuldade (frequência de paredes)
- Sons e música

## Dicas de Jogo

- Planeje seu caminho com antecedência
- Evite ficar preso entre paredes
- Comidas vermelhas podem ajudar a remover paredes inconvenientes
- O jogo acelera conforme sua pontuação aumenta

## Solução de Problemas

- **Erro ao carregar fontes**: O jogo usa fontes alternativas se as principais não estiverem disponíveis
- **Erro ao salvar placar**: Verificar permissões de escrita no diretório
- **Problemas de áudio**: Verificar se os arquivos de som estão no diretório correto

## Créditos

Este jogo foi desenvolvido como um projeto demonstrativo de programação em Python utilizando a biblioteca Pygame, com foco em efeitos visuais avançados e mecânicas de jogo dinâmicas.

---


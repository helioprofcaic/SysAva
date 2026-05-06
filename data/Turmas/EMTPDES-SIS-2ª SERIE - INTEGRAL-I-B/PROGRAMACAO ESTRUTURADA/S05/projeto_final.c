/**
 * @file projeto_final.c
 * @brief Implementação do Jogo da Velha (Tic-Tac-Toe) em C.
 * @details Este projeto consolida os conhecimentos de Matrizes e Funções.
 *          Disciplina: Programação Estruturada - Aula 39
 */

#include <stdio.h>
#include <stdlib.h> // Para system("cls") ou system("clear")

// --- Protótipos das Funções ---

/**
 * @brief Preenche o tabuleiro com espaços vazios no início do jogo.
 * @param tabuleiro A matriz 3x3 do jogo.
 */
void inicializarTabuleiro(char tabuleiro[3][3]);

/**
 * @brief Exibe o estado atual do tabuleiro na tela.
 * @param tabuleiro A matriz 3x3 do jogo.
 */
void desenharTabuleiro(char tabuleiro[3][3]);

/**
 * @brief Verifica se algum jogador venceu o jogo.
 * @param tabuleiro A matriz 3x3 do jogo.
 * @return 1 se houver um vencedor, 0 caso contrário.
 */
int verificarVitoria(char tabuleiro[3][3]);

/**
 * @brief Verifica se o jogo terminou em empate (tabuleiro cheio sem vencedor).
 * @param tabuleiro A matriz 3x3 do jogo.
 * @return 1 se for empate, 0 caso contrário.
 */
int verificarEmpate(char tabuleiro[3][3]);

/**
 * @brief Controla o fluxo principal do jogo, alternando jogadores e verificando o estado.
 */
void jogar();


// --- Função Principal ---
int main() {
    jogar(); // Inicia o jogo
    return 0;
}


// --- Implementação das Funções ---

void jogar() {
    char tabuleiro[3][3];
    int jogador_atual = 1; // 1 para 'X', 2 para 'O'
    int linha, coluna;
    int status_jogo = 0; // 0 = em andamento, 1 = vitoria, 2 = empate

    inicializarTabuleiro(tabuleiro);

    // Loop principal do jogo
    while (status_jogo == 0) {
        system("cls || clear"); // Limpa a tela (funciona em Windows, Linux e Mac)
        desenharTabuleiro(tabuleiro);

        char simbolo_jogador = (jogador_atual == 1) ? 'X' : 'O';
        printf("\n--- Vez do Jogador %d (%c) ---\n", jogador_atual, simbolo_jogador);
        printf("Digite a linha (0-2): ");
        scanf("%d", &linha);
        printf("Digite a coluna (0-2): ");
        scanf("%d", &coluna);

        // Validação da jogada
        if (linha < 0 || linha > 2 || coluna < 0 || coluna > 2 || tabuleiro[linha][coluna] != ' ') {
            printf("\nJogada invalida! A posicao ja esta ocupada ou fora dos limites.\n");
            printf("Pressione Enter para tentar novamente...");
            while(getchar() != '\n'); // Limpa o buffer de entrada do teclado
            getchar();
            continue; // Pula para a próxima iteração do loop
        }

        // Realiza a jogada
        tabuleiro[linha][coluna] = simbolo_jogador;

        // Verifica o estado do jogo após a jogada
        if (verificarVitoria(tabuleiro)) {
            status_jogo = 1; // Vitória
        } else if (verificarEmpate(tabuleiro)) {
            status_jogo = 2; // Empate
        } else {
            // Se ninguém venceu ou empatou, troca o jogador
            jogador_atual = (jogador_atual == 1) ? 2 : 1;
        }
    }

    // Exibe o resultado final
    system("cls || clear");
    desenharTabuleiro(tabuleiro);
    if (status_jogo == 1) {
        printf("\n*** FIM DE JOGO! O Jogador %d venceu! ***\n\n", jogador_atual);
    } else {
        printf("\n*** FIM DE JOGO! Deu velha (empate)! ***\n\n");
    }
}

void inicializarTabuleiro(char t[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            t[i][j] = ' ';
        }
    }
}

void desenharTabuleiro(char t[3][3]) {
    printf("\n   JOGO DA VELHA\n");
    printf("     0   1   2\n");
    printf("   +---+---+---+\n");
    printf(" 0 | %c | %c | %c |\n", t[0][0], t[0][1], t[0][2]);
    printf("   +---+---+---+\n");
    printf(" 1 | %c | %c | %c |\n", t[1][0], t[1][1], t[1][2]);
    printf("   +---+---+---+\n");
    printf(" 2 | %c | %c | %c |\n", t[2][0], t[2][1], t[2][2]);
    printf("   +---+---+---+\n");
}

int verificarVitoria(char t[3][3]) {
    // Verificar linhas e colunas
    for (int i = 0; i < 3; i++) {
        if (t[i][0] != ' ' && t[i][0] == t[i][1] && t[i][1] == t[i][2]) return 1;
        if (t[0][i] != ' ' && t[0][i] == t[1][i] && t[1][i] == t[2][i]) return 1;
    }
    // Verificar diagonais
    if (t[0][0] != ' ' && t[0][0] == t[1][1] && t[1][1] == t[2][2]) return 1;
    if (t[0][2] != ' ' && t[0][2] == t[1][1] && t[1][1] == t[2][0]) return 1;
    return 0; // Nenhuma vitória
}

int verificarEmpate(char t[3][3]) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            if (t[i][j] == ' ') return 0; // Ainda há espaços, não é empate
        }
    }
    return 1; // Tabuleiro cheio, é empate
}
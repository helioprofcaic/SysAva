#include <stdio.h>
#include <stdlib.h>

// Estrutura do Nó
struct No {
    int dado;
    struct No *esq;
    struct No *dir;
};

// Função para criar um novo nó
struct No* criarNo(int valor) {
    struct No* novoNo = (struct No*)malloc(sizeof(struct No));
    novoNo->dado = valor;
    novoNo->esq = novoNo->dir = NULL;
    return novoNo;
}

// Inserção em árvore binária de busca
struct No* inserir(struct No* raiz, int valor) {
    if (raiz == NULL) return criarNo(valor);
    if (valor < raiz->dado)
        raiz->esq = inserir(raiz->esq, valor);
    else if (valor > raiz->dado)
        raiz->dir = inserir(raiz->dir, valor);
    return raiz;
}

// Percurso em Ordem (esquerda, raiz, direita)
void emOrdem(struct No* raiz) {
    if (raiz != NULL) {
        emOrdem(raiz->esq);
        printf("%d ", raiz->dado);
        emOrdem(raiz->dir);
    }
}

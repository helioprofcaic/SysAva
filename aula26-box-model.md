# Aula 26: Box Model no CSS

**Disciplina:** Programação Web Front-End 2026B  
**Turma:** 2ª Série - Turma I-B (Técnico DS)  
**Escola:** CETI Professor Florestan Fernandes  
**Professor:** Helio P. Lima  

---

## 🎯 Objetivos

1. Compreender os quatro elementos que compõem o Box Model no CSS (conteúdo, preenchimento, borda e margem).
2. Identificar como cada parte do Box Model influencia o layout e o posicionamento dos elementos em uma página web.
3. Aplicar as propriedades CSS de largura, altura, padding, border e margin para criar layouts responsivos e visualmente organizados.

---

## 💡 Conteúdo Teórico

### O que é o Box Model?

O **Box Model** é um dos conceitos fundamentais no desenvolvimento web com CSS. Ele descreve como os elementos HTML são renderizados na página: cada elemento é visualizado como uma **caixa retangular** composta por quatro partes principais.

### As Quatro Partes do Box Model

#### 1. Conteúdo (Content)
- É o **espaço interno** da caixa onde o texto, imagens ou outros elementos HTML são exibidos.
- É o componente central e mais básico da caixa.
- Suas dimensões são definidas pelas propriedades `width` (largura) e `height` (altura).

#### 2. Preenchimento (Padding)
- É uma área **transparente ao redor do conteúdo**.
- Cria **espaçamento interno** entre o conteúdo e a borda da caixa.
- Propriedades CSS: `padding-top`, `padding-right`, `padding-bottom`, `padding-left` (ou abreviação `padding`).

#### 3. Borda (Border)
- É a **linha que envolve a caixa**.
- Pode ter diferentes estilos, cores e espessuras.
- Propriedades CSS:
  - `border-width` — espessura da borda
  - `border-style` — estilo da borda (solid, dashed, dotted, etc.)
  - `border-color` — cor da borda

#### 4. Margem (Margin)
- É uma área **transparente fora da borda**.
- Cria **espaçamento externo** entre as caixas.
- Define o espaço entre um elemento e seus elementos vizinhos.
- Propriedades CSS: `margin-top`, `margin-right`, `margin-bottom`, `margin-left` (ou abreviação `margin`).

### Cálculo da Largura Total

Para calcular a **largura total** de uma caixa, deve-se somar:

```
Largura Total = width + padding-left + padding-right + border-left + border-right + margin-left + margin-right
```

> **Dica:** Para simplificar, use `box-sizing: border-box;` — assim, o `width` já inclui padding e border.

---

## 🛠️ Atividade Prática

### Exercício: Construindo uma Caixa com Box Model

Crie um arquivo HTML com o seguinte CSS e analise os efeitos de cada propriedade:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Atividade - Box Model</title>
  <style>
    .caixa {
      width: 300px;
      height: 200px;
      padding: 20px;
      border: 5px solid #333;
      margin: 30px;
      background-color: #e0f7fa;
    }
  </style>
</head>
<body>
  <div class="caixa">Conteúdo da caixa</div>
</body>
</html>
```

### Tarefas:

1. **Desenhe no papel** a dimensão de cada parte do Box Model com base nos valores do CSS acima.
2. **Calcule a largura total** da caixa (considerando padding, border e margin).
3. **Modifique o CSS** para adicionar um `padding` diferente em cada lado e observe o resultado no navegador.
4. **Remova a borda** e compare o espaço ocupado. O que acontece com a largura total?

---

## 📝 Quiz

**1. Quais são as quatro partes que compõem o Box Model no CSS?**

a) Título, parágrafo, link e imagem  
b) Conteúdo, preenchimento, borda e margem  
c) Largura, altura, profundidade e cor  
d) Container, section, div e span  

**2. Qual propriedade CSS cria espaço interno entre o conteúdo e a borda de um elemento?**

a) `margin`  
b) `border`  
c) `padding`  
d) `spacing`  

**3. Para que o valor de `width` já inclua padding e border no cálculo, qual propriedade deve ser utilizada?**

a) `display: box`  
b) `position: border-box`  
c) `box-sizing: border-box`  
d) `layout: inclusive`  

---

### ✅ Gabarito

1. **b)** Conteúdo, preenchimento, borda e margem  
2. **c)** `padding`  
3. **c)** `box-sizing: border-box`  

---

## 📚 Referências

- MDN Web Docs - CSS Box Model: https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_box_model
- W3Schools - CSS Box Model: https://www.w3schools.com/css/css_boxmodel.asp

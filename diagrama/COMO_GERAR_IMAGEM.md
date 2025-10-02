# 📸 Como Gerar a Imagem do Diagrama

Para incluir o diagrama no README, você precisa exportar o arquivo Mermaid para PNG.

## Opção 1: Via Mermaid Live Editor (Mais Fácil)

1. Acesse: https://mermaid.live/
2. Cole o conteúdo de `diagrama/fluxo_lambda_gerencial.mmd`
3. Clique em **"Download PNG"**
4. Salve o arquivo como `fluxo_lambda_gerencial.png` na pasta `diagrama/`

## Opção 2: Via VS Code (Recomendado)

1. Instale a extensão **Markdown Preview Mermaid Support** no VS Code
2. Abra o arquivo `fluxo_lambda_gerencial.mmd`
3. Use o preview do Mermaid (já aberto)
4. Faça um screenshot ou use a funcionalidade de export da extensão
5. Salve como `diagrama/fluxo_lambda_gerencial.png`

## Opção 3: Via CLI (Para Desenvolvedores)

### Instalar Mermaid CLI:
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Gerar a imagem:
```bash
cd diagrama
mmdc -i fluxo_lambda_gerencial.mmd -o fluxo_lambda_gerencial.png -w 2400 -H 800 -b transparent
```

### Parâmetros:
- `-i`: arquivo de entrada (.mmd)
- `-o`: arquivo de saída (.png)
- `-w`: largura em pixels
- `-H`: altura em pixels
- `-b`: cor de fundo (transparent para fundo transparente)

## ✅ Após Gerar a Imagem

A imagem será automaticamente referenciada no README.md:
```markdown
![Arquitetura do Sistema](diagrama/fluxo_lambda_gerencial.png)
```

## 🎨 Dica de Qualidade

Para apresentações ou documentação profissional, use:
- **Largura**: 2400px ou maior
- **Formato**: PNG com fundo transparente
- **DPI**: 300 para impressão

---

**Nota**: O README.md já está configurado para mostrar o diagrama. Basta gerar a imagem e salvá-la no local correto.

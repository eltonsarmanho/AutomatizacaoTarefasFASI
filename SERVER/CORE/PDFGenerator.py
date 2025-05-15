from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import locale
from datetime import datetime

def gerar_pdf_projetos(resposta):
    """Gera um PDF contendo as informações do formulário de Projetos, ajustando o conteúdo conforme Natureza e Solicitação."""
    
    nome_arquivo = f"Parecer_{resposta[1].replace(' ', '_')}.pdf"
    caminho_pdf = os.path.join( nome_arquivo)  # Salvar no diretório temporário

    # Configuração do PDF
    largura, altura = A4
    margem_esquerda = 80
    margem_direita = largura - 80
    margem_superior = altura - 50  # Ajuste do topo
    largura_texto = margem_direita - margem_esquerda

    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    c.setFont("Helvetica", 12)

    # Variáveis do formulário
    docente = resposta[1]
    parecerista_1 = resposta[2]
    parecerista_2 = resposta[3]
    projeto = resposta[4]
    carga_horaria = resposta[5]
    edital = resposta[6]
    natureza = resposta[7]  # Pesquisa, Ensino ou Extensão
    ano_edital = resposta[8]
    solicitacao = resposta[9]  # Novo, Encerramento ou Renovação

    # Cabeçalho (centralizado)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(largura / 2, margem_superior, "UNIVERSIDADE FEDERAL DO PARÁ")
    c.drawCentredString(largura / 2, margem_superior - 15, "CAMPUS UNIVERSITÁRIO DO TOCANTINS/CAMETÁ")
    c.drawCentredString(largura / 2, margem_superior - 30, "FACULDADE DE SISTEMAS DE INFORMAÇÃO - FASI")

    # Título do Parecer
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(largura / 2, margem_superior - 70, "PARECER")

    # Dados do Projeto
    c.setFont("Helvetica", 12)
    y_pos = margem_superior - 100
    
    # Aplicar quebra de linha para o título do projeto
    titulo_texto = f"Título do Projeto: {projeto}"
    linhas_titulo = wrap_text(titulo_texto, largura_texto, c)
    for linha in linhas_titulo:
        c.drawString(margem_esquerda, y_pos, linha)
        y_pos -= 20
    
    # Aplicar quebra de linha para o coordenador caso necessário
    coord_texto = f"Coordenador: {docente}"
    linhas_coord = wrap_text(coord_texto, largura_texto, c)
    for linha in linhas_coord:
        c.drawString(margem_esquerda, y_pos, linha)
        y_pos -= 20

    # Corpo do parecer ajustado conforme natureza e solicitação
    parecer_texto = gerar_texto_parecer(natureza, solicitacao, docente, parecerista_1, parecerista_2, carga_horaria)

    # Escrever o texto do parecer com JUSTIFICAÇÃO
    y_pos -= 40
    c.setFont("Helvetica", 12)
    y_pos = desenhar_texto_justificado(c, parecer_texto, margem_esquerda, y_pos, largura_texto)

    # Data e Aprovação dos Pareceristas
    y_pos -= 40
    c.setFont("Helvetica", 12)
    c.drawString(largura - 200, y_pos, f"Cametá, {obter_data_formatada()}.")

    y_pos -= 40
    c.drawString(margem_esquerda, y_pos, f"Aprovação do {parecerista_1}")
    y_pos -= 60
    c.drawString(margem_esquerda, y_pos, f"Aprovação do {parecerista_2}")

    c.save()
    return caminho_pdf  # Retorna o caminho do PDF gerado

def desenhar_texto_justificado(c, texto, x, y, largura_texto):
    """Desenha um parágrafo de texto justificado no PDF, evitando palavras grudadas."""
    linhas = wrap_text(texto, largura_texto, c)
    
    for i, linha in enumerate(linhas):
        palavras = linha.split()
        num_palavras = len(palavras)

        if i == len(linhas) - 1 or num_palavras == 1:
            # Última linha ou linha com uma única palavra → alinha à esquerda
            c.drawString(x, y, linha)
        else:
            # Justificação distribuindo espaços entre as palavras
            largura_linha = sum(c.stringWidth(palavra, "Helvetica", 12) for palavra in palavras)
            espaco_total = largura_texto - largura_linha  # Espaço restante na linha
            espaco_por_palavra = espaco_total / (num_palavras - 1)  # Espaço extra entre palavras

            x_temp = x
            for palavra in palavras[:-1]:
                c.drawString(x_temp, y, palavra)
                x_temp += c.stringWidth(palavra, "Helvetica", 12) + espaco_por_palavra + 1  # Adicionando 1px extra
            c.drawString(x_temp, y, palavras[-1])  # Última palavra na posição final
        
        y -= 20  # Espaçamento entre as linhas
    return y


def wrap_text(texto, largura_texto, c):
    """Quebra o texto em linhas que cabem na largura especificada."""
    palavras = texto.split()
    linhas = []
    linha_atual = ""
    
    for palavra in palavras:
        largura_linha = c.stringWidth(linha_atual + " " + palavra, "Helvetica", 12)
        if largura_linha <= largura_texto:
            linha_atual += " " + palavra
        else:
            linhas.append(linha_atual.strip())
            linha_atual = palavra
    
    if linha_atual:
        linhas.append(linha_atual.strip())

    return linhas

def gerar_texto_parecer(natureza, solicitacao, docente, parecerista_1, parecerista_2, carga_horaria):
    """Gera o texto do parecer conforme a Natureza e a Solicitação."""
    
    parecer_base = f"A comissão de pareceristas composta pelos professores: {parecerista_1} e {parecerista_2} avaliou o projeto de {natureza.lower()} do professor {docente}."
    
    if solicitacao == "Novo":
        parecer_base += f" O projeto foi analisado quanto à sua relevância acadêmica e institucional, e após avaliação favorável, a comissão parecerista declara Parecer Favorável para sua realização com carga horária de {carga_horaria} horas."
        parecer_base += "\n\nO projeto proposto prevê atender os critérios exigidos na resolução vigente N. 4.918, DE 25 DE ABRIL DE 2017."

    elif solicitacao == "Encerramento":
        parecer_base += f" Após análise da documentação final e cumprimento dos objetivos estabelecidos, a comissão parecerista atesta o encerramento do projeto e aprova a finalização das atividades realizadas pelo docente."
        parecer_base += "\n\nO projeto atendeu aos diversos critérios exigidos na resolução vigente N. 4.918, DE 25 DE ABRIL DE 2017 e contribui significativamente para o desenvolvimento acadêmico e institucional."

    elif solicitacao == "Renovação":
        parecer_base += f" Com base na análise dos relatórios apresentados e no impacto positivo do projeto, a comissão parecerista aprova sua renovação, recomendando continuidade das ações previstas com carga horária de {carga_horaria} horas."
        parecer_base += "\n\nO projeto atendeu aos diversos critérios exigidos na resolução vigente N. 4.918, DE 25 DE ABRIL DE 2017 e contribui significativamente para o desenvolvimento acadêmico e institucional."

    
    return parecer_base

def obter_data_formatada():
    """Retorna a data atual formatada corretamente em português."""
    locale.setlocale(locale.LC_TIME, "C")
    return datetime.now().strftime("%d/%m/%Y")

import os
import sys
import unittest


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from PyPDF2 import PdfReader

from SERVER.CORE.PDFGenerator import (  # noqa: E402
    gerar_pdf_projetos,
    gerar_pdf_declaracao_projeto,
    obter_data_extenso,
)


def _normalizar_texto(texto):
    return "".join(texto.lower().split())


class TestPDFGenerator(unittest.TestCase):
    def setUp(self):
        self.resposta = [
            "0",  # índice 0 não utilizado
            "Elton Sarmanho Siqueira",  # docente
            "Allan Barbosa Costa",  # parecerista_1
            "Carlos dos Santos Portela",  # parecerista_2
            "Dashboard Interativo com IA e Sistema Preditivo para Recomendação de Estratégias de Ensino Baseado em Análise de Desempenho Acadêmico",
            "120",  # carga_horaria
            "PIBIC-PRODOUTOR",  # edital
            "Extensão",  # natureza
            "2024",  # ano_edital
            "Novo",  # solicitacao
        ]
        self._arquivos_gerados = []

    def tearDown(self):
        for caminho in self._arquivos_gerados:
            if caminho and os.path.exists(caminho):
                os.remove(caminho)

    def test_parecer_pdf_gerado(self):
        caminho_pdf = gerar_pdf_projetos(self.resposta)
        self._arquivos_gerados.append(caminho_pdf)

        self.assertIsNotNone(caminho_pdf)
        self.assertTrue(os.path.exists(caminho_pdf))

        with open(caminho_pdf, "rb") as arquivo:
            reader = PdfReader(arquivo)
            texto = "\n".join(page.extract_text() or "" for page in reader.pages)

        self.assertIn(_normalizar_texto(self.resposta[4]), _normalizar_texto(texto))
        self.assertIn(_normalizar_texto(self.resposta[1]), _normalizar_texto(texto))

    def test_declaracao_pdf_conteudo(self):
        caminho_pdf = gerar_pdf_declaracao_projeto(self.resposta)
        self._arquivos_gerados.append(caminho_pdf)

        self.assertIsNotNone(caminho_pdf)
        self.assertTrue(os.path.exists(caminho_pdf))

        with open(caminho_pdf, "rb") as arquivo:
            reader = PdfReader(arquivo)
            conteudo = "\n".join(page.extract_text() or "" for page in reader.pages)

        conteudo_normalizado = _normalizar_texto(conteudo)

        self.assertIn(_normalizar_texto(self.resposta[4]), conteudo_normalizado)
        self.assertIn(_normalizar_texto(self.resposta[1]), conteudo_normalizado)
        self.assertIn(_normalizar_texto(obter_data_extenso()), conteudo_normalizado)


if __name__ == "__main__":
	unittest.main()

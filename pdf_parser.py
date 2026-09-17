"""
PDF Parser para Motor de Decisão Tributária
Extrai dados de PDFs: PGDAS-D, Entradas, Saídas, Serviços
"""

import pdfplumber
import re
from typing import Dict, List, Any
from pathlib import Path


class PDFParser:
    """Parser de documentos fiscais PDF"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pdf = None

    def abrir(self):
        """Abre o PDF"""
        self.pdf = pdfplumber.open(self.pdf_path)
        return self.pdf

    def fechar(self):
        """Fecha o PDF"""
        if self.pdf:
            self.pdf.close()

    def extrair_texto_completo(self) -> str:
        """Extrai todo o texto do PDF"""
        if not self.pdf:
            self.abrir()

        texto_completo = ""
        for pagina in self.pdf.pages:
            texto_completo += pagina.extract_text() or ""

        return texto_completo

    def extrair_tabelas(self) -> List[List[Dict]]:
        """Extrai todas as tabelas do PDF"""
        if not self.pdf:
            self.abrir()

        tabelas = []
        for pagina in self.pdf.pages:
            tabelas_pagina = pagina.extract_tables()
            if tabelas_pagina:
                tabelas.extend(tabelas_pagina)

        return tabelas

    @staticmethod
    def normalizar_cnpj(cnpj_str: str) -> str:
        """Normaliza CNPJ para formato XX.XXX.XXX/XXXX-XX"""
        if not cnpj_str:
            return ""

        # Remove caracteres não numéricos
        cnpj_limpo = re.sub(r'\D', '', cnpj_str)

        # Se tem menos de 14 dígitos, tenta preencher com zeros
        if len(cnpj_limpo) < 14:
            cnpj_limpo = cnpj_limpo.ljust(14, '0')

        # Formato: XX.XXX.XXX/XXXX-XX
        if len(cnpj_limpo) >= 14:
            return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:14]}"

        return cnpj_limpo

    @staticmethod
    def normalizar_valor(valor_str: str) -> float:
        """Converte string de valor para float"""
        if not valor_str:
            return 0.0

        # Remove espaços
        valor_str = valor_str.strip()

        # Remove prefixos de moeda
        valor_str = re.sub(r'[R$\s]', '', valor_str)

        # Trata separadores decimais brasileiros (. ou ,)
        # Se houver mais de um separador, o último é decimal
        if ',' in valor_str and '.' in valor_str:
            # Brasileiro: 1.234.567,89
            valor_str = valor_str.replace('.', '').replace(',', '.')
        elif ',' in valor_str:
            # Pode ser 1234,56 ou 1,234.56
            # Conta quantas vezes aparece
            partes = valor_str.split(',')
            if len(partes) > 2:
                valor_str = valor_str.replace(',', '')
            else:
                valor_str = valor_str.replace(',', '.')

        try:
            return float(valor_str)
        except ValueError:
            return 0.0

    def identificar_tipo_documento(self, texto: str = None) -> str:
        """Identifica o tipo de documento (PGDAS, Entrada, Saída, Serviço)"""
        if not texto:
            texto = self.extrair_texto_completo()

        texto_upper = texto.upper()

        if 'PGDAS' in texto_upper or 'DAS' in texto_upper:
            return 'PGDAS'
        elif 'ENTRADA' in texto_upper or 'AQUISIÇÃO' in texto_upper:
            return 'ENTRADA'
        elif 'SAÍDA' in texto_upper or 'VENDA' in texto_upper or 'MERCADORIA' in texto_upper:
            return 'SAIDA'
        elif 'SERVIÇO' in texto_upper or 'SERVIÇOS' in texto_upper:
            return 'SERVICO'

        return 'DESCONHECIDO'


class ParserPGDAS(PDFParser):
    """Parser específico para PGDAS-D"""

    def extrair_dados(self) -> Dict[str, Any]:
        """Extrai dados do PGDAS-D"""
        if not self.pdf:
            self.abrir()

        texto = self.extrair_texto_completo()
        dados = {
            'tipo': 'PGDAS',
            'cnpj': self._extrair_cnpj(texto),
            'razao_social': self._extrair_razao_social(texto),
            'rbt12': self._extrair_rbt12(texto),
            'das': self._extrair_das(texto),
            'periodo': self._extrair_periodo(texto),
        }

        return dados

    @staticmethod
    def _extrair_cnpj(texto: str) -> str:
        """Extrai CNPJ do PGDAS"""
        # Padrão: XX.XXX.XXX/XXXX-XX
        padrao = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
        match = re.search(padrao, texto)
        if match:
            return match.group()
        return ""

    @staticmethod
    def _extrair_razao_social(texto: str) -> str:
        """Extrai Razão Social"""
        # Procura por linhas que contêm "Razão Social"
        linhas = texto.split('\n')
        for i, linha in enumerate(linhas):
            if 'razão social' in linha.lower():
                # Tenta pegar a próxima linha ou o resto da linha
                if i + 1 < len(linhas):
                    return linhas[i + 1].strip()
        return ""

    @staticmethod
    def _extrair_rbt12(texto: str) -> float:
        """Extrai RBT12"""
        # Procura por "RBT12" ou "Receita Bruta"
        linhas = texto.split('\n')
        for linha in linhas:
            if 'RBT12' in linha.upper() or 'RECEITA BRUTA TOTAL' in linha.upper():
                # Tenta extrair número da linha
                valores = re.findall(r'[\d.,]+', linha)
                if valores:
                    return PDFParser.normalizar_valor(valores[-1])
        return 0.0

    @staticmethod
    def _extrair_das(texto: str) -> float:
        """Extrai DAS"""
        # Procura por "DAS" ou "Débito"
        linhas = texto.split('\n')
        for linha in linhas:
            if 'DAS' in linha.upper() and 'débito' in linha.lower():
                valores = re.findall(r'[\d.,]+', linha)
                if valores:
                    return PDFParser.normalizar_valor(valores[-1])
        return 0.0

    @staticmethod
    def _extrair_periodo(texto: str) -> str:
        """Extrai período do documento"""
        # Procura por data no formato MM/YYYY
        padrao = r'(\d{2})/(\d{4})'
        match = re.search(padrao, texto)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        return ""


class ParserAcompanhamento(PDFParser):
    """Parser para Acompanhamentos (Entradas, Saídas, Serviços)"""

    def extrair_dados(self) -> Dict[str, Any]:
        """Extrai dados do acompanhamento"""
        if not self.pdf:
            self.abrir()

        tipo = self.identificar_tipo_documento()

        dados = {
            'tipo': tipo,
            'periodo': self._extrair_periodo(),
            'empresa_cnpj': self._extrair_cnpj_empresa(),
            'total': self._extrair_total(),
            'itens': self._extrair_itens(),
        }

        return dados

    def _extrair_periodo(self) -> str:
        """Extrai período de competência"""
        texto = self.extrair_texto_completo()

        # Procura por "01/01/2026 a 31/08/2026"
        padrao = r'(\d{2}/\d{2}/\d{4})\s*a\s*(\d{2}/\d{2}/\d{4})'
        match = re.search(padrao, texto)
        if match:
            return f"{match.group(1)} a {match.group(2)}"

        return ""

    def _extrair_cnpj_empresa(self) -> str:
        """Extrai CNPJ da empresa"""
        texto = self.extrair_texto_completo()

        # Primeira ocorrência de CNPJ é geralmente da empresa
        padrao = r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
        match = re.search(padrao, texto)
        if match:
            return match.group()

        return ""

    def _extrair_total(self) -> float:
        """Extrai valor total do acompanhamento"""
        tabelas = self.extrair_tabelas()

        # Procura por "Total Geral" ou similar na última linha
        for tabela in tabelas:
            if isinstance(tabela, list) and len(tabela) > 0:
                ultima_linha = tabela[-1]
                if isinstance(ultima_linha, (list, dict)):
                    # Tenta extrair valor
                    valores = []
                    if isinstance(ultima_linha, list):
                        valores = [str(v) for v in ultima_linha if v]
                    elif isinstance(ultima_linha, dict):
                        valores = [str(v) for v in ultima_linha.values() if v]

                    # Procura pelo último valor numérico
                    for valor in reversed(valores):
                        valor_float = self.normalizar_valor(valor)
                        if valor_float > 0:
                            return valor_float

        return 0.0

    def _extrair_itens(self) -> List[Dict[str, Any]]:
        """Extrai itens (fornecedores/clientes) do acompanhamento"""
        tabelas = self.extrair_tabelas()
        itens = []

        for tabela in tabelas:
            if not isinstance(tabela, list):
                continue

            # Pula cabeçalho
            linhas_dados = tabela[1:] if len(tabela) > 1 else tabela

            for linha in linhas_dados:
                if not isinstance(linha, (list, tuple)):
                    continue

                # Procura por CNPJ na linha
                cnpj = None
                razao_social = None
                valor = 0.0

                for celula in linha:
                    celula_str = str(celula) if celula else ""

                    # Verifica se é CNPJ
                    if re.match(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}', celula_str):
                        cnpj = self.normalizar_cnpj(celula_str)
                    # Verifica se é valor
                    elif self.normalizar_valor(celula_str) > 0:
                        valor = max(valor, self.normalizar_valor(celula_str))
                    # Trata como razão social se for texto longo
                    elif len(celula_str) > 10 and not razao_social:
                        razao_social = celula_str.strip()

                if cnpj or razao_social:
                    item = {
                        'cnpj': cnpj or '',
                        'razao_social': razao_social or '',
                        'valor': valor,
                    }

                    # Evita duplicatas
                    if item not in itens:
                        itens.append(item)

        return itens


def processar_pdf(caminho_pdf: str) -> Dict[str, Any]:
    """Processa um PDF e retorna dados estruturados"""

    parser = PDFParser(caminho_pdf)
    tipo = parser.identificar_tipo_documento()

    try:
        if tipo == 'PGDAS':
            parser_especifico = ParserPGDAS(caminho_pdf)
            dados = parser_especifico.extrair_dados()
        else:
            parser_especifico = ParserAcompanhamento(caminho_pdf)
            dados = parser_especifico.extrair_dados()

        parser_especifico.fechar()

        return {
            'sucesso': True,
            'tipo': tipo,
            'dados': dados,
            'arquivo': Path(caminho_pdf).name,
        }

    except Exception as e:
        return {
            'sucesso': False,
            'tipo': tipo,
            'erro': str(e),
            'arquivo': Path(caminho_pdf).name,
        }

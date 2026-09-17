"""
Motor de Decisão Tributária — FastAPI Backend
Versão: 0.5.0
Descrição: API REST para análise tributária com upload de PDFs e cálculos
Com suporte a extração automática de dados de documentos fiscais
"""

import os
import json
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Importar o parser de PDFs
try:
    from pdf_parser import PDFParser, ParserPGDAS, ParserAcompanhamento, processar_pdf
    PDF_PARSER_AVAILABLE = True
    print("✅ pdf_parser.py carregado com sucesso")
except ImportError as e:
    PDF_PARSER_AVAILABLE = False
    print(f"⚠️ AVISO: pdf_parser.py não encontrado - {str(e)}")
except Exception as e:
    PDF_PARSER_AVAILABLE = False
    print(f"⚠️ ERRO ao carregar pdf_parser.py: {str(e)}")

# =========================================================================
# CONFIGURAÇÃO
# =========================================================================

load_dotenv()

app = FastAPI(
    title="Motor de Decisão Tributária",
    description="Análise tributária para Simples Nacional vs Híbrido IBS/CBS",
    version="0.4.0"
)

# CORS — Permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção: ["https://seu-dominio.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretórios
UPLOAD_DIR = Path("uploads")
REPORTS_DIR = Path("reports")
UPLOAD_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Ler index.html uma única vez no startup
HTML_CONTENT = None
def load_html():
    global HTML_CONTENT
    html_path = Path("index.html")
    if html_path.exists():
        with open(html_path, "r", encoding="utf-8") as f:
            HTML_CONTENT = f.read()
    else:
        HTML_CONTENT = "<h1>Dashboard não encontrado</h1>"

# =========================================================================
# MODELOS DE DADOS
# =========================================================================

class Fornecedor(BaseModel):
    cnpj: str
    razao_social: str
    compras: float
    regime: Optional[str] = "A validar"
    credito_ibs: float = 0.0
    credito_cbs: float = 0.0
    observacao: Optional[str] = None

class Cliente(BaseModel):
    cnpj: str
    razao_social: str
    faturamento: float
    percentual_faturamento: float = 0.0
    regime: Optional[str] = "A validar"
    risco_comercial: str = "MÉDIO"
    observacao: Optional[str] = None

class Empresa(BaseModel):
    cnpj: str
    razao_social: str
    cidade: str
    uf: str
    regime: str = "Simples Nacional"
    anexo: str = "III"
    rbt12: float
    das: float
    data_documento: Optional[str] = None

class DadosEntrada(BaseModel):
    empresa: Empresa
    fornecedores: List[Fornecedor]
    clientes: List[Cliente]
    cbs_estimada: float = 8.80

class ResultadoSimulacao(BaseModel):
    simulacao_id: str
    timestamp: str
    empresa: Empresa
    cenario_2026_real: float
    cenario_2027_simples_puro: float
    cenario_2027_hibrido: float
    recomendacao: str
    economia_anual: float
    confianca: str
    fornecedores: List[Fornecedor]
    clientes: List[Cliente]
    observacoes: List[str]

class DadosExtraidos(BaseModel):
    """Dados extraídos de um documento PDF"""
    arquivo: str
    tipo: str
    sucesso: bool
    dados: Dict[str, Any] = {}
    erro: Optional[str] = None
    timestamp: str = None

class RespostaUpload(BaseModel):
    """Resposta do upload de PDFs"""
    upload_id: str
    arquivos_recebidos: List[str]
    status: str
    timestamp: str

# =========================================================================
# ROTAS
# =========================================================================

@app.get("/health")
def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "upload_dir": str(UPLOAD_DIR.exists()),
        "reports_dir": str(REPORTS_DIR.exists()),
        "pdf_parser_available": PDF_PARSER_AVAILABLE
    }

@app.get("/api/status")
def api_status():
    """Status da API e dependências"""
    return JSONResponse(
        status_code=200,
        content={
            "versao": "0.5.0",
            "status": "online",
            "pdf_parser_disponivel": PDF_PARSER_AVAILABLE,
            "upload_dir_existe": UPLOAD_DIR.exists(),
            "reports_dir_existe": REPORTS_DIR.exists(),
            "timestamp": datetime.now().isoformat()
        }
    )

@app.post("/api/upload")
async def upload_arquivos(
    files: List[UploadFile] = File(...),
):
    """
    Upload de arquivos PDF (PGDAS, Entradas, Saídas, Serviços)

    Retorna:
    - upload_id: UUID para referência dos arquivos
    - arquivos_recebidos: lista de nomes
    - status: "pendente_processamento"
    """
    if not PDF_PARSER_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={
                "erro": "PDF Parser não disponível. Verifique se pdfplumber está instalado.",
                "status": "erro_indisponivel"
            }
        )

    upload_id = str(uuid.uuid4())
    upload_subdir = UPLOAD_DIR / upload_id
    upload_subdir.mkdir(exist_ok=True)

    arquivos_salvos = []

    for file in files:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail=f"Arquivo {file.filename} não é PDF"
            )

        filepath = upload_subdir / file.filename
        contents = await file.read()

        with open(filepath, "wb") as f:
            f.write(contents)

        arquivos_salvos.append(file.filename)

    return JSONResponse(
        status_code=200,
        content={
            "upload_id": upload_id,
            "arquivos_recebidos": arquivos_salvos,
            "status": "pendente_processamento",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.post("/api/processar-pdfs")
async def processar_pdfs_endpoint(upload_id: str):
    """
    Processa PDFs de um upload e extrai dados estruturados

    Retorna lista de dados extraídos de cada documento
    """
    if not PDF_PARSER_AVAILABLE:
        return JSONResponse(
            status_code=503,
            content={
                "erro": "PDF Parser não disponível",
                "upload_id": upload_id,
                "status": "erro_indisponivel"
            }
        )

    upload_subdir = UPLOAD_DIR / upload_id

    if not upload_subdir.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Upload com ID {upload_id} não encontrado"
        )

    arquivos_pdf = list(upload_subdir.glob("*.pdf"))

    if not arquivos_pdf:
        raise HTTPException(
            status_code=400,
            detail="Nenhum arquivo PDF encontrado no upload"
        )

    resultados_extracao = []

    for arquivo_pdf in arquivos_pdf:
        try:
            resultado = processar_pdf(str(arquivo_pdf))
            resultado['timestamp'] = datetime.now().isoformat()
            resultados_extracao.append(resultado)
        except Exception as e:
            resultados_extracao.append({
                'arquivo': arquivo_pdf.name,
                'sucesso': False,
                'erro': str(e),
                'timestamp': datetime.now().isoformat()
            })

    # Salvar resultados da extração
    extracao_path = REPORTS_DIR / f"extracao_{upload_id}.json"
    with open(extracao_path, "w", encoding="utf-8") as f:
        json.dump(resultados_extracao, f, ensure_ascii=False, indent=2, default=str)

    return JSONResponse(
        status_code=200,
        content={
            "upload_id": upload_id,
            "total_arquivos": len(arquivos_pdf),
            "sucessos": len([r for r in resultados_extracao if r.get('sucesso', False)]),
            "erros": len([r for r in resultados_extracao if not r.get('sucesso', True)]),
            "dados_extraidos": resultados_extracao,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.get("/api/dados-extraidos/{upload_id}")
async def obter_dados_extraidos(upload_id: str):
    """
    Obtém dados extraídos de um upload processado
    """
    extracao_path = REPORTS_DIR / f"extracao_{upload_id}.json"

    if not extracao_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Dados extraídos para upload {upload_id} não encontrados"
        )

    with open(extracao_path, "r", encoding="utf-8") as f:
        dados = json.load(f)

    return JSONResponse(
        status_code=200,
        content=dados
    )

@app.post("/api/calcular")
async def calcular_cenarios(dados: DadosEntrada):
    """
    Calcula os três cenários tributários:
    1. 2026 Real (validação)
    2. 2027 Simples Puro
    3. 2027 Simples Híbrido

    Retorna simulacao_id e resultados
    """

    simulacao_id = str(uuid.uuid4())

    # =====================================================================
    # CÁLCULOS (VERSÃO SIMPLIFICADA PARA MVP)
    # =====================================================================

    try:
        empresa = dados.empresa
        fornecedores = dados.fornecedores
        clientes = dados.clientes
        cbs = dados.cbs_estimada

        # Validação básica
        if not empresa.cnpj or not empresa.rbt12:
            raise ValueError("CNPJ ou RBT12 faltando")

        # =====================================================================
        # CENÁRIO 2026 REAL
        # =====================================================================

        valor_2026 = empresa.das

        # =====================================================================
        # CENÁRIO 2027 SIMPLES PURO
        # =====================================================================

        # Mantém alíquota efetiva de 2026
        aliquota_efetiva_2026 = (empresa.das / empresa.rbt12) * 100
        valor_2027_simples = (aliquota_efetiva_2026 / 100) * empresa.rbt12

        # =====================================================================
        # CENÁRIO 2027 SIMPLES HÍBRIDO
        # =====================================================================

        # Tributos mantidos no Simples (85% do DAS)
        tributos_simples = empresa.das * 0.85

        # Cálculos de crédito e débito
        total_vendas = sum(c.faturamento for c in clientes)
        total_compras = sum(f.compras for f in fornecedores)

        # IBS (0,10%) e CBS (estimada)
        ibs_aliquota = 0.001  # 0,10%
        cbs_aliquota = cbs / 100

        # Débitos
        ibs_debito = total_vendas * ibs_aliquota
        cbs_debito = total_vendas * cbs_aliquota

        # Créditos (simplificado: 50% das compras no regime regular)
        total_compras_regular = total_compras * 0.5
        ibs_credito = total_compras_regular * ibs_aliquota
        cbs_credito = total_compras_regular * cbs_aliquota

        # IBS/CBS Líquido
        ibs_liquido = max(0, ibs_debito - ibs_credito)
        cbs_liquido = max(0, cbs_debito - cbs_credito)

        # Total híbrido
        valor_2027_hibrido = tributos_simples + ibs_liquido + cbs_liquido

        # =====================================================================
        # RECOMENDAÇÃO
        # =====================================================================

        economia = valor_2027_simples - valor_2027_hibrido

        if economia > 0:
            recomendacao = "MANTER_SIMPLES_NACIONAL"
            confianca = "ALTA"
        else:
            recomendacao = "CONSIDERAR_HIBRIDO"
            confianca = "MÉDIA"

        # =====================================================================
        # OBSERVAÇÕES
        # =====================================================================

        observacoes = []

        if economia > 50000:
            observacoes.append(f"Economia significativa: R$ {economia:,.2f}")

        concentracao_cliente_principal = max(
            (c.faturamento / total_vendas) * 100 for c in clientes
        ) if clientes else 0

        if concentracao_cliente_principal > 80:
            observacoes.append(
                f"⚠️ Concentração crítica: {concentracao_cliente_principal:.1f}% "
                f"do faturamento em um único cliente"
            )

        observacoes.append(f"CBS utilizada: {cbs}% (estimada)")

        # =====================================================================
        # RESULTADO FINAL
        # =====================================================================

        resultado = ResultadoSimulacao(
            simulacao_id=simulacao_id,
            timestamp=datetime.now().isoformat(),
            empresa=empresa,
            cenario_2026_real=valor_2026,
            cenario_2027_simples_puro=valor_2027_simples,
            cenario_2027_hibrido=valor_2027_hibrido,
            recomendacao=recomendacao,
            economia_anual=abs(economia),
            confianca=confianca,
            fornecedores=fornecedores,
            clientes=clientes,
            observacoes=observacoes
        )

        # Salvar resultado
        report_path = REPORTS_DIR / f"{simulacao_id}.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(resultado.dict(), f, ensure_ascii=False, indent=2, default=str)

        return JSONResponse(
            status_code=200,
            content={
                "simulacao_id": simulacao_id,
                "status": "sucesso",
                "cenario_2026_real": valor_2026,
                "cenario_2027_simples_puro": valor_2027_simples,
                "cenario_2027_hibrido": valor_2027_hibrido,
                "recomendacao": recomendacao,
                "economia_anual": abs(economia),
                "confianca": confianca,
                "observacoes": observacoes,
                "timestamp": datetime.now().isoformat()
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "erro": str(e),
                "simulacao_id": simulacao_id,
                "status": "erro"
            }
        )

@app.get("/api/resultado/{simulacao_id}")
async def obter_resultado(simulacao_id: str):
    """Obtém resultado completo da simulação"""

    report_path = REPORTS_DIR / f"{simulacao_id}.json"

    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Simulação não encontrada")

    with open(report_path, "r", encoding="utf-8") as f:
        resultado = json.load(f)

    return resultado

@app.get("/api/resultado/{simulacao_id}/download")
async def download_resultado(simulacao_id: str):
    """Download do resultado em JSON"""

    report_path = REPORTS_DIR / f"{simulacao_id}.json"

    if not report_path.exists():
        raise HTTPException(status_code=404, detail="Simulação não encontrada")

    return FileResponse(
        report_path,
        filename=f"resultado_{simulacao_id[:8]}.json",
        media_type="application/json"
    )

@app.post("/api/resultado/{simulacao_id}/pdf")
async def gerar_pdf(simulacao_id: str):
    """
    Gera e retorna PDF do relatório
    (Implementado na Fase 2)
    """
    return JSONResponse(
        status_code=200,
        content={
            "status": "em_desenvolvimento",
            "mensagem": "Geração de PDF será implementada na Fase 2",
            "simulacao_id": simulacao_id
        }
    )

# =========================================================================
# STARTUP
# =========================================================================

# =========================================================================
# SERVIR FRONTEND (index.html)
# =========================================================================

@app.get("/")
async def serve_frontend():
    """Serve o dashboard HTML"""
    if HTML_CONTENT:
        return HTMLResponse(content=HTML_CONTENT)
    return HTMLResponse(content="<h1>Erro: index.html não encontrado</h1>", status_code=404)

# =========================================================================
# STARTUP
# =========================================================================

@app.on_event("startup")
async def startup_event():
    load_html()  # Carregar HTML no startup
    print("✅ Motor de Decisão Tributária — API iniciada")
    print(f"📁 Upload dir: {UPLOAD_DIR.absolute()}")
    print(f"📁 Reports dir: {REPORTS_DIR.absolute()}")
    if HTML_CONTENT:
        print("✅ Dashboard HTML carregado com sucesso")
    else:
        print("⚠️ AVISO: index.html não encontrado")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )

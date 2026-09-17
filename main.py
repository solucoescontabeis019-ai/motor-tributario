"""
Motor de Decisão Tributária — FastAPI Backend
Versão: 0.5.1
Descrição: API REST para análise tributária com upload de PDFs e cálculos
Novo: Endpoint /api/empresa/dados retorna dados consolidados
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
    version="0.5.1"
)

# CORS — Permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretórios
UPLOAD_DIR = Path("uploads")
REPORTS_DIR = Path("reports")
UPLOAD_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Carregar dados consolidados no startup
DADOS_EMPRESA = {}
def carregar_dados_empresa():
    global DADOS_EMPRESA
    try:
        dados_path = Path("static/empresa_dados.json")
        if dados_path.exists():
            with open(dados_path, "r", encoding="utf-8") as f:
                DADOS_EMPRESA = json.load(f)
            print("✅ Dados consolidados carregados: empresa_dados.json")
        else:
            print("⚠️ AVISO: empresa_dados.json não encontrado em static/")
    except Exception as e:
        print(f"⚠️ ERRO ao carregar dados: {str(e)}")

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
# INICIALIZAÇÃO
# =========================================================================

@app.on_event("startup")
async def startup_event():
    load_html()
    carregar_dados_empresa()
    print("✅ Motor de Decisão Tributária — API iniciada")
    print(f"📁 Upload dir: {UPLOAD_DIR}")
    print(f"📁 Reports dir: {REPORTS_DIR}")
    print(f"✅ Dashboard HTML carregado com sucesso")

# =========================================================================
# ROTAS
# =========================================================================

@app.get("/")
def root():
    """Retorna o HTML do dashboard"""
    if HTML_CONTENT:
        return HTMLResponse(content=HTML_CONTENT)
    return {"message": "Dashboard não encontrado"}

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
    pdfplumber_version = "não instalado"
    if PDF_PARSER_AVAILABLE:
        try:
            import pdfplumber
            pdfplumber_version = pdfplumber.__version__ if hasattr(pdfplumber, '__version__') else "instalado (versão desconhecida)"
        except:
            pdfplumber_version = "erro ao verificar versão"

    return JSONResponse(
        status_code=200,
        content={
            "versao": "0.5.1",
            "status": "online",
            "pdf_parser_disponivel": PDF_PARSER_AVAILABLE,
            "pdfplumber_status": pdfplumber_version,
            "upload_dir_existe": UPLOAD_DIR.exists(),
            "reports_dir_existe": REPORTS_DIR.exists(),
            "timestamp": datetime.now().isoformat()
        }
    )

@app.get("/api/debug")
def api_debug():
    """Informações de debug para diagnóstico"""
    info = {
        "versao": "0.5.1",
        "python_version": __import__('sys').version,
        "pdf_parser_available": PDF_PARSER_AVAILABLE,
        "upload_dir_exists": UPLOAD_DIR.exists(),
        "reports_dir_exists": REPORTS_DIR.exists(),
        "upload_dir_path": str(UPLOAD_DIR.absolute()),
        "reports_dir_path": str(REPORTS_DIR.absolute()),
        "timestamp": datetime.now().isoformat(),
    }

    try:
        import pdfplumber
        info["pdfplumber_available"] = True
        info["pdfplumber_version"] = getattr(pdfplumber, '__version__', 'desconhecido')
    except ImportError as e:
        info["pdfplumber_available"] = False
        info["pdfplumber_error"] = str(e)

    try:
        import pdf_parser
        info["pdf_parser_module_available"] = True
    except ImportError as e:
        info["pdf_parser_module_available"] = False
        info["pdf_parser_module_error"] = str(e)

    return JSONResponse(status_code=200, content=info)

# =========================================================================
# NOVO ENDPOINT: RETORNA DADOS CONSOLIDADOS DA EMPRESA
# =========================================================================

@app.get("/api/empresa/dados")
def obter_dados_empresa():
    """
    Retorna os dados consolidados da empresa extraídos dos PDFs

    Inclui:
    - Dados da empresa (CNPJ, RBT12, DAS, etc)
    - Lista de fornecedores com totais consolidados
    - Lista de clientes com totais consolidados
    - Validações cruzadas
    - Achados críticos
    """
    if not DADOS_EMPRESA:
        return JSONResponse(
            status_code=404,
            content={
                "erro": "Dados da empresa não carregados",
                "status": "não_disponível",
                "mensagem": "Execute a importação de PDFs primeiro"
            }
        )

    return JSONResponse(
        status_code=200,
        content=DADOS_EMPRESA
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

    try:
        empresa = dados.empresa
        fornecedores = dados.fornecedores
        clientes = dados.clientes
        cbs = dados.cbs_estimada

        if not empresa.cnpj or not empresa.rbt12:
            raise ValueError("CNPJ ou RBT12 faltando")

        # CENÁRIO 2026 REAL
        valor_2026 = empresa.das

        # CENÁRIO 2027 SIMPLES PURO
        aliquota_efetiva_2026 = (empresa.das / empresa.rbt12) * 100
        valor_2027_simples = (aliquota_efetiva_2026 / 100) * empresa.rbt12

        # CENÁRIO 2027 SIMPLES HÍBRIDO
        tributos_simples = empresa.das * 0.85
        total_vendas = sum(c.faturamento for c in clientes)
        total_compras = sum(f.compras for f in fornecedores)

        ibs_estimado = (total_vendas * 0.0010)  # 0.10% de IBS
        cbs_estimado = (total_vendas * (cbs / 100))
        creditos_estimados = (total_compras * (cbs / 100)) * 0.50

        valor_2027_hibrido = tributos_simples + ibs_estimado + (cbs_estimado - creditos_estimados)

        # RECOMENDAÇÃO
        if valor_2027_hibrido < valor_2027_simples:
            recomendacao = "🟢 CONSIDERAR HÍBRIDO"
            economia = valor_2027_simples - valor_2027_hibrido
        else:
            recomendacao = "🔴 MANTER SIMPLES PURO"
            economia = 0

        resultado = {
            "simulacao_id": simulacao_id,
            "timestamp": datetime.now().isoformat(),
            "empresa_cnpj": empresa.cnpj,
            "cenario_2026_real": round(valor_2026, 2),
            "cenario_2027_simples_puro": round(valor_2027_simples, 2),
            "cenario_2027_hibrido": round(valor_2027_hibrido, 2),
            "recomendacao": recomendacao,
            "economia_anual": round(economia, 2),
            "confianca": "BAIXA - Dados incompletos (regimes não validados)",
            "total_fornecedores": len(fornecedores),
            "total_clientes": len(clientes),
            "observacoes": [
                "Simulação baseada em estimativas",
                "Aguardando validação de regimes tributários",
                "CBS utilizada: estimativa"
            ]
        }

        return JSONResponse(status_code=200, content=resultado)

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "erro": str(e),
                "simulacao_id": simulacao_id,
                "timestamp": datetime.now().isoformat()
            }
        )

# =========================================================================
# TRATAMENTO DE ERROS
# =========================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"erro": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "erro": "Erro interno do servidor",
            "detalhes": str(exc)
        }
    )

# =========================================================================
# FIM
# =========================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

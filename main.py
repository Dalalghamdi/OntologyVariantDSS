from pathlib import Path
import csv, io, json
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .graph import KnowledgeGraph
from .acmg import classify, strength
from .pubmed import search_pubmed

BASE_DIR = Path(__file__).resolve().parent.parent
GRAPH_PATH = BASE_DIR / "data" / "knowledge_graph.ttl"
kg = KnowledgeGraph(str(GRAPH_PATH))
app = FastAPI(title="Ontology Variant DSS", version="0.1.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request":request, "variants":kg.variants()})

@app.get("/variant/new", response_class=HTMLResponse)
def new_variant(request: Request):
    return templates.TemplateResponse("new_variant.html", {"request":request})

@app.post("/variant/new")
def create_variant(variant: str = Form(...), gene: str = Form(""), disease: str = Form(""), phenotypes: str = Form(""), allele_frequency: str = Form(""), clinvar_significance: str = Form(""), criteria: str = Form(""), evidence_notes: str = Form(""), evidence_source: str = Form(""), pmid: str = Form("")):
    rec={"variant":variant.strip(),"gene":gene.strip(),"disease":disease.strip(),"phenotypes":[x.strip() for x in phenotypes.split(",") if x.strip()],"allele_frequency":float(allele_frequency) if allele_frequency.strip() else None,"clinvar_significance":clinvar_significance.strip()}
    v=kg.add_variant(rec)
    codes=[x.strip().upper() for x in criteria.replace(";",",").split(",") if x.strip()]
    for code in codes:
        kg.add_evidence(v,{"criterion":code,"strength":strength(code),"description":evidence_notes.strip() or f"Evidence assessed as {code}","source":evidence_source.strip() or "User-assessed evidence","pmid":pmid.strip()})
    result=classify(codes); kg.add_classification(v,result); kg.save()
    return RedirectResponse(url=f"/variant?uri={v}", status_code=303)

@app.get("/variant", response_class=HTMLResponse)
def variant_detail(request: Request, uri: str):
    return templates.TemplateResponse("variant.html", {"request":request, "x":kg.variant_detail(uri)})

@app.get("/pubmed", response_class=HTMLResponse)
def pubmed_page(request: Request, q: str = ""):
    results=[]; error=None
    if q:
        try: results=search_pubmed(q)
        except Exception as e: error=str(e)
    return templates.TemplateResponse("pubmed.html", {"request":request,"q":q,"results":results,"error":error})

@app.get("/sparql", response_class=HTMLResponse)
def sparql_page(request: Request):
    default='''PREFIX dss: <https://example.org/variant-dss/>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nSELECT ?variant ?classification WHERE {\n  ?v a dss:Variant ; rdfs:label ?variant .\n  OPTIONAL { ?v dss:hasClassification ?classification }\n} ORDER BY ?variant'''
    return templates.TemplateResponse("sparql.html", {"request":request,"query":default,"columns":[],"rows":[],"error":None})

@app.post("/sparql", response_class=HTMLResponse)
def sparql_run(request: Request, query: str = Form(...)):
    try: cols, rows=kg.sparql(query); err=None
    except Exception as e: cols, rows, err=[],[],str(e)
    return templates.TemplateResponse("sparql.html", {"request":request,"query":query,"columns":cols,"rows":rows,"error":err})

@app.get("/export/ttl")
def export_ttl():
    return PlainTextResponse(kg.g.serialize(format="turtle"), media_type="text/turtle")

@app.get("/api/variants")
def api_variants(): return kg.variants()

@app.post("/api/classify")
async def api_classify(request: Request):
    payload=await request.json(); return classify(payload.get("criteria",[]))

@app.post("/import/csv", response_class=HTMLResponse)
async def import_csv(request: Request, file: UploadFile = File(...)):
    data=(await file.read()).decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(data)); n=0
    for row in reader:
        variant=(row.get("variant") or "").strip()
        if not variant: continue
        rec={"variant":variant,"gene":row.get("gene","").strip(),"disease":row.get("disease","").strip(),"phenotypes":[x.strip() for x in row.get("phenotypes","").split("|") if x.strip()],"allele_frequency":float(row["allele_frequency"]) if row.get("allele_frequency","").strip() else None,"clinvar_significance":row.get("clinvar_significance","").strip()}
        v=kg.add_variant(rec)
        codes=[x.strip().upper() for x in row.get("criteria","").replace(";",",").split(",") if x.strip()]
        for code in codes:
            kg.add_evidence(v,{"criterion":code,"strength":strength(code),"description":row.get("evidence_notes","") or f"Imported evidence: {code}","source":row.get("evidence_source","") or file.filename,"pmid":row.get("pmid","")})
        kg.add_classification(v,classify(codes)); n+=1
    kg.save()
    return templates.TemplateResponse("import_done.html", {"request":request,"count":n})

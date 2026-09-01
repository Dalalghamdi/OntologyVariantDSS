import requests
import xml.etree.ElementTree as ET

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
UA = {"User-Agent": "OntologyVariantDSS/0.1 research-prototype"}

def search_pubmed(query: str, retmax: int = 10):
    r = requests.get(f"{BASE}/esearch.fcgi", params={"db":"pubmed","term":query,"retmode":"json","retmax":retmax}, headers=UA, timeout=15)
    r.raise_for_status()
    ids = r.json().get("esearchresult", {}).get("idlist", [])
    if not ids: return []
    s = requests.get(f"{BASE}/esummary.fcgi", params={"db":"pubmed","id":",".join(ids),"retmode":"json"}, headers=UA, timeout=15)
    s.raise_for_status(); data=s.json().get("result", {})
    out=[]
    for pmid in ids:
        x=data.get(pmid, {})
        out.append({"pmid":pmid,"title":x.get("title",""),"journal":x.get("fulljournalname") or x.get("source",""),"date":x.get("pubdate","")})
    return out

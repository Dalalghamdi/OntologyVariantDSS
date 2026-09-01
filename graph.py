from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, Literal, URIRef
from rdflib.namespace import XSD, DCTERMS
from urllib.parse import quote

BASE = Namespace("https://example.org/variant-dss/")
SO = Namespace("http://purl.obolibrary.org/obo/SO_")
HPO = Namespace("http://purl.obolibrary.org/obo/HP_")
DOID = Namespace("http://purl.obolibrary.org/obo/DOID_")
IAO = Namespace("http://purl.obolibrary.org/obo/IAO_")

class KnowledgeGraph:
    def __init__(self, path: str):
        self.path = Path(path)
        self.g = Graph()
        self.g.bind("dss", BASE)
        self.g.bind("dct", DCTERMS)
        if self.path.exists():
            self.g.parse(self.path, format="turtle")
        self._schema()

    def _schema(self):
        classes = ["Variant", "Gene", "Disease", "Phenotype", "Publication", "EvidenceStatement", "ACMGCriterion", "Classification"]
        for c in classes:
            self.g.add((BASE[c], RDF.type, RDFS.Class))
        for p, label in [
            ("locatedInGene", "located in gene"), ("associatedWithDisease", "associated with disease"),
            ("hasPhenotype", "has phenotype"), ("supportedByPublication", "supported by publication"),
            ("hasEvidence", "has evidence"), ("satisfiesCriterion", "satisfies ACMG criterion"),
            ("hasClassification", "has classification"), ("hasProvenance", "has provenance")]:
            self.g.add((BASE[p], RDF.type, RDF.Property)); self.g.add((BASE[p], RDFS.label, Literal(label)))

    def _uri(self, kind: str, value: str):
        return BASE[f"{kind}/{quote(value.strip(), safe='')}"]

    def add_variant(self, record: dict):
        v = self._uri("variant", record["variant"])
        self.g.add((v, RDF.type, BASE.Variant))
        self.g.set((v, RDFS.label, Literal(record["variant"])))
        if record.get("gene"):
            gene = self._uri("gene", record["gene"])
            self.g.add((gene, RDF.type, BASE.Gene)); self.g.set((gene, RDFS.label, Literal(record["gene"])))
            self.g.add((v, BASE.locatedInGene, gene))
        if record.get("disease"):
            d = self._uri("disease", record["disease"])
            self.g.add((d, RDF.type, BASE.Disease)); self.g.set((d, RDFS.label, Literal(record["disease"])))
            self.g.add((v, BASE.associatedWithDisease, d))
        for hp in record.get("phenotypes", []):
            p = self._uri("phenotype", hp)
            self.g.add((p, RDF.type, BASE.Phenotype)); self.g.set((p, RDFS.label, Literal(hp)))
            self.g.add((v, BASE.hasPhenotype, p))
        if record.get("allele_frequency") not in (None, ""):
            self.g.set((v, BASE.alleleFrequency, Literal(float(record["allele_frequency"]), datatype=XSD.double)))
        if record.get("clinvar_significance"):
            self.g.set((v, BASE.clinVarSignificance, Literal(record["clinvar_significance"])))
        return v

    def add_evidence(self, variant_uri, evidence: dict):
        eid = evidence.get("id") or f"{evidence['criterion']}-{abs(hash((evidence.get('description',''), evidence.get('source',''))))}"
        e = self._uri("evidence", eid)
        c = self._uri("criterion", evidence["criterion"].upper())
        self.g.add((e, RDF.type, BASE.EvidenceStatement))
        self.g.set((e, RDFS.label, Literal(evidence.get("description", evidence["criterion"]))))
        self.g.set((e, BASE.evidenceStrength, Literal(evidence.get("strength", ""))))
        self.g.add((e, BASE.satisfiesCriterion, c))
        self.g.add((c, RDF.type, BASE.ACMGCriterion)); self.g.set((c, RDFS.label, Literal(evidence["criterion"].upper())))
        self.g.add((variant_uri, BASE.hasEvidence, e))
        if evidence.get("source"):
            self.g.set((e, BASE.hasProvenance, Literal(evidence["source"])))
        if evidence.get("pmid"):
            p = URIRef(f"https://pubmed.ncbi.nlm.nih.gov/{evidence['pmid']}/")
            self.g.add((p, RDF.type, BASE.Publication)); self.g.set((p, BASE.pubmedId, Literal(evidence["pmid"])))
            self.g.add((e, BASE.supportedByPublication, p))
        return e

    def add_classification(self, variant_uri, result: dict):
        self.g.set((variant_uri, BASE.hasClassification, Literal(result["classification"])))
        self.g.set((variant_uri, BASE.classificationReason, Literal(result["reason"])))

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.g.serialize(self.path, format="turtle")

    def variants(self):
        q = """
        PREFIX dss: <https://example.org/variant-dss/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?v ?label ?classification WHERE {
          ?v a dss:Variant ; rdfs:label ?label .
          OPTIONAL { ?v dss:hasClassification ?classification }
        } ORDER BY ?label
        """
        return [{"uri": str(r.v), "variant": str(r.label), "classification": str(r.classification or "Unclassified")} for r in self.g.query(q)]

    def variant_detail(self, uri: str):
        v = URIRef(uri)
        def one(pred):
            x = next(self.g.objects(v, pred), None); return str(x) if x is not None else None
        label = one(RDFS.label)
        gene_uri = next(self.g.objects(v, BASE.locatedInGene), None)
        disease_uri = next(self.g.objects(v, BASE.associatedWithDisease), None)
        phenotypes = []
        for p in self.g.objects(v, BASE.hasPhenotype):
            phenotypes.append(str(next(self.g.objects(p, RDFS.label), p)))
        evs=[]
        for e in self.g.objects(v, BASE.hasEvidence):
            criterion_uri = next(self.g.objects(e, BASE.satisfiesCriterion), None)
            evs.append({
                "criterion": str(next(self.g.objects(criterion_uri, RDFS.label), "")) if criterion_uri else "",
                "description": str(next(self.g.objects(e, RDFS.label), "")),
                "source": str(next(self.g.objects(e, BASE.hasProvenance), "")),
                "pmid": str(next(self.g.objects(next(self.g.objects(e, BASE.supportedByPublication), URIRef("urn:none")), BASE.pubmedId), "")) if next(self.g.objects(e, BASE.supportedByPublication), None) else "",
            })
        return {
            "uri": uri, "variant": label,
            "gene": str(next(self.g.objects(gene_uri, RDFS.label), "")) if gene_uri else "",
            "disease": str(next(self.g.objects(disease_uri, RDFS.label), "")) if disease_uri else "",
            "phenotypes": phenotypes,
            "allele_frequency": one(BASE.alleleFrequency),
            "clinvar_significance": one(BASE.clinVarSignificance),
            "classification": one(BASE.hasClassification),
            "reason": one(BASE.classificationReason), "evidence": evs,
        }

    def sparql(self, query: str):
        rows = self.g.query(query)
        cols = [str(v) for v in rows.vars]
        return cols, [[str(x) if x is not None else "" for x in r] for r in rows]

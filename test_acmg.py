from app.acmg import classify

def test_pathogenic_pvs_pm_pp(): assert classify(["PVS1","PM2","PP1"])["classification"] == "Pathogenic"
def test_likely_pathogenic(): assert classify(["PVS1","PM2"])["classification"] == "Likely pathogenic"
def test_benign(): assert classify(["BS1","BS2"])["classification"] == "Benign"
def test_likely_benign(): assert classify(["BP1","BP4"])["classification"] == "Likely benign"
def test_conflict(): assert classify(["PS3","BS3"])["classification"] == "Variant of uncertain significance"

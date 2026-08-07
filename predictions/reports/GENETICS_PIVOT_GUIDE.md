# Genetics pivot — plain-language guide (for non-biologists)

**Audience:** same person who just ran asteroid residual packs on a home PC.  
**Goal:** reuse the **same program pattern** (residual law · domains · storage caps · dual language) on **life molecules**, without BS jargon and without pretending we are DeepMind.

---

## 1. Paradigm check (astronomy → biology)

| Astronomy (what we just did) | Genetics / proteins (next) |
|------------------------------|----------------------------|
| Body = asteroid / comet | Molecule set = **gene / protein** |
| Catalog elements \(a,e,i,n\) | **Measurable numbers**: sequence length, mass, fold confidence, … |
| Domain = Planetary / Astro / Meteorology | Domain = **Biology / Biochemistry** (and related) |
| Law | **Same:** `computed = measured × (1 + \|S\| × factor)` at \(D_{\mathrm{eff}}\) |
| Wrong framing | Secular sky drift |
| Wrong framing here | “We invented AlphaFold 3 in Python over the weekend” |

You are **not** solving sky drift.  
You are **not** required to re-simulate every atom of a protein.  
You **are** residual-matching **real measured (or public-database) quantities** through the fluid scalar — same paradigm.

---

## 2. Jargon → shop-floor English

| Term | Plain meaning |
|------|----------------|
| **DNA** | Long instruction tape made of 4 letters: A, C, G, T |
| **Gene** | A stretch of DNA that usually codes for one protein (or control info) |
| **Genome** | The whole instruction book for an organism |
| **Sequencing** | Reading the letter order of DNA (or RNA) |
| **RNA** | Working copy of a gene message |
| **Codon** | Three DNA/RNA letters → one amino acid (like a 3-digit shop code) |
| **Amino acid** | One of ~20 Lego bricks that build proteins |
| **Protein** | Folded chain of amino acids — the machine that does work in a cell |
| **Sequence** | The ordered list of bricks (letters or amino acids) |
| **Fold / structure** | The 3D shape the chain settles into |
| **PDB** | Public library of **measured** 3D protein shapes (crystallography / cryo-EM) |
| **UniProt** | Public library of protein **annotations** (name, length, mass, function tags) |
| **AlphaFold** | Google DeepMind AI that **predicts** 3D shape from sequence |
| **pLDDT** | AlphaFold’s **self-confidence score** (0–100) per region — higher = more sure |
| **AlphaFold DB** | Free website of precomputed AF predictions (what we can residual-check) |

**Mechanic analogy**

- DNA = full service manual  
- Gene = procedure for one part  
- Protein sequence = parts list order  
- Folded protein = assembled component that actually bolts onto the engine  
- AlphaFold = a very good **estimator** of what the assembled part looks like before you machine it  
- FSOT residual pack = check that **public measured/predicted numbers** sit on your **one fluid formula** at the right “depth of scale” (\(D_{\mathrm{eff}}\))

---

## 3. What AlphaFold does vs what FSOT can honestly do

### AlphaFold (industry SOTA)

- **Input:** amino-acid sequence  
- **Output:** full 3D coordinates of the protein  
- **Trained** on huge PDB data + clever neural nets  
- Wins when shape prediction matches experiment  

### FSOT residual biology (this repo’s honest layer)

- **Input:** measured or published numbers from open databases  
- **Output:** `computed` from residual law at Biology / Biochemistry domains  
- **Wins** when residual stays under the framework gate (0.5%, often ~0.02%)  
- **Does not** (yet) claim “we generate atomic coordinates better than AF”

**Good claim language**

> FSOT residual-matches AlphaFold DB / UniProt / longevity-genetics observables at Biochemistry/Biology interfaces with zero free parameters.

**Bad claim language**

> We replaced AlphaFold.

Same honesty rule as asteroids: **dual language OK** (their metrics + your residual), **paradigm switch required** (no secular-drift style hacks).

---

## 4. What you already have verified (you’re not starting at zero)

You already have green-style biology/genetics panels in-repo, including:

| Area | Example | Role |
|------|---------|------|
| Longevity genetics | Tier 94 AnAge / NCBI panels | Species lifespan & genetics coupling |
| Wet-lab / zebrafish | Tier 95 | Developmental tracks |
| AlphaFold DB meta | `alphafold_batch_meta_open_benchmark.json` | pLDDT / confidence-style metrics residual |
| UniProt | `uniprot_protein_annotations_benchmark.json` | sequence length, molecular weight |
| Consciousness–genetics | coupling panels | Cross-domain bridge |
| Code “genomes” | separate metaphor (software) | Not DNA — don’t mix them |

So the pivot is: **granular open molecular data + same residual pipeline**, not inventing genetics from scratch.

---

## 5. “Genome sequencing” on a home PC — reality check

| Data type | Size / cost | Home-PC friendly? |
|-----------|-------------|-------------------|
| UniProt protein rows (length, mass) | Tiny | **Yes** |
| AlphaFold DB **metadata** (confidence scores) | Small | **Yes** |
| Full human genome FASTA | ~3 GB compressed | Possible but heavy |
| Raw sequencing reads (FASTQ) | tens–hundreds of GB | **No** for routine packs |
| Full AF coordinate dumps for thousands of proteins | Large | Cap hard |

**High-value, low-storage strategy (like diversity pack):**

1. **Protein layer** — length, mass, basic annotations (UniProt)  
2. **Fold-confidence layer** — AlphaFold DB metrics (pLDDT etc.), not full atom dumps  
3. **Longevity / gene-set layer** — reuse Tier 94 anchors you already trust  
4. **Optional later** — small FASTA slices (one chromosome region, one model organism gene set)

Same as asteroids: **elements first**, full “optical dump” only when worth the disk.

---

## 6. Domains / \(D_{\mathrm{eff}}\) (routing, not free parameters)

| Topic | Typical FSOT domain | Why |
|-------|---------------------|-----|
| Sequence length, organism biology | **Biology** | Meso life scale |
| Mass, biochemistry numbers | **Biochemistry** | Molecular chemistry interface |
| Mind–genetics coupling | Neuroscience / psychology bridges | Already in tier panels |
| Chaos / high-variability expression | Meteorology-like only if preregistered | Don’t invent |

Mismatch rule (same as MPCORB): **wrong \(D_{\mathrm{eff}}\) first**, not a new fitted coefficient.

---

## 7. Program shape (same as astronomy epochs)

```
collect public IDs (proteins / genes)
  → residual-match measured quantities at Biology/Biochemistry
  → optional light download (metadata only, budget MB)
  → dual report: FSOT residual %  +  field metrics (pLDDT, mass, length)
  → STOP on budget / gate fail
  → push summaries, not multi-GB FASTQ
```

Scripts:

- Existing: `verify_tier95_genetics_system.py`, AlphaFold/UniProt builders already in tree  
- New pattern: `scripts/run_genetics_diversity_pack.py` (storage-capped, like `run_mpcorb_diversity_pack.py`)

---

## 8. What you need to know (checklist)

You do **not** need a biology degree. You need:

1. **What is measured** (length? mass? confidence score?)  
2. **Where it came from** (UniProt / AF DB / AnAge — public URL)  
3. **Which domain** routes it  
4. **Residual still under 0.5%**  
5. **Storage cap** (you’re on a 35L Omen — treat GB like garage floor space)

Ignore until later: wet-lab protocols, CRISPR design, full clinical genomics.

---

## 9. Suggested first “diversity cells” (biology)

| Cell | Analogy to asteroids | Example sources |
|------|----------------------|-----------------|
| Housekeeping proteins | Main belt | Hemoglobin, actin (UniProt) |
| Disease-relevant | NEO-like high interest | p53 (already in AF batch) |
| Small peptides | Sparse / hard | Short UniProt entries |
| Longevity gene products | Distant / rare | Tier 94 anchors |
| AF confidence channels | Classical O–C dual language | pLDDT very-high fraction |

---

## 10. Bottom line

- **Paradigm:** same residual engine — correct.  
- **Pivot:** from sky catalogs to **molecular catalogs**.  
- **AlphaFold:** partner/public metric source, not the thing we replace on day one.  
- **Home PC:** metadata + residual packs, not full sequencing warehouses.  
- **You already have** longevity + AF/UniProt seeds; next is a **capped granular pack** and clear claims.

When ready: run `python scripts/run_genetics_diversity_pack.py` (scaffold) and expand cells the same way we did comets/NEO/distant.

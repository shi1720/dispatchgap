"""Exploratory controls: permute document dates within each calendar year."""
import csv
import datetime as dt
import json
import random
from collections import defaultdict
from pathlib import Path
from analyze import ROOT, tokens
from dispatchgap import Contact, pair_count, temporal_masks

rows = list(csv.DictReader((ROOT/'data/rotunda_data_1771-1783_full.csv').open(encoding='utf-8-sig')))
by_year = defaultdict(list)
for r in rows:
    a, b = tokens(r['authorIDs']), tokens(r['recipientIDs'])
    if a and b:
        date = dt.date.fromisoformat(r['Date'])
        by_year[date.year].append((r['DocumentID'], a, b, date.toordinal()))
output=[]
for seed in range(20):
    rng=random.Random(seed)
    for year, records in sorted(by_year.items()):
        dates=[r[3] for r in records]; rng.shuffle(dates)
        nodes=sorted({n for _, a, b, _ in records for n in a+b})
        cc=[Contact(date,a,b,doc) for (doc,aa,bb,_),date in zip(records,dates)
            for a in aa for b in bb if a!=b]
        for gap in (0,7,30):
            output.append(dict(seed=seed,year=year,gap=gap,pairs=pair_count(temporal_masks(cc,nodes,gap))))
    print('Finished date permutation seed',seed,flush=True)
with (ROOT/'results/date_controls.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
summary={}
for gap in (0,7,30):
    pooled=[sum(x['pairs'] for x in output if x['seed']==s and x['gap']==gap) for s in range(20)]
    summary[gap]=dict(min=min(pooled),max=max(pooled),mean=sum(pooled)/len(pooled),seeds=20)
(ROOT/'results/control_summary.json').write_text(json.dumps(summary,indent=2))
print(summary)

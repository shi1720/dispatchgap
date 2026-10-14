"""Independent state-space verification on three complete annual graphs."""
import csv
import datetime as dt
import json
from collections import Counter
from analyze import ROOT, tokens
from dispatchgap import Contact, oracle, temporal_masks

rows=list(csv.DictReader((ROOT/'data/rotunda_data_1771-1783_full.csv').open(encoding='utf-8-sig')))
reports=[]
for year in (1771,1776,1781):
    contacts=[]
    counts=Counter()
    for r in rows:
        if int(r['Date'][:4])!=year: continue
        aa,bb=tokens(r['authorIDs']),tokens(r['recipientIDs'])
        if not aa or not bb:continue
        counts.update(set(aa+bb))
        for a in aa:
            for b in bb:
                if a!=b:contacts.append(Contact(dt.date.fromisoformat(r['Date']).toordinal(),a,b,r['DocumentID']))
    nodes=sorted(counts);source=counts.most_common(1)[0][0];i=nodes.index(source)
    for gap in (0,7,30):
        masks=temporal_masks(contacts,nodes,gap)
        got={v for j,v in enumerate(nodes) if masks[j]&(1<<i)}
        expected=oracle(contacts,source,gap)
        assert got==expected
        reports.append(dict(year=year,source=source,gap=gap,reachable_including_self=len(got),agreement=True))
        print(reports[-1],flush=True)
(ROOT/'results/real_oracle_checks.json').write_text(json.dumps(reports,indent=2))

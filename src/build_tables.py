"""Build LaTeX tables exclusively from the released numerical CSV outputs."""
import csv
from collections import defaultdict
from analyze import ROOT

rows=list(csv.DictReader((ROOT/'results/annual.csv').open()))
lines=[r'\begin{tabular}{rrrrrrr}\toprule Year&Documents&Nodes&Contacts&Aggregate&Gap 0&Gap 30\\\midrule']
for row in rows:
    if row['gap']!='0': continue
    last=next(r for r in rows if r['year']==row['year'] and r['gap']=='30')
    cells=[row['year']]+[f'{int(row[k]):,}' for k in ['documents','nodes','contacts','static_pairs','temporal_pairs']]+[f"{int(last['temporal_pairs']):,}"]
    lines.append('&'.join(cells)+r'\\')
lines.append(r'\bottomrule\end{tabular}')
(ROOT/'paper/annual_table.tex').write_text('\n'.join(lines))
profiles=list(csv.DictReader((ROOT/'results/profiles.csv').open()));counts=defaultdict(int)
for row in profiles: counts[(row['profile'],row['gap'])]+=int(row['temporal_pairs'])
lines=[r'\begin{tabular}{lrrr}\toprule Profile&Gap 0&Gap 7&Gap 30\\\midrule']
for key,label in [('singleton','Singleton documents'),('no_org','No RN-ORG identifiers'),('no_EA','No EA-labelled rows'),('link_dedup','Source-link deduplicated')]:
    lines.append(label+'&'+'&'.join(f'{counts[(key,str(g))]:,}' for g in (0,7,30))+r'\\')
lines.append(r'\bottomrule\end{tabular}')
(ROOT/'paper/profile_table.tex').write_text('\n'.join(lines))

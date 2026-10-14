"""Reproduce the pinned Revolutionary Networks audit; stdlib analysis only."""
import csv
import datetime as dt
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from dispatchgap import Contact, temporal_masks, static_masks, pair_count, route, critical_gap

ROOT = Path(__file__).resolve().parents[1]
GAPS = (0, 1, 3, 7, 14, 30, 60)


def tokens(value):
    return tuple(dict.fromkeys(v.strip() for v in value.split(';') if v.strip()))


def main():
    path = ROOT / 'data' / 'rotunda_data_1771-1783_full.csv'
    rows = list(csv.DictReader(path.open(encoding='utf-8-sig', newline='')))
    assert len({r['DocumentID'] for r in rows}) == len(rows)
    names = defaultdict(Counter)
    usable = []
    exclusions = Counter()
    for r in rows:
        date = dt.date.fromisoformat(r['Date'])
        assert 1771 <= date.year <= 1783
        a, b = tokens(r['authorIDs']), tokens(r['recipientIDs'])
        if not a or not b:
            exclusions['missing_author' if not a else 'missing_recipient'] += 1
            continue
        # Name/ID lists need not have equal arity. Names are labels, not joins.
        for field, ids in [('Author', a), ('Recipient', b)]:
            labels = [s.strip() for s in r[field].split(';')]
            if len(labels) == len(ids):
                for i, label in zip(ids, labels):
                    names[i][label] += 1
        r['_a'], r['_b'], r['_date'] = a, b, date
        usable.append(r)
    out = ROOT / 'results'; out.mkdir(exist_ok=True)
    annual, examples, profiles = [], [], []
    totals = Counter()
    for year in range(1771, 1784):
        rr = [r for r in usable if r['_date'].year == year]
        nodes = sorted({n for r in rr for n in r['_a'] + r['_b']})
        epoch = dt.date(year, 1, 1)
        def expand(records):
            return [Contact((r['_date'] - epoch).days, a, b, r['DocumentID'])
                    for r in records for a in r['_a'] for b in r['_b'] if a != b]
        contacts = expand(rr)
        baseline = static_masks(contacts, nodes)
        static_count = pair_count(baseline)
        masks = {g: temporal_masks(contacts, nodes, g) for g in GAPS}
        for g in GAPS:
            count = pair_count(masks[g])
            assert all(m & b == m for m, b in zip(masks[g], baseline))
            if g:
                previous = GAPS[GAPS.index(g)-1]
                assert all(m & b == m for m, b in zip(masks[g], masks[previous]))
            annual.append(dict(year=year, documents=len(rr), nodes=len(nodes),
                contacts=len(contacts), gap=g, static_pairs=static_count,
                temporal_pairs=count, retention=count/static_count))
            totals['gap_'+str(g)] += count
        totals['static'] += static_count
        # Controlled exclusions use the full year's vertex set and denominator.
        seen = set(); dedup = []
        for r in rr:
            key = r['Founders Online'] or r['Rotunda'] or r['DocumentID']
            if key not in seen:
                seen.add(key); dedup.append(r)
        variants = {
            'singleton': [r for r in rr if len(r['_a']) == len(r['_b']) == 1],
            'no_org': [r for r in rr if not any(n.startswith('RN-ORG-') for n in r['_a']+r['_b'])],
            'no_EA': [r for r in rr if r['Publication'] != 'EA'],
            'link_dedup': dedup,
        }
        for profile, records in variants.items():
            cc = expand(records)
            for g in (0, 7, 30):
                count = pair_count(temporal_masks(cc, nodes, g))
                profiles.append(dict(year=year, profile=profile, gap=g,
                    documents=len(records), contacts=len(cc), temporal_pairs=count,
                    full_static_pairs=static_count))
        # Predeclared illustration rule: first lexicographic lost pair where
        # a 7-day route has >=2 legs and no direct contact, destroyed at 30 days.
        found = False
        direct = {(e.author, e.recipient) for e in contacts}
        for j, target in enumerate(nodes):
            lost = masks[7][j] & ~masks[30][j]
            for i, source in enumerate(nodes):
                if not lost & (1 << i) or (source, target) in direct:
                    continue
                witness = route(contacts, source, target, 7)
                assert witness is not None
                threshold = critical_gap(contacts, source, target)
                critical_witness = route(contacts, source, target, threshold)
                assert route(contacts, source, target, threshold + 1) is None
                def label(n):
                    return names[n].most_common(1)[0][0] if names[n] else n
                def encode(path):
                    return [dict(document=e.document, date=str(epoch+dt.timedelta(days=e.day)),
                                 author=e.author, author_name=label(e.author),
                                 recipient=e.recipient, recipient_name=label(e.recipient)) for e in path]
                examples.append(dict(year=year, source=source, target=target,
                    source_name=label(source), target_name=label(target),
                    critical_gap=threshold, witness_at_7=encode(witness),
                    witness_at_critical=encode(critical_witness)))
                found = True; break
            if found: break
        print(year, len(nodes), static_count, pair_count(masks[0]), pair_count(masks[7]), pair_count(masks[30]), flush=True)
    def write_csv(name, rr):
        with (out / name).open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rr[0])); writer.writeheader(); writer.writerows(rr)
    write_csv('annual.csv', annual); write_csv('profiles.csv', profiles)
    (out / 'witnesses.json').write_text(json.dumps(examples, indent=2))
    summary = dict(raw_rows=len(rows), usable_rows=len(usable), exclusions=dict(exclusions),
        group_documents=sum(len(r['_a'])>1 or len(r['_b'])>1 for r in usable),
        raw_cartesian_contacts=sum(len(r['_a'])*len(r['_b']) for r in usable),
        self_contacts_removed=sum(a==b for r in usable for a in r['_a'] for b in r['_b']),
        unique_nodes=len({n for r in usable for n in r['_a']+r['_b']}),
        source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        source_commit='dacbbff257a769740c5bf8e25c6fb0a5212bf671', totals=dict(totals),
        pooled_retention={str(g): totals['gap_'+str(g)]/totals['static'] for g in GAPS})
    (out / 'summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()

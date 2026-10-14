"""Inspect a route and its critical calendar-date gap from the command line."""
import argparse
import csv
import datetime as dt
import json
from analyze import ROOT, tokens
from dispatchgap import Contact, route, critical_gap


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--year', type=int, required=True, choices=range(1771,1784))
    parser.add_argument('--source', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--gap', type=int, required=True)
    args = parser.parse_args()
    if args.gap < 0 or args.source == args.target:
        parser.error('gap must be nonnegative and source and target must differ')
    contacts=[]; records={}
    for r in csv.DictReader((ROOT/'data/rotunda_data_1771-1783_full.csv').open(encoding='utf-8-sig')):
        if int(r['Date'][:4]) != args.year:
            continue
        records[r['DocumentID']]=r
        for a in tokens(r['authorIDs']):
            for b in tokens(r['recipientIDs']):
                if a != b:
                    contacts.append(Contact(dt.date.fromisoformat(r['Date']).toordinal(),a,b,r['DocumentID']))
    nodes={v for e in contacts for v in (e.author,e.recipient)}
    if args.source not in nodes or args.target not in nodes:
        parser.error('one or both identifiers are absent from this usable annual graph')
    witness=route(contacts,args.source,args.target,args.gap)
    threshold=critical_gap(contacts,args.source,args.target)
    result=dict(year=args.year,source=args.source,target=args.target,gap=args.gap,
        admissible=witness is not None,critical_gap=threshold,
        interpretation='Existence of a modeled document-date route; no assertion of receipt or content transmission.',
        witness=[] if witness is None else [dict(document=e.document,date=records[e.document]['Date'],
          author=e.author,recipient=e.recipient,founders_url=records[e.document]['Founders Online'],
          rotunda_url=records[e.document]['Rotunda']) for e in witness])
    print(json.dumps(result,indent=2))


if __name__=='__main__': main()

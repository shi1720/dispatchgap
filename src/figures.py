"""Generate vector publication figures directly from released result tables."""
import csv
import json
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'paper'/'figures'; OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,
    'axes.spines.right':False,'axes.labelsize':9,'legend.fontsize':8,'pdf.fonttype':42})
BLUE='#174f70'; ORANGE='#be6535'; GREEN='#47796b'
annual=list(csv.DictReader((ROOT/'results/annual.csv').open()))
summary=json.loads((ROOT/'results/summary.json').read_text())
def save(fig,name):
    fig.savefig(OUT/(name+'.pdf'),bbox_inches='tight')
    fig.savefig(OUT/(name+'.png'),bbox_inches='tight',dpi=200)
    plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(7.1,2.55))
gaps=[int(g) for g in summary['pooled_retention']]
axs[0].plot(gaps,[100*summary['pooled_retention'][str(g)] for g in gaps],'-o',color=BLUE,ms=4)
axs[0].set(xlabel='Minimum inter-document gap (days)',ylabel='Aggregate pairs retained (%)',ylim=(0,105),xlim=(-2,62))
axs[0].axhline(100,color='#999999',ls=':',lw=1)
axs[0].annotate('Aggregate graph',xy=(37,100),xytext=(37,91),fontsize=8,color='#666666')
for g in [0,7,30,60]:
    y=100*summary['pooled_retention'][str(g)]
    axs[0].annotate(f'{y:.1f}',(g,y),xytext=((8,-13) if g==7 else (0,7)),textcoords='offset points',ha='center',fontsize=8)
for gap,c in [(0,BLUE),(7,GREEN),(30,ORANGE)]:
    rr=[r for r in annual if int(r['gap'])==gap]
    axs[1].plot([int(r['year']) for r in rr],[100*float(r['retention']) for r in rr],'-o',label=f'{gap}-day gap',ms=3,color=c)
axs[1].set(xlabel='Calendar-year window',ylabel='Aggregate pairs retained (%)',ylim=(20,70))
axs[1].set_xticks([1771,1774,1777,1780,1783]);axs[1].legend(frameon=False,loc='lower right')
for ax,label in zip(axs,['A  Pooled source-year pairs','B  Annual retention']):
    ax.set_title(label,loc='left',fontweight='bold',fontsize=10);ax.grid(axis='y',alpha=.18)
fig.tight_layout();save(fig,'reachability')

profiles=list(csv.DictReader((ROOT/'results/profiles.csv').open()))
pooled=defaultdict(int)
for r in profiles: pooled[(r['profile'],int(r['gap']))]+=int(r['temporal_pairs'])
fig,axs=plt.subplots(1,2,figsize=(7.1,3.1),gridspec_kw={'width_ratios':[1.2,1]})
names=['Full corpus','Singleton documents','No RN-ORG IDs','No EA-labelled rows','Link deduplicated']
keys=['full','singleton','no_org','no_EA','link_dedup'];y=np.arange(5)
for off,g,c in [(-.13,0,BLUE),(.13,30,ORANGE)]:
    values=[100*(summary['totals']['gap_'+str(g)] if k=='full' else pooled[(k,g)])/summary['totals']['static'] for k in keys]
    axs[0].barh(y+off,values,height=.24,label=f'{g}-day gap',color=c)
axs[0].set_yticks(y,names);axs[0].invert_yaxis();axs[0].set(xlabel='Full aggregate denominator retained (%)',xlim=(0,70));axs[0].legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,-.20),ncol=2,fontsize=7)
control=json.loads((ROOT/'results/control_summary.json').read_text())
gg=[0,7,30];den=summary['totals']['static']
axs[1].fill_between(gg,[100*control[str(g)]['min']/den for g in gg],[100*control[str(g)]['max']/den for g in gg],alpha=.2,color=GREEN,label='20 permutations: min-max')
axs[1].plot(gg,[100*control[str(g)]['mean']/den for g in gg],'-s',ms=4,color=GREEN,label='Permutation mean')
axs[1].plot(gg,[100*summary['pooled_retention'][str(g)] for g in gg],'-o',ms=4,color=BLUE,label='Observed dates')
axs[1].set(xlabel='Minimum gap (days)',ylabel='Aggregate pairs retained (%)',ylim=(30,75));axs[1].legend(frameon=False,loc='lower left',fontsize=7)
for ax,label in zip(axs,['A  Controlled document exclusions','B  Within-year date permutation']):
    ax.set_title(label,loc='left',fontweight='bold',fontsize=9);ax.grid(axis='x' if ax==axs[0] else 'y',alpha=.18)
fig.tight_layout();save(fig,'sensitivity')

fig,ax=plt.subplots(figsize=(7.1,1.9));ax.axis('off')
for x,text,c in [(0.10,'John Foxcroft',BLUE),(0.50,'Benjamin Franklin',GREEN),(0.90,'Samuel Rhoads Sr.',ORANGE)]:
    ax.text(x,.66,text,ha='center',va='center',transform=ax.transAxes,fontsize=10,
        bbox=dict(boxstyle='round,pad=.5',fc='#f3f6f7',ec=c,lw=1.4))
for a,b in [(.21,.36),(.66,.78)]:
    ax.annotate('',xy=(b,.66),xytext=(a,.66),xycoords='axes fraction',arrowprops=dict(arrowstyle='->',color='#444444',lw=1.3))
ax.text(.28,.36,'14 January 1771\nBNFN-01-18-02-0005',ha='center',transform=ax.transAxes,fontsize=8)
ax.text(.72,.36,'10 February 1771\nBNFN-01-18-02-0022',ha='center',transform=ax.transAxes,fontsize=8)
ax.text(.5,.04,'Maximum feasible minimum gap: 27 days\nNo admissible route at 28 days in the full 1771 model',ha='center',transform=ax.transAxes,fontsize=9,fontweight='bold')
save(fig,'witness')

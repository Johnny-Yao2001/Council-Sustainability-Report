from pathlib import Path
import pandas as pd,numpy as np
import os
os.environ.setdefault('MPLCONFIGDIR','/tmp/council-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import openpyxl
root=Path(__file__).resolve().parents[1]
df=pd.read_csv(root/'sources/owid_consumption_co2_selected.csv')
w=openpyxl.load_workbook(root/'Labels.xlsx',read_only=True,data_only=True)
F=w['Footprint summary']['B3'].value
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
# Table-style country values and sparklines inspired by the teacher's example, with separate metrics.
fig=plt.figure(figsize=(11.2,8.4),facecolor='white')
fig.text(.055,.955,'Per-capita emissions: personal estimate and country context',fontsize=18,fontweight='bold',color='#17365D')
fig.text(.055,.92,'Consumption accounting in both panels; greenhouse-gas and system boundaries differ.',fontsize=11,color='#555555')
fig.text(.055,.865,'PERSONAL ESTIMATE — CO₂-EQUIVALENT',fontsize=10,fontweight='bold',color='#17365D')
fig.text(.055,.823,'Illustrative Redfern resident',fontsize=13)
fig.text(.52,.823,f'{F:.2f} t CO₂-e/person/year',fontsize=13,fontweight='bold',color='#17365D')
fig.text(.055,.787,'2025–26 spending × 2018 IO intensities; provisional private-consumption footprint.',fontsize=10,color='#555555')
fig.text(.055,.725,'NATIONAL REFERENCES — CO₂ ONLY',fontsize=10,fontweight='bold',color='#17365D')
fig.text(.055,.685,'Country',fontweight='bold');fig.text(.48,.685,'2018: t CO₂/person',fontweight='bold');fig.text(.76,.685,'Trend: 1990–2023',fontweight='bold')
order=['United States','Australia','Japan','United Kingdom','China','India']
for i,country in enumerate(order):
 y=.625-i*.073
 color='#B34E27' if country=='Australia' else '#17365D'
 fig.text(.055,y,country,fontsize=12,fontweight='bold' if country=='Australia' else 'normal',color=color)
 value=df[(df.country==country)&(df.year==2018)].consumption_co2_per_capita.iloc[0]
 fig.text(.53,y,f'{value:.2f}',fontsize=12,fontweight='bold',color=color)
 ax=fig.add_axes([.76,y-.007,.18,.04])
 z=df[df.country==country].sort_values('year')
 ax.plot(z.year,z.consumption_co2_per_capita,color=color,lw=1.7)
 v=z[z.year==2018].iloc[0];ax.scatter([2018],[v.consumption_co2_per_capita],s=13,color=color,zorder=3)
 ax.set_xlim(1990,2023);ax.axis('off')
fig.text(.055,.145,'Country figures: fossil-fuel and industrial CO₂, adjusted for trade; excludes land-use change.',fontsize=9,color='#444444')
fig.text(.055,.115,'Source: Our World in Data / Global Carbon Budget (2025); accessed 8 November 2026.',fontsize=9,color='#444444')
fig.text(.055,.075,'Contextual comparison, not a like-for-like ranking. Do not infer a percentage below Australia:',fontsize=10,fontweight='bold',color='#9B3C26')
fig.text(.055,.045,'the personal result includes non-CO₂ gases and differs in year, valuation and final-demand coverage.',fontsize=9,color='#444444')
fig.savefig(root/'figures/Figure_2_per_capita_context.png',dpi=230,bbox_inches='tight')
fig.savefig(root/'figures/Figure_2_per_capita_context.pdf',bbox_inches='tight');plt.close(fig)
# Replace the empty Figure 1 placeholder with a real concise sector chart.
rows=list(w['Footprint sectors'].values)[1:];top=sorted(rows,key=lambda r:r[6],reverse=True)[:6]
names=[r[1] for r in top]+['Other sectors'];vals=[r[6] for r in top]+[F-sum(r[6] for r in top)]
fig,ax=plt.subplots(figsize=(9.5,4.7));colors=['#17365D']*6+['#AAB7C4']
ax.barh(names[::-1],vals[::-1],color=colors[::-1]);ax.set_xlabel('Provisional t CO₂-e/person/year')
ax.set_title('Consumption categories driving the resident’s footprint',loc='left',fontweight='bold',pad=15)
for k,v in enumerate(vals[::-1]):ax.text(v+.035,k,f'{v:.2f}',va='center',fontsize=10)
ax.set_xlim(0,max(vals)*1.2);ax.grid(axis='x',alpha=.2);ax.set_axisbelow(True)
fig.text(.01,.015,'Source: Labels.xlsx; nominal illustrative spending × 2018 IO intensities. “Other” sums all remaining sectors.',fontsize=8)
fig.tight_layout(rect=(0,.035,1,1));fig.savefig(root/'figures/Figure_1_sector_footprint.png',dpi=230,bbox_inches='tight');fig.savefig(root/'figures/Figure_1_sector_footprint.pdf',bbox_inches='tight')
print('Created figures 1 and 2 with explicit definitions and source notes.')

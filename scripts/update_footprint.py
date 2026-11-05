"""Refresh provisional footprint sheets in Labels.xlsx; requires numpy/openpyxl.

Run from repository root: python scripts/update_footprint.py
Original input worksheet XML is preserved exactly. L is a numeric snapshot:
rerun after changing T or x. Expenditure formulas use live Excel links.
Formula caches are supplied for immediate inspection without recalculation.
"""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from tempfile import TemporaryDirectory
from copy import deepcopy
import hashlib
import xml.etree.ElementTree as ET
import numpy as np
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as col

ROOT=Path(__file__).resolve().parents[1]; path=ROOT/'Labels.xlsx'
source=path.read_bytes()
w=openpyxl.load_workbook(path)
cached=openpyxl.load_workbook(path,data_only=True)
T=np.array(list(cached['IntermediateDemand'].values),dtype=float)
x=np.array(list(cached['Output'].values),dtype=float).ravel()
Q=np.array(list(cached['Satellite'].values),dtype=float).ravel()
labels=[r[0] for r in cached['row labels'].values]
assert T.shape==(345,345) and len(x)==len(Q)==len(labels)==345
assert np.isfinite(T).all() and np.isfinite(x).all() and np.isfinite(Q).all() and (x>0).all()
# Rebuild personal demand from current source amounts/shares; never rely on old caches.
y_aud=np.zeros(345); split_aud={}; shares={}
split=w['Expenditure split']; expenditure=w['Annual expenditure']
for r in range(2,split.max_row):
 source_row=int(split.cell(r,1).value); sector=int(split.cell(r,4).value)
 share=float(split.cell(r,6).value)
 annual=float(expenditure.cell(source_row,3).value)*float(expenditure.cell(source_row,4).value)
 assert share>=0 and 1<=sector<=345
 y_aud[sector-1]+=annual*share; split_aud[r]=annual*share
 shares[source_row]=shares.get(source_row,0)+share
assert all(abs(v-1)<1e-12 for v in shares.values())
y=y_aud/1e6; A=T/x[None,:]; B=np.eye(345)-A
L=np.linalg.solve(B,np.eye(345)); q=Q/x; m=q@L; z=L@y
c=m*y; e=q*z; F=float(q@z)
assert F>0 and np.allclose(c.sum(),F) and np.allclose(e.sum(),F)
assert np.max(np.abs(B@L-np.eye(345)))<1e-10
assert np.max(np.abs(B@z-y))<1e-10
for name in ['A coefficients','L inverse','Footprint sectors','Footprint summary','Footprint checks']:
 if name in w: del w[name]
cache={}
def formula(s,r,c,text,value):
 s.cell(r,c,text);cache[(s.title,f'{col(c)}{r}')]=float(value)
# Supply current caches for preexisting expenditure / mapping formulas as well.
for r in range(2,expenditure.max_row):
 cache[(expenditure.title,f'E{r}')]=float(expenditure.cell(r,3).value)*float(expenditure.cell(r,4).value)
cache[(expenditure.title,f'E{expenditure.max_row}')]=float(y_aud.sum())
for r,val in split_aud.items():
 source_row=int(split.cell(r,1).value)
 cache[(split.title,f'G{r}')]=float(expenditure.cell(source_row,3).value)*float(expenditure.cell(source_row,4).value)
 cache[(split.title,f'H{r}')]=val
cache[(split.title,f'H{split.max_row}')]=float(y_aud.sum())
demand=w['IO_345 demand']
for i in range(345):
 r=i+2
 for cidx,val in [(3,y_aud[i]),(4,y[i]),(5,x[i]),(6,Q[i])]:cache[(demand.title,f'{col(cidx)}{r}')]=val
cache[(demand.title,'C347')]=float(y_aud.sum());cache[(demand.title,'D347')]=float(y.sum())
a=w.create_sheet('A coefficients'); l=w.create_sheet('L inverse')
for s,title in [(a,'A_ij = T_ij / x_j; dimensionless'),(l,'L = inverse(I-A); numeric snapshot; rerun script after T/x changes')]:
 s.cell(1,1,title)
 for i,label in enumerate(labels,1):s.cell(1,i+1,f'{i}: {label}');s.cell(i+1,1,f'{i}: {label}')
 s.freeze_panes='B2';s.column_dimensions['A'].width=48
for i in range(345):
 for j in range(345):
  formula(a,i+2,j+2,f'=IntermediateDemand!{col(j+1)}{i+1}/Output!A{j+1}',A[i,j])
  l.cell(i+2,j+2,float(L[i,j]))
s=w.create_sheet('Footprint sectors')
s.append(['Sector ID','Sector name','Personal annual AUD','y (AUD million)','q (kt/AUD million)','m=qL (kt/AUD million)','Consumption contribution (t CO2-e)','Share of footprint','Induced output Ly (AUD million)','Emitting-sector contribution (t CO2-e)'])
for i,label in enumerate(labels):
 r=i+2;s.cell(r,1,i+1);s.cell(r,2,label)
 formula(s,r,3,f"='IO_345 demand'!C{r}",y_aud[i])
 formula(s,r,4,f'=C{r}/1000000',y[i])
 formula(s,r,5,f'=Satellite!{col(i+1)}1/Output!A{i+1}',q[i])
 formula(s,r,6,f"=SUMPRODUCT($E$2:$E$346,'L inverse'!{col(i+2)}2:{col(i+2)}346)",m[i])
 formula(s,r,7,f'=F{r}*D{r}*1000',c[i]*1000)
 formula(s,r,8,f'=G{r}/SUM($G$2:$G$346)',c[i]/F)
 formula(s,r,9,f"=SUMPRODUCT('L inverse'!B{r}:MH{r},TRANSPOSE($D$2:$D$346))",z[i])
 formula(s,r,10,f'=E{r}*I{r}*1000',e[i]*1000)
 s.cell(r,8).number_format='0.0%'
s.freeze_panes='C2';s.auto_filter.ref='A1:J346'
summary=w.create_sheet('Footprint summary')
summary.append(['PRELIMINARY ONLY','Nominal spending × 2018 sector intensities; valuation and boundary limitations remain.'])
summary.append(['Annual personal expenditure (AUD)',float(y_aud.sum())])
formula(summary,3,2,"=SUM('Footprint sectors'!G2:G346)",F*1000);summary.cell(3,1,'Provisional IO footprint (t CO2-e/person/year)')
summary.append(['Interpretation','Supply-chain estimate from supplied Q/T/x. Not a verified comprehensive personal inventory or comparable national statistic.'])
summary.append(['Unresolved price basis','2025–26 illustrative nominal spending has NOT been deflated to 2018; no claim of constant-price accuracy.'])
summary.append(['Unresolved valuation','Full purchaser spending mapped to sectors. Taxes, trade/transport margins and insurance service-charge valuation not adjusted.'])
summary.append(['Direct household emissions','Do not assume qLy includes household gas combustion. No activity-based fuel estimate added. No private car does not imply zero direct household emissions.'])
summary.append(['Other boundaries','Imports, government consumption and capital formation require documentation before national comparisons.'])
summary.append(['Model maintenance','A and q update with input changes; L is a numeric snapshot. Rerun python scripts/update_footprint.py after changing T/x or to rebuild ranking/chart order.'])
summary.append(['Input fingerprint SHA256',hashlib.sha256(T.tobytes()+x.tobytes()+Q.tobytes()).hexdigest()])
summary.append(['Rank','Consumption category (purchase sector)','t CO2-e/year','Share'])
for rank,i in enumerate(np.argsort(c)[::-1][:10],1):
 r=rank+11;summary.cell(r,1,rank);summary.cell(r,2,labels[i])
 formula(summary,r,3,f"='Footprint sectors'!G{i+2}",c[i]*1000)
 formula(summary,r,4,f"='Footprint sectors'!H{i+2}",c[i]/F);summary.cell(r,4).number_format='0.0%'
summary.append(['','Other sectors',float((F-c[np.argsort(c)[::-1][:10]].sum())*1000),''])
chart=BarChart();chart.type='bar';chart.title='Top 10 consumption-sector contributions (provisional)';chart.x_axis.title='t CO2-e/person/year';chart.y_axis.title='Consumption sector'
chart.add_data(Reference(summary,min_col=3,min_row=11,max_row=21),titles_from_data=True)
chart.set_categories(Reference(summary,min_col=2,min_row=12,max_row=21));chart.width=25;chart.height=15
summary.add_chart(chart,'F2')
checks=w.create_sheet('Footprint checks')
checks.append(['Check','Value','Acceptance'])
checks.append(['A/L dimensions','345 × 345','345 × 345'])
checks.append(['Minimum total output x',float(x.min()),'> 0'])
checks.append(['max abs((I-A)L-I)',float(np.max(np.abs(B@L-np.eye(345)))),'< 1e-10'])
checks.append(['max abs((I-A)Ly-y)',float(np.max(np.abs(B@z-y))),'< 1e-10'])
checks.append(['sum consumption minus qLy (t)',float((c.sum()-F)*1000),'absolute value < 1e-9'])
checks.append(['sum emitting sectors minus qLy (t)',float((e.sum()-F)*1000),'absolute value < 1e-9'])
checks.append(['Condition number of I-A',float(np.linalg.cond(B)),'Diagnostic; no universal pass threshold'])
checks.append(['Validation scope','Numerical consistency only','Does not resolve valuation, price year or system boundary.'])
for sh in [a,l,s,summary,checks]:
 for cell in sh[1]:cell.font=Font(bold=True,color='FFFFFF');cell.fill=PatternFill('solid',fgColor='17365D')
 if sh not in [a,l]:
  for row in sh:
   for cell in row:cell.alignment=Alignment(vertical='top',wrap_text=True)
  sh.column_dimensions['A'].width=48;sh.column_dimensions['B'].width=95 if sh==summary else 45
  for ci in range(3,sh.max_column+1):sh.column_dimensions[col(ci)].width=25
 if sh==summary:
  for r in range(1,11):sh.row_dimensions[r].height=42
  sh.column_dimensions['C'].width=22;sh.column_dimensions['D'].width=18
with TemporaryDirectory() as td:
 tmp=Path(td)/'new.xlsx';w.save(tmp)
 import io
 ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
 main=ns['s'];rel='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
 with ZipFile(tmp) as z,ZipFile(io.BytesIO(source)) as original,ZipFile(Path(td)/'final.xlsx','w',ZIP_DEFLATED) as out:
  wb=ET.fromstring(z.read('xl/workbook.xml'));rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
  targets={r.get('Id'):r.get('Target').lstrip('/') for r in rels}
  names={}
  for sh in wb.find('s:sheets',ns):
   target=targets[sh.get('{'+rel+'}id')]
   if not target.startswith('xl/'):target='xl/'+target
   names[target]=sh.get('name')
  for name in z.namelist():
   data=z.read(name)
   # Keep all four supplied input sheets byte-for-byte, avoiding float round-trip changes.
   if name in ['xl/worksheets/sheet1.xml','xl/worksheets/sheet2.xml','xl/worksheets/sheet3.xml','xl/worksheets/sheet4.xml']:
    data=original.read(name)
   elif name in names:
    sheet=names[name];xml=ET.fromstring(data)
    for cell in xml.findall('.//s:sheetData/s:row/s:c',ns):
     key=(sheet,cell.get('r'))
     if key not in cache:continue
     for prev in list(cell.findall('s:v',ns)):cell.remove(prev)
     cell.attrib.pop('t',None)
     ET.SubElement(cell,'{'+main+'}v').text=repr(float(cache[key]))
    data=ET.tostring(xml,encoding='utf-8',xml_declaration=True)
   out.writestr(name,data)
 path.write_bytes((Path(td)/'final.xlsx').read_bytes())
print(f'Provisional footprint: {F*1000:.6f} t CO2-e/person/year; annual expenditure AUD {y_aud.sum():,.0f}')

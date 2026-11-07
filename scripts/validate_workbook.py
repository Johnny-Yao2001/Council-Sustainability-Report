"""Read-only audit of Labels.xlsx. Never writes or replaces the user's Excel formulas.
Run: python scripts/validate_workbook.py
Dependencies: numpy, openpyxl. Report printed as JSON; redirect if desired.
"""
from pathlib import Path
import json,hashlib
import numpy as np
import openpyxl
from openpyxl.worksheet.formula import ArrayFormula
p=Path(__file__).resolve().parents[1]/'Labels.xlsx'
w=openpyxl.load_workbook(p,read_only=True,data_only=True)
f=openpyxl.load_workbook(p,read_only=True,data_only=False)
T=np.array(list(w['IntermediateDemand'].values),float)
x=np.array([r[0] for r in w['Output'].values],float)
Q=np.array(next(w['Satellite'].values),float)
y=np.array([r[3] for r in list(w['IO_345 demand'].values)[1:346]],float)
A=np.array([r[1:346] for r in list(w['A coefficients'].values)[1:346]],float)
L=np.array([r[1:346] for r in list(w['L matrix'].values)[1:346]],float)
q=np.array(list(w['q matrix'].values)[1][1:346],float)
m=np.array(list(w['m matrix'].values)[1][1:346],float)
assert T.shape==A.shape==L.shape==(345,345)
assert (x>0).all()
B=np.eye(345)-T/x[None,:]
expected=float((Q/x)@np.linalg.solve(B,y))*1000
rows=list(w['Footprint sectors'].values)[1:346]
err=[]
for s in w:
 for row in s:
  for c in row:
   if c.data_type=='e':err.append(f'{s.title}!{c.coordinate}: {c.value}')
assert not err,err[:10]
assert np.allclose(A,T/x[None,:],rtol=1e-10,atol=1e-12)
assert np.allclose(q,Q/x,rtol=1e-10,atol=1e-12)
assert np.allclose(m,q@L,rtol=1e-10,atol=1e-12)
res=float(np.max(np.abs(B@L-np.eye(345))));assert res<1e-10
actual=w['Footprint summary']['B3'].value;assert abs(actual-expected)<1e-8
assert abs(sum(r[6] for r in rows)-actual)<1e-8
assert abs(sum(r[9] for r in rows)-actual)<1e-8
arrays={}
for s in f:
 for row in s:
  for c in row:
   if isinstance(c.value,ArrayFormula):
    assert '[1]' not in c.value.text,(s.title,c.coordinate)
    arrays[f'{s.title}!{c.coordinate}']={'range':c.value.ref,'formula':c.value.text}
print(json.dumps({'status':'passed','workbook_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'provisional_t_co2e_per_person_year':actual,'independent_numpy_t_co2e':expected,'max_inverse_residual':res,'formula_errors':err,'excel_array_formulas':arrays,'remaining_limitations':['2018 price basis','purchaser/basic-price valuation','insurance service charge','household direct combustion boundary','Australian and international per-capita comparisons not yet completed']},indent=2,ensure_ascii=False))

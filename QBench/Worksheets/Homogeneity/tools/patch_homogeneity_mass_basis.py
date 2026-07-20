#!/usr/bin/env python3
"""Create a new Homogeneity JSON with explicit mass-entry basis."""
import copy, json, re, sys
INDIVIDUAL = "Individual unit/serving mass"
CONTAINER = "Full container mass/volume"
def ci(col):
    n=0
    for ch in col: n=n*26+ord(ch)-64
    return n-1
def rc(cell):
    m=re.fullmatch(r"([A-Z]+)(\d+)",cell)
    return int(m.group(2))-1,ci(m.group(1))
def setv(a,cell,v):
    r,c=rc(cell)
    while len(a)<=r:a.append([])
    while len(a[r])<=c:a[r].append(None)
    a[r][c]=v
def ws(j,name):
    return next(x for x in j['config']['worksheets'] if x['worksheetName']==name)
def add_style(styles,s):
    if s not in styles:styles.append(s)
    return styles.index(s)
def cellcfg(w,src,dst,**kw):
    d=copy.deepcopy(w.get('cells',{}).get(src,{'readonly':False,'type':'text','width':18}))
    d.update(kw);w.setdefault('cells',{})[dst]=d
def patch(j):
    j=copy.deepcopy(j)
    styles=j['config']['style']
    s2=add_style(styles,'background-color:#f5f5f5;border-top:1px solid black;border-right:1px solid black;border-bottom:1px solid black;border-left:1px solid black;text-align:right;mso-number-format:"0.00"')
    s3=add_style(styles,'background-color:#f5f5f5;border-top:1px solid black;border-right:1px solid black;border-bottom:1px solid black;border-left:1px solid black;text-align:right;mso-number-format:"0.000"')
    p,d,c=ws(j,'Paste'),ws(j,'Data'),ws(j,'COA');P,D,C=p['data'],d['data'],c['data']
    setv(P,'A2','Paste exactly 10 Cannabinoid Potency replicate rows into A10:AG19. Enter each measured mass in AH10:AH19 and select whether those values are individual unit/serving masses or full container masses/volumes.');setv(P,'B2',None)
    setv(P,'A8','Paste rows below. Leave AI:AJ formulas intact. AH10:AH19 must contain all 10 measured masses. Mass Entry Basis in G5 controls whether mg/unit uses the mass directly or divides full-container mass by Servings Per Container.');setv(P,'B8',None)
    setv(P,'F5','Mass Entry Basis');setv(P,'G5',INDIVIDUAL);setv(P,'H5','Select Full container mass/volume only when AH10:AH19 contains total package/container mass or volume.')
    setv(P,'AH9','=IF($G$5="Full container mass/volume","Actual Total Container Mass/Volume g","Actual Unit/Serving Mass g")')
    setv(P,'B22','Results are converted from ug/g to mg/g. Individual unit/serving mass: mg/unit = mg/g x entered mass. Full container mass/volume: mg/unit = mg/g x entered total container mass/volume / servings per container.')
    cellcfg(p,'F4','F5',style=45,width=18,readonly=False);cellcfg(p,'H4','G5',style=46,width=28,readonly=False);cellcfg(p,'A2','H5',style=2,width=42,readonly=True)
    for x in ['D4','H4','Q4','U4','W4','AC4','AG4','AM4','AO4','AQ4','B5','D5','B6']:
        if x in p.get('cells',{}):p['cells'][x]['readonly']=True
    setv(D,'B2','Results are converted from ug/g to mg/g. Individual unit/serving mass: mg/unit = mg/g x entered mass. Full container mass/volume: mg/unit = mg/g x entered total container mass/volume / servings per container.')
    setv(D,'C10','Mass Entry Basis');setv(D,'D10','=PASTE!G5')
    setv(D,'H11','=IF($D$10="Full container mass/volume","Actual Total Container Mass/Volume g","Actual Unit/Serving Mass g")');setv(D,'I11','Mass Per Unit g');setv(D,'J11','Mass Entry Basis Used')
    for r in range(12,22):
        setv(D,f'I{r}',f'=IF(H{r}="","",IF(LOWER(TRIM($D$10))="individual unit/serving mass",H{r},IF(LOWER(TRIM($D$10))="full container mass/volume",IF(OR($B$43="",VALUE($B$43)<=0),"",H{r}/VALUE($B$43)),"")))')
        setv(D,f'J{r}','=$D$10');setv(D,f'K{r}',f'=IF(H{r}="","",IF(OR($B$7="",$B$7=0),IF(OR($B$8="",$B$8=0),"",(H{r}-$B$8)/$B$8),(H{r}-$B$7)/$B$7))')
        setv(D,f'M{r}',f'=IF(OR($C{r}="",I{r}="",E{r}=""),"",IFERROR(E{r}*I{r},""))');setv(D,f'P{r}',f'=IF($B$5="","",IF(OR($C{r}="",I{r}="",G{r}=""),"",IFERROR(G{r}*I{r},"")))')
        for x in [f'H{r}',f'I{r}']:cellcfg(d,'H12',x,style=s3,readonly=True,width=18)
        cellcfg(d,'J12',f'J{r}',style=47,readonly=True,width=28);cellcfg(d,'K12',f'K{r}',style=57,readonly=True,width=16);cellcfg(d,'M12',f'M{r}',style=s2,readonly=True,width=14);cellcfg(d,'N12',f'N{r}',style=57,readonly=True,width=16);cellcfg(d,'P12',f'P{r}',style=s2,readonly=True,width=14);cellcfg(d,'Q12',f'Q{r}',style=57,readonly=True,width=16)
    setv(D,'A25','=IF($D$10="Full container mass/volume","Highest Reported Container Mass/Volume g","Highest Reported Unit/Serving Mass g")')
    setv(D,'B42','=IF(AND(B34=10,B36="PASS",B37="PASS",OR(B38="PASS",B38="REVIEWER_CONFIRMED"),B39="PASS",B40="PASS",B41="PASS",OR(B48="PASS",B48="NOT REQUIRED"),B50="PASS"),"READY","INCOMPLETE")')
    setv(D,'C42','pass_fail remains INCOMPLETE until all required checks pass, including Mass Entry Basis validation.');setv(D,'C43','Required only when Mass Entry Basis is Full container mass/volume.')
    setv(D,'B48','=IF(LOWER(TRIM($D$10))="full container mass/volume",IF(B43="","INCOMPLETE",IFERROR(IF(VALUE(B43)>0,"PASS","INCOMPLETE"),"INCOMPLETE")),IF(LOWER(TRIM($D$10))="individual unit/serving mass","NOT REQUIRED","INCOMPLETE"))');setv(D,'C48','Required and greater than 0 only for Full container mass/volume mode.')
    setv(D,'A50','Mass Entry Basis Check');setv(D,'B50','=IF(OR($D$10="Individual unit/serving mass",$D$10="Full container mass/volume"),"PASS","INCOMPLETE")');setv(D,'C50','Must be exactly Individual unit/serving mass or Full container mass/volume.')
    cellcfg(d,'A10','C10',style=45,width=22,readonly=True);cellcfg(d,'B10','D10',style=46,width=30,readonly=True);cellcfg(d,'A49','A50',width=34,readonly=True);cellcfg(d,'B49','B50',width=24,readonly=True);cellcfg(d,'C49','C50',width=82,readonly=True)
    if len(d.get('rows',[]))<50:d.setdefault('rows',[]).append({'height':25})
    for x,s in {'B4':s2,'B6':s2,'B7':s3,'B8':s3,'B9':57,'B25':s3,'B26':57,'B27':s2,'B28':57,'B29':s2,'B30':57}.items():
        if x in d.get('cells',{}):d['cells'][x].update(style=s,readonly=True)
    setv(C,'A4','Mass Entry Basis');setv(C,'B4','=DATA!D10');setv(C,'C4','Servings Per Container');setv(C,'D4','=IF(DATA!D10="Full container mass/volume",DATA!B43,"N/A")')
    setv(C,'A6','=IF(DATA!D10="Full container mass/volume","Highest Container Mass/Volume g","Highest Unit/Serving Mass g")');setv(C,'B10','=IF(DATA!D10="Full container mass/volume","Container Mass/Volume g","Unit/Serving Mass g")')
    for x,src,s in [('A4','A3',51),('B4','B3',52),('C4','C3',51),('D4','D3',52)]:cellcfg(c,src,x,style=s,readonly=True)
    n=j['qb_config'].setdefault('named_cells',{});n['mass_entry_basis']={'cell':'Data!D10','display_name':'Mass Entry Basis','export':True};n['mass_entry_basis_check']={'cell':'Data!B50','display_name':'Mass Entry Basis Check','export':True}
    for w in [p,d,c]:j.setdefault('data',{})[w['worksheetName']]=copy.deepcopy(w['data'])
    return j
if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: patch_homogeneity_mass_basis.py input.json output.json')
    src=json.load(open(sys.argv[1],encoding='utf-8'));json.dump(patch(src),open(sys.argv[2],'w',encoding='utf-8'),indent=2,ensure_ascii=False)

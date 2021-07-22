import streamlit as st
import math

global age
global gen
global height
global weight
global SCr
global dose
global tau

st.title('VCMパラメータ計算')
"""
#### 1-コンパートメントモデルを用いてトラフ値およびAUCを計算します。
#### 当サイトのご利用は自己責任でお願いします。
####
"""
st.sidebar.title('基本情報')
age = st.sidebar.slider('■年齢', 0, 100, 60)
gen = st.sidebar.radio('■性別', ('M', 'F'), index=0)
height = st.sidebar.slider('■身長（cm）', 120, 200, 160)
weight = st.sidebar.slider('■体重（kg）', 20, 150, 50)
SCr = st.sidebar.slider('■SCr', 0.00, 2.50, 0.70)

st.sidebar.title('設定値')
dose_select = st.sidebar.radio('投与量の入力方法', ('選択', '任意'), index=0)
if dose_select ==  '選択':
    dose = st.sidebar.slider('■投与量（mg）', 250, 4000, 2000, step=250)
elif dose_select == '任意':
    dose = st.sidebar.number_input('■投与量（mg）')
tau = st.sidebar.radio('■投与間隔（hr）', (6, 8, 12, 24, 48), index=3)

"""
## ―体格―
"""
def cal_BMI(height, weight):
    BMI = weight/(height/100)**2
    return BMI
BMI = cal_BMI(height, weight)

if BMI >25:
    adj_BW = 25 * (height/100)**2
    comment = f'  ※補正体重 {round(adj_BW, 1)} (kg)を使用してください'
else:
    comment = ''
'BMI = ', round(BMI, 2), comment

def cal_BSA(height, weight):
    BSA = weight**0.425 * height**0.725 * 0.007184
    return BSA
BSA = cal_BSA(height, weight)
'BSA (m2) = ', round(BSA, 3)


"""
## ―腎機能―
"""
def cal_CLcr(age, weight, SCr):
    CLcr = (140-age)*weight / (72*SCr)
    return CLcr
if gen == 'M':
    CLcr = cal_CLcr(age, weight, SCr)
else:
    CLcr = cal_CLcr(age, weight, SCr)*0.85
'CLcr (mL/min) = ', round(CLcr, 1)

def cal_eGFR(SCr, age):
    eGFR = 194*(SCr**(-1.094))*(age**(-0.287))
    return eGFR
if gen == 'M':
    eGFR = cal_eGFR(SCr, age)
else:
    eGFR = cal_eGFR(SCr, age) *0.739
'eGFR (mL/min/1.73) = ', round(eGFR, 1)

adj_eGFR = eGFR * BSA /1.73
'BSA未補正eGFR (mL/min) = ', round(adj_eGFR, 1)

"""
## 
## ―VCM初期パラメータ―
"""
CLvcm = CLcr * 0.797*60/1000
'CLvcm (L/hr) = ', round(CLvcm, 2)
Vd = weight * 0.7
'Vd (L) = ', round(Vd, 1)
kel = CLvcm / Vd
'kel (/hr) = ', round(kel, 3)
t_half = math.log(2)/kel
't1/2 (hr) = ', round(t_half, 1)
Ctrough = ((dose/Vd)/(1-math.exp(-kel*tau)))*math.exp(-kel*tau)
'Ctrough (mg/L) = ', round(Ctrough, 2)
AUC = dose/CLvcm *24/tau
'AUC (mg・hr/L) = ', round(AUC, 1)


st.title('VCMパラメータ Fitting')

kel_select = st.radio('kel検討レンジ', ('kel < 0.1', 'kel > 0.1'), index=0)
"""
### 
## ―Simulation #1―
"""
if kel_select == 'kel < 0.1':
    kel_max = 110
else:
    kel_max =1000

f_Vd = st.slider('Vd', 0.0, 100.0, round(Vd, 1), step=0.1)
f_kel = st.slider('kel（x 0.001）', 0, kel_max, int(kel*1000))

f_CLvcm = f_Vd * (f_kel/1000)
'CLvcm (L/hr) = ', round(f_CLvcm, 2)
f_t_half = math.log(2) / (f_kel/1000)
't1/2 (/hr) = ', round(f_t_half, 1)
f_Ctrough = ((dose/f_Vd)/(1-math.exp(-(f_kel/1000)*tau)))*math.exp(-(f_kel/1000)*tau)
'Ctrough (mg/L) = ', round(f_Ctrough, 2)
f_AUC = dose/f_CLvcm *24/tau
'AUC (mg・hr/L) = ', round(f_AUC, 1)

"""
# 
"""
S2_display = st.checkbox('表示する')
if S2_display == True:
    """
    ## ―Simulation #2―
    """
    f2_Vd = st.slider('Vd', 0.0, 100.0, 30.0, step=0.1)
    f2_kel = st.slider('kel（x 0.001）', 0, kel_max, 100)

    f2_CLvcm = f2_Vd * (f2_kel/1000)
    'CLvcm (L/hr) = ', round(f2_CLvcm, 2)
    f2_t_half = math.log(2) / (f2_kel/1000)
    't1/2 (/hr) = ', round(f2_t_half, 1)
    f2_Ctrough = ((dose/f2_Vd)/(1-math.exp(-(f2_kel/1000)*tau)))*math.exp(-(f2_kel/1000)*tau)
    'Ctrough (mg/L) = ', round(f2_Ctrough, 2)
    f2_AUC = dose/f2_CLvcm *24/tau
    'AUC (mg・hr/L) = ', round(f2_AUC, 1)

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
#st.sidebar.title('')
st.sidebar.title('基本情報')
age = st.sidebar.slider('■年齢', 0, 100, 60)
gen = st.sidebar.radio('■性別', ('M', 'F'), index=0)
height = st.sidebar.slider('■身長（cm）', 120, 200, 160)
weight = st.sidebar.slider('■体重（kg）', 20, 150, 50)
SCr = st.sidebar.slider('■SCr', 0.00, 2.50, 0.60)

st.sidebar.title('設定値')
#dose = st.sidebar.selectbox('■投与量（mg）', list((250, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000)), index=5)
#dose = st.sidebar.number_input('■投与量（mg）', 1)
dose = st.sidebar.slider('■投与量（mg）', 250, 4000, 2000, step=250)
#tau = st.sidebar.selectbox('■投与間隔（hr）', list((6, 8, 12, 24, 48)), index=3)
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
AUC = dose/CLvcm
'AUC (mg・hr/L) = ', round(AUC, 1)


st.title('VCMパラメータ Fitting')
f_Vd = st.slider('Vd', 0.0, 150.0, round(Vd, 1), step=0.1)
f_kel = st.slider('kel（x 0.001）', 0, 1000, int(kel*1000))
#f_Vd = st.number_input('Vd', 1.0, 150.0, Vd)
#f_kel = st.number_input('kel  *小数点第3位以下の数字も計算には反映されます', 0.000, 2.000, kel)


f_CLvcm = f_Vd * (f_kel/1000)
'CLvcm (L/hr) = ', round(f_CLvcm, 2)
f_t_half = math.log(2) / (f_kel/1000)
't1/2 (/hr) = ', round(f_t_half, 1)
f_Ctrough = ((dose/f_Vd)/(1-math.exp(-(f_kel/1000)*tau)))*math.exp(-(f_kel/1000)*tau)
'Ctrough (mg/L) = ', round(f_Ctrough, 2)
f_AUC = dose/f_CLvcm
'AUC (mg・hr/L) = ', round(f_AUC, 1)

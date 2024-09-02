import streamlit as st
import pandas as pd
import re
from natural_breaks import getJenksBreaks as Jenks
from variaveis_cor import faixa
from variaveis_cor import selcor
from nova_legenda import legenda_prod_vertical as LEG
from GERAR_MAPA_MUN_PROD import PLOTTING as PLOT
from MONTAGEM_CAP_PROD import APRESENTACAO as MONTAGEM
import sys
from io import StringIO



st.set_page_config(page_title="CARTOGRAMA",layout="wide")


Filename = st.file_uploader("Escolha um CSV ou Excel (xlsx)",type=["csv", "xlsx"])



if Filename:
    var=Filename.name.split(".")
    if var[1]=="xlsx":
        df = pd.read_excel(Filename, sheet_name=None,engine="openpyxl")   
        # Prints all the sheets name in an ordered dictionary
        lista_sheet=[]
        for it in df.keys():
            lista_sheet.append(it)
        #Then, depending on the sheet one wants to read, one can pass each of them to a specific dataframe, such as
        select=st.selectbox("selecione uma planilha",lista_sheet)
        st.write(select)
        DF = pd.read_excel(Filename, sheet_name=select,engine="openpyxl")
        if "DF" not in st.session_state:
            st.session_state.DF = DF
        st.dataframe(DF) 
        cols=DF.columns
        if "cols" not  in st.session_state:
            st.session_state["cols"] = cols

    if var[1]=="csv":
        df = pd.read_csv(Filename)
        list0=list(df.iloc[0].index)
        lista_del=[]
        lista=df.values.tolist()
        delimitador=","
        cont=[0,0]
        l_teste=[]
        for ll in lista:
            if len(ll)==1:
                tripa=ll[0]
                x = re.findall('[;\t]', tripa)
                l_teste.append(x)
                cont[1]+=len(x)
            cont[0]+=1
            if cont[0] > 5:
                break
        if len(l_teste)>0:
            raz=int(cont[1]/cont[0])
            flag=True
            for lt in l_teste:
                var_del=lt[0]

                if len(lt)!=raz:
                    flag=False

            if flag==True:
                delimitador=var_del
                cont=0
                indice=list0[0].split(delimitador)
                for ll in lista:
                     temp=ll[0].split(delimitador)
                     lista_del.append(temp)
                df=pd.DataFrame(lista_del,columns=indice)

        DF=df
                     

        if "DF" not in st.session_state:
            st.session_state.DF = DF
        st.dataframe(DF) 
        cols=DF.columns
        if "cols" not  in st.session_state:
            st.session_state["cols"] = cols
  
    with st.form("Selecionar opcões:"):
            select2=st.selectbox("selecione a variável de código",st.session_state["cols"])
            select3=st.selectbox("selecione a variável numérica",st.session_state["cols"])
            sl1=st.slider("Número de Quebras:",min_value=2,max_value=7)
            rd1=st.radio("Selecione a cor:",options=["azul","verde","vermelho","laranja",
                                                    "cinza-azul","marron","roxo","rosa","amarelo",
                                                    "cinza","azul-escuro","verde-escuro"])
            st.text("LEGENDA")
            txt1=st.text_input('LINHA1:',max_chars=39)
            txt2=st.text_input('LINHA2:',max_chars=39)
            botao=st.form_submit_button("Confirmar")
    def testar_var(var1,var2):
            DFA=st.session_state.DF[[var1,var2]]
            dicA={}
            cont=[0,0]
            for x,y in DFA.iterrows():
                v1= re.search(r"[0-9]+", str(y[var1]))
                v2= re.search(r"[0-9]+", str(y[var2]))
                if v1:
                    if v2:
                        dicA[v1.group()]=v2.group()
                    else:
                        cont[1]+=1
                else:
                    cont[0]+=1

            dfa = pd.DataFrame(list(dicA.items()), columns=[var1, var2])
            print(cont[0],cont[1],sep="---")
            return(dfa)

    def cor(fx,l_cor):
            lista_cor=[]
            for n in fx:
                lista_cor.append(l_cor[n])
            return(lista_cor)
    if botao:
            dfn=testar_var(select2,select3)
            dfn[select3] =pd.to_numeric(dfn[select3])    
            listavp=list(dfn[select3])
            lista_jenks=Jenks(listavp,sl1)
            st.write(lista_jenks)
            faixa=faixa(sl1)
            l_cores=selcor(rd1)
            lista_cores=cor(faixa,l_cores)
            legtxt=txt1+"\n"+txt2
            LEG(lista_cores,lista_jenks,txt1,txt2)
            PLOT(dfn,lista_jenks,lista_cores,select3,select2)
            MONTAGEM(
                 
            )
            st.image("prov_r.png")
        



    
      




    

            
      
 

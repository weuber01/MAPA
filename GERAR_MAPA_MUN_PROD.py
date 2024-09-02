import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import shapefile as shp
import seaborn as sns
import json
import os
import math

class PLOTTING():

    def __init__(self,data,LISTAFX,LISTACORES,V1,V2):
        self.color_sq=[]
        for lcores in LISTACORES:
            cor_hex=self.rgb_hex(lcores)
            self.color_sq.append(cor_hex)
        print(self.color_sq[0])
        for sq in self.color_sq:
            print(sq)
        self.LISTAFX=LISTAFX
        self.dirpath=os.getcwd()
        sns.set(style="whitegrid", palette="pastel", color_codes=True)
        sns.mpl.rc("figure", figsize=(10,6))
##        data = pd.read_csv(arquivo,encoding='latin-1',dtype={variv1:'str',variv2:'str'})
        data=data.rename(columns = {V2:'codig'})
        data[V1] =pd.to_numeric(data[V1])
        data["codig"] =pd.to_numeric(data["codig"])
        print(data.head())
        print(data.dtypes)
        SFILE=self.dirpath+"\\malhas\\55mu2500gsd.shp"
        SFILE_UF=self.dirpath+"\\malhas\\BRUFE250GC_SIR.shp"
        self.sf = shp.Reader(SFILE,encoding="latin1")
        self.sfuf = shp.Reader(SFILE_UF)
        self.comp=len(self.sf.shapes())
        print(self.comp)
        self.df = self.read_shapefile()
        print(self.df.dtypes)
        print(self.df.head())
        self.df["codig"]=self.df.codig.astype("object")
        self.varlabel="codig"
        self.dfuf = pd.merge(self.df, data, on="codig",how="left")
##        listav1=list(self.dfuf[V1])
##        for lv1 in listav1:
##            print(lv1)
##        exit()
##        self.dfuf[V1]=self.dfuf[V1].astype(float)
        self.variv=V1
        self.DIC_FILTRO={}
        self.selecao_fx()
        self.Colorir_Poligonos()


    def Colorir_Poligonos(self):
        fig, ax = plt.subplots(figsize=(12,10))
#        fig.suptitle('COMPARATIVO DE PRODUÇÃO - VARIAÇÃO ',fontsize=16)
        ax.set_axis_off()
        indice_s=0
        records = self.sf.records()
        for shape in self.sfuf.shapeRecords():
            npoints=len(shape.shape.points)
            nparts=len(shape.shape.parts)
            if nparts==1:
                x = [i[0] for i in shape.shape.points[:]]
                y = [i[1] for i in shape.shape.points[:]]
                ax.plot(x, y, 'k',linewidth=0.4) 
                shape_ex = self.sfuf.shape(indice_s)
            else: # loop over parts of each shape, plot separately
               for ip in range(nparts): # loop over parts, plot separately
                 i0=shape.shape.parts[ip]
                 if ip < nparts-1:
                      i1 = shape.shape.parts[ip+1]-1
                 else:
                      i1 = npoints
                 seg=shape.shape.points[i0:i1+1]
                 x_lon = np.zeros((len(seg),1))
                 y_lat = np.zeros((len(seg),1))
                 for ip in range(len(seg)):
                     x_lon[ip] = seg[ip][0]
                     y_lat[ip] = seg[ip][1]
                 ax.plot(x_lon,y_lat,'k',linewidth=0.4)
        for shape in self.sf.shapeRecords():
            COD=records[indice_s][self.varlabel]
            npoints=len(shape.shape.points)
            nparts=len(shape.shape.parts)
            if nparts==1:
                x = [i[0] for i in shape.shape.points[:]]
                y = [i[1] for i in shape.shape.points[:]]
                #ax.plot(x, y, 'k') 
                shape_ex = self.sf.shape(indice_s)
                x_lon = np.zeros((len(shape_ex.points),1))
                y_lat = np.zeros((len(shape_ex.points),1))
                for ip in range(len(shape_ex.points)):
                    x_lon[ip] = shape_ex.points[ip][0]
                    y_lat[ip] = shape_ex.points[ip][1]
                try:
                    ax.fill(x_lon,y_lat,color=self.color_sq[self.DIC_FILTRO[int(COD)]],linestyle='None',edgecolor ='grey',
                     linewidth = 0)
##                    ax.fill(x_lon,y_lat, color=self.color_sq[self.DIC_FILTRO[int(COD)]],edgecolor ='grey',
##                     linewidth = 1)
                except:
                    ax.fill(x_lon,y_lat, color='white',linestyle='None')
                   
            else: # loop over parts of each shape, plot separately
               for ip in range(nparts): # loop over parts, plot separately
                 i0=shape.shape.parts[ip]
                 if ip < nparts-1:
                      i1 = shape.shape.parts[ip+1]-1
                 else:
                      i1 = npoints
                 seg=shape.shape.points[i0:i1+1]
                 x_lon = np.zeros((len(seg),1))
                 y_lat = np.zeros((len(seg),1))
                 for ip in range(len(seg)):
                     x_lon[ip] = seg[ip][0]
                     y_lat[ip] = seg[ip][1]
                 #ax.plot(x_lon,y_lat,'k', color='white',linestyle='None')
                 for ip in range(len(seg)):
                     x_lon[ip] = seg[ip][0]
                     y_lat[ip] = seg[ip][1] 
                 try:
##                    ax.fill(x_lon,y_lat, color=self.color_sq[self.DIC_FILTRO[int(COD)]],linestyle='None',edgecolor ='grey',
##                     linewidth = 1)
                     ax.fill(x_lon,y_lat, self.color_sq[self.DIC_FILTRO[int(COD)]],edgecolor ='grey',
                     linewidth = 0)
                 except:
                    ax.fill(x_lon,y_lat, color='white',linestyle='None')
                    
            indice_s=indice_s+1
        fig.savefig(self.dirpath+"\\mapa_temp.png", dpi=100)

    def selecao_fx(self):
            comp=len(self.LISTAFX)-1
            lista_comp=[]
            for n in range(0,comp):
                lista_comp.append(n)
            self.dfuf["label"] = pd.cut(x=self.dfuf[self.variv], 
                     bins=self.LISTAFX, 
                     labels=lista_comp)
            self.DIC_FILTRO={}
            for x,y in self.dfuf.iterrows():
                try:
                    self.DIC_FILTRO[int(y["codig"])]=int(y["label"])
                except:
                    self.DIC_FILTRO[int(y["codig"])]=99
           
            

            

    

####    def selecao_fx(self):
####        for ix in range(0,len(self.LISTAFX)-1):
####            selecao=self.variv+'<='+str(self.LISTAFX[ix+1])
####            selecao=selecao+ ' & '+self.variv+'>'+str(self.LISTAFX[ix])
####            print(selecao)
####            FILTRO=self.dfuf.query(selecao)
####            FILTRO=FILTRO[self.varlabel]
####            for FF in FILTRO:
####                self.DIC_FILTRO[FF]=ix
####        for x,y in self.dfuf.iterrows():
####            if y[self.variv]==0:
####                self.DIC_FILTRO[y[self.varlabel]]=99
####  
                
        
    def read_shapefile(self):
        """
        Read a shapefile into a Pandas dataframe with a 'coords' 
        column holding the geometry information. This uses the pyshp
        package
        """
        fields = [x[0] for x in self.sf.fields][1:]
        records = self.sf.records()
        shps = [s.points for s in self.sf.shapes()]
        df = pd.DataFrame(columns=fields, data=records)
        df = df.assign(coords=shps)
        return(df)

    def rgb_hex(self,lista_rgb):
        LHEX=["0","1","2","3","4","5",
              "6","7","8","9","A","B",
              "C","D","E","F"]
        vhex="#"
        p1=(lista_rgb[0])
        raz=p1/16
        f1=math.floor(raz)
        dif=raz-f1
        f2=dif*16
        #print(f1,f2)
        vhex+=LHEX[int(f1)]+LHEX[int(f2)]
        p2=lista_rgb[1]
        raz=p2/16
        f1=math.floor(raz)
        dif=raz-f1
        f2=dif*16
        #print(f1,f2)
        vhex+=LHEX[int(f1)]+LHEX[int(f2)]
        p3=lista_rgb[2]
        raz=p3/16
        f1=math.floor(raz)
        dif=raz-f1
        f2=dif*16
        #print(f1,f2)
        vhex+=LHEX[int(f1)]+LHEX[int(f2)]
        #print(vhex)
        return(vhex)            
    


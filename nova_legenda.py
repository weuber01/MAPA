import cv2 as cv

import numpy as np

def legenda_prod_vertical(lcores,faixa,rot0,rot1):

    l_cor=lcores

    # Create a black image
    im = np.full((420, 420, 3), 
                            255, dtype = np.uint8) 
    
    #param
    font = cv.FONT_HERSHEY_COMPLEX
    font2 = cv.FONT_ITALIC

    # fontScale
    fontScale = 0.7
    
    # Blue color in BGR
    color = (0, 0, 0)

    # Line thickness of 2 px
    thickness = 2
    
    # Draw a diagonal blue line with thickness of 5 px
    cv.line(im,(0,0),(420,420),(255,255,0),5)

    lado=40
    l_cor=lcores
    maxi=max(faixa)
    lraz=[]
    lenmax=0
    for ff in faixa:
        s_raz="{:,}".format(ff).replace(",", " ")
        lraz.append(s_raz)
    l_raz=[]
    for lr in lraz:
        temp=lr.replace(".0","")
        l_raz.append(temp)
        print(temp)

    for y in range(0,len(l_cor)):
        print(y)
        comp=len(l_raz[y])
        cv.rectangle(im,(20, 60+y*lado),(20+lado,60+lado+y*lado),l_cor[y],-1)
        cv.rectangle(im,(20, 60+y*lado),(20+lado,60+lado+y*lado),(0,0,0),3)
        cv.putText(im,l_raz[y], (65,88+y*lado), font, 
                    fontScale, color, thickness, cv.LINE_AA)
        if comp<4:
            cv.line(im,(62+(comp+1)*16,82+y*lado),(82+(comp+1)*16,82+y*lado),(0,0,0),3)
            cv.putText(im,l_raz[y+1], (82+(comp+2)*16,88+y*lado), font, 
                    fontScale, color, thickness, cv.LINE_AA)
        else:      
            cv.line(im,(62+comp*16,82+y*lado),(82+comp*16,82+y*lado),(0,0,0),3)
            cv.putText(im,l_raz[y+1], (82+(comp+1)*16,88+y*lado), font, 
                    fontScale, color, thickness, cv.LINE_AA)
    cv.putText(im,rot0, (20,20), font2, 
                    fontScale, color, thickness, cv.LINE_AA)
    cv.putText(im,rot1, (20,45), font2, 
                    fontScale, color, thickness, cv.LINE_AA)
    cv.imwrite("leg_temp.png", im)


 
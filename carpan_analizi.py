from cgitb import text
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


hisseler=["AKSEN","ARASE","AYEN","AYDEM","BASGZ","CANTE","CONSE","ENJSA","ESEN","GESAN","GWIND","HUNER","KARYE","MAGEN","NATEN","NTGAZ","ODAS","ORGE"]
veriler={"Hisse":[],"FD/FAVOK":[],"FAVOK":[],"ToplamBorc":[],"NakitBenzer":[],"FinansalYat":[],"Gayrimenkul":[],"OzkYontem":[],"OdenmisSermaye":[],"AnlikFiyat":[]}


for i in hisseler:
    options=Options()

    options.add_experimental_option('excludeSwitches',['enable-logging'])

    driver=webdriver.Chrome(executable_path=r"C:/Users/ufuk_/OneDrive/Masaüstü/chromedriver.exe",chrome_options=options)


    url1="https://www.halkyatirim.com.tr/skorkart/{}".format(i)
    url2="https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(i)

    driver.get(url1)


    driver.maximize_window()

    time.sleep(2)


    fd_favok=driver.find_element(By.XPATH,'//*[@id="TBLTEMELANALIZ"]/tbody/tr[3]/td[2]')
    favok=driver.find_element(By.XPATH,'//*[@id="TBLFINANSALVERİLER3"]/tbody/tr[1]/td[5]')
    topborc=driver.find_element(By.XPATH,'//*[@id="TBLFINANSALVERİLER3"]/tbody/tr[1]/td[10]')
    odenmis=driver.find_element(By.XPATH,'//*[@id="TBLPAZARENDEKSLERI"]/tbody/tr[3]/td[2]')
    anlikfiyat=driver.find_element(By.XPATH,'//*[@id="TBLFIYATOZET"]/tbody/tr[1]/td[2]')
    veriler["AnlikFiyat"].append(anlikfiyat.text)
    veriler["FD/FAVOK"].append(fd_favok.text.replace(",",""))
    veriler["FAVOK"].append(favok.text.replace(",",""))
    veriler["ToplamBorc"].append(topborc.text.replace(",",""))
    veriler["OdenmisSermaye"].append(odenmis.text.replace(",","").replace(" TL",""))
   

    driver.close()


    driver2=webdriver.Chrome(executable_path=r"C:/Users/ufuk_/OneDrive/Masaüstü/chromedriver.exe",chrome_options=options)

    driver2.maximize_window()

    driver2.get(url2)
    time.sleep(2)
    tablo=driver2.find_element(By.CSS_SELECTOR,'#page-4')
    tablo.click()
    nakitbenzer=driver2.find_element(By.XPATH,'//*[@id="tbodyMTablo"]/tr[3]/td[2]')
    finansalyatirimlar=driver2.find_element(By.XPATH,'//*[@id="tbodyMTablo"]/tr[19]/td[2]')
    gayrimenkul=driver2.find_element(By.XPATH,'//*[@id="tbodyMTablo"]/tr[22]/td[2]')
    ozkaynakyontem=driver2.find_element(By.XPATH,'//*[@id="tbodyMTablo"]/tr[20]/td[2]')
    
    veriler["NakitBenzer"].append(nakitbenzer.text.replace(".",""))
    veriler["FinansalYat"].append(finansalyatirimlar.text.replace(".",""))
    veriler["Gayrimenkul"].append(gayrimenkul.text.replace(".",""))
    veriler["OzkYontem"].append(ozkaynakyontem.text.replace(".",""))
    veriler["Hisse"].append(i)
    
    driver2.close()



x=pd.DataFrame(veriler)
x.to_csv("VerilerElektrik.csv")

df=pd.read_csv("VerilerElektrik.csv",index_col=0)

kolonlar=["NakitBenzer","FinansalYat","Gayrimenkul","OzkYontem","OdenmisSermaye"]

for i in kolonlar:
    df[i]=df[i]/1000000

fd_favokort=df['FD/FAVOK'].mean()
df["FirmaDegeri"]=df["FAVOK"]*fd_favokort
df["OKPiyasaDeger"]=df["NakitBenzer"]+df["FinansalYat"]+df["Gayrimenkul"]+df["OzkYontem"]-df["ToplamBorc"]+df["FirmaDegeri"]
df["DeğerlemeSonuc"]=df["OKPiyasaDeger"]/df["OdenmisSermaye"]
df["Potansiyel(TL)"]=df["DeğerlemeSonuc"]-df["AnlikFiyat"]
df["Potansiyel(%)"]=((df["DeğerlemeSonuc"]-df["AnlikFiyat"])/df["AnlikFiyat"])*100
print(df)
df.to_csv("CarpanAnaliziElektrik.csv")







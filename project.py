class Scrapper:
    def __init__(self,url):
        import pandas as pd
        import numpy as np
        import requests
        from bs4 import BeautifulSoup
        self.url=url
        page=requests.get(self.url)
        soup= BeautifulSoup(page.text,'lxml')
        table= soup.findAll('li')
        self.raw_data=[]
        for i in table:
            self.raw_data.append(i.text)
    def data_clean(self):
        
        self.clean_data1=[]
        
        for i in self.raw_data:
            v=(i.replace('\n'," ").strip()).split()
            self.clean_data1.append(v)
        self.clean_data1=self.clean_data1[:-9]
        for i in self.clean_data1:
            if ord(i[1][0])>=65 and ord(i[1][0])<=122:
                i[0]=i[0]+" "+i[1]
                i[1]=i[2]
        for i in self.clean_data1:
            if len(i)==3:
                if i[-1]== "Million":
                    i[-2] = int((float(i[-2])*1000000))
    def display_raw(self):
        print(self.raw_data)
    def display_clean(self):
        print(self.clean_data1)
    def structured_data(self):
        import pandas as pd
        df=pd.DataFrame(self.clean_data1)
        df.drop(2,axis='columns', inplace= True)
        df.rename(columns={0:'Country',1:'no_of_tenders(K)'},inplace=True)
        num_of_tend=df['no_of_tenders(K)'].tolist()
        convert=[]
        for i in num_of_tend:
           if type(i)==str:
                num_of_tend=int(i.replace(",",""))
                convert.append(num_of_tend)
           else:
                convert.append(i)
        df['no_of_tenders(K)']= convert
        df['no_of_tenders(K)']=(df['no_of_tenders(K)']/1000).astype('int64')
        print(df)
        df.to_csv(r'tenders.csv')
        self.df1=df
    def visulisation_bar(self):
        import matplotlib.pyplot as plt
        import seaborn as sns
        df2=self.df1
        df3=self.df1
        df2=df2.sort_values(by='no_of_tenders(K)', ascending=False)
        df3=df3.sort_values(by='no_of_tenders(K)')
        top_10_count= df2.head(10)
        lowest_10_count= df3.head(10)
        y=top_10_count['no_of_tenders(K)'].tolist()
        x=top_10_count['Country'].tolist()
        plt.bar(x,y,color=['r','g','b','orange','y','pink','black','grey','m','c'])
        plt.xticks(rotation=45)
        plt.title("Top 10 highest no of tender's countries ")
        plt.xlabel("counrtry")
        plt.ylabel('no of vendors\n (in thousand)')
        plt.show()

        x1=lowest_10_count['Country'].tolist()
        y1=lowest_10_count['no_of_tenders(K)'].tolist()
        plt.bar(x1,y1,color=['r','g','b','orange','y','pink','black','grey','m','c'])
        plt.xticks(rotation=45)
        plt.title("Top 10 least no of tender's countries ")
        plt.xlabel("counrtry")
        plt.ylabel('no of vendors \n (in thousand)')
        plt.show()


url= 'https://opentender.eu/start'
obj= Scrapper(url)
obj.data_clean()
obj.structured_data()
obj.visulisation_bar()


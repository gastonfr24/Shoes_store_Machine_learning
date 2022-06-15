import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

#1 Importamos los datos 
shoes_df= pd.read_csv('shoes_dataset.csv')

#2 Nos fijamos si hay algun dato que vamos a usar esta en str
shoes_df.info()

#Fecha a datetime
shoes_df['Date']=pd.to_datetime(shoes_df['Date'])
shoes_df['Year']=shoes_df['Date'].dt.year
shoes_df['Day']=shoes_df['Date'].dt.day
shoes_df['Month']=shoes_df['Date'].dt.month

#Precio str con " $" por delante lo pasasmos a número

shoes_df['UnitPrice'] = shoes_df['UnitPrice'].apply(lambda x: float(x[2:]))
shoes_df['SalePrice'] = shoes_df['SalePrice'].apply(lambda x: float(x[2:]))


#3 Depuracion de datos

#Elegimos los datos que vamos a usar y los categorizamos en float y str
categorical_variables= ['Country', 'ProductID','Shop','Gender','Size (US)',
                        'Discount','Year','Month']
numerical_variables= ['UnitPrice','SalePrice']

#Graficamos cada una de las variables de categoría
for cat_variable in categorical_variables:
    frequency = shoes_df[cat_variable].value_counts()
    df_frequency = pd.DataFrame({'index': frequency.index.tolist(),'values': frequency.tolist()})
    sns.barplot(x='index', y='values', data=df_frequency)
    plt.show()

#Graficamos las primeras 10 Tiendas para que se vea mejor
frequency_shop = shoes_df['Shop'].value_counts().head(10)
 df_frequency_shop = pd.DataFrame({'Shop': frequency_shop.index.tolist(),'cantidad': frequency_shop.tolist()})
sns.barplot(x='Shop', y='cantidad', data=df_frequency_shop)
 plt.show()

#Graficamos cada una de las variables numéricas
for num_variable in numerical_variables:
    sns.histplot(shoes_df[num_variable], bins='auto')
    plt.show()
    
#Graficamos variables correlacionadas
#.corr() nos ayuda a ver las que clases estan relacionadas entre si
#Ademas ignora los que son str y solo nos trae los que son float, por que pueden
#ser relacionadas
corr = shoes_df.corr()
sns.heatmap(corr, vmin=-1, vmax=1, center=0,cmap=sns.diverging_palette(20, 220, n=200),square=True)
plt.show()

#Creamos intervalos de confiaza
#Primero agrupamos los datos
grouped = shoes_df[(shoes_df['Year'] != 2014) & (shoes_df['Gender'] == 'Male') & (shoes_df['Country'] == 'United States')].groupby(['Size (US)', 'Year', 'Month']).size().unstack(level =0).fillna(value=0)
# las columas son de tallas(Size)

#Ahora creamos la media y el error estandar
means = []
standard_errors = []
for column in grouped.columns:
    means.append(grouped[column].mean())
    #por cada columna calculamos la media
    standard_errors.append(grouped[column].sem())
    #por cada columna calculamos el error estandar

#Para trabajar con esto los metemos en un dataframe
d = {'means': means, 'std_error': standard_errors}
df_calculations = pd.DataFrame(data=d, index=grouped.columns)

#Calculamos margen de error
#Ahora realizaremos el cálculo del margen de error que es multiplicar 
#t-score por el error estándar
#En grpou, contamos cuantodos datos hay en cada columna y le reestamos 1
# y buscamos en t-score que valor va a tomar con un nivel de confianza del 95%

df_calculations['error_margin'] = df_calculations['std_error'].apply(lambda x: x * 2.07)

#https://medium.com/@benjachods/estadística-con-python-proyecto-real-empresa-de-zapatillas-b8ece598384e
#para ver la formula xd

#ahora calculamos intervalo de confianza máximo y mínimo
df_calculations['low_margin'] = df_calculations.apply(lambda x: x['means']- x ['error_margin'], axis=1)
df_calculations['up_margin'] = df_calculations.apply(lambda x: x['means']+ x ['error_margin'], axis=1)
#redondeamos los nuemeros de arriba para trabajar con ellos(del margen maximo)
df_calculations['math_round_up'] = df_calculations.apply(lambda x: math.ceil(x['up_margin']), axis=1)



# HEMOS CALCULADO LA CANTIDAD MAXIMA DE ZAPATILLAS QUE DEBERIA TENER UNA TIENDA
# DE ZAPATILLAS DE CADA TALLA







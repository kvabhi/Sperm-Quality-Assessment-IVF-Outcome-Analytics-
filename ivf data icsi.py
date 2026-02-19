import pandas as pd 
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns',None)
pd.set_option('display.float_format','{:.2f}'.format)


df= pd.read_excel(r"C:\Users\LENOVO\Downloads\Copy of 312.xlsx",
                  sheet_name="ICSI_Data")

print(df.head())
print(df.tail())
print(df.shape)
print(df.info())
print(df.columns)
print(df.describe())

df.describe(include='all')

numeric_cols = [
    'Cycle_Number',
    'Embryologist_Experience_Years',
    'Sperm_Concentration_M_per_ml',
    'Total_Motility_Percent',
    'Progressive_Motility_Percent',
    'Normal_Morphology_Percent',
    'Selection_Time_Seconds',
    'Lab_Temperature_C',
    'Lab_Humidity_Percent'
]
#find mean------
mean_df = df[numeric_cols].mean()
print("MEAN")
print(mean_df)
#find median--------------
median_df = df[numeric_cols].median()
print("\nMEDIAN")
print(median_df)
# find mode ------------------- 
mode_df_first = df[numeric_cols].mode().iloc[0]
print("\nMODE (first)")
print(mode_df_first)
# combine them-------------
first_moment = pd.DataFrame({
    'Mean': mean_df,
    'Median': median_df,
    'Mode': mode_df_first
})

print("\nFIRST MOMENT (Mean, Median, Mode)")
print(first_moment)

# find variance---------
variance_df = df[numeric_cols].var()
print("VARIANCE")
print(variance_df)
#find standard deviation-----------
std_df = df[numeric_cols].std()
print("\nSTANDARD DEVIATION")
print(std_df)
#find range---------
range_df = df[numeric_cols].max() - df[numeric_cols].min()
print("\nRANGE")
print(range_df)
#combain them------------
second_moment = pd.DataFrame({
    'Variance': variance_df,
    'Std_Deviation': std_df,
    'Range': range_df
})

print("\nSECOND MOMENT (Dispersion Measures)")
print(second_moment)

#find swewness-------------
skewness_df = df[numeric_cols].skew()
print("SKEWNESS")
print(skewness_df)

#find kurtosis----------
kurtosis_df = df[numeric_cols].kurt()
print("KURTOSIS")
print(kurtosis_df)

#Graphical representation------
#Univariate------------
#Histogram-------
plt.figure(figsize=(15, 10))
for i, col in enumerate(numeric_cols, 1):
    plt.subplot(3, 3, i)
    sns.histplot(df[col], kde=True)
    plt.title(col)

plt.tight_layout()
plt.show()

#Boxplot--------
plt.figure(figsize=(12, 8))
sns.boxplot(data=df[numeric_cols], orient='h')
plt.title("Boxplot of Numeric Variables")
plt.show()

#Bivariate--------
#Scatter plot--------
target = 'Fertilization_Success'

plt.figure(figsize=(15, 10))

for i, col in enumerate(numeric_cols, 1):
    plt.subplot(3, 3, i)
    plt.scatter(df[col], df[target], alpha=0.6)
    plt.xlabel(col)
    plt.ylabel(target)
    plt.title(f'{col} vs Fertilization_Success')

plt.tight_layout()
plt.show()

#Multivariate-----------
corr_matrix = df[numeric_cols + ['Fertilization_Success']].corr()

plt.figure(figsize=(12, 8))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap='coolwarm',
    linewidths=0.5
)
plt.title("Correlation Heatmap (Multivariate Analysis)")
plt.show()

#Typecasting---------
df.dtypes



#Duplicates----------
df.duplicated().sum()

#Outlier Analysis--------
df[numeric_cols].describe()
plt.figure(figsize=(12, 8))
sns.boxplot(data=df[numeric_cols], orient='h')
plt.title("Outlier Detection Using Boxplot")
plt.show()

#cheak zero vaalues-----------

zero_count = (df == 0).sum().sort_values(ascending=False)
zero_count

df.loc[df['Normal_Morphology_Percent'] == 0, 'Normal_Morphology_Percent'] = np.nan
df['Normal_Morphology_Percent'].fillna(
    df['Normal_Morphology_Percent'].median(),
    inplace=True
)
(df == 0).sum().sort_values(ascending=False)

zero_variance_cols = df.nunique()[df.nunique() == 1]
zero_variance_cols

df.drop(columns=zero_variance_cols.index, inplace=True)

for col in df.columns:
    top_freq = df[col].value_counts(normalize=True,dropna=False).iloc[0]
    if top_freq >0.95:
        print(col,round(top_freq,3))
df.nunique()

#Missing values---------

missing_count = df.isnull().sum()
missing_percent = (missing_count / len(df)) * 100

missing_df = pd.DataFrame({
    'Missing_Count': missing_count,
    'Missing_Percent': missing_percent
}).sort_values(by='Missing_Percent', ascending=False)

df['Tail_Assessment'].fillna('Not_Assessed', inplace=True)
df['Midpiece_Assessment'].fillna('Not_Assessed', inplace=True)

df['Midpiece_Assessment'] = df['Midpiece_Assessment'].replace('not_Assessed', 'Not_Assessed')

df['Vacuoles_Present'].fillna('Not_Assessed', inplace=True)
df['Vacuoles_Present'].value_counts(dropna=False)

missing_df

#Final cheak-----------
df.info()
df.isnull().sum().sort_values(ascending=False)

df.describe().T

#IVF ---------------------

id_cols = ['Record_ID', 'Patient_ID', 'Embryologist_ID', 'Oocyte_ID']
target = 'Fertilization_Success'

df_vif = df.drop(columns=id_cols + [target], errors='ignore')

df_vif = df_vif.select_dtypes(include=['int64', 'float64'])

df_vif = df_vif.fillna(df_vif.median())

from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data['Feature'] = df_vif.columns
vif_data['VIF'] = [
    variance_inflation_factor(df_vif.values, i)
    for i in range(df_vif.shape[1])
]

vif_data.sort_values(by='VIF', ascending=False)


for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df['Selection_Date'] = pd.to_datetime(df['Selection_Date'], errors='coerce')



df.to_csv(
    r"C:\Users\LENOVO\Downloads\ICSI_Cleaned_Data.csv",
    index=False
)
















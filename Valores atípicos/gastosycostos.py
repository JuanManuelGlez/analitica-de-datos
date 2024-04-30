import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the excel file
df = pd.read_excel('gastos_costos_20_23.xlsx')

# Select three columns for outlier analysis
columns_to_analyze = ['IMPORTE', 'IVA', 'TOTAL MX']

# Handling null values
for column in columns_to_analyze:
    df[column].fillna(df[column].mean(), inplace=True)

# Function to remove outliers using Standard Deviation
def remove_outliers_std(df, column, z_score_threshold=3):
    mean = df[column].mean()
    std = df[column].std()
    df_filtered = df[np.abs(df[column] - mean) <= (z_score_threshold * std)]
    return df_filtered

# Function to remove outliers using Interquartile Range
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return df_filtered

# Apply outlier removal for the selected three columns
for column in columns_to_analyze:
    df = remove_outliers_std(df, column)
    df = remove_outliers_iqr(df, column)

# Create boxplots for the selected three columns after outlier removal
plt.figure(figsize=(15, 5))
for i, column in enumerate(columns_to_analyze, 1):
    plt.subplot(1, 3, i)
    sns.boxplot(y=df[column])
    plt.title(f'Boxplot post-outlier removal for {column}')

plt.tight_layout()
plt.show()

# Save the clean data to CSV files
for column in columns_to_analyze:
    clean_df = df[['FECHA', 'FOLIO', 'UUID', 'RFC', 'PROVEEDOR', 'TIPO GASTO', column]].copy()
    clean_df.to_csv(f'{column}_clean.csv', index=False)

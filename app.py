import pandas as pd
import streamlit as st

st.title('Vente de voitures aux États-Unis')

# Charger le jeu de données avec Pandas
df = pd.read_csv('car_prices_clean.csv')

# Renommer les colonnes de la DataFrame en français
df.rename(columns={
    'make': 'marque_du_véhicule',
    'model': 'modèle',
    'year': 'année',
    'price': 'prix',
    'mileage': 'kilométrage',
    'color': 'couleur',
    'state': 'état',
    'date': 'date'
}, inplace=True)

# Choisir la colonne de tri et l'ordre
sort_column = st.sidebar.selectbox("Trier sur cette colonne :", [""] + list(df.columns))
sort_order = st.sidebar.radio("Type de tri :", ('Ascendant', 'Descendant'))

if sort_column:
    df = df.sort_values(by=sort_column, ascending=(sort_order == 'Ascendant'))

# **Filtrage par marque**
if 'marque_du_véhicule' in df.columns:
    df['marque_du_véhicule'] = df['marque_du_véhicule'].astype('category')
    marques = df['marque_du_véhicule'].cat.categories.tolist()
    selected_marques = st.sidebar.multiselect('Sélectionnez la ou les marques du véhicule à filtrer :', [""] + marques)

    if selected_marques and "" not in selected_marques:
        df = df[df['marque_du_véhicule'].isin(selected_marques)]
        
        # **Filtrage par modèle en fonction de la marque sélectionnée**
        if 'modèle' in df.columns:
            modèles_disponibles = df['modèle'].unique().tolist()
            selected_model = st.sidebar.selectbox("Sélectionnez le modèle :", [""] + modèles_disponibles)
            if selected_model:
                df = df[df['modèle'] == selected_model]

# **Filtrage pour les colonnes numériques**
numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
if numeric_columns:
    selected_numeric_column = st.sidebar.selectbox("Sélectionnez la colonne numérique à filtrer :", [""] + numeric_columns)
    if selected_numeric_column:
        min_value = float(df[selected_numeric_column].min())
        max_value = float(df[selected_numeric_column].max())
        selected_range = st.sidebar.slider(f"Sélectionnez une plage pour {selected_numeric_column} :", min_value, max_value, (min_value, max_value))
        df = df[df[selected_numeric_column].between(selected_range[0], selected_range[1])]

# **Téléchargement des données**
def convert_df_to_csv(dataframe):
    return dataframe.to_csv(index=False).encode('utf-8')

csv_data = convert_df_to_csv(df)
st.sidebar.download_button(
    label="Télécharger les données en CSV",
    data=csv_data,
    file_name='données_filtrées.csv',
    mime='text/csv'
)

# **Affichage du tableau**
st.write("**Données après application des filtres et du tri :**")
st.dataframe(df)

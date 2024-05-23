from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
import dtreeviz

app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allows CORS for this domain
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

async def load_data_file(datafile):
    print("Uploading csv as temp file")
    # Save the uploaded file
    if not datafile.filename.endswith(".csv"):
        raise ValueError("File must be a CSV file")
        
    temp_filename = "temp_" + datafile.filename
    with open(temp_filename, "wb") as buffer:
        buffer.write(await datafile.read())

    # Read the CSV file
    df = pd.read_csv(temp_filename)

    return df

def preprocess_data(df, target_column):
    print("Preprocessing data...")

    if(target_column not in df.columns):
        raise ValueError("Target column not found in the dataset")
    
    # Remove any columns named "Unnamed" or starting with "Unnamed"
    unnamed_cols = [col for col in df.columns if col.startswith("Unnamed")]
    print("Dropping unnamed columns: ", unnamed_cols)
    df.drop(columns=unnamed_cols, inplace=True)

    # Remove any columns named "Id" or starting with "Id"
    id_cols = [col for col in df.columns if col.lower() == "id" or col.lower().startswith("id")]
    print("Dropping id columns: ", id_cols)
    df.drop(columns=id_cols, inplace=True)

    # Remove null values
    print("dropping "+ str(df.shape[0] - df.dropna().shape[0]) + " rows with null values")
    df.dropna(inplace=True)

    if(df.shape[0] == 0):
        raise ValueError("Dataset is empty after removing null values")

    # One-hot encode categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    print("One-hot encoding columns: ", categorical_cols)
    # if any of the categorical columns have over 100 unique values, raise an exception
    for col in categorical_cols:
        if len(df[col].unique()) > 100:
            raise ValueError(f"Column {col} has over 100 unique values, which is too many for one-hot encoding")

    # Exclude the target column in the one-hot encoding process
    if target_column in categorical_cols:
        categorical_cols = categorical_cols.drop(target_column)
    

    df = pd.get_dummies(df, columns=categorical_cols)

    # Label encode target column if categorical
    if df[target_column].dtype == 'object':
        print("Label encoding target column: ", target_column)
        label_encoder = LabelEncoder()
        df[target_column] = label_encoder.fit_transform(df[target_column])

    print("Data preprocessing complete")
    print("Final dataset shape: ", df.shape)
    return df

def generate_tree_image(df, target_column):
    print("Training decision tree...")
    # Train decision tree
    X = df.drop(columns=[target_column])
    y = df[target_column]
    clf = DecisionTreeClassifier(max_depth=5)
    clf.fit(X, y)
    
    print("Generating decision tree visualization...")
    # Visualize decision tree
    viz = dtreeviz.model(clf, X, y,
                    target_name=target_column,
                    feature_names=X.columns,
                    class_names=[str(i) for i in clf.classes_],
                    )
    v = viz.view()     # render as SVG into internal object 
    v.save("temp_decision_tree.svg")
    print("Decision tree visualization saved as temp_decision_tree.svg")
    return "temp_decision_tree.svg"

def remove_temp_files():
    print("Removing temporary files")
    for file in os.listdir():
        if file.startswith("temp_"):
            os.remove(file)

def train_kmeans_model(df, target_column, n_clusters=3):
    print("Training KMeans model...")
    # Train KMeans model
    X = df.drop(columns=[target_column])
    y = df[target_column]
    clf = KMeans(n_clusters=n_clusters)
    clf.fit(X, y)

    return clf

def pca_reduction(df, target_column=None):
    print("Reducing dimensions using PCA...")
    # Use PCA to reduce dimensions to 2D
    pca = PCA(n_components=2)
    if target_column is None:
        X = df
        y = None
    else:
        X = df.drop(columns=[target_column])
        y = df[target_column]
    X_pca = pca.fit_transform(X)

    return X_pca, y

def generate_clusters_image(df, target_column, n_clusters=3):
    print("Generating clusters visualization...")
    # Train KMeans model
    clf = train_kmeans_model(df, target_column, n_clusters)

    # Use PCA to reduce dimensions to 2D
    X_pca, y = pca_reduction(df, target_column)

    # Visualize clusters
    fig, ax = plt.subplots()
    ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clf.labels_, cmap='viridis')
    ax.set_title("Clusters Visualization")
    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    
    plt.savefig("temp_clusters.png")
    print("Clusters visualization saved as temp_clusters.png")
    return "temp_clusters.png"

def train_multilayer_perceptron(df, target_column=None):
    print("Training Multilayer Perceptron model...")
    # Train Multilayer Perceptron model
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    clf = MLPClassifier(hidden_layer_sizes=(100, 100), max_iter=1000)
    clf.fit(X, y)

    return clf

def generate_decision_boundary_image(df, target_column):
    print("Generating decision boundary visualization...")

    # Use PCA to reduce dimensions to 2D
    X_pca, y = pca_reduction(df, target_column)
    df_pca = pd.DataFrame(X_pca, columns=["PCA1", "PCA2"])
    df_pca[target_column] = y

    # Train Multilayer Perceptron model
    clf = train_multilayer_perceptron(df_pca, target_column)
    print("Training complete")

    # Visualize decision boundary
    fig, ax = plt.subplots()
    ax.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis')
    ax.set_title("Decision Boundary Visualization")
    ax.set_xlabel("PCA 1")
    ax.set_ylabel("PCA 2")
    
    

    plt.savefig("temp_decision_boundary.png")
    print("Decision boundary visualization saved as temp_decision_boundary.png")
    return "temp_decision_boundary.png"


@app.post("/decision_tree/")
async def decision_tree(file: UploadFile = File(...), target_column: str = Query(...)):
    try:
        # Load the data
        df = await load_data_file(file)
    
        # Preprocess the data
        df = preprocess_data(df, target_column)
        # Train the model and generate the tree
        image_path = generate_tree_image(df, target_column)

        # Respond with decision tree file
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        remove_temp_files()

    return {"decision_tree": image_data}

@app.post("/kmeans_clusters/")
async def kmeans_clusters(file: UploadFile = File(...), target_column: str = Query(...), n_clusters: int = Query(3)):
    try:
        # Load the data
        df = await load_data_file(file)
    
        # Preprocess the data
        df = preprocess_data(df, target_column)
        # Generate the clusters visualization
        image_path = generate_clusters_image(df, target_column, n_clusters)

        # Respond with clusters image
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
    finally:
        remove_temp_files()

    return {"clusters_image": image_data}

@app.post("/multilayer-perceptron/")
async def multilayer_perceptron(file: UploadFile = File(...), target_column: str = Query(...)):
    try:
        # Load the data
        df = await load_data_file(file)
    
        # Preprocess the data
        df = preprocess_data(df, target_column)
        # Generate the decision boundary visualization
        image_path = generate_decision_boundary_image(df, target_column)

        # Respond with decision boundary image
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
    remove_temp_files()

    return {"decision_boundary": image_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

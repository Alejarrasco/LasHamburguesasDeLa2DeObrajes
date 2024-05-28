from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, classification_report
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

def train_multilayer_perceptron(df, target_column, hidden_layers, max_iter):
    print("Training Multilayer Perceptron model...")
    # Train Multilayer Perceptron model
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    clf = MLPClassifier(hidden_layer_sizes=hidden_layers, max_iter=max_iter)
    clf.fit(X, y)

    return clf

def generate_report(clf, X, y):
    """
    Generate a txt report with the weights of each layer
    The accuracy of the model
    The confusion matrix
    The classification report
    and some headers
    X: The features of the validation dataset
    y: The target of the validation dataset
    """
    
    report = "Multilayer Perceptron Report\n\n"
    report += "Weights of each layer:\n"
    for i, layer in enumerate(clf.coefs_):
        report += f"Layer {i}:\n{layer}\n\n"

    report += "Accuracy: " + str(clf.score(X, y)) + "\n\n"

    report += "Confusion Matrix:\n"
    report += str(confusion_matrix(y, clf.predict(X))) + "\n\n"

    report += "Classification Report:\n"
    report += classification_report(y, clf.predict(X)) + "\n\n"

    # Save to a txt file
    with open("temp_report.txt", "w") as file:
        file.write(report)

    return "temp_report.txt"

def plot_confusion_matrix(clf, X, y):
    cm = confusion_matrix(y, clf.predict(X))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.savefig("temp_confusion_matrix.png")
    plt.close()
    return "temp_confusion_matrix.png"

def plot_decision_boundary(clf, X, y):
    h = .02  # step size in the mesh

    # Create color maps
    cmap_light = plt.cm.Pastel2
    cmap_bold = plt.cm.Dark2

    # we only take the first two features for visualization
    X = X.iloc[:, :2].values
    y = y.values

    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

    Z = Z.reshape(xx.shape)
    plt.figure()
    plt.contourf(xx, yy, Z, cmap=cmap_light)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
                edgecolor='k', s=20)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.title("Decision boundary of MLP")

    plt.savefig("temp_decision_boundary.png")
    plt.close()
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
async def multilayer_perceptron(file: UploadFile = File(...), target_column: str = Query(...), hidden_layers: str = Query("2,2"), max_iter: int = Query(100)):
    try:
        # Convert the hidden_layers string to a tuple of integers
        hidden_layers_tuple = tuple(map(int, hidden_layers.split(',')))
        
        # Load the data
        df = await load_data_file(file)
    
        # Preprocess the data
        df = preprocess_data(df, target_column)

        # Generate the txt report
        clf = train_multilayer_perceptron(df, target_column, hidden_layers_tuple, max_iter)
        X = df.drop(columns=[target_column])
        y = df[target_column]
        report_path = generate_report(clf, X, y)
        confusion_matrix_path = plot_confusion_matrix(clf, X, y)

        # Only plot decision boundary if there are two features
        if X.shape[1] == 2:
            decision_boundary_path = plot_decision_boundary(clf, X, y)
        else:
            decision_boundary_path = None

        # Respond with report and images
        with open(report_path, "rb") as report_file:
            report_data = base64.b64encode(report_file.read()).decode("utf-8")
        with open(confusion_matrix_path, "rb") as cm_file:
            cm_data = base64.b64encode(cm_file.read()).decode("utf-8")
        if decision_boundary_path:
            with open(decision_boundary_path, "rb") as db_file:
                db_data = base64.b64encode(db_file.read()).decode("utf-8")
        else:
            db_data = None

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    
    remove_temp_files()

    return {"report": report_data, "confusion_matrix": cm_data, "decision_boundary": db_data}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

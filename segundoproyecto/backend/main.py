from fastapi import FastAPI, File, HTTPException, UploadFile, Query
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64

app = FastAPI()

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
    # Train decision tree
    X = df.drop(columns=[target_column])
    y = df[target_column]
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    
    # Visualize decision tree
    plt.figure(figsize=(20, 10))
    cnames = [str(i) for i in clf.classes_]
    plot_tree(clf, filled=True, feature_names=X.columns, class_names=cnames, rounded=True, max_depth=5)
    image_file_path = "temp_decision_tree.png"
    plt.savefig(image_file_path)

    return image_file_path

def remove_temp_files():
    print("Removing temporary files")
    for file in os.listdir():
        if file.startswith("temp_"):
            os.remove(file)


@app.post("/process_csv/")
async def process_csv(file: UploadFile = File(...), target_column: str = Query(...)):
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

        # Remove temporary files
        remove_temp_files()

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"decision_tree": image_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import FastAPI, File, UploadFile, Query
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64

app = FastAPI()

def preprocess_data(df, target_column):
    # Print columns
    #print(target_column in df.columns)
    #print("Target column: ", target_column)
    #print(df.columns)

    # Remove null values
    df.dropna(inplace=True)

    # One-hot encode categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    # Exclude the target column in the one-hot encoding process
    if target_column in categorical_cols:
        categorical_cols = categorical_cols.drop(target_column)
    df = pd.get_dummies(df, columns=categorical_cols)
    #print(df.columns)
    # Label encode target column if categorical
    if df[target_column].dtype == 'object':
        label_encoder = LabelEncoder()
        df[target_column] = label_encoder.fit_transform(df[target_column])

    return df

@app.post("/process_csv/")
async def process_csv(file: UploadFile = File(...), target_column: str = Query(...)):
    # Save the uploaded file
    with open(file.filename, "wb") as buffer:
        buffer.write(await file.read())

    # Read the CSV file
    df = pd.read_csv(file.filename)

    # Preprocess the data
    df = preprocess_data(df, target_column)

    # Train decision tree
    X = df.drop(columns=[target_column])
    y = df[target_column]
    clf = DecisionTreeClassifier()
    clf.fit(X, y)
    
    # Visualize decision tree
    plt.figure(figsize=(20, 10))
    cnames = [str(i) for i in clf.classes_]
    plot_tree(clf, filled=True, feature_names=X.columns, class_names=cnames, rounded=True)
    plt.savefig("decision_tree.png")

    # Respond with decision tree file
    with open("decision_tree.png", "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Remove temporary files
    os.remove(file.filename)
    os.remove("decision_tree.png")

    return {"decision_tree": image_data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

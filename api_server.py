
from fastapi import FastAPI
import pandas as pd

app = FastAPI()

# You can adjust the file path to where your latest CSV is saved
DATA_FILE_PATH = "trade_recommendations.csv"

@app.get("/get_recommendations")
def get_recommendations():
    try:
        df = pd.read_csv(DATA_FILE_PATH)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


# import library
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

app = FastAPI()

# create API Key
API_Key = "hck024data"

## create endoint : pintu gerbang
@app.get("/")
def home():
    return {"message": "Selamat datang di Toko Pak Edi!"}

## create endpoint data
@app.get("/data")
def read_data():
    # read data from file csv
    df = pd.read_csv("data.csv")
    # convert dataframe to dictionary with orient="records" for each row
    #return df.to_dict(orient="records")

# create endpoint data with number of parameter id
@app.get("/data/{number_id}")
def read_item(number_id: int):

    df = pd.read_csv("data.csv")


    #filter data by id
    filter_data= df[df["id"] == number_id]

    # check if filtered data is empty
    if len(filter_data) == 0:
        raise HTTPException(status_code=404, detail="Waduh, data yang lu cari ga ada bro, maap :")

    

    return filter_data.to_dict(orient="records")

# create endpoint update file csv data
@app.put("/items/{number_id}")
def update_item(number_id: int, nama_barang: str, harga: float):

    df = pd.read_csv("data.csv")

#create dataframe ffrom updated input
    update_df = pd.DataFrame([
        {"id":number_id,
        "nama_barang":nama_barang,
        "harga":harga}])

#merge updated dtaframe with original dataframe
    df = pd.concat([df, update_df], ignore_index=True)

    df.to_csv("data.csv", index=False)

    return {"message": f"Item with name {nama_barang} has been saved succesfully."}

@app.get("/secret")
def read_secret(api_key: str = Header(None)):
    # read data from csv
    secret_df = pd.read_csv("secret_data.csv")
    # check if api key is valid
    if api_key != API_Key:
        raise HTTPException(status_code=401, detail="API Key tidak valid.")
    return secret_df.to_dict(orient='records')


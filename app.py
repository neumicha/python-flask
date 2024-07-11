from flask import Flask, Response, request
import requests

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

@app.route("/")
def hello_world():
    return "<p>Working!</p>"

def escape(s):
    return s.translate(str.maketrans({"\n":  r"\n",
                                          "\\": r"\\"}))


@app.route("/search",methods=["GET"])
def search():
    api_url = "https://api.fda.gov/device/recall.json"
    params = dict()
    for arg in request.args:
        params[arg]=request.args.get(arg)
    try:
        response = requests.get(api_url, params=params)
    except requests.exceptions.RequestException as e:
        return e, 503
    data = []
    data.append(list(response.json().get("results")[0].keys())) # Handle exception when no result is found # Relies on having all keys set on entry 0
    data[0].remove("openfda")
    for i,row in enumerate(response.json().get("results")):
        data.append([])
        for key_index,key in enumerate(data[0]):
            data[i+1].append(row.get(key))
    csv_out = ""
    for dat in data:
        for val in dat:
            if isinstance(val,list):
                csv_out += f"\"{"|".join(val)}\";"
            elif val is None:
                csv_out += f"\"\";"
            else:
                csv_out += f"\"{escape(val)}\";"
        csv_out += "\n"

    response = Response(csv_out, content_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=out.csv"
    return response

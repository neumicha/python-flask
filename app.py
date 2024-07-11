from flask import Flask, Response, request, send_file
import requests
import io
import csv

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
    fields = []
    fields=list(response.json().get("results")[0].keys()) # Handle exception when no result is found; Relies on having all keys set on entry 0
    fields.remove("openfda")

    results = response.json().get("results")

    for row_index,row in enumerate(results):
        row.pop("openfda", None)
        for col_index, value in enumerate(fields):
            if isinstance(value,list):
                results[row_index][col_index] = "|".join(value)
    output = io.StringIO()
    writer = csv.DictWriter(output, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fields)
    print("DATA")
    print(results)

    mem = io.BytesIO()
    mem.write(output.getvalue().encode())

    mem.seek(0)
    

    writer.writeheader()
    writer.writerows(results)
    output.close()
    return send_file(
        mem,
        as_attachment=True,
        download_name='test.csv',
        mimetype='text/csv'
    )

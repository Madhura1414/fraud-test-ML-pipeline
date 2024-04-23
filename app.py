from flask import Flask, request, render_template, jsonify
# Alternatively can use Django, FastAPI, or anything similar
from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application

@app.route('/')
def home_page():
    return render_template('index.html')
@app.route('/predict', methods = ['POST', "GET"])

def predict_datapoint(): 
    if request.method == "GET": 
        return render_template("form.html")
    else: 
        data = CustomData(
            trans_date_trans_time = request.form.get('trans_date_trans_time'),
            cc_num =request.form.get('cc_num'),
            merchant = request.form.get("merchant"), 
            category = request.form.get("category"), 
            amt = float(request.form.get("amt")),
            first = request.form.get("first"), 
            last = request.form.get("last"), 
            gender = request.form.get("gender"), 
            street = request.form.get("street"),
            city = request.form.get('city'),
            state = request.form.get('state'),
            zip = int(request.form.get('zip')),
            lat = float(request.form.get('lat')),
            long = float(request.form.get('long')),
            city_pop = int(request.form.get('city_pop')),
            job = request.form.get('job'),
            dob = request.form.get('dob'),
            trans_num = request.form.get('trans_num'),
            unix_time = int(request.form.get('unix_time')),
            merch_lat= float(request.form.get('merch_lat')),
            merch_long=float(request.form.get('merch_long'))
        )
    new_data = data.get_data_as_dataframe()
    predict_pipeline = PredictPipeline()
    pred = predict_pipeline.predict(new_data)

    results = round(pred[0])

    return render_template("results.html", final_result = results)

if __name__ == "__main__": 
    app.run(host = "0.0.0.0", debug= True)

#http://127.0.0.1:5000/ in browser
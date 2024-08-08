from flask import Flask, render_template, request, jsonify, url_for
import image_classify
app = Flask(__name__, template_folder='../user_interface/template', static_folder='../user_interface/static')

@app.route('/classify_image', methods=['GET','POST'])
def classify_image():
    if request.method == "POST":
        image_data = request.form.get('image_data')
        #image_data = "./image_test/66617.png"
        #if not image_data:
            
            #return jsonify({'error': 'No image data provided'}), 405
        result = jsonify(image_classify.classify_image(image_data))
        result.headers.add('Access-Control-Allow-Origin', '*')
        print(result)
        return result
    return render_template('index.html')

if __name__ == "__main__":
    image_classify.load_saved_artifacts()
    app.run(debug=True)
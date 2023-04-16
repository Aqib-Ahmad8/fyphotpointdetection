from flask import (
    Flask,
    redirect,
    render_template,
    request,
    g,
    session,
    url_for,
    Response,
    jsonify
)
import cv2
import pyrebase
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = 'secretkey'


config = {
 
    'apiKey': "AIzaSyCqlKZso8LlooKBCn-wIgj_9z2KJOcaIBM",
    'authDomain': "bulletdetection.firebaseapp.com",
"databaseURL": "https://bulletdetection-default-rtdb.firebaseio.com/",    
'projectId': "bulletdetection",
    'storageBucket': "bulletdetection.appspot.com",
    'messagingSenderId': "38767613412",
    'appId': "1:38767613412:web:45c659803ea6a8704fa3f1",
    'measurementId': "G-T3ZLP8F22X"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


def dumpSession():
    session.pop('user', None)

# def gen_real_frames():
#     cam = cv2.VideoCapture('static/video.mp4')
#     while True:
#         success, frame = cam.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/real_video')
# def real_video():
#     return Response(gen_real_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# def gen_derivative_frames():
#     cam = cv2.VideoCapture('static/video.mp4')
#     while True:
#         success, frame = cam.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             gray_image = cv2.GaussianBlur(gray_image, (7, 7), 0)
#             edges = cv2.Canny(gray_image, 50, 100)
#             ret, buffer = cv2.imencode('.jpg', edges)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/derivative_video')
# def derivative_video():
#     return Response(gen_derivative_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# def gen_detection_frames():
#     cam = cv2.VideoCapture('static/video.mp4')
#     while True:
#         success, frame = cam.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             gray_image = cv2.GaussianBlur(gray_image, (3, 3), 0)
#             dst = cv2.Laplacian(gray_image, cv2.CV_32F, 3)
#             abs_dst = cv2.convertScaleAbs(dst)
#             dst, result = cv2.threshold(
#                 abs_dst, 27, 255, cv2.THRESH_BINARY_INV)
#             ret, buffer = cv2.imencode('.jpg', result)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# @app.route('/detection_video')
# def detection_video():
#     return Response(gen_detection_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = request.form
        email = result["email"]
        password = result["password"]
        try:
            user = auth.sign_in_with_email_and_password(email, password)

            check = str(auth.get_account_info(user['idToken']))
            if ("'emailVerified': True" in check):
                session['user'] = user['idToken']
                return redirect(url_for('index'))
            else:
                return 'Verify your email to login.'

        except:
            dumpSession()
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@ app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' in session:
        if request.method == 'POST':
            if request.form['action'] == 'upload':
                try:
                    f = request.files['file']
                    f.save('static/queries/'+secure_filename(f.filename))
                    return render_template('index.html', message='success')
                except:
                    return render_template('index.html', message='error')
            elif request.form['action'] == 'next':
                return redirect(url_for('processing'))
        else:
            return render_template('index.html', message='')
    else:
        return redirect(url_for('login'))


@ app.route('/processing', methods=['GET',  'POST'])
def processing():
    if 'user' in session:
        return render_template('processing.html')
    else:
        return redirect(url_for('login'))


@ app.route('/fogot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        result = request.form
        email = result["email"]
        try:
            auth.send_password_reset_email(email)
            return 'Password reset email has been sent! kindly check your email.'
        except:
            return 'no such registered email found!'
    else:
        return render_template('forgot.html')


@ app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = request.form  # Get the data submitted
        email = result["email"]
        password = result["password"]
        name = result["name"]
        print(email, password, name)
        try:
            user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(user['idToken'])
            return redirect(url_for('login'))
        except:
            print('error')
            return redirect(url_for('register'))
    else:
        return render_template('register.html')


@ app.route('/reset', methods=['GET', 'POST'])
def reset():
    return render_template('reset.html')


if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)
    app.run()
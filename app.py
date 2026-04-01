from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
		# 여기에 내 데이터를 만든다!
    my_profile = {
        "name": "김우주",
        "age": 19,
        "school": "종로산업정보학교",
        "hobby": "헬스",
        "email": "wooju2942@naver.com",
        "phon": "010-7759-2942",
        "dream": "데이터 사이언스",
        "favorite_food": "고기"
    }

    # 이 부분이 바뀌었다!
    return render_template('index.html', data=my_profile)

if __name__ == '__main__':
    app.run(debug=True)
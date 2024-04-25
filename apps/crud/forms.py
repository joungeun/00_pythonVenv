from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length


class UserForm(FlaskForm):
    
    username = StringField(
        "사용자명",
        validators=[
            DataRequired(message="사용자명은 필수。"),
            length(max=30, message="30문자 이내로 입력。"),
        ],
    )

    email = StringField(
        "메일주소",
        validators=[
            DataRequired(message="메일주소 필수"),
            Email(message="메일주소의 형식으로 입력바람"),
        ],
    )


    password = PasswordField("비밀번호", validators=[DataRequired(message="비밀번호 필수")])

  
    submit = SubmitField("신규등록")
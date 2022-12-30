//로그인 유효성 검사 (1229 22:46)
//수정 필요~

const inputId = document.getElementById('InputId')          //아이디 input
const inputPw = document.getElementById('InputPassword')    //비밀번호 input
const loginForm = document.getElementById('loginForm')      //로그인폼 자체
const loginBtn = document.getElementById('loginBtn')        //로그인 버튼

//아이디 유효성 검사
inputId.addEventListener('input',function(){
    inputId.classList.remove('is-invalid')
    inputId.classList.remove('is-valid')

    if(inputId.value.length < 1) {  //아이디 input창 빈칸일 때
        $('#noInputId').show();
        inputId.classList.add('is-invalid')
        inputId.classList.remove('is-valid')
    } else {
        $('#noInputId').hide();
        inputId.classList.remove('is-invalid')
        inputId.classList.add('is-valid')
    }
})

//비밀번호 유효성 검사
inputPw.addEventListener('input',function(){
    inputPw.classList.remove('is-invalid')
    inputPw.classList.remove('is-valid')

    if(inputPw.value.length < 1) {  //비밀번호 input창 빈칸일 때
        $('#noInputPw').show();
        inputPw.classList.add('is-invalid')
        inputPw.classList.remove('is-valid')
    } else {
        $('#noInputPw').hide();
        inputPw.classList.remove('is-invalid')
        inputPw.classList.add('is-valid')
    }
})

loginForm.addEventListener('change',function(){
    if(inputId.classList.contains('is-valid') && inputPw.classList.contains('is-valid')) {
        //로그인 가능
        loginBtn.removeAttribute('disabled',false)
        loginBtn.style.backgroundColor = "#FD7537";
    } else {
        //로그인 불가
        loginBtn.setAttribute("disabled",true)
		loginBtn.style.backgroundColor = "#ddd"
    }
})
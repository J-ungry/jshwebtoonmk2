var InputPassword = document.getElementById("InputPassword")
var InputPasswordCheck = document.getElementById("InputPasswordCheck")
var InputEmail = document.getElementById("InputEmail")
var infoForm = document.getElementById("infoForm")
var InputName = document.getElementById("InputName")
var submitBtn = document.getElementById("submitBtn")

InputPassword.addEventListener("input",function(){
    InputPassword.classList.remove("is-invalid")
    InputPassword.classList.remove("is-valid")

    if(InputPassword.value == ""){
        InputPasswordCheck.classList.remove("is-invalid")
        InputPasswordCheck.classList.remove("is-valid")

        if(InputPasswordCheck.value == "") return
        else InputPasswordCheck.classList.add("is-invalid")

        return
    }

    var reg = /(?=.*\d{1,50})(?=.*[a-zA-Z]{2,50}).{8,50}$/

    if( !reg.test(InputPassword.value) ) InputPassword.classList.add("is-invalid")
    else InputPassword.classList.add("is-valid")

    InputPasswordCheck.classList.remove("is-invalid")
    InputPasswordCheck.classList.remove("is-valid")
    if( InputPassword.value != InputPasswordCheck.value) InputPasswordCheck.classList.add("is-invalid")
    else InputPasswordCheck.classList.add("is-valid")
})

InputPasswordCheck.addEventListener("input",function(){
    InputPasswordCheck.classList.remove("is-invalid")
    InputPasswordCheck.classList.remove("is-valid")

    if(InputPasswordCheck.value == "") return;

    if( InputPassword.value != InputPasswordCheck.value) InputPasswordCheck.classList.add("is-invalid")
    else InputPasswordCheck.classList.add("is-valid")
})

InputEmail.addEventListener("input",function(){
    InputEmail.classList.remove("is-invalid")
    InputEmail.classList.remove("is-valid")

    var reg = /^[a-z0-9_+.-]+@([a-z0-9-]+\.)+[a-z0-9]{2,4}$/

    if( !reg.test(InputEmail.value) ) InputEmail.classList.add("is-invalid")
    else InputEmail.classList.add("is-valid")
})

infoForm.addEventListener("change",function(){

    if((InputPassword.classList.contains("is-invalid") == false) && (InputPasswordCheck.classList.contains("is-invalid") == false) && InputEmail.classList.contains("is-valid") && InputName.value.length>0) {
        submitBtn.removeAttribute("disabled",false)
        submitBtn.style.backgroundColor = "#FD7537"
    }
    else{
        submitBtn.setAttribute("disabled",true)
		submitBtn.style.backgroundColor = "#ddd"
    }
})
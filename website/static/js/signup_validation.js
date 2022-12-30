var InputId = document.getElementById("InputId")
var InputPassword = document.getElementById("InputPassword")
var InputPasswordCheck = document.getElementById("InputPasswordCheck")
var InputEmail = document.getElementById("InputEmail")
var infoForm = document.getElementById("infoForm")
var InputName = document.getElementById("InputName")
var InputGender = document.getElementById("InputGender")
var InputAge = document.getElementById("InputAge")
var submitBtn = document.getElementById("submitBtn")
$('#duplicateId').hide();
$('#posibleId').hide();

InputId.addEventListener("input",function(){
    InputId.classList.remove("is-invalid")
    InputId.classList.remove("is-valid")

    if(InputId.value.length < 1) {
        InputId.classList.remove("is-invalid")
        InputId.classList.remove("is-valid")
        $('#duplicateId').hide();
        $('#posibleId').hide();
        return
    }

    if(InputId.value.length < 5) {
        InputId.classList.add("is-invalid")
    } else {
        $.ajax({
            type: 'POST',
            url: '/duplicate_id',
            data: {"input_id":InputId.value},
            dataType: "json",
            success: function(response) {
                if(response["check"]) { 
                    //회원가입 가능
                    $('#duplicateId').hide();
                    $('#posibleId').show();
                    InputId.classList.add("is-valid")
                    InputId.classList.remove("is-invalid")
                } else {
                    //회원가입 불가능
                    $('#duplicateId').show();
                    $('#posibleId').hide();
                    InputId.classList.add("is-invalid")
                    InputId.classList.remove("is-valid")
                }
            },
            error: function(request,status,error) {
                console.log("no ajax")
            }
        });
    }
})

InputPassword.addEventListener("input",function(){
    InputPassword.classList.remove("is-invalid")
    InputPassword.classList.remove("is-valid")

    var reg = /(?=.*\d{1,50})(?=.*[a-zA-Z]{2,50}).{8,50}$/

    if( !reg.test(InputPassword.value) ) InputPassword.classList.add("is-invalid")
    else InputPassword.classList.add("is-valid")

    if(InputPassword.value == "") {
        InputPasswordCheck.classList.remove("is-invalid")
        InputPasswordCheck.classList.remove("is-valid")

        return
    }

    InputPasswordCheck.classList.remove("is-invalid")
    InputPasswordCheck.classList.remove("is-valid")
    if( InputPassword.value != InputPasswordCheck.value) InputPasswordCheck.classList.add("is-invalid")
    else InputPasswordCheck.classList.add("is-valid")
})

InputPasswordCheck.addEventListener("input",function(){
    InputPasswordCheck.classList.remove("is-invalid")
    InputPasswordCheck.classList.remove("is-valid")

    if(InputPasswordCheck.value == "") return

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

    if(InputId.classList.contains("is-valid") && InputPassword.classList.contains("is-valid") && InputPasswordCheck.classList.contains("is-valid") && InputEmail.classList.contains("is-valid") && InputName.value.length>0 && InputAge.value != 'else' && InputGender.value != 'else') {
        submitBtn.removeAttribute("disabled",false)
        submitBtn.style.backgroundColor = "#FD7537"
    }
    else{
        submitBtn.setAttribute("disabled",true)
		submitBtn.style.backgroundColor = "#ddd"
    }
})
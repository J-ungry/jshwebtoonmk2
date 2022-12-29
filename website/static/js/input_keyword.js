//자동완성 클릭 시 키워드 추가 필요
const release_btn = document.getElementsByClassName("release-btn");
const output=document.getElementById("reload_location")
let select_user_keyword=[]

const test = document.getElementById("test");
// 버튼태그 test
$('.button-result').on('click',function(event){
    console.log($(this).attr('value'))
})

//리스트 선택시 발생
$('li').on('click',function(event){
    const select_user=document.getElementById("select_keyword")
    let keyword=$(this).attr('name')    
    let user_keyword=$(this).text()

    //동일한 값 안들어가도록 수정
    if (select_user_keyword.includes(user_keyword)){
        return
    } else {
        select_user_keyword.push(user_keyword);
    }
    console.log(select_user_keyword)
    $.ajax({
        type: 'POST',
        url: '/input_keyword',
        data: { "keyword": keyword, "user_keyword": user_keyword },
        dataType: "json",
        success: function (response) {
            for (let prop in select_user_keyword) {
                if (user_keyword == select_user_keyword[prop]) {
                    fun_key = user_keyword.replace(' ', '_')
                    select_user.innerHTML += `
                        <div id="keyword_btn${prop}">
                            <button type="button" class="btn btn-info">${select_user_keyword[prop]}</button>
                            <button onclick="remove_btn(${prop},'${fun_key}')" name="${prop}" type="button" class="btn-close" aria-label="Close"></button>
                        </div>
                    `
                }
            }

            const list_len = $(response["webtoon_title"]).length
            output.innerHTML+=`
                    <div id="${fun_key}" class="keywords">
            `
            let keyword_result = document.getElementById(fun_key)
            for (let i = 0; i < list_len; i++) {
                //전체를 div를 감싼다. 어떤 키워드를 삭제할지 알아야함
                keyword_result.innerHTML+=`
                    <a class="button-result" href="/get_rcm/${response["webtoon_title"][i]}">
                        <div>
                            <img src='${response["webtoon_thumb"][i]}' style="width:100px; height:100px">
                        </div>  

                        <div>
                            <p>${response["webtoon_title"][i]}</p>
                        </div>

                        <div>
                            <p>${response["webtoon_author"][i]}</p>
                        </div>
                        <div>
                            <p>${response["webtoon_intro"][i]}</p>
                        </div>                    
                    </a>
                `
            }
            output.innerHTML += `</div>`
        },
        error: function (request, status, error) {
            console.log("no ajax")
        }
    });
})

// 키워드 삭제 버튼
function remove_btn(number, keyword) {
    index = "keyword_btn" + number
    const close_number = document.getElementById(index)
    const div_container = document.getElementById(keyword)
    select_user_keyword.splice(index, 1)
    div_container.remove()
    close_number.remove();
}


// 키워드 검색 자동완성
$('#inputAutoCompleteKeyword').autocomplete({
    source: function (request, response) { //source: 입력시 보일 목록
        $.ajax({
            url: "/keyword_autocomplete"
            , type: "POST"
            , data: { value: request.term }	// 검색 키워드
            , success: function (data) { 	// 성공
                response(
                    $.map(data.keywordList, function (item) {
                        return {
                            label: item  	// 목록에 표시되는 값
                            , value: item		// 선택 시 input창에 표시되는 값
                        };
                    })
                );    //response
            }
            , error: function () { //실패
                alert("오류가 발생했습니다.");
            }
        });
    }
    , focus: function (event, ui) { // 방향키로 자동완성단어 선택 가능하게 만들어줌	
        return false;
    }
    , minLength: 1// 최소 글자수
    , autoFocus: false // true == 첫 번째 항목에 자동으로 초점이 맞춰짐
    , delay: 100	//autocomplete 딜레이 시간(ms)
});

$(release_btn).on('click',function(event){
    let select_user=document.getElementById("select_keyword")
    let keywords = $(output).find('div')
    select_user_keyword = []
    select_user.innerHTML = ''
    keywords.remove();
});

// 검색한 키워드 추가 버튼
$('.addAutoCompleteKeyword').on('click', function (event) {
    const inputValue = document.getElementById('inputAutoCompleteKeyword').value;
    console.log("inputValue :", inputValue);
    $.ajax({
        type: 'POST',
        url: '/addAutoCompleteKeyword',
        data: { "inputValue": inputValue },
        dataType: "json",
        success: function (response) { 	// 성공
            console.log(response);
            console.log(response.num);
        },
        error: function (request, status, error) {
            console.log("no ajax")
        }
    });
})


//자동완성 클릭 시 키워드 추가 필요
const release_btn = document.getElementsByClassName("release-btn");

const output = document.getElementById("reload_location")
const select_user = document.getElementById("select_keyword")
let select_user_keyword = []

const test = document.getElementById("test");

//리스트 선택시 발생
$('li').on('click', function (event) {
    let keyword = $(this).attr('name')
    let user_keyword = $(this).text()

    //동일한 값 안들어가도록 수정
    if (select_user_keyword.includes(user_keyword)) {
        return
    } else {
        select_user_keyword.push(user_keyword);
    }
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
                        <div id="keyword_btn${prop}" class="button-keywords d-flex align-items-center mb-3">
                            <button id="scroll_btn" onclick="scroll_btn(${fun_key})" type="button" class="btn btn-info">
                                ${select_user_keyword[prop]}
                            </button>
                            <button onclick="remove_btn(${prop},'${fun_key}')" name="${prop}" type="button" class="btn-close" aria-label="Close"></button>
                        </div>
                    `
                }
            }

            const list_len = $(response["webtoon_title"]).length
            output.innerHTML += `
                <div id="${fun_key}" class="keywords">
                    <p class="mt-3" style="font-size: 20px;"><strong>${user_keyword}</strong></p>
            `
            let keyword_result = document.getElementById(fun_key)
            for (let i = 0; i < list_len; i++) {
                //전체를 div를 감싼다. 어떤 키워드를 삭제할지 알아야함
                keyword_result.innerHTML += `
                <div class="div-result">
                    <a class="button-result d-flex align-items-center" href="/get_rcm/${response["webtoon_title"][i]}">
                        <div class="div-img">
                            <img src='${response["webtoon_thumb"][i]}' style="width:100px; height:100px">
                        </div>  
                        <div class="div-tai">
                        <div class="div-title">
                            <p style="font-size:24px;">${response["webtoon_title"][i]}</p>
                        </div>

                        <div class="div-author">
                            <p style="font-size:16px;">${response["webtoon_author"][i]}</p>
                        </div>
                        <div class="div-intro">
                            <p style="font-size:16px; line-height: 2;">${response["webtoon_intro"][i]}</p>
                        </div>    
                        </div>                
                    </a>
                </div>
                `
            }
            output.innerHTML += `</div>`
        },
        error: function (request, status, error) {
            console.log("no ajax")
        }
    });3
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

$(release_btn).on('click', function (event) {
    let select_user = document.getElementById("select_keyword")
    let keywords = $(output).find('div')
    select_user_keyword = []
    select_user.innerHTML = ''
    keywords.remove();
});

// 검색한 키워드 추가 버튼
$('.addAutoCompleteKeyword').on('click', function (event) {
    const inputValue = document.getElementById('inputAutoCompleteKeyword').value;

    $.ajax({
        type: 'POST',
        url: '/addAutoCompleteKeyword',
        data: { "inputValue": inputValue },
        dataType: "json",
        success: function (response) {
            const { existInDB } = response;
            if (existInDB) {
                const { inputValue, keyword_type, webtoon_title,
                    webtoon_author, webtoon_thumb, webtoon_intro } = response;

                let keyword = keyword_type
                let user_keyword = inputValue

                //동일한 값 안들어가도록 수정
                if (select_user_keyword.includes(user_keyword)) {
                    return
                } else {
                    select_user_keyword.push(user_keyword);
                }

                for (let prop in select_user_keyword) {
                    if (user_keyword == select_user_keyword[prop]) {
                        fun_key = user_keyword.replace(' ', '_')
                        select_user.innerHTML += `
                            <div id="keyword_btn${prop}" class="button-keywords d-flex align-items-center mb-3">
                                <button id="scroll_btn" onclick="scroll_btn(${fun_key})" type="button" class="btn btn-info">
                                    ${select_user_keyword[prop]}
                                </button>
                                <button onclick="remove_btn(${prop},'${fun_key}')" name="${prop}" type="button" class="btn-close" aria-label="Close"></button>
                            </div>
                        `
                    }
                }

                const list_len = $(response["webtoon_title"]).length

                output.innerHTML += `
                <div id="${fun_key}" class="keywords">
                    <p class="mt-3" style="font-size: 20px;"><strong>${user_keyword}</strong></p>
                `
                let keyword_result = document.getElementById(fun_key)
                for (let i = 0; i < list_len; i++) {
                    //전체를 div를 감싼다. 어떤 키워드를 삭제할지 알아야함
                    keyword_result.innerHTML += `
                    <div class="div-result">
                        <a class="button-result d-flex align-items-center" href="/get_rcm/${response["webtoon_title"][i]}">
                            <div class="div-img">
                                <img src='${response["webtoon_thumb"][i]}' style="width:100px; height:100px">
                            </div>  
                            <div class="div-tai">
                            <div class="div-title">
                                <p style="font-size:24px;">${response["webtoon_title"][i]}</p>
                            </div>
    
                            <div class="div-author">
                                <p style="font-size:16px;">${response["webtoon_author"][i]}</p>
                            </div>
                            <div class="div-intro">
                                <p style="font-size:16px; line-height: 2;">${response["webtoon_intro"][i]}</p>
                            </div>    
                            </div>                
                        </a>
                    </div>
                    `
                }
                output.innerHTML += `</div>`

                $('#inputAutoCompleteKeyword').val('');

            } else {
                alert('검색한 키워드가 존재하지 않습니다.');
            }
        },
        error: function (request, status, error) {
            console.log("no ajax")
        }
    });

})

// 해당 스크롤 이동 : 수정 필요
function scroll_btn(scroll_index) {
    let offset = $(scroll_index).offset();
    $('html,body').animate({scrollTop : offset.top},200)    // 200. 숫자가 클수록 천천히 스크롤 이동
}

function scroll_up() {
    let keyword_input = $('#keyword_container').offset();
    $('html,body').animate({scrollTop : keyword_input.top},200)
}
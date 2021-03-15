
colors = ['#F3F799', '#F7819F', '#F7BE81', '#81F781', '#D6DBDF', '#AED6F1', '#D7BDE2']

carawl_id_tag =  document.querySelector("#carawl_id_tag")

index_tag = document.querySelector("#index_tag")
title_tag = document.querySelector("#title_tag")
text_tag = document.querySelector("#text_tag")
keyword_tag = document.querySelector("#keyword_tag")

btn_tag = document.querySelector("#btn_tag")
btn_prev_tag = document.querySelector("#btn_prev_tag")

product_tag = document.querySelector("#product_tag")
att_midle_tag = document.querySelector("#att_midle_tag")
att_low_tag = document.querySelector("#att_low_tag")
link_tag = document.querySelector("#link_tag")
sensitive_tag = document.querySelector("#sensitive_tag")


exception_word=['되다', '안되다', '하다', '이다', '다']

exception_company = ['다이슨']

function prev(){
    btn_tag.disabled=false
    count = 1*title_tag.dataset.num-1
    show(count,data)

    if(count <= 0){
        btn_prev_tag.disabled=true
    }
    now_url = window.location.href
    if(now_url.includes('validation_checkbox')){
        check_checkbox(count)
    }

}
//form에 data의 값을 표시해주는것
function check_checkbox(count){
    comm_tag=document.getElementById("comment_result")
    garbage_tag=document.getElementById("garbage_result")
    for (var i=0; i<5; i++) {
        checkbox_tag = document.getElementsByName("result")[i]
        if ( data[count][checkbox_tag.value] == "Y") {
            checkbox_tag.checked = true

        }else{
            checkbox_tag.checked = false
            if (data[count]['진성여부']=='N') {
                comm_tag.value=data[count]['진성여부_comment'] 
            } else if ((data[count]['진성여부']=='Y' && data[count]['L1']=='N')) {
                comm_tag.value=data[count]['L1_comment'] 
            } else if ((data[count]['진성여부']=='Y' && data[count]['L1']=='Y' && data[count]['L3']=='N')) {
                comm_tag.value=data[count]['L3_comment'] 
            } else if ((data[count]['진성여부']=='Y' && data[count]['L1']=='Y' && data[count]['L3']=='Y' && data[count]['L6']=='N')) {
                comm_tag.value=data[count]['L6_comment'] 
            } else if ((data[count]['진성여부']=='Y' && data[count]['L1']=='Y' && data[count]['L3']=='Y' && data[count]['L6']=='Y' && data[count]['L7']=='N')) {
                comm_tag.value=data[count]['L7_comment'] 
            } else if ((data[count]['진성여부']=='Y' && data[count]['L1']=='Y' && data[count]['L3']=='Y' && data[count]['L6']=='Y' && data[count]['L7']=='Y')) {
                comm_tag.value=data[count]['비고'] 
            }
        }
        
    }

    garbage_tag.value=data[count]['가비지키워드']
    
}

$(document).keydown(function(event) {  
    focusEle = document.activeElement;     
    if (document.getElementById('comment_result') == focusEle) {         
    }    
    else {                
        if (event.keyCode == '37') {
            prev()
        }
        else if (event.keyCode == '39') {
            next()
            // $("input:checkbox[value='진성여부']").prop("checked", true);
            // $("input:checkbox[value='L1']").prop("checked", true);
            // $("input:checkbox[value='L3']").prop("checked", true);
        }
        else if (event.keyCode == '81') {
            if ($("input:checkbox[value='진성여부']").is(":checked") == true){
                $("input:checkbox[value='진성여부']").prop("checked", false)
                $("input:checkbox[value='L1']").prop("checked", false) 
                $("input:checkbox[value='L3']").prop("checked", false) 
                $("input:checkbox[value='L6']").prop("checked", false)    
                $("input:checkbox[value='L7']").prop("checked", false)    
            }
            else {
                $("input:checkbox[value='진성여부']").prop("checked", true)
            }
        }
        else if (event.keyCode == '87') {
            if ($("input:checkbox[value='L1']").is(":checked") == true){
                $("input:checkbox[value='L1']").prop("checked", false)
                $("input:checkbox[value='L3']").prop("checked", false) 
                $("input:checkbox[value='L6']").prop("checked", false)    
                $("input:checkbox[value='L7']").prop("checked", false)    
            }
            else {
                $("input:checkbox[value='진성여부']").prop("checked", true)
                $("input:checkbox[value='L1']").prop("checked", true)
            }
        }
        else if (event.keyCode == '69') {
            if ($("input:checkbox[value='L3']").is(":checked") == true){

                $("input:checkbox[value='L3']").prop("checked", false)
                $("input:checkbox[value='L6']").prop("checked", false)
                $("input:checkbox[value='L7']").prop("checked", false)   
            }
            else {
                $("input:checkbox[value='진성여부']").prop("checked", true)
                $("input:checkbox[value='L1']").prop("checked", true)
                $("input:checkbox[value='L3']").prop("checked", true)
            }
        }
        else if (event.keyCode == '82') {
            if ($("input:checkbox[value='L6']").is(":checked") == true){
                $("input:checkbox[value='L6']").prop("checked", false)   
                $("input:checkbox[value='L7']").prop("checked", false)   

            }
            else {
                $("input:checkbox[value='진성여부']").prop("checked", true)
                $("input:checkbox[value='L1']").prop("checked", true)
                $("input:checkbox[value='L3']").prop("checked", true)
                $("input:checkbox[value='L6']").prop("checked", true)

            }
        }
        else if (event.keyCode == '32') {
            $(':focus').blur();
            event.preventDefault();
            if ($("input:checkbox[value='L7']").is(":checked") == true){

                $("input:checkbox[value='L7']").prop("checked", false)    
            }
            else {
                $("input:checkbox[value='진성여부']").prop("checked", true)
                $("input:checkbox[value='L1']").prop("checked", true)
                $("input:checkbox[value='L3']").prop("checked", true)
                $("input:checkbox[value='L6']").prop("checked", true)
                $("input:checkbox[value='L7']").prop("checked", true)
            }
        }
    }           
})

function show(count, data){
    show_count = count+2
    keys = data[count]['매치워드'].split('/')

    if(data[count]['키워드'] == undefined)
        index_num=show_count+"행"
    else
        index_num=show_count+"행 " + "( "+data[count]['키워드']+" )"

    title = data[count]['제목'] 
    text = data[count]['원문']
    keyword = data[count]['매치워드']

    

    for(i =0 ;i < keys.length ; i++){
        //각 키워드를 공란으로 쪼갠 뒤 첫 글자가져온다
        key = keys[i].split(' ')[0]
        
        if (!exception_company.includes(key)){
            for (j=0; j<exception_word.length; j++) {
                // 파싱 시 하다, 되다 등 예외 단어가 있다면 그 전 까지가 key가 된다.
                if (key.includes(exception_word[j])) {
                    index=key.indexOf(exception_word[j])
                    key=key.substr(0, index)
                    break
                }
            }
        }


        //하이라으트의 색상을 다르게 하기위해 색상 정보를 담은 colors 리스트를 사용
        if(i >= colors.length )
            color = colors[colors.length-1]
        else
            color = colors[i]

        //key와 replace를 할 배경색이 있는 key 생성
        mark_tag = "<mark style ='background-color: "+color+"'>"+key+"</mark>"

        title = title.replaceAll(key, mark_tag)
        text = text.replaceAll(key, mark_tag)
        keyword = keyword.replaceAll(key, mark_tag)


    }

    product_tag.innerHTML = data[count]['제품']
    att_midle_tag.innerHTML = data[count]['속성중분류']
    att_low_tag.innerHTML = data[count]['속성소분류']
    sensitive_tag.innerHTML = data[count]['감성']
    carawl_id_tag.innerHTML = data[count]['크롤아이디']

    link_tag.href = data[count]['url']
    
    index_tag.innerHTML = index_num
    title_tag.innerHTML = title
    text_tag.innerHTML = text
    keyword_tag.innerHTML = keyword
    

    

    title_tag.dataset.num = count
}

window.onload = function(){         
    next() 
    // $("input:checkbox[value='진성여부']").prop("checked", true);
    // $("input:checkbox[value='L1']").prop("checked", true);
    // $("input:checkbox[value='L3']").prop("checked", true);          
 }

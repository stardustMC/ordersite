$(function () {
    bindSendEvent();
    bindLoginEvent();
})

let total_seconds = 10;
let count = total_seconds;

function bindSendEvent() {
    $("#send-btn").on('click', function () {
        // ajax request
        let role_data = $('#id_role_0').prop('checked') ? 1 : 2;
        let email_data = $('#id_email').val()
        $.ajax({
            url: '/email_send/',
            type: 'get',
            data: {role: role_data, email: email_data},
            success: function (res) {
                if(res.status){
                    countdown("send-btn");
                }else{
                    console.log(res.details)
                }
            }
        })
    })
}

function countdown(id_btn) {
    const ID = setInterval(function () {
        count = count - 1;
        let $btn = $(`#${id_btn}`);
        $btn.prop('disabled', true);
        $btn.text(`${count}秒后可重发`);
        if(count === 0){
            clearInterval(ID);
            $btn.prop('disabled', false);
            $btn.text("发送验证码");
            count = total_seconds;
        }
    }, 1000)
}

function bindLoginEvent() {
    $('#login-btn').on('click', function () {
        let role_data = $('#id_role_0').prop('checked') ? 1 : 2;
        let email_data = $('#id_email').val();
        let code_data = $('#id_code').val();
        $.ajax({
            url: '/email_login/',
            data: {role: role_data, email: email_data, code: code_data},
            type: 'post',
            success: function (res) {
                if(res.status){
                    window.location.assign("/home/");
                }else{
                    const details = JSON.parse(res.details)
                    for(let field in details){
                        $(`.${field}-error`).html(details[field][0]['message'])
                    }
                }
            }
        })
    })
}
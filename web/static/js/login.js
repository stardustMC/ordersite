$(function () {
    $('#id_role_0').prop('checked', true);

})

$('#login button').on('click', function () {
    let r1 = $("#id_role_0");
    // let r2 = $("#id_role_1");
    let role = r1.prop("checked") ? 1 : 2;
    let data = {
        role: role,
        username: $("#id_username").val(),
        password: $("#id_password").val(),
    }

    $.ajax({
        url: "/login/",
        type: "POST",
        data: data,
        success: function (res){
            if(res.status){
                window.location.assign("/home/")
            }else{
                const details = JSON.parse(res.details)
                for(let field in details){
                    $(`.${field}-error`).html(details[field][0]['message'])
                }
            }
        }
    })
})
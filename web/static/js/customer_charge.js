function format_date(date) {
    let year = date.getFullYear();
    let month = date.getMonth().toString().padStart(2, '0');
    let day = date.getDate().toString().padStart(2, '0');
    let hour = date.getHours().toString().padStart(2, '0');
    let minutes = date.getMinutes().toString().padStart(2, '0');
    let seconds = date.getSeconds().toString().padStart(2, '0');

    return `${year}/${month}/${day} ${hour}:${minutes}:${seconds}`
}

function isJSONSerializable(str) {
    try {
        JSON.parse(str);
        return true;
    } catch (e) {
        return false;
    }
}

$(function () {
    $("#confirm-btn").on('click', function (){
        let cid = $(this).attr("cid");
        $.ajax({
            url: `/customer/charge/${cid}/add/`,
            type: "post",
            data: $("#add_charge_form").serialize(),
            headers: {
                "X-CSRFTOKEN" : "uAdq75mAvvKe9f2Ot5pDOCuXkO4JYYiLlyHYvTCx2lrHe4iViltoeuCHm2qUxtLW"
            },
            success: function (res) {
                if(res.status){
                    window.location.reload();
                }else{
                    if(isJSONSerializable(res.details)){
                        let error_dict = JSON.parse(res.details);
                        console.log(error_dict)
                        for (let field in error_dict) {
                            $(`.${field}-error-span`).html(error_dict[field][0]);
                        }
                    }else{
                        $(".__all__-error-span").html(res.details);
                    }
                }
            }
        })
    })
})
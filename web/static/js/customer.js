let row_id = 1;
let row_username = "";

$('.table-prior').on('click', '.delete-btn', function () {
    let row = $(this).parents('tr');
    row_id = row.attr('row-id');
    row_title = row.attr('row-title');
    $('.modal-body').text(`确定要删除ID为${row_id}的用户${row_username}吗？`);
})

$('#modal-delete-btn').on('click', function () {
    $.ajax({
        url: `/customer/delete/${row_id}/`,
        type: 'post',
        headers: {
            "X-CSRFTOKEN" : "uAdq75mAvvKe9f2Ot5pDOCuXkO4JYYiLlyHYvTCx2lrHe4iViltoeuCHm2qUxtLW"
        },
        success: function (res) {
            if(res.status){
                $(`tr[row-id=${row_id}]`).remove()
                $("#modal-cancel-btn").trigger("click")
            }else{

            }
        }
    })
})
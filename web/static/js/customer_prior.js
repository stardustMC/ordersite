let row_id = 1;
let row_title = "";
let row_discount = 0;

$('.table-prior').on('click', '.delete-btn', function () {
    let row = $(this).parents('tr');
    row_id = row.attr('row-id');
    row_title = row.attr('row-title');
    row_discount = row.attr('row-discount');
    $('.modal-body').text(`确定要删除ID为${row_id}级别（头衔：${row_title}，折扣：${row_discount}%）吗？`);
})

$('#modal-delete-btn').on('click', function () {
    $.ajax({
        url: `/customer/prior/delete/${row_id}`,
        type: 'post',
        headers: {
            "X-CSRFTOKEN" : "uAdq75mAvvKe9f2Ot5pDOCuXkO4JYYiLlyHYvTCx2lrHe4iViltoeuCHm2qUxtLW"
        },
        success: function (res) {
            if(res.status){
                $(`tr[row-id=${row_id}]`).remove()
                $('#modal-cancel-btn').trigger("click")
            }else{
                $('.modal-error-span').html(res.details)
            }
        }
    })
})
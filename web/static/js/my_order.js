let row_id = 1;
let row_oid = "";

$('.table-prior').on('click', '.revoke-btn', function () {
    let row = $(this).parents('tr');
    row_id = row.attr('row-id');
    row_oid = row.attr('row_oid');
    $('.modal-body').text(`确定要撤销订单${row_oid}吗？`);
})

$('#modal-revoke-btn').on('click', function () {
    $.ajax({
        url: `/my_order/revoke/${row_id}/`,
        type: 'post',
        headers: {
            "X-CSRFTOKEN" : "uAdq75mAvvKe9f2Ot5pDOCuXkO4JYYiLlyHYvTCx2lrHe4iViltoeuCHm2qUxtLW"
        },
        success: function (res) {
            if(res.status){
                window.location.reload()
                $('#modal-cancel-btn').trigger("click")
            }else{
                $('.modal-error-span').html(res.details)
            }
        }
    })
})
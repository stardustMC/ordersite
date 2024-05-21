let row_id = 1;
let row_count = 0;
let row_price = 0;

$('.table-prior').on('click', '.delete-btn', function () {
    let row = $(this).parents('tr');
    row_id = row.attr('row-id');
    row_count = row.attr('row-count');
    row_price = row.attr('row-price');
    $('.modal-body').text(`确定要删除ID为${row_id}定价（播放量：${row_count}，价格：${row_price}%）吗？`);
})

$('#modal-delete-btn').on('click', function () {
    $.ajax({
        url: `/price/delete/${row_id}`,
        type: 'post',
        headers: {
            "X-CSRFTOKEN" : "uAdq75mAvvKe9f2Ot5pDOCuXkO4JYYiLlyHYvTCx2lrHe4iViltoeuCHm2qUxtLW"
        },
        success: function (res) {
            if(res.status){
                window.location.reload();
            }else{
                $('.modal-error-span').html(res.details)
            }
        }
    })
})
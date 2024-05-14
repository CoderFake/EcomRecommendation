$(document).ready(function() {
    function downloadReport() {
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var startDate = $('#order-overview .start_date').val();
        var endDate = $('#order-overview .end_date').val();

        $.ajax({
            url: '/admin/api/download-order-report/',
            type: 'POST',
            data: JSON.stringify({ start_date: startDate, end_date: endDate }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            xhrFields: {
                responseType: 'blob'
            },
            success: function(blob) {
                var url = window.URL.createObjectURL(blob);
                var a = document.createElement("a");
                a.href = url;
                a.download = "orders_report_" + startDate.replaceAll('/', '-') + "_to_" + endDate.replaceAll('/', '-') + ".xlsx"; // Sửa đổi định dạng tên file
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            },
            error: function(xhr, status, error) {
                console.error('Error downloading the report:', error);
            }
        });
    }

    $('#order-overview-download').click(function(e) {
        e.preventDefault(); // Ngăn chặn hành động mặc định của thẻ a
        downloadReport(); // Gọi hàm tải xuống khi người dùng click vào liên kết
    });
});

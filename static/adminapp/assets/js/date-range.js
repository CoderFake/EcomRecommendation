/* ====== Index ======

1. RECNT ORDERS
2. USER ACTIVITY
3. ANALYTICS COUNTRY
4. PAGE VIEWS
5. ACTIVITY USER

====== End ======*/
$(function () {
    "use strict";


    /*======== 1. RECNT ORDERS ========*/
    if ($("#recent-orders")) {
        var start = moment().subtract(29, "days");
        var end = moment();
        var cb = function (start, end) {
            $("#recent-orders .date-range-report span").html(
                start.format("ll") + " - " + end.format("ll")
            );
            var startDate = $('#recent-orders .start_date').val();
            var endDate = $('#recent-orders .end_date').val();
            recent_order();
        };

        $("#recent-orders .date-range-report").daterangepicker(
            {
                startDate: start,
                endDate: end,
                opens: 'left',
                ranges: {
                    Today: [moment(), moment()],
                    Yesterday: [
                        moment().subtract(1, "days"),
                        moment().subtract(1, "days")
                    ],
                    "Last 7 Days": [moment().subtract(6, "days"), moment()],
                    "Last 30 Days": [moment().subtract(29, "days"), moment()],
                    "This Month": [moment().startOf("month"), moment().endOf("month")],
                    "Last Month": [
                        moment()
                            .subtract(1, "month")
                            .startOf("month"),
                        moment()
                            .subtract(1, "month")
                            .endOf("month")
                    ]
                }
            },
            cb
        );
        cb(start, end);
    }

    function recent_order() {
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var startDate = $('#user-overview .start_date').val();
        var endDate = $('#user-overview .end_date').val();

        $.ajax({
            url: '/admin/api/recent_orders/',
            type: 'POST',
            data: JSON.stringify({start_date: startDate, end_date: endDate}),
            contentType: 'application/json',
            dataType: 'json',
            headers: {'X-CSRFToken': csrfToken},
            success: function (data) {
                populateOrdersTable(data);
            },
            error: function (error) {
                console.error('Error fetching login data:', error);
            }
        });
    }

    function populateOrdersTable(orders) {
        var tableBody = $('.recent-orders tbody');
        tableBody.empty();
        const statusColorMap = {
            'Accepted': 'badge-primary',
            'Ready to ship': 'badge-warning',
            'On shipping': 'badge-info',
            'Delivered': 'badge-success',
            'Cancelled': 'badge-danger',
            'Return': 'badge-secondary'
        };
        orders.forEach(function (order) {
            var badgeClass = statusColorMap[order.status] || 'badge-light';
            var productRows = order.products.map(product => `
                <div class="col-12">
                   <a class="text-dark" href="${product.product_url}">${product.product_name} - ${product.quantity} Unit(s)</a>
                </div>
            `).join('');

            var row = `
            <tr>
                <td> <a href="${order.url_view}">${order.order_number}</a></td>
                <td>
                    ${productRows}
                </td>
                <td class="d-none d-lg-table-cell">${order.order_date}</td>
                <td class="d-none d-lg-table-cell">${order.order_cost}</td>
                <td>
                    <span class="badge ${badgeClass}">${order.status}</span>
                </td>
                <td class="text-right">
                    <div class="dropdown show d-inline-block widget-dropdown">
                        <a class="dropdown-toggle icon-burger-mini" href="#"
                           role="button" id="dropdown-recent-order1"
                           data-bs-toggle="dropdown" aria-haspopup="true"
                           aria-expanded="false" data-display="static"></a>
                        <ul class="dropdown-menu dropdown-menu-right">
                            <li class="dropdown-item">
                                <a href="${order.url_view}">View</a>
                            </li>
                            <li class="dropdown-item">
                                <a href="${order.url_edit}">Edit</a>
                            </li>
                        </ul>
                    </div>
                </td>
            </tr>
       
        `;
            tableBody.append(row);
        });
    }

    recent_order();
    setInterval(recent_order, 60000);

    /*======== 2. USER ACTIVITY ========*/
    // if ($("#user-activity")) {
    //     var start = moment().subtract(1, "days");
    //     var end = moment().subtract(1, "days");
    //     var cb = function (start, end) {
    //         $("#user-activity .date-range-report span").html(
    //             start.format("ll") + " - " + end.format("ll")
    //         );
    //     };
    //
    //     $("#user-activity .date-range-report").daterangepicker(
    //         {
    //             startDate: start,
    //             endDate: end,
    //             opens: 'left',
    //             ranges: {
    //                 Today: [moment(), moment()],
    //                 Yesterday: [
    //                     moment().subtract(1, "days"),
    //                     moment().subtract(1, "days")
    //                 ],
    //                 "Last 7 Days": [moment().subtract(6, "days"), moment()],
    //                 "Last 30 Days": [moment().subtract(29, "days"), moment()],
    //                 "This Month": [moment().startOf("month"), moment().endOf("month")],
    //                 "Last Month": [
    //                     moment()
    //                         .subtract(1, "month")
    //                         .startOf("month"),
    //                     moment()
    //                         .subtract(1, "month")
    //                         .endOf("month")
    //                 ]
    //             }
    //         },
    //         cb
    //     );
    //     cb(start, end);
    // }

    /*======== 3. ANALYTICS COUNTRY ========*/
    // if ($("#analytics-country")) {
    //     var start = moment();
    //     var end = moment();
    //     var cb = function (start, end) {
    //         $("#analytics-country .date-range-report span").html(
    //             start.format("ll") + " - " + end.format("ll")
    //         );
    //     };
    //
    //     $("#analytics-country .date-range-report").daterangepicker(
    //         {
    //             startDate: start,
    //             endDate: end,
    //             opens: 'left',
    //             ranges: {
    //                 Today: [moment(), moment()],
    //                 Yesterday: [
    //                     moment().subtract(1, "days"),
    //                     moment().subtract(1, "days")
    //                 ],
    //                 "Last 7 Days": [moment().subtract(6, "days"), moment()],
    //                 "Last 30 Days": [moment().subtract(29, "days"), moment()],
    //                 "This Month": [moment().startOf("month"), moment().endOf("month")],
    //                 "Last Month": [
    //                     moment()
    //                         .subtract(1, "month")
    //                         .startOf("month"),
    //                     moment()
    //                         .subtract(1, "month")
    //                         .endOf("month")
    //                 ]
    //             }
    //         },
    //         cb
    //     );
    //     cb(start, end);
    // }

    /*======== 4. PAGE VIEWS ========*/
    if ($("#page-views")) {
        var start = moment();
        var end = moment();
        var cb = function (start, end) {
            $("#page-views .date-range-report span").html(
                start.format("ll") + " - " + end.format("ll")
            );
        };

        $("#page-views .date-range-report").daterangepicker(
            {
                startDate: start,
                endDate: end,
                opens: 'left',
                ranges: {
                    Today: [moment(), moment()],
                    Yesterday: [
                        moment().subtract(1, "days"),
                        moment().subtract(1, "days")
                    ],
                    "Last 7 Days": [moment().subtract(6, "days"), moment()],
                    "Last 30 Days": [moment().subtract(29, "days"), moment()],
                    "This Month": [moment().startOf("month"), moment().endOf("month")],
                    "Last Month": [
                        moment()
                            .subtract(1, "month")
                            .startOf("month"),
                        moment()
                            .subtract(1, "month")
                            .endOf("month")
                    ]
                }
            },
            cb
        );
        cb(start, end);
    }
    /*======== 5. ACTIVITY USER ========*/
    if ($("#activity-user")) {
        var start = moment();
        var end = moment();
        var cb = function (start, end) {
            $("#activity-user .date-range-report span").html(
                start.format("ll") + " - " + end.format("ll")
            );
        };

        $("#activity-user .date-range-report").daterangepicker(
            {
                startDate: start,
                endDate: end,
                opens: 'left',
                ranges: {
                    Today: [moment(), moment()],
                    Yesterday: [
                        moment().subtract(1, "days"),
                        moment().subtract(1, "days")
                    ],
                    "Last 7 Days": [moment().subtract(6, "days"), moment()],
                    "Last 30 Days": [moment().subtract(29, "days"), moment()],
                    "This Month": [moment().startOf("month"), moment().endOf("month")],
                    "Last Month": [
                        moment()
                            .subtract(1, "month")
                            .startOf("month"),
                        moment()
                            .subtract(1, "month")
                            .endOf("month")
                    ]
                }
            },
            cb
        );
        cb(start, end);
    }
});

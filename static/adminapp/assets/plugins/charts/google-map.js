/*======== 17. HORIZONTAL BAR CHART1 ========*/
    var hbar1 = document.getElementById("hbar1");
    var hbChart1;
    if (hbar1 !== null) {
        hbChart1 = new Chart(hbar1, {
            type: "horizontalBar",
            data: {
                labels: [],
                datasets: [{
                    label: "Revenue",
                    data: [],
                    callback: function (value) {
                        return value + "USD";
                    },
                    backgroundColor: "#88aaf3"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {display: false},
                scales: {
                    xAxes: [{
                        gridLines: {
                            drawBorder: false,
                            display: true,
                            color: "#eee",
                            zeroLineColor: "#eee",
                            tickMarkLength: 3
                        },
                        ticks: {
                            display: true,
                            beginAtZero: true,
                            fontFamily: "Roboto, sans-serif",
                            fontColor: "#8a909d",
                            callback: function (value) {
                                return value + "USD";
                            }
                        }
                    }],
                    yAxes: [{
                        gridLines: {
                            drawBorder: false,
                            display: false
                        },
                        ticks: {
                            display: true,
                            beginAtZero: false,
                            fontFamily: "Roboto, sans-serif",
                            fontColor: "#8a909d",
                            fontSize: 14
                        },
                        barPercentage: 1.6,
                        categoryPercentage: 0.2
                    }]
                },
                tooltips: {
                    mode: "index",
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 15,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: true,
                    xPadding: 10,
                    yPadding: 7,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2,
                    caretSize: 6,
                    caretPadding: 5
                }
            }
        });

    }


    google.charts.load('current', {
        'packages': ['geochart'],
        'mapsApiKey': 'AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY'
    });
    google.charts.setOnLoadCallback(drawRegionsMap);


    function drawRegionsMap() {
        fetchDataAndUpdateMap();
    }

    function fetchDataAndUpdateMap() {
        if (!google.visualization || !google.visualization.arrayToDataTable) {
            console.error("Google Visualization API has not been loaded yet.");
            return;
        }
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var startDate = $('#analytics-country .start_date').val();
        var endDate = $('#analytics-country .end_date').val();

        if (startDate && endDate && (startDate !== lastStartDate || endDate !== lastEndDate)) {
            $.ajax({
                url: '/admin/api/get-payment-by-city/',
                method: 'POST',
                headers: {'X-CSRFToken': csrfToken},
                data: JSON.stringify({start_date: startDate, end_date: endDate}),
                contentType: 'application/json',
                dataType: 'json',
                success: function (response) {
                    if (response && response.length > 1) {
                        var data = google.visualization.arrayToDataTable(response);
                        var options = {
                            region: 'VN',
                            displayMode: 'regions',
                            resolution: 'provinces',
                            colorAxis: {colors: ['#cedbf9', '#6588d5']},
                            enableRegionInteractivity: true,
                            keepAspectRatio: true,
                            width: 600,
                            height: 400
                        };
                        var chart = new google.visualization.GeoChart(document.getElementById('regions_purchase'));
                        chart.draw(data, options);
                    } else {
                        console.error('No data to display.');
                    }
                },
                error: function (error) {
                    console.error('Error fetching data:', error);
                }
            });

            $.ajax({
                url: '/admin/api/top_purchase/',
                type: 'POST',
                data: JSON.stringify({start_date: startDate, end_date: endDate}),
                contentType: 'application/json',
                dataType: 'json',
                headers: {'X-CSRFToken': csrfToken},
                success: function (response) {
                    hbChart1.data.labels = response.labels;
                    hbChart1.data.datasets[0].data = response.data;
                    hbChart1.update();
                },
                error: function (error) {
                    console.error('Error fetching acquisition data:', error);
                }
            });
            lastStartDate = startDate;
            lastEndDate = endDate;
        }
    }

    var lastStartDate = null;
    var lastEndDate = null;

    if ($("#analytics-country").length) {
        var start = moment();
        var end = moment();
        var cb = function (start, end) {
            $("#analytics-country .date-range-report span").html(
                start.format("ll") + " - " + end.format("ll")
            );
            $('#analytics-country .start_date').val(start.format('YYYY-MM-DD'));
            $('#analytics-country .end_date').val(end.format('YYYY-MM-DD'));

            fetchDataAndUpdateMap();
        };

        $("#analytics-country .date-range-report").daterangepicker({
            startDate: start,
            endDate: end,
            opens: 'left',
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, "days"), moment().subtract(1, "days")],
                'Last 7 Days': [moment().subtract(6, "days"), moment()],
                'Last 30 Days': [moment().subtract(29, "days"), moment()],
                'This Month': [moment().startOf("month"), moment().endOf("month")],
                'Last Month': [
                    moment().subtract(1, "month").startOf("month"),
                    moment().subtract(1, "month").endOf("month")
                ]
            }
        }, cb);
        cb(start, end);
    }

    setInterval(fetchDataAndUpdateMap, 60000);


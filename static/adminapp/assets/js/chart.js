/* ====== Index ======

1. DUAL LINE CHART
2. DUAL LINE CHART2
3. LINE CHART
4. LINE CHART1
5. LINE CHART2
6. AREA CHART
7. AREA CHART1
8. AREA CHART2
9. AREA CHART3
10. GRADIENT LINE CHART
11. DOUGHNUT CHART
12. POLAR CHART
13. RADAR CHART
14. CURRENT USER BAR CHART
15. ANALYTICS - USER ACQUISITION
16. ANALYTICS - ACTIVITY CHART
17. HORIZONTAL BAR CHART1
18. HORIZONTAL BAR CHART2
19. DEVICE - DOUGHNUT CHART
20. BAR CHART
21. BAR CHART1
22. BAR CHART2
23. BAR CHART3
24. GRADIENT LINE CHART1
25. GRADIENT LINE CHART2
26. GRADIENT LINE CHART3
27. ACQUISITION3
28. STATISTICS

====== End ======*/

$(document).ready(function () {
    "use strict";

    /*======== 1. DUAL LINE CHART ========*/
    var dual = document.getElementById("dual-line");
    if (dual !== null) {
        var urChart = new Chart(dual, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "Old",
                        pointRadius: 4,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        fill: false,
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        borderColor: "#fdc506",
                        data: [0, 4, 3, 5.5, 3, 4.7, 0]
                    },
                    {
                        label: "New",
                        fill: false,
                        pointRadius: 4,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        borderColor: "#88aaf3",
                        data: [0, 2, 4.3, 3.8, 5.2, 1.8, 2.2]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        right: 10
                    }
                },

                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 14,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: true,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2
                }
            }
        });
    }

    /*======== 1. DUAL LINE CHART2 ========*/
    var dual3 = document.getElementById("dual-line3");
    if (dual3 !== null) {
        var urdChart = new Chart(dual3, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "Old",
                        pointRadius: 4,
                        pointBackgroundColor: "#fec400",
                        pointBorderWidth: 2,
                        fill: false,
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        borderColor: "#fcdf80",
                        data: [0, 4, 3, 5.5, 3, 4.7, 0]
                    },
                    {
                        label: "New",
                        fill: false,
                        pointRadius: 4,
                        pointBackgroundColor: "#fec400",
                        pointBorderWidth: 2,
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        borderColor: "#ffffff",
                        data: [0, 2, 4.3, 3.8, 5.2, 1.8, 2.2]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                layout: {
                    padding: {
                        right: 10
                    }
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: true
                }
            }
        });
    }

    /*======== 3. LINE CHART ========*/
    var ctx = document.getElementById("linechart");
    if (ctx !== null) {
        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: "line",

            // The data for our dataset
            data: {
                labels: [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec"
                ],
                datasets: [
                    {
                        label: "",
                        backgroundColor: "transparent",
                        borderColor: "rgb(82, 136, 255)",
                        data: [
                            100,
                            11000,
                            10000,
                            14000,
                            11000,
                            17000,
                            14500,
                            18000,
                            5000,
                            23000,
                            14000,
                            19000
                        ],
                        lineTension: 0.3,
                        pointRadius: 5,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointHoverBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        pointHoverRadius: 8,
                        pointHoverBorderWidth: 1
                    }
                ]
            },

            // Configuration options go here
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                layout: {
                    padding: {
                        right: 10
                    }
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                display: false
                            }
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                display: true,
                                color: "#eee",
                                zeroLineColor: "#eee",
                            },
                            ticks: {
                                callback: function (value) {
                                    var ranges = [
                                        {divider: 1e6, suffix: "M"},
                                        {divider: 1e4, suffix: "k"}
                                    ];

                                    function formatNumber(n) {
                                        for (var i = 0; i < ranges.length; i++) {
                                            if (n >= ranges[i].divider) {
                                                return (
                                                    (n / ranges[i].divider).toString() + ranges[i].suffix
                                                );
                                            }
                                        }
                                        return n;
                                    }

                                    return formatNumber(value);
                                }
                            }
                        }
                    ]
                },
                tooltips: {
                    callbacks: {
                        title: function (tooltipItem, data) {
                            return data["labels"][tooltipItem[0]["index"]];
                        },
                        label: function (tooltipItem, data) {
                            return "$" + data["datasets"][0]["data"][tooltipItem["index"]];
                        }
                    },
                    responsive: true,
                    intersect: false,
                    enabled: true,
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 18,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    xPadding: 20,
                    yPadding: 10,
                    displayColors: false,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2,
                    caretSize: 10,
                    caretPadding: 15
                }
            }
        });
    }

    /*======== 4. LINE CHART1 ========*/
    var lchart1 = document.getElementById("linechart1");
    if (lchart1 !== null) {
        var urChart = new Chart(lchart1, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "Old",
                        pointRadius: 0,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        fill: false,
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        borderColor: "#fcdf80",
                        data: [0, 5, 2.5, 9.5, 3.3, 8, 0]
                    },
                    {
                        label: "New",
                        fill: false,
                        pointRadius: 0,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        borderColor: "#88aaf3",
                        data: [0, 2, 6, 5, 8.5, 3, 3.8]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: false
                }
            }
        });
    }

    /*======== 5. LINE CHART2 ========*/
    var lchart2 = document.getElementById("linechart2");
    if (lchart2 !== null) {
        var urChart2 = new Chart(lchart2, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "Old",
                        pointRadius: 0,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        fill: false,
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        borderColor: "#fcdf80",
                        data: [0, 5, 2.5, 9.5, 3.3, 8, 0]
                    },
                    {
                        label: "New",
                        fill: false,
                        pointRadius: 0,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        borderColor: "#ffffff",
                        data: [0, 2, 6, 5, 8.5, 3, 3.8]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: false
                }
            }
        });
    }

    /*======== 6. AREA CHART ========*/
    var area = document.getElementById("area-chart");
    if (area !== null) {
        var areaChart = new Chart(area, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "New",
                        pointHitRadius: 10,
                        pointRadius: 0,
                        fill: true,
                        backgroundColor: "rgba(76, 132, 255, 0.9)",
                        borderColor: "rgba(76, 132, 255, 0.9)",
                        data: [0, 4, 2, 6.5, 3, 4.7, 0]
                    },
                    {
                        label: "Old",
                        pointHitRadius: 10,
                        pointRadius: 0,
                        fill: true,
                        backgroundColor: "rgba(253, 197, 6, 0.9)",
                        borderColor: "rgba(253, 197, 6, 1)",
                        data: [0, 2, 4.3, 3.8, 5.2, 1.8, 2.2]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                layout: {
                    padding: {
                        right: 10
                    }
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 14,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: true,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2
                }
            }
        });
    }

    /*======== 7. AREA CHART1 ========*/
    var area1 = document.getElementById("areaChart1");
    if (area1 !== null) {
        var areaChart = new Chart(area1, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "New",
                        pointRadius: 0.1,
                        fill: true,
                        lineTension: 0.3,
                        backgroundColor: "rgba(76, 132, 255, 0.9)",
                        borderColor: "rgba(76, 132, 255, 0.9)",
                        data: [0, 5, 2.5, 9, 3.5, 6.5, 0]
                    },
                    {
                        label: "Old",
                        pointRadius: 0.1,
                        fill: true,
                        lineTension: 0.3,
                        backgroundColor: "rgba(253, 197, 6, 0.9)",
                        borderColor: "rgba(253, 197, 6, 1)",
                        data: [0, 2, 5.5, 2.6, 5.7, 4, 2.8]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: false
                }
            }
        });
    }

    /*======== 8. AREA CHART2 ========*/
    var area2 = document.getElementById("areaChart2");
    if (area2 !== null) {
        var areaChart = new Chart(area2, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "New",
                        pointRadius: 0.1,
                        fill: true,
                        lineTension: 0.6,
                        backgroundColor: "rgba(255, 255, 255, 0.4)",
                        borderColor: "rgba(255, 255, 255,0)",
                        data: [0, 5, 2.5, 9, 3.5, 6.5, 0]
                    },
                    {
                        label: "Old",
                        pointRadius: 0.1,
                        fill: true,
                        lineTension: 0.6,
                        backgroundColor: "rgba(255, 255, 255, 0.8)",
                        borderColor: "rgba(255, 255, 255, 0)",
                        data: [0, 2, 5.5, 2.6, 5.7, 4, 2.8]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: false
                }
            }
        });
    }

    /*======== 9. AREA CHART3 ========*/
    var area3 = document.getElementById("area-chart3");
    if (area3 !== null) {
        var areaChart3 = new Chart(area3, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "New",
                        pointHitRadius: 10,
                        pointRadius: 0,
                        fill: true,
                        backgroundColor: "rgba(255, 255, 255, 0.4)",
                        borderColor: "rgba(255, 255, 255,0)",
                        data: [0, 4, 2, 6.5, 3, 4.7, 0]
                    },
                    {
                        label: "Old",
                        pointHitRadius: 10,
                        pointRadius: 0,
                        fill: true,
                        backgroundColor: "rgba(255, 255, 255, 0.8)",
                        borderColor: "rgba(255, 255, 255, 0)",
                        data: [0, 2, 4.3, 3.8, 5.2, 1.8, 2.2]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                layout: {
                    padding: {
                        right: 10
                    }
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: true
                }
            }
        });
    }

    /*======== 10. GRADIENT LINE CHART ========*/
    var line = document.getElementById("line");
    if (line !== null) {
        line = line.getContext("2d");
        var gradientFill = line.createLinearGradient(0, 120, 0, 0);
        gradientFill.addColorStop(0, "rgba(41,204,151,0.10196)");
        gradientFill.addColorStop(1, "rgba(41,204,151,0.30196)");

        var lChart = new Chart(line, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "Rev",
                        lineTension: 0,
                        pointRadius: 4,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        fill: true,
                        backgroundColor: gradientFill,
                        borderColor: "#29cc97",
                        borderWidth: 2,
                        data: [0, 4, 3, 5.5, 3, 4.7, 1]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                layout: {
                    padding: {
                        right: 10
                    }
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 14,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: true,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2
                }
            }
        });
    }

    /*======== 11. DOUGHNUT CHART ========*/
    // var doughnut = document.getElementById("doChart");
    // if (doughnut !== null) {
    //     var myDoughnutChart = new Chart(doughnut, {
    //         type: "doughnut",
    //         data: {
    //             labels: ["completed", "unpaid", "pending", "canceled", "returned", "Broken"],
    //             datasets: [
    //                 {
    //                     label: ["completed", "unpaid", "pending", "canceled", "returned", "Broken"],
    //                     data: [4100, 2500, 1800, 2300, 400, 150],
    //                     backgroundColor: ["#88aaf3", "#50d7ab", "#9586cd", "#f3d676", "#ed9090", "#a4d9e5"],
    //                     borderWidth: 1
    //                     // borderColor: ['#88aaf3','#29cc97','#8061ef','#fec402']
    //                     // hoverBorderColor: ['#88aaf3', '#29cc97', '#8061ef', '#fec402']
    //                 }
    //             ]
    //         },
    //         options: {
    //             responsive: true,
    //             maintainAspectRatio: false,
    //             legend: {
    //                 display: false
    //             },
    //             cutoutPercentage: 75,
    //             tooltips: {
    //                 callbacks: {
    //                     title: function (tooltipItem, data) {
    //                         return "Order : " + data["labels"][tooltipItem[0]["index"]];
    //                     },
    //                     label: function (tooltipItem, data) {
    //                         return data["datasets"][0]["data"][tooltipItem["index"]];
    //                     }
    //                 },
    //                 titleFontColor: "#888",
    //                 bodyFontColor: "#555",
    //                 titleFontSize: 12,
    //                 bodyFontSize: 14,
    //                 backgroundColor: "rgba(256,256,256,0.95)",
    //                 displayColors: true,
    //                 borderColor: "rgba(220, 220, 220, 0.9)",
    //                 borderWidth: 2
    //             }
    //         }
    //     });
    // }
    var doughnut = document.getElementById("doChart");
    var myDoughnutChart = null;

    if (doughnut) {
        myDoughnutChart = new Chart(doughnut, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    label: "Order Status",
                    data: [],
                    backgroundColor: [],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                cutoutPercentage: 75,
                tooltips: {
                    callbacks: {
                        title: function (tooltipItem, data) {
                            return "Order Status: " + data["labels"][tooltipItem[0]["index"]];
                        },
                        label: function (tooltipItem, data) {
                            return data["datasets"][0]["data"][tooltipItem["index"]];
                        }
                    },
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 14,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: true,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2
                }
            }
        });
    }

    // function fetchDataAndUpdateChart() {
    //     fetch('/admin/api/order-status/')
    //         .then(response => {
    //             if (!response.ok) {
    //                 throw new Error('Network response was not ok');
    //             }
    //             return response.json();
    //         })
    //         .then(data => {
    //             if (Array.isArray(data.labels) && Array.isArray(data.data) && Array.isArray(data.backgroundColor)) {
    //                 myDoughnutChart.data.labels = data.labels;
    //                 myDoughnutChart.data.datasets.forEach((dataset) => {
    //                     dataset.data = data.data;
    //                     dataset.backgroundColor = data.backgroundColor;
    //                 });
    //                 myDoughnutChart.update();
    //             } else {
    //                 console.error('Data format is incorrect:', data);
    //             }
    //         })
    //         .catch(error => console.error('Error fetching order data:', error));
    // }

    function fetchDataAndUpdateChart() {
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var startDate = $('#order-overview .start_date').val();
        var endDate = $('#order-overview .end_date').val();

        $.ajax({
            url: '/admin/api/order-status/',
            type: 'POST',
            data: JSON.stringify({start_date: startDate, end_date: endDate}),
            contentType: 'application/json',
            dataType: 'json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (data) {
                if (Array.isArray(data.labels) && Array.isArray(data.data) && Array.isArray(data.backgroundColor)) {
                    myDoughnutChart.data.labels = data.labels;
                    myDoughnutChart.data.datasets.forEach((dataset) => {
                        dataset.data = data.data;
                        dataset.backgroundColor = data.backgroundColor;
                    });
                    myDoughnutChart.update();
                } else {
                    console.error('Data format is incorrect:', data);
                }
            },
            error: function (xhr, status, error) {
                console.error('Error fetching order data:', error);
            }
        });
    }

    if ($("#order-overview").length) {
        var start = moment().subtract(29, "days");
        var end = moment();

        var cb = function (start, end) {
            $("#order-overview .date-range-report span").html(
                start.format("ll") + " - " + end.format("ll")
            );
            $('#order-overview .start_date').val(start.format('YYYY-MM-DD'));
            $('#order-overview .end_date').val(end.format('YYYY-MM-DD'));

            fetchDataAndUpdateChart();
        };

        $("#order-overview .date-range-report").daterangepicker({
            startDate: start,
            endDate: end,
            opens: 'left',
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [
                    moment().subtract(1, "days"),
                    moment().subtract(1, "days")
                ],
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
    setInterval(fetchDataAndUpdateChart, 60000);


    /*======== 12. POLAR CHART ========*/
    var polar = document.getElementById("polar");
    if (polar !== null) {
        var configPolar = {
            data: {
                datasets: [
                    {
                        data: [43, 23, 53, 33, 55],
                        backgroundColor: [
                            "rgba(41,204,151,0.5)",
                            "rgba(254,88,101,0.5)",
                            "rgba(128,97,239,0.5)",
                            "rgba(254,196,0,0.5)",
                            "rgba(76,132,255,0.5)"
                        ],
                        label: "" // for legend
                    }
                ],
                labels: ["Total Sales", "Rejected", "Completed", "Pending", "Reserve"]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    position: "right",
                    display: false
                },
                layout: {
                    padding: {
                        top: 10,
                        bottom: 10,
                        right: 10,
                        left: 10
                    }
                },
                title: {
                    display: false,
                    text: "Chart.js Polar Area Chart"
                },
                scale: {
                    ticks: {
                        beginAtZero: true,
                        fontColor: "#1b223c",
                        fontSize: 12,
                        stepSize: 10,
                        max: 60
                    },
                    reverse: false
                },
                animation: {
                    animateRotate: false,
                    animateScale: true
                },
                tooltips: {
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 14,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: true,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2
                }
            }
        };
        window.myPolarArea = Chart.PolarArea(polar, configPolar);
    }

    /*======== 13. RADAR CHART ========*/
    var radar = document.getElementById("radar");
    if (radar !== null) {
        var myRadar = new Chart(radar, {
            type: "radar",
            data: {
                labels: [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December"
                ],
                datasets: [
                    {
                        label: "Current Year",
                        backgroundColor: "rgba(76,132,255,0.2)",
                        borderColor: "#88aaf3",
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointBorderColor: "rgba(76,132,255,1)",
                        pointBackgroundColor: "#ffffff",
                        data: [25, 31, 43, 48, 21, 36, 23, 12, 33, 36, 28, 55]
                    },
                    {
                        label: "Previous Year",
                        backgroundColor: "rgba(41, 204, 151, 0.2)",
                        borderColor: "#29cc97",
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointBorderColor: "#29cc97",
                        pointBackgroundColor: "#ffffff",
                        data: [45, 77, 22, 12, 56, 43, 71, 23, 54, 19, 32, 55]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                title: {
                    display: false,
                    text: "Chart.js Radar Chart"
                },
                layout: {
                    padding: {
                        top: 10,
                        bottom: 10,
                        right: 10,
                        left: 10
                    }
                },
                scale: {
                    ticks: {
                        beginAtZero: true,
                        fontColor: "#1b223c",
                        fontSize: 12,
                        stepSize: 10,
                        max: 60
                    }
                },
                tooltips: {
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 14,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: true,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2
                }
            }
        });
    }

    /*======== 14. CURRENT USER BAR CHART ========*/
    var cUser = document.getElementById("currentUser");
    var myUChart;

    if (cUser !== null) {
        myUChart = new Chart(cUser, {
            type: "bar",
            data: {
                labels: ["00h-2h", "2h-4h", "4h-6h", "6h-8h", "8h-10h", "10h-12h", "12h-14h", "14h-16h", "16h-18h", "20h-22h", "22h-00h"],
                datasets: [{
                    label: "Signin",
                    data: [],
                    backgroundColor: "#88aaf3"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {display: false},
                scales: {
                    xAxes: [{
                        gridLines: {drawBorder: true, display: false},
                        ticks: {
                            fontColor: "#8a909d",
                            fontFamily: "Roboto, sans-serif",
                            display: true,
                            beginAtZero: true
                        },
                        barPercentage: 0.5,
                        categoryPercentage: 0.5
                    }],
                    yAxes: [{
                        gridLines: {drawBorder: true, display: true, color: "#eee", zeroLineColor: "#eee"},
                        ticks: {
                            fontColor: "#8a909d",
                            fontFamily: "Roboto, sans-serif",
                            display: true,
                            beginAtZero: true,
                            precision: 0,
                            callback: function (value) {
                                if (value % 1 === 0) {
                                    return value;
                                }
                            }
                        }
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

    if ($("#user-overview").length) {
        var start = moment().subtract(29, "days");
        var end = moment();

        var cb = function (start, end) {
            $("#user-overview .date-range-report span").html(
                start.format("ll") + " - " + end.format("ll")
            );
            $('#user-overview .start_date').val(start.format('YYYY-MM-DD'));
            $('#user-overview .end_date').val(end.format('YYYY-MM-DD'));

            updateChartData();
        };


        $("#user-overview .date-range-report").daterangepicker({
            startDate: start,
            endDate: end,
            opens: 'left',
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [
                    moment().subtract(1, "days"),
                    moment().subtract(1, "days")
                ],
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

    function updateChartData() {
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var startDate = $('#user-overview .start_date').val();
        var endDate = $('#user-overview .end_date').val();

        $.ajax({
            url: '/admin/api/get-login-frequency/',
            type: 'POST',
            data: JSON.stringify({start_date: startDate, end_date: endDate}),
            contentType: 'application/json',
            dataType: 'json',
            headers: {'X-CSRFToken': csrfToken},
            success: function (response) {
                if (myUChart) {
                    myUChart.data.datasets[0].data = response.data;
                    myUChart.update();
                }
            },
            error: function (error) {
                console.error('Error fetching login data:', error);
            }
        });
    }

    setInterval(updateChartData, 60000);


    /*======== 15. ANALYTICS - USER ACQUISITION ========*/
    var acquisition = document.getElementById("acquisition");
    var myAcqChart;

    if (acquisition) {
        var ctx = acquisition.getContext("2d");
        acquisition.style.height = '300px';
        myAcqChart = new Chart(ctx, {
            type: "line",
            data: {
                labels: ["00h-2h", "2h-4h", "4h-6h", "6h-8h", "8h-10h", "10h-12h", "12h-14h", "14h-16h", "16h-18h", "20h-22h", "22h-00h"],
                datasets: [
                    {
                        label: "View",
                        backgroundColor: "rgba(52, 116, 212, .2)",
                        borderColor: "rgba(52, 116, 212, .7)",
                        data: [],
                        lineTension: 0.3,
                        pointBackgroundColor: "rgba(52, 116, 212, 0)",
                        pointHoverBackgroundColor: "rgba(52, 116, 212, 1)",
                        pointHoverRadius: 3,
                        pointHitRadius: 30,
                        pointBorderWidth: 2,
                        pointStyle: "rectRounded"
                    },
                    {
                        label: "Cart",
                        backgroundColor: "rgba(255, 192, 203, .3)",
                        borderColor: "rgba(255, 192, 203, .7)",
                        data: [],
                        lineTension: 0.3,
                        pointBackgroundColor: "rgba(255, 192, 203, 0)",
                        pointHoverBackgroundColor: "rgba(255, 192, 203, 1)",
                        pointHoverRadius: 3,
                        pointHitRadius: 30,
                        pointBorderWidth: 2,
                        pointStyle: "rectRounded"
                    },
                    {
                        label: "Payment",
                        backgroundColor: "rgba(178, 251, 212, .3)",
                        borderColor: "rgba(178, 251, 212, .7)",
                        data: [],
                        lineTension: 0.3,
                        pointBackgroundColor: "rgba(178, 251, 212, 0)",
                        pointHoverBackgroundColor: "rgba(178, 251, 212, 1)",
                        pointHoverRadius: 3,
                        pointHitRadius: 30,
                        pointBorderWidth: 2,
                        pointStyle: "rectRounded"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {display: false},
                scales: {
                    xAxes: [{gridLines: {display: false}}],
                    yAxes: [{
                        gridLines: {display: true, color: "#eee", zeroLineColor: "#eee"},
                        ticks: {
                            beginAtZero: true,
                            suggestedMax: 10,
                            precision: 0,
                            callback: function (value) {
                                if (value % 1 === 0) {
                                    return value;
                                }
                            }
                        }
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
                    xPadding: 20,
                    yPadding: 10,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2,
                    caretSize: 10,
                    caretPadding: 15
                }
            }
        });
    }

    if ($("#user-acquisition").length) {
        var start = moment().subtract(29, "days");
        var end = moment();

        var cb = function (start, end) {
            $("#user-acquisition .date-range-report span").html(
                start.format("MMMM D, YYYY") + " - " + end.format("MMMM D, YYYY")
            );
            $('#user-acquisition .start_date').val(start.format('YYYY-MM-DD'));
            $('#user-acquisition .end_date').val(end.format('YYYY-MM-DD'));

            updateAcqData();
        };

        $("#user-acquisition .date-range-report").daterangepicker({
            startDate: start,
            endDate: end,
            opens: 'left',
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, "days"), moment().subtract(1, "days")],
                'Last 7 Days': [moment().subtract(6, "days"), moment()],
                'Last 30 Days': [moment().subtract(29, "days"), moment()],
                'This Month': [moment().startOf("month"), moment().endOf("month")],
                'This Year': [moment().startOf("year"), moment().endOf("year")],
                'Custom Range': [moment().subtract(29, "days"), moment()]
            }
        }, cb);
        cb(start, end);

        // Set up click listeners for tabs
        $('.nav-link.todays').on('click', function () {
            var today = moment();
            $('#user-acquisition .date-range-report').data('daterangepicker').setStartDate(today);
            $('#user-acquisition .date-range-report').data('daterangepicker').setEndDate(today);
            cb(today, today);
        });

        $('.nav-link.monthly').on('click', function () {
            var startOfMonth = moment().startOf('month');
            var endOfMonth = moment().endOf('month');
            $('#user-acquisition .date-range-report').data('daterangepicker').setStartDate(startOfMonth);
            $('#user-acquisition .date-range-report').data('daterangepicker').setEndDate(endOfMonth);
            cb(startOfMonth, endOfMonth);
        });

        $('.nav-link.yearly').on('click', function () {
            var startOfYear = moment().startOf('year');
            var endOfYear = moment().endOf('year');
            $('#user-acquisition .date-range-report').data('daterangepicker').setStartDate(startOfYear);
            $('#user-acquisition .date-range-report').data('daterangepicker').setEndDate(endOfYear);
            cb(startOfYear, endOfYear);
        });
    }

    function updateAcqData() {
        var csrfToken = $('meta[name="csrf-token"]').attr('content');
        var startDate = $('#user-acquisition .start_date').val();
        var endDate = $('#user-acquisition .end_date').val();

        $.ajax({
            url: '/admin/api/get-user-acquisition/',
            type: 'POST',
            data: JSON.stringify({start_date: startDate, end_date: endDate}),
            contentType: 'application/json',
            dataType: 'json',
            headers: {'X-CSRFToken': csrfToken},
            success: function (response) {
                myAcqChart.data.datasets[0].data = response.View;
                myAcqChart.data.datasets[1].data = response.Cart;
                myAcqChart.data.datasets[2].data = response.Pay;
                var maxViewValue = Math.max(...response.View);
                myAcqChart.options.scales.yAxes[0].ticks.suggestedMax = maxViewValue + 1;
                myAcqChart.update();
            },
            error: function (error) {
                console.error('Error fetching acquisition data:', error);
            }
        });
    }

    setInterval(updateAcqData, 60000);


    /*======== 16. ANALYTICS - ACTIVITY CHART ========*/
    var activity = document.getElementById("activity");
    var config;
    var activityData = {
        accepted: [],
        ready_to_ship: [],
        on_shipping: [],
        delivered: [],
        cancelled: [],
        returned: []
    };

    if (activity !== null) {
        config = {
            type: "line",
            data: {
                labels: [],
                datasets: [
                    {
                        label: "Accepted",
                        backgroundColor: "transparent",
                        borderColor: "#80e1c1",
                        data: activityData.accepted,
                        lineTension: 0,
                        pointRadius: 5,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointHoverBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        pointHoverRadius: 7,
                        pointHoverBorderWidth: 1
                    },
                    {
                        label: "Ready to ship",
                        backgroundColor: "transparent",
                        borderColor: "#f3d676",
                        data: activityData.ready_to_ship,
                        lineTension: 0,
                        pointRadius: 5,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointHoverBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        pointHoverRadius: 7,
                        pointHoverBorderWidth: 1
                    },
                    {
                        label: "On shipping",
                        backgroundColor: "transparent",
                        borderColor: "#f2994a",
                        data: activityData.on_shipping,
                        lineTension: 0,
                        pointRadius: 5,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointHoverBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        pointHoverRadius: 7,
                        pointHoverBorderWidth: 1
                    },
                    {
                        label: "Delivered",
                        backgroundColor: "transparent",
                        borderColor: "#4c84ff",
                        data: activityData.delivered,
                        lineTension: 0,
                        pointRadius: 5,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointHoverBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        pointHoverRadius: 7,
                        pointHoverBorderWidth: 1
                    },
                    {
                        label: "Cancelled",
                        backgroundColor: "transparent",
                        borderColor: "#ff7b7b",
                        data: activityData.cancelled,
                        lineTension: 0,
                        pointRadius: 5,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointHoverBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        pointHoverRadius: 7,
                        pointHoverBorderWidth: 1
                    },
                    {
                        label: "Return",
                        backgroundColor: "transparent",
                        borderColor: "#bb6bd9",
                        data: activityData.returned,
                        lineTension: 0,
                        pointRadius: 5,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointHoverBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        pointHoverRadius: 7,
                        pointHoverBorderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                display: false,
                            },
                            ticks: {
                                fontColor: "#8a909d",
                            },
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                fontColor: "#8a909d",
                                fontFamily: "Roboto, sans-serif",
                                display: true,
                                color: "#eee",
                                zeroLineColor: "#eee"
                            },
                            ticks: {
                                beginAtZero: true,
                                fontColor: "#8a909d",
                                fontFamily: "Roboto, sans-serif",
                                callback: function(value) {
                                    return Number.isInteger(value) ? value : null;
                                }
                            }
                        }
                    ]
                },
                tooltips: {
                    mode: "index",
                    intersect: false,
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
                },
                plugins: {
                    zoom: {
                        pan: {
                            enabled: true,
                            mode: 'x',
                        },
                        zoom: {
                            enabled: true,
                            mode: 'x',
                            drag: false,
                            speed: 0.1,
                        }
                    }
                }
            }
        };

        var ctx = document.getElementById("activity").getContext("2d");
        var myLine = new Chart(ctx, config);

        var updateOrderChart = function (startDate, endDate, period) {
            var csrfToken = $('meta[name="csrf-token"]').attr('content');
            $.ajax({
                url: '/admin/api/update_order_line_chart/',
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                contentType: 'application/json',
                data: JSON.stringify({
                    start_date: startDate,
                    end_date: endDate,
                    period: period
                }),
                success: function (response) {
                    config.data.labels = response.labels;
                    config.data.datasets[0].data = response.accepted;
                    config.data.datasets[1].data = response.ready_to_ship;
                    config.data.datasets[2].data = response.on_shipping;
                    config.data.datasets[3].data = response.delivered;
                    config.data.datasets[4].data = response.cancelled;
                    config.data.datasets[5].data = response.returned;

                    // Find the maximum value from all datasets
                    var allData = response.accepted.concat(response.ready_to_ship, response.on_shipping, response.delivered, response.cancelled, response.returned);
                    var maxYValue = Math.max.apply(null, allData);
                    var stepSize = Math.ceil(maxYValue / 10);

                    config.options.scales.yAxes[0].ticks.max = maxYValue + stepSize;
                    config.options.scales.yAxes[0].ticks.stepSize = stepSize;

                    myLine.update();
                }
            });
        };

        $('#order-time').on('change', function () {
            var period = $(this).val();
            var startDate = $('#user-activity .start_date').val();
            var endDate = $('#user-activity .end_date').val();
            updateOrderChart(startDate, endDate, period);
        });

        var start = moment().subtract(1, "days");
        var end = moment().subtract(1, "days");
        var cb = function (start, end) {
            $("#user-activity .date-range-report span").html(
                start.format("ll") + " - " + end.format("ll")
            );
            $('#user-activity .start_date').val(start.format('YYYY-MM-DD'));
            $('#user-activity .end_date').val(end.format('YYYY-MM-DD'));
            var period = $('#order-time').val();
            updateOrderChart(start.format('YYYY-MM-DD'), end.format('YYYY-MM-DD'), period);
        };

        $("#user-activity .date-range-report").daterangepicker(
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

        // Set an interval to refresh the chart data every minute
        setInterval(function() {
            var period = $('#order-time').val();
            var startDate = $('#user-activity .start_date').val();
            var endDate = $('#user-activity .end_date').val();
            updateOrderChart(startDate, endDate, period);
        }, 60000);
    }

    var time_options = {
        label1: ["00h-2h", "2h-4h", "4h-6h", "6h-8h", "8h-10h", "10h-12h", "12h-14h", "14h-16h", "16h-18h", "20h-22h", "22h-00h"],
        label2:[],
        label3:[]

    }
    // var currentDate = moment();
    // var lastDayOfMonth = currentDate.endOf('month').date();
    // for (var i = 1; i <= lastDayOfMonth; i++) {
    //     time_options.label2.push(i);
    // }
    // var currentMonth = moment().month();
    // for (var i = 1; i <= currentMonth + 1; i++) {
    //     time_options.label3.push(i);
    // }
    // $('#order-time').on('change', function(){
    //     if ($(this).val() === "hour")
    //         config.data.labels = time_options.label1;
    //     else if ($(this).val() === "hour")
    //         config.data.labels = time_options.label2;
    //     else
    //         config.data.labels = time_options.label2
    //
    // })



    /*======== 19. DEVICE - DOUGHNUT CHART ========*/
    var deviceChart = document.getElementById("deviceChart");
    if (deviceChart !== null) {
        var mydeviceChart = new Chart(deviceChart, {
            type: "doughnut",
            data: {
                labels: ["Desktop", "Tablet", "Mobile"],
                datasets: [
                    {
                        label: ["Desktop", "Tablet", "Mobile"],
                        data: [60000, 15000, 25000],
                        backgroundColor: [
                            "rgba(76, 132, 255, 1)",
                            "rgba(76, 132, 255, 0.85)",
                            "rgba(76, 132, 255, 0.70)",
                        ],
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                cutoutPercentage: 75,
                tooltips: {
                    callbacks: {
                        title: function (tooltipItem, data) {
                            return data["labels"][tooltipItem[0]["index"]];
                        },
                        label: function (tooltipItem, data) {
                            return (
                                data["datasets"][0]["data"][tooltipItem["index"]] + " Sessions"
                            );
                        }
                    },

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


    /*======== 20. BAR CHART ========*/
    var barX = document.getElementById("barChart");
    if (barX !== null) {
        var myChart = new Chart(barX, {
            type: "bar",
            data: {
                labels: [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec"
                ],
                datasets: [
                    {
                        label: "signup",
                        data: [5, 6, 4.5, 5.5, 3, 6, 4.5, 6, 8, 3, 5.5, 4],
                        // data: [2, 3.2, 1.8, 2.1, 1.5, 3.5, 4, 2.3, 2.9, 4.5, 1.8, 3.4, 2.8],
                        backgroundColor: "#88aaf3"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    titleFontColor: "#888",
                    bodyFontColor: "#555",
                    titleFontSize: 12,
                    bodyFontSize: 15,
                    backgroundColor: "rgba(256,256,256,0.95)",
                    displayColors: false,
                    borderColor: "rgba(220, 220, 220, 0.9)",
                    borderWidth: 2
                }
            }
        });
    }

    /*======== 21. BAR CHART1 ========*/
    var bar1 = document.getElementById("barChart1");
    if (bar1 !== null) {
        var myChart = new Chart(bar1, {
            type: "bar",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                datasets: [
                    {
                        label: "signup",
                        data: [5, 7.5, 5.5, 6.5, 4, 9],
                        // data: [2, 3.2, 1.8, 2.1, 1.5, 3.5, 4, 2.3, 2.9, 4.5, 1.8, 3.4, 2.8],
                        backgroundColor: "#88aaf3"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: false
                }
            }
        });
    }

    /*======== 22. BAR CHART2 ========*/
    var bar2 = document.getElementById("barChart2");
    if (bar2 !== null) {
        var myChart2 = new Chart(bar2, {
            type: "bar",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                datasets: [
                    {
                        label: "signup",
                        data: [5, 7.5, 5.5, 6.5, 4, 9],
                        // data: [2, 3.2, 1.8, 2.1, 1.5, 3.5, 4, 2.3, 2.9, 4.5, 1.8, 3.4, 2.8],
                        backgroundColor: "#ffffff"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: false
                }
            }
        });
    }

    /*======== 23. BAR CHART3 ========*/
    var bar3 = document.getElementById("barChart3");
    if (bar3 !== null) {
        var bar_Chart = new Chart(bar3, {
            type: "bar",
            data: {
                labels: [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec"
                ],
                datasets: [
                    {
                        label: "signup",
                        data: [5, 6, 4.5, 5.5, 3, 6, 4.5, 6, 8, 3, 5.5, 4],
                        // data: [2, 3.2, 1.8, 2.1, 1.5, 3.5, 4, 2.3, 2.9, 4.5, 1.8, 3.4, 2.8],
                        backgroundColor: "#ffffff"
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: true
                }
            }
        });
    }

    /*======== 24. GRADIENT LINE CHART1 ========*/
    var gline1 = document.getElementById("gline1");
    if (gline1 !== null) {
        gline1 = gline1.getContext("2d");
        var gradientFill = gline1.createLinearGradient(0, 120, 0, 0);
        gradientFill.addColorStop(0, "rgba(41,204,151,0.10196)");
        gradientFill.addColorStop(1, "rgba(41,204,151,0.30196)");

        var lChart = new Chart(gline1, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "Rev",
                        lineTension: 0,
                        pointRadius: 0.1,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        fill: true,
                        backgroundColor: gradientFill,
                        borderColor: "#29cc97",
                        borderWidth: 2,
                        data: [0, 5.5, 4, 9, 4, 7, 4.7]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: false
                }
            }
        });
    }

    /*======== 25. GRADIENT LINE CHART2 ========*/
    var gline2 = document.getElementById("gline2");
    if (gline2 !== null) {
        gline2 = gline2.getContext("2d");
        var gradientFill = gline2.createLinearGradient(0, 90, 0, 0);
        gradientFill.addColorStop(0, "rgba(255,255,255,0.10196)");
        gradientFill.addColorStop(1, "rgba(255,255,255,0.30196)");

        var lChart2 = new Chart(gline2, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "Rev",
                        lineTension: 0,
                        pointRadius: 0.1,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        fill: true,
                        backgroundColor: gradientFill,
                        borderColor: "#ffffff",
                        borderWidth: 2,
                        data: [0, 5.5, 4, 9, 4, 7, 4.7]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: false
                }
            }
        });
    }

    /*======== 26. GRADIENT LINE CHART3 ========*/
    var gline3 = document.getElementById("line3");
    if (gline3 !== null) {
        gline3 = gline3.getContext("2d");
        var gradientFill = gline3.createLinearGradient(0, 90, 0, 0);
        gradientFill.addColorStop(0, "rgba(255,255,255,0.10196)");
        gradientFill.addColorStop(1, "rgba(255,255,255,0.30196)");

        var lChart3 = new Chart(gline3, {
            type: "line",
            data: {
                labels: ["Fri", "Sat", "Sun", "Mon", "Tue", "Wed", "Thu"],
                datasets: [
                    {
                        label: "Rev",
                        lineTension: 0,
                        pointRadius: 4,
                        pointBackgroundColor: "#29cc97",
                        pointBorderWidth: 2,
                        fill: true,
                        backgroundColor: gradientFill,
                        borderColor: "#ffffff",
                        borderWidth: 2,
                        data: [0, 4, 3, 5.5, 3, 4.7, 1]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        right: 10
                    }
                },
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: false,
                                display: false
                            },
                            ticks: {
                                display: false, // hide main x-axis line
                                beginAtZero: true
                            },
                            barPercentage: 1.8,
                            categoryPercentage: 0.2
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: false, // hide main y-axis line
                                display: false
                            },
                            ticks: {
                                display: false,
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: true
                }
            }
        });
    }
    /*==
    ====== 27. ACQUISITION3 ========*/
    var acquisition3 = document.getElementById("bar3");
    if (acquisition3 !== null) {
        var acChart3 = new Chart(acquisition3, {
            // The type of chart we want to create
            type: "bar",

            // The data for our dataset
            data: {
                labels: ["4 Jan", "5 Jan", "6 Jan", "7 Jan", "8 Jan", "9 Jan", "10 Jan"],
                datasets: [
                    {
                        label: "Referral",
                        backgroundColor: "rgb(76, 132, 255)",
                        borderColor: "rgba(76, 132, 255,0)",
                        data: [78, 90, 70, 75, 45, 52, 22],
                        pointBackgroundColor: "rgba(76, 132, 255,0)",
                        pointHoverBackgroundColor: "rgba(76, 132, 255,1)",
                        pointHoverRadius: 3,
                        pointHitRadius: 30
                    },
                    {
                        label: "Direct",
                        backgroundColor: "rgb(254, 196, 0)",
                        borderColor: "rgba(254, 196, 0,0)",
                        data: [88, 115, 80, 96, 65, 77, 38],
                        pointBackgroundColor: "rgba(254, 196, 0,0)",
                        pointHoverBackgroundColor: "rgba(254, 196, 0,1)",
                        pointHoverRadius: 3,
                        pointHitRadius: 30
                    },
                    {
                        label: "Social",
                        backgroundColor: "rgb(41, 204, 151)",
                        borderColor: "rgba(41, 204, 151,0)",
                        data: [103, 135, 102, 116, 83, 97, 55],
                        pointBackgroundColor: "rgba(41, 204, 151,0)",
                        pointHoverBackgroundColor: "rgba(41, 204, 151,1)",
                        pointHoverRadius: 3,
                        pointHitRadius: 30
                    }
                ]
            },

            // Configuration options go here
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                display: false
                            }
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                display: true
                            },
                            ticks: {
                                beginAtZero: true,
                                stepSize: 50,
                                fontColor: "#8a909d",
                                fontFamily: "Roboto, sans-serif",
                                max: 200
                            }
                        }
                    ]
                },
                tooltips: {}
            }
        });
        document.getElementById("customLegend").innerHTML = acChart3.generateLegend();
    }

    /*======== 28. STATISTICS ========*/
    var mstat = document.getElementById("mstat");
    if (mstat !== null) {
        var msdChart = new Chart(mstat, {
            type: "line",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
                datasets: [
                    {
                        label: "Old",
                        pointRadius: 4,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        fill: true,
                        lineTension: 0,
                        backgroundColor: "rgba(66,208,163,0.2)",
                        borderWidth: 2.5,
                        borderColor: "#42d0a3",
                        data: [10000, 17500, 2000, 11000, 19000, 10500, 18000]
                    },
                    {
                        label: "New",
                        pointRadius: 4,
                        pointBackgroundColor: "rgba(255,255,255,1)",
                        pointBorderWidth: 2,
                        fill: true,
                        lineTension: 0,
                        backgroundColor: "rgba(76,132,255,0.2)",
                        borderWidth: 2.5,
                        borderColor: "#88aaf3",
                        data: [2000, 11500, 10000, 14000, 11000, 16800, 14500]
                    }
                ]
            },
            options: {
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [
                        {
                            gridLines: {
                                drawBorder: true,
                                display: false
                            },
                            ticks: {
                                display: true, // hide main x-axis line
                                beginAtZero: true,
                                fontFamily: "Roboto, sans-serif",
                                fontColor: "#8a909d"
                            }
                        }
                    ],
                    yAxes: [
                        {
                            gridLines: {
                                drawBorder: true, // hide main y-axis line
                                display: true
                            },
                            ticks: {
                                callback: function (value) {
                                    var ranges = [
                                        {divider: 1e6, suffix: "M"},
                                        {divider: 1e3, suffix: "k"}
                                    ];

                                    function formatNumber(n) {
                                        for (var i = 0; i < ranges.length; i++) {
                                            if (n >= ranges[i].divider) {
                                                return (
                                                    (n / ranges[i].divider).toString() + ranges[i].suffix
                                                );
                                            }
                                        }
                                        return n;
                                    }

                                    return formatNumber(value);
                                },
                                stepSize: 5000,
                                fontColor: "#8a909d",
                                fontFamily: "Roboto, sans-serif",
                                beginAtZero: true
                            }
                        }
                    ]
                },
                tooltips: {
                    enabled: true
                }
            }
        });
    }

    /*======== 29. Line Gredient ========*/
    var elem = document.getElementById('myChart');
    if (typeof elem !== 'undefined' && elem !== null) {

        var ctx = elem.getContext("2d");

        var barStroke = ctx.createLinearGradient(700, 0, 120, 0);
        barStroke.addColorStop(0, 'rgba(0, 255, 188, 0.6)');
        barStroke.addColorStop(1, 'rgba(0, 205, 194, 0.6)');

        var barFill = ctx.createLinearGradient(700, 0, 120, 0);
        barFill.addColorStop(0, "rgba(0, 255, 188, 0.6)");
        barFill.addColorStop(1, "rgba(0, 205, 194, 0.6)");

        var barFillHover = ctx.createLinearGradient(700, 0, 120, 0);
        barFillHover.addColorStop(0, "rgba(0, 255, 188, 0.8)");
        barFillHover.addColorStop(1, "rgba(0, 205, 194, 0.6)");

        var myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: ["Data Set 1", "Data Set 2", "Data Set 3", "Data Set 4", "Data Set 5"],
                datasets: [{
                    label: "Data",
                    borderColor: barStroke,
                    borderWidth: 1,
                    fill: true,
                    backgroundColor: barFill,
                    hoverBackgroundColor: barFillHover,
                    data: [100, 50, 60, 80, 70]
                }]
            },
            options: {
                animation: {
                    easing: "easeOutQuart"
                },
                legend: {
                    position: "bottom",
                    display: false
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            fontColor: "#fafafa",
                            fontStyle: "bold",
                            beginAtZero: true,
                            padding: 15,
                            //display: false - remove this and commenting to display: false
                        },
                        gridLines: {
                            drawTicks: false,
                            display: false,
                            color: "transparent",
                            zeroLineColor: "transparent"
                        }
                    }],
                    xAxes: [{
                        gridLines: {
                            display: false,
                            color: "transparent",
                            zeroLineColor: "transparent"
                        },
                        ticks: {
                            padding: 15,
                            beginAtZero: true,
                            fontColor: "#fafafa",
                            fontStyle: "bold",
                            maxTicksLimit: 20,
                            //display: false - remove this and commenting to display: false
                        }
                    }]
                }
            }
        });
    }

    /*======== 30. Bar Round Line ========*/
// var data = {
//   labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
//   datasets: [{
//     label: "Dataset #1",
//     backgroundColor: "rgba(255,99,132,0.2)",
//     borderColor: "rgba(255,99,132,1)",
//     borderWidth: 2,
//     hoverBackgroundColor: "rgba(255,99,132,0.4)",
//     hoverBorderColor: "rgba(255,99,132,1)",
//     data: [65, 59, 20, 81, 56, 55, 40],
//   }]
// };

// var options = {
//   maintainAspectRatio: false,
//   scales: {
//     y: {
//       stacked: true,
//       grid: {
//         display: true,
//         color: "rgba(255,99,132,0.2)"
//       }
//     },
//     x: {
//       grid: {
//         display: false
//       }
//     }
//   }
// };

// new Chart('chart', {
//   type: 'bar',
//   options: options,
//   data: data
// });


    /*======== 31. Bar Round Line ========*/
// Chart.defaults.global.elements.rectangle.backgroundColor = '#FF0000';

    var elmbar_ctx = document.getElementById('bar-chart');
    if (typeof elmbar_ctx !== 'undefined' && elmbar_ctx !== null) {
        var bar_ctx = elmbar_ctx.getContext('2d');

        var purple_orange_gradient = bar_ctx.createLinearGradient(0, 0, 0, 600);
        purple_orange_gradient.addColorStop(0, 'orange');
        purple_orange_gradient.addColorStop(1, 'purple');

        var bar_chart = new Chart(bar_ctx, {
            type: 'bar',
            data: {
                labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3, 8, 14, 5],
                    backgroundColor: purple_orange_gradient,
                    hoverBackgroundColor: purple_orange_gradient,
                    hoverBorderWidth: 2,
                    hoverBorderColor: 'purple'
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }

    /*======== 32. Double Bar Line Chart ========*/

    var baremlctx = document.getElementById("myBarChart");
    if (typeof baremlctx !== 'undefined' && baremlctx !== null) {

        var ctx = baremlctx.getContext('2d');
        var myBarChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                },

                    {
                        label: '# of Votes2',
                        data: [24, 38, 6, 10, 4, 6],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    },


                ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            },


            onClick: function (e) {
                /*var activePoints = myBarChart.getElementsAtEvent(e);
                var selectedIndex = activePoints[0]._index; */
                /* alert(this.data.datasets[0].data[selectedIndex]);
                console.log(this.data.datasets[0].data[selectedIndex]);
                */
            }
        });

        /* https://github.com/chartjs/Chart.js/issues/2292 */
        document.getElementById("myBarChart").onclick = function (evt) {
            var activePoints = myBarChart.getElementsAtEventForMode(evt, 'point', myBarChart.options);
            var firstPoint = activePoints[0];
            var label = myBarChart.data.labels[firstPoint._index];
            var value = myBarChart.data.datasets[firstPoint._datasetIndex].data[firstPoint._index];
            alert(label + ": " + value);
        };
    }

    /*======== 33. Color Curve Bar Progressive Chart ========*/

    var curveeml_ctx = document.getElementById("chartCurveBar");
    if (typeof curveeml_ctx !== 'undefined' && curveeml_ctx !== null) {
        var ctx = curveeml_ctx.getContext('2d');

        var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
        gradientStroke.addColorStop(0, "#ff6c00");
        gradientStroke.addColorStop(1, "#ff3b74");

        var gradientBkgrd = ctx.createLinearGradient(0, 100, 0, 400);
        gradientBkgrd.addColorStop(0, "rgba(244,94,132,0.2)");
        gradientBkgrd.addColorStop(1, "rgba(249,135,94,0)");

        var draw = Chart.controllers.line.prototype.draw;
        Chart.controllers.line = Chart.controllers.line.extend({
            draw: function () {
                draw.apply(this, arguments);
                var ctx = this.chart.chart.ctx;
                var _stroke = ctx.stroke;
                ctx.stroke = function () {
                    ctx.save();
                    //ctx.shadowColor = 'rgba(244,94,132,0.8)';
                    ctx.shadowBlur = 8;
                    ctx.shadowOffsetX = 0;
                    ctx.shadowOffsetY = 6;
                    _stroke.apply(this, arguments)
                    ctx.restore();
                }
            }
        });

        var chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'line',

            // The data for our dataset
            data: {
                labels: ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr"],
                datasets: [{
                    label: "Income",
                    backgroundColor: gradientBkgrd,
                    borderColor: gradientStroke,
                    data: [5500, 2500, 10000, 6000, 14000, 1500, 7000, 20000],
                    pointBorderColor: "rgba(255,255,255,0)",
                    pointBackgroundColor: "rgba(255,255,255,0)",
                    pointBorderWidth: 0,
                    pointHoverRadius: 8,
                    pointHoverBackgroundColor: gradientStroke,
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointHoverBorderWidth: 4,
                    pointRadius: 1,
                    borderWidth: 5,
                    pointHitRadius: 16,
                }]
            },

            options: {
                tooltips: {
                    backgroundColor: '#fff',
                    displayColors: false,
                    titleFontColor: '#000',
                    bodyFontColor: '#000'

                },
                legend: {
                    display: false
                },
                scales: {
                    xAxes: [{
                        gridLines: {
                            display: false
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            // Include a dollar sign in the ticks
                            callback: function (value, index, values) {
                                return (value / 1000) + 'K';
                            }
                        }
                    }],
                }
            }
        });
    }

    /*======== 34. Color Curve Bar Progressive Chart ========*/

// var labels = ["January", "February", "March", "April", "May", "June", "July"];
// var getRandomValues = function() {
//   var array = [];

//   for (var i = 0; i < labels.length; i++) {
//     var a = Math.round(Math.random() * 7);
//     array.push(a);
//   }

//   return array;
// };

// window.chartColors = {
//   red: 	'rgba(255, 99, 132, 0.5)',
//   orange: 'rgba(255, 159, 64, 0.5)',
//   yellow: 'rgba(255, 205, 86, 0.5)',
//   green: 	'rgba(75, 192, 192, 0.5)',
//   blue: 	'rgba(54, 162, 235, 0.5)',
//   purple: 'rgba(153, 102, 255, 0.5)',
//   grey: 	'rgba(231, 233, 237, 0.5)'
// };

// var barChartData = {
//   labels: labels,
//   datasets: [
//     {
//       label: 'Dataset 1 - bar',
//       backgroundColor: [
//         window.chartColors.red,
//         window.chartColors.orange,
//         window.chartColors.yellow,
//         window.chartColors.green,
//         window.chartColors.blue,
//         window.chartColors.purple,
//         window.chartColors.red
//       ],
//       yAxisID: "y-axis-1",
//       data: getRandomValues()
//         },
//     {
//       label: 'Dataset 2 - bar',
//       backgroundColor: window.chartColors.grey,
//       yAxisID: "y-axis-1",
//       data: getRandomValues()
//         },
//     {
//       label: 'Dataset 3 - line',
//       yAxisID: "y-axis-2",
//       data: getRandomValues(),
//       type: 'line',
//       fill: false
//     },
//     {
//       label: 'Dataset 4 - line',
//       yAxisID: "y-axis-2",
//       data: getRandomValues(),
//       type: 'line',
//       fill: false
//     }
//   ]
// };

// window.onload = function() {
//   var canvas_ctx = document.getElementById("barCanvasChart");
//   if(typeof canvas_ctx !== 'undefined' && canvas_ctx !== null) {
//     var ctx = canvas_ctx.getContext("2d");

//     window.myBar = new Chart(ctx, {
//         type: 'bar',
//         data: barChartData,
//         options: {
//             responsive: true,
//             title:{
//                 display:true,
//                 text:"Chart.js Bar Chart - Multi Axis"
//             },
//             tooltips: {
//                 mode: 'index',
//                 intersect: true
//             },
//             scales: {
//       xAxes: [{
//         stacked: true
//       }],
//                 yAxes: [{
//                     type: "linear", // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
//         stacked: true,
//                     display: true,
//                     position: "left",
//                     id: "y-axis-1",
//         ticks: {
//           beginAtZero: true,
//           suggestedMin: 0,
//           suggestedMax: 10,
//                 min: 0
//         }
//                 }, {
//                     type: "linear", // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
//                     display: false,
//                     id: "y-axis-2",
//         ticks: {
//           beginAtZero: true,
//           suggestedMin: 0,
//           suggestedMax: 10,
//           min: 0
//         }
//                 }],
//             }
//         }
//     });
//   }
// };

});
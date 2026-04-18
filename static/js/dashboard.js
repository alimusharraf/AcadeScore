// =============================
// SIDEBAR TOGGLE
// =============================

function toggleSidebar() {

    const sidebar = document.getElementById("sidebar");
    const main = document.getElementById("main");

    sidebar.classList.toggle("active");
    main.classList.toggle("shift");

}


// =============================
// PERFORMANCE TREND CHART
// =============================
function renderLineChart(ctx, labels, scores) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: "Performance",
                data: scores,
                borderColor: "#ec4899",
                backgroundColor: "rgba(236,72,153,0.2)",
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            animation: {
                duration: 1500   // 🔥 smooth animation
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#fff"
                    }
                }
            },
            scales: {
                x: {
                    ticks: { color: "#aaa" }
                },
                y: {
                    ticks: { color: "#aaa" }
                }
            }
        }
    });
}


// =============================
// INFLUENCING FACTORS CHART
// =============================

function renderPieChart(canvasId, values) {

    const ctx = document.getElementById(canvasId);

    if (!ctx) return;

    new Chart(ctx, {

        type: "doughnut",

        data: {

            labels: [
                "Study",
                "Social",
                "Part Time",
                "Attendance",
                "Sleep",
                "Mental"
            ],

            datasets: [{

                data: values,

                backgroundColor: [

                    "#8b5cf6",
                    "#ec4899",
                    "#6366f1",
                    "#f472b6",
                    "#a855f7",
                    "#db2777"

                ],

                borderWidth: 0

            }]

        },

        options: {

            responsive: true,

            maintainAspectRatio: false,

            plugins: {

                legend: {

                    position: "bottom",

                    labels: {
                        color: "#ccc",
                        boxWidth: 12
                    }

                }

            }

        }

    });

}
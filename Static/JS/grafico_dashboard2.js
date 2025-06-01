document.addEventListener("DOMContentLoaded", () => {
  Chart.defaults.font.family = 'Poppins, sans-serif';
  Chart.defaults.font.size = 14;

  fetch("/api/top3-monthly")
    .then(res => res.json())
    .then(data => {
      const months = [...new Set(data.map(d => d.sale_month))];
      const products = [...new Set(data.map(d => d.product_desc))];

      const datasets = products.map((product, index) => {
        const colorPalette = ['#08416f', '#6ce5e8', '#5271ff'];
        const color = colorPalette[index % colorPalette.length];

        return {
          label: product,
          data: months.map(month => {
            const item = data.find(d => d.sale_month === month && d.product_desc === product);
            return item ? item.quantidade_total : 0;
          }),
          borderColor: color,
          backgroundColor: color,
          borderWidth: 3,
          pointRadius: 5,
          pointHoverRadius: 7,
          fill: false,
        };
      });

      const ctx = document.getElementById("salesChart").getContext("2d");
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: months,
          datasets: datasets
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          devicePixelRatio: 2, // melhora qualidade em telas retina
          interaction: {
            mode: 'nearest',
            intersect: false
          },
          plugins: {
            title: {
              display: false,
            },
            legend: {
              labels: {
                usePointStyle: true,
                pointStyle: 'rect',
                font: {
                  size: 12
                }
              }
            },
            tooltip: {
              enabled: true
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Quantidade Vendida',
                font: {
                  size: 16,
                  weight: '600'
                }
              },
              ticks: {
                font: {
                  size: 12
                }
              }
            },
            x: {
              grid: {
                display: false
              },
              title: {
                display: true,
                text: 'Mês',
                font: {
                  size: 16,
                  weight: '600'
                }
              },
              ticks: {
                font: {
                  size: 12
                }
              }
            }
          }
        }
      });
    })
    .catch(error => {
      console.error("Erro ao carregar os dados:", error);
    });
});

document.addEventListener("DOMContentLoaded", () => {
  // Definir a fonte padrão globalmente
  Chart.defaults.font.family = 'Poppins, sans-serif';
  Chart.defaults.font.size = 14;

  fetch("/api/faturamento_mensal")
    .then(response => {
      if (!response.ok) {
        throw new Error(`Erro na requisição: ${response.status}`);
      }
      return response.json();
    })
    .then(dadosFaturamento => {
      console.log("Dados recebidos:", dadosFaturamento);

      if (!dadosFaturamento || dadosFaturamento.length === 0) {
        console.error("Nenhum dado recebido!");
        return;
      }

      const labels = dadosFaturamento.map(item => item.data);
      const valores = dadosFaturamento.map(item => item.valor);

      const ctx = document.getElementById('graficoFaturamento').getContext('2d');
      if (!ctx) {
        console.error("Canvas não encontrado!");
        return;
      }

      const chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Faturamento Mensal', // O label ainda é definido, mas não será exibido
            data: valores,
            backgroundColor: ['rgba(144,202,249)', '#1c75bc', '#1162a6', '#5271ff', '#283778', '#298f68'],
            borderRadius: 5
          }]
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 250000,
              ticks: {
                stepSize: 10000,
                maxTicksLimit: 6,
                font: {
                  family: 'Poppins, sans-serif',
                  size: 12
                },
                callback: function(value) {
                  return 'R$ ' + value.toLocaleString('pt-BR', { minimumFractionDigits: 0 });
                }
              },
              title: {
                display: true,
                text: 'Faturamento (R$)',
                font: {
                  family: 'Poppins, sans-serif',
                  size: 16,
                  weight: '600'
                }
              }
            },
            x: {
              grid: {
                display: false // Esconde as linhas verticais
              },
              title: {
                display: true,
                text: 'Mês',
                font: {
                  family: 'Poppins, sans-serif',
                  size: 16,
                  weight: '600'
                }
              },
              ticks: {
                font: {
                  family: 'Poppins, sans-serif',
                  size: 12
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false // Desativa a legenda completamente
            }
          }
        }
      });
    })
    .catch(error => {
      console.error("Erro ao carregar os dados:", error);
    });
});


// GRAFICO DE VENDAS MENSAL

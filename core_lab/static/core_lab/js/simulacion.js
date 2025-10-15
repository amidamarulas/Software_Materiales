// core_lab/static/core_lab/js/simulacion.js
document.addEventListener("DOMContentLoaded", () => {
  const tipoEnsayo = document.getElementById("tipo-ensayo");
  const playBtn = document.getElementById("play-btn");
  const resetBtn = document.getElementById("reset-btn");
  const tablaDatos = document.getElementById("tabla-datos").querySelector("tbody");
  const canvas = document.getElementById("grafica");
  const ctx = canvas.getContext("2d");

  // 🔧 Fijar tamaño del canvas (NO se estira)
  canvas.width = 600;
  canvas.height = 300;

  // ⚙️ Configuración del gráfico
  const chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label: "Esfuerzo vs Deformación",
        data: [],
        borderColor: "#007bff",
        borderWidth: 2,
        pointRadius: 0,
        tension: 0.3
      }]
    },
    options: {
      responsive: false, // ❌ evita que se ajuste automáticamente
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: "Deformación (%)"
          }
        },
        y: {
          title: {
            display: true,
            text: "Esfuerzo (Pa)"
          }
        }
      },
      plugins: {
        legend: { display: true, position: "top" }
      }
    }
  });

  let tiempo = 0;
  let intervalo = null;

  // 📈 Simulación básica
  function generarDato() {
    const deformacion = tiempo * 0.5; // %
    const esfuerzoBase = tipoEnsayo.value === "traccion" ? 2.5 : 1.8;
    const esfuerzo = esfuerzoBase * deformacion * (1 + 0.1 * Math.random());

    chart.data.labels.push(deformacion.toFixed(2));
    chart.data.datasets[0].data.push(esfuerzo.toFixed(2));
    chart.update();

    const fila = document.createElement("tr");
    fila.innerHTML = `
      <td>${tiempo.toFixed(1)}</td>
      <td>${deformacion.toFixed(2)}</td>
      <td>${esfuerzo.toFixed(2)}</td>
    `;
    tablaDatos.appendChild(fila);

    tiempo += 0.5;
  }

  // ▶ Iniciar simulación
  playBtn.addEventListener("click", () => {
    if (intervalo) return;
    tablaDatos.innerHTML = "";
    tiempo = 0;
    intervalo = setInterval(generarDato, 500);
  });

  // 🔁 Reiniciar
  resetBtn.addEventListener("click", () => {
    clearInterval(intervalo);
    intervalo = null;
    tiempo = 0;
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.update();
    tablaDatos.innerHTML = `<tr><td colspan="3">Sin datos por ahora</td></tr>`;
  });
});

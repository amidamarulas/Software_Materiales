// ==========================================================
//  SIMULACION.JS - VERSIÓN FINAL Y FUNCIONAL
// ==========================================================
document.addEventListener("DOMContentLoaded", () => {
  // Variable global para mantener la instancia del gráfico
  let chartInstance = null;

  // Obtenemos todos los elementos del DOM
  const tipoEnsayoSelect = document.getElementById("tipo-ensayo");
  const materialSelect = document.getElementById("material");
  const playBtn = document.getElementById("play-btn");
  const resetBtn = document.getElementById("reset-btn");
  const tablaDatos = document.getElementById("tabla-datos").querySelector("tbody");
  const canvas = document.getElementById("grafica");
  const ctx = canvas.getContext("2d");

  // Función para crear o actualizar el gráfico
  function crearGrafico(labels = [], data = [], xLabel = "Deformación (%)", yLabel = "Esfuerzo (Pa)") {
    // Si ya existe un gráfico, lo destruimos antes de crear uno nuevo
    if (chartInstance) {
      chartInstance.destroy();
    }
    
    chartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [{
          label: "Esfuerzo vs Deformación",
          data: data,
          borderColor: "#007bff",
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: xLabel } },
          y: { title: { display: true, text: yLabel, beginAtZero: true } }
        },
        plugins: {
          legend: { display: true, position: "top" }
        }
      }
    });
  }

  // Función para reiniciar la simulación
  function reiniciarSimulacion() {
    crearGrafico(); // Llamamos a crearGrafico sin datos para mostrarlo vacío
    tablaDatos.innerHTML = `<tr><td colspan="3">Selecciona material y ensayo</td></tr>`;
  }

  resetBtn.addEventListener("click", reiniciarSimulacion);

  // Función para cargar los datos desde la API de Django
  async function cargarDatos(materialNombre, tipoEnsayo) {
    const url = `/obtener_datos?material=${encodeURIComponent(materialNombre)}&tipo_ensayo=${encodeURIComponent(tipoEnsayo)}`;
    try {
      const response = await fetch(url);
      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error);
      }

      // Extraer datos para el gráfico
      const labels = data.datos_grafica.map(d => d.x);
      const values = data.datos_grafica.map(d => d.y);

      // Llenar la tabla de datos
      const filas = data.datos_tabla.map(fila => `
        <tr>
          <td>${parseFloat(fila.tiempo).toFixed(2)}</td>
          <td>${parseFloat(fila.deformacion).toFixed(4)}</td>
          <td>${parseFloat(fila.esfuerzo).toFixed(4)}</td>
        </tr>`).join("");
      
      tablaDatos.innerHTML = filas;
      
      // Actualizar el gráfico con los nuevos datos y etiquetas de ejes
      crearGrafico(labels, values, data.eje_x_label, data.eje_y_label);

    } catch (err) {
      console.error("❌ Error al obtener datos:", err);
      tablaDatos.innerHTML = `<tr><td colspan="3">Error: ${err.message}</td></tr>`;
      reiniciarSimulacion(); // Limpiamos la gráfica si hay un error
    }
  }

  // Event Listener para el botón "Iniciar Simulación"
  playBtn.addEventListener("click", () => {
    const materialNombre = materialSelect.value;
    const tipo = tipoEnsayoSelect.value;
    
    if (!materialNombre || !tipo) {
      alert("Selecciona un material y un tipo de ensayo antes de iniciar.");
      return;
    }
    
    tablaDatos.innerHTML = `<tr><td colspan="3">Cargando datos...</td></tr>`;
    cargarDatos(materialNombre, tipo);
  });

  // Al cargar la página, creamos el gráfico vacío inicial
  crearGrafico();
});
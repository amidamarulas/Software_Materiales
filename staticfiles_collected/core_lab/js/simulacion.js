document.addEventListener("DOMContentLoaded", () => {
  // Obtenemos referencias a los elementos del DOM
  const playBtn = document.getElementById("play-btn");
  const resetBtn = document.getElementById("reset-btn");
  const machine = document.getElementById("machine"); // La imagen de la máquina
  const ctx = document.getElementById("grafica").getContext("2d"); // Contexto 2D del canvas para la gráfica
  const tabla = document.querySelector("#tabla-datos tbody"); // El cuerpo de la tabla para insertar datos
  const placeholderText = document.querySelector(".placeholder-text"); // Mensaje de la gráfica vacía

  let interval; // Variable para almacenar el ID del intervalo de la simulación
  let tiempo = 0; // Contador de tiempo de la simulación
  let datos = []; // Array para almacenar los datos generados

  // Configuración inicial de la gráfica usando Chart.js
  const chart = new Chart(ctx, {
    type: "line", // Tipo de gráfica: línea
    data: {
      labels: [], // Etiquetas del eje X (tiempo)
      datasets: [
        {
          label: "Esfuerzo (Pa)", // Etiqueta para la línea de datos
          data: [], // Datos del eje Y (esfuerzo)
          borderColor: "#004080", // Color de la línea
          borderWidth: 2, // Ancho de la línea
          fill: false, // No rellenar el área bajo la línea
          tension: 0.3, // Suavidad de la línea (curvatura)
        },
      ],
    },
    options: {
      responsive: true, // La gráfica se adapta al tamaño de su contenedor
      maintainAspectRatio: false, // Permite que la altura definida en CSS se use
      scales: {
        x: {
          title: {
            display: true,
            text: "Tiempo (s)", // Título del eje X
          },
        },
        y: {
          title: {
            display: true,
            text: "Esfuerzo (Pa)", // Título del eje Y
          },
          beginAtZero: true, // El eje Y comienza en cero
        },
      },
      plugins: {
        legend: {
          display: true, // Mostrar la leyenda (Esfuerzo Pa)
        },
      },
    },
  });

  // Función principal para iniciar la simulación
  function iniciarSimulacion() {
    clearInterval(interval); // Limpiar cualquier intervalo anterior para evitar múltiples simulaciones
    datos = []; // Resetear datos
    tiempo = 0; // Resetear tiempo
    chart.data.labels = []; // Limpiar etiquetas del gráfico
    chart.data.datasets[0].data = []; // Limpiar datos del gráfico
    tabla.innerHTML = ""; // Limpiar el contenido de la tabla

    // Ocultar el texto placeholder de la gráfica una vez que la simulación comienza
    if (placeholderText) {
      placeholderText.style.display = "none";
    }

    // Activar el efecto visual en la máquina (sombra)
    machine.classList.add("simulando");

    // Deshabilitar los botones mientras la simulación está en curso
    playBtn.disabled = true;
    resetBtn.disabled = false; // Asegurarse de que el reset esté habilitado

    // Iniciar el intervalo de la simulación
    interval = setInterval(() => {
      tiempo += 0.5; // Incremento de tiempo en cada paso (más pequeño para fluidez)

      // Simulación de datos de deformación y esfuerzo
      // Estas fórmulas generan un patrón de aumento con algunas fluctuaciones
      const deformacion = Math.sin(tiempo / 8) * 4 + 4 + (tiempo * 0.2); // Incremento progresivo con onda
      const esfuerzo = deformacion * 3.5 + Math.random() * 2; // Relación esfuerzo-deformación con ruido

      datos.push({ tiempo, deformacion, esfuerzo }); // Guardar los datos

      // Actualizar gráfico
      chart.data.labels.push(tiempo.toFixed(1)); // Añadir tiempo al eje X (con 1 decimal)
      chart.data.datasets[0].data.push(esfuerzo); // Añadir esfuerzo al eje Y
      chart.update(); // Redibujar el gráfico

      // Actualizar tabla
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${tiempo.toFixed(1)}</td>
        <td>${deformacion.toFixed(2)}</td>
        <td>${esfuerzo.toFixed(2)}</td>
      `;
      tabla.appendChild(fila);
      tabla.scrollTop = tabla.scrollHeight; // Scroll automático al final de la tabla para ver los últimos datos

      // ✨ Animación de la máquina para simular tracción
      // Cuanto mayor sea la deformación, mayor será el movimiento y el "estiramiento"
      const movimientoY = deformacion * 0.8; // Desplazamiento vertical (pinza superior sube)
      const escalaY = 1 + deformacion * 0.003; // Estiramiento vertical ligero de la máquina

      machine.style.transform = `translateY(-${movimientoY}px) scaleY(${escalaY})`;

      // Condición para finalizar la simulación automáticamente
      if (tiempo >= 25) { // La simulación dura 25 segundos
        reiniciarSimulacion(); // Llama a la función de reinicio para detener y limpiar
        alert("Simulación de ensayo de tracción finalizada.");
      }
    }, 200); // Intervalo de 200 milisegundos (5 veces por segundo)
  }

  // Función para reiniciar la simulación
  function reiniciarSimulacion() {
    clearInterval(interval); // Detener el intervalo de la simulación
    machine.style.transform = "translateY(0) scaleY(1)"; // Resetear la transformación de la máquina
    machine.classList.remove("simulando"); // Quitar la clase de simulación (quita la sombra)

    // Resetear gráfica
    chart.data.labels = [];
    chart.data.datasets[0].data = [];
    chart.update();

    // Resetear tabla
    tabla.innerHTML = "<tr><td colspan='3'>Sin datos por ahora</td></tr>";

    // Mostrar el texto placeholder de la gráfica de nuevo
    if (placeholderText) {
      placeholderText.style.display = "block";
    }

    tiempo = 0; // Resetear el contador de tiempo
    datos = []; // Resetear los datos

    // Re-habilitar el botón de play y deshabilitar el de reset
    playBtn.disabled = false;
    resetBtn.disabled = true;
  }

  // Asignar los event listeners a los botones
  playBtn.addEventListener("click", iniciarSimulacion);
  resetBtn.addEventListener("click", reiniciarSimulacion);

  // Inicializar el estado de los botones al cargar la página
  resetBtn.disabled = true; // El botón de Reiniciar está deshabilitado al principio
});
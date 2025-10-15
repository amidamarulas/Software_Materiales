// core_lab/static/core_lab/js/machine.js
document.addEventListener('DOMContentLoaded', function(){
  // SVG elements
  const crosshead = document.getElementById('crosshead');
  const specimenRect = document.getElementById('specimen-rect');
  const upperGrip = document.getElementById('upper-grip');
  const lowerGrip = document.getElementById('lower-grip');

  // Controls
  const btnPlay = document.getElementById('btn-play');
  const btnPause = document.getElementById('btn-pause');
  const btnStep = document.getElementById('btn-step');
  const btnReset = document.getElementById('btn-reset');
  const speedEl = document.getElementById('speed');
  const forceEl = document.getElementById('force');

  const dataTableBody = document.querySelector('#sim-data-table tbody');
  const materialsTableBody = document.querySelector('#materials-table tbody');

  const btnDownloadCSV = document.getElementById('btn-download-csv');
  const btnDownloadPNG = document.getElementById('btn-download-png');

  // Chart.js setup
  const ctx = document.getElementById('chartED').getContext('2d');
  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [], // deformación
      datasets: [
        { label: 'Esfuerzo (Pa)', data: [], fill: true, tension:0.2, pointRadius:2 }
      ]
    },
    options: {
      responsive: true,
      scales: {
        x: { title: { display:true, text:'Deformación (unit)' } },
        y: { title: { display:true, text:'Esfuerzo (Pa)' } }
      }
    }
  });

  // Simulation state (vacío por ahora)
  let running = false;
  let animationId = null;
  let position = 0;         // posición del crosshead (px relativo)
  const minPos = 0;
  const maxPos = 160;       // recorrido disponible (px)
  let speed = parseFloat(speedEl.value); // factor
  let appliedForce = parseFloat(forceEl.value); // kN display: not applied to data yet

  // Data arrays (vacías, listos para añadir datos reales)
  let simTime = [];         // segundos
  let simStrain = [];       // deformación
  let simStress = [];       // esfuerzo

  // helper: set transforms
  function setCrossheadY(y){
    // crosshead transform translate(x,y) -> we change only Y
    // original transform stored as "translate(120,80)"
    const tx = 120;
    crosshead.setAttribute('transform', `translate(${tx},${y})`);
    // update upper grip position (attached below crosshead)
    upperGrip.setAttribute('transform', `translate(290, ${y + 40})`);
    // lower grip anchored near bottom
    const lowerY = 300;
    lowerGrip.setAttribute('transform', `translate(290, ${lowerY})`);
    // specimen rectangle top anchored at upper grip + offset
    const specimenTopY = y + 44; // gap
    specimenRect.setAttribute('y', specimenTopY);
    // specimen height set by difference between grips:
    const gap = (lowerY - (y + 44));
    specimenRect.setAttribute('height', Math.max(6, gap));
  }

  // initial placement
  setCrossheadY(80);

  function stepSimulation(dt){
    // dt in seconds scaled by speed factor
    // For now we only animate crosshead up/down as placeholder and append empty data rows
    position += 10 * dt * speed; // px per second approx
    if(position > maxPos) position = maxPos;
    // compute y from position
    const y = 80 + position;
    setCrossheadY(y);

    // placeholder "deformación" as normalized gap / maxGap
    const lowerY = 300;
    const gap = (lowerY - (y + 44));
    const maxGap = lowerY - (80 + 44); // initial max gap
    const strain = Math.max(0, (maxGap - gap) / Math.max(1, maxGap)); // 0..1
    const stress = 0; // vacío por ahora (0 Pa)

    // append a sample time / data point if we want to show rows (for now keep sparse)
    const t = (simTime.length>0 ? simTime[simTime.length-1] + dt : 0);
    // only add every 0.2s to avoid huge tables
    if(simTime.length === 0 || t - simTime[simTime.length-1] >= 0.2){
      simTime.push(Number(t.toFixed(3)));
      simStrain.push(Number(strain.toFixed(6)));
      simStress.push(Number(stress.toFixed(3)));
      pushRowToTable(t, strain, stress);
      updateChart();
    }
  }

  function pushRowToTable(t, eps, sigma){
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${t.toFixed(3)}</td><td>${eps.toFixed(6)}</td><td>${sigma.toFixed(3)}</td>`;
    dataTableBody.appendChild(tr);
  }

  function updateChart(){
    chart.data.labels = simStrain.slice();
    chart.data.datasets[0].data = simStress.slice();
    chart.update();
  }

  // Loop
  let lastTime = null;
  function loop(now){
    if(!running) return;
    if(lastTime === null) lastTime = now;
    const dt_ms = now - lastTime;
    lastTime = now;
    const dt = Math.min(0.05, dt_ms / 1000); // clamp
    stepSimulation(dt);
    animationId = requestAnimationFrame(loop);
  }

  // Controls events
  btnPlay.addEventListener('click', ()=>{
    if(running) return;
    running = true;
    lastTime = null;
    animationId = requestAnimationFrame(loop);
  });
  btnPause.addEventListener('click', ()=>{
    running = false;
    if(animationId) cancelAnimationFrame(animationId);
    animationId = null;
    lastTime = null;
  });
  btnStep.addEventListener('click', ()=>{
    // step a 0.1s
    stepSimulation(0.1);
  });
  btnReset.addEventListener('click', ()=>{
    running = false;
    if(animationId) cancelAnimationFrame(animationId);
    animationId = null;
    position = 0;
    setCrossheadY(80);
    // clear data
    simTime = []; simStrain=[]; simStress=[];
    dataTableBody.innerHTML = '';
    updateChart();
  });

  speedEl.addEventListener('input', (e)=>{ speed = parseFloat(e.target.value); });
  forceEl.addEventListener('input', (e)=>{ appliedForce = parseFloat(e.target.value); });

  // Downloads
  btnDownloadCSV.addEventListener('click', ()=>{
    // build CSV from arrays (if empty, create header-only)
    let csv = 't[s],deformacion,esfuerzo[Pa]\n';
    for(let i=0;i<simTime.length;i++){
      csv += `${simTime[i]},${simStrain[i]},${simStress[i]}\n`;
    }
    const blob = new Blob([csv], {type:'text/csv;charset=utf-8;'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'simulacion_corelab.csv';
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  });

  btnDownloadPNG.addEventListener('click', ()=>{
    // Chart.js toBase64Image
    try {
      const dataUrl = chart.toBase64Image();
      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = 'grafica_corelab.png';
      document.body.appendChild(a); a.click(); a.remove();
    } catch (e) {
      alert('No hay gráfica disponible para descargar.');
    }
  });

  // (Opcional) Hook para llenar la tabla de materiales desde servidor (vacío por ahora)
  function loadMaterialsPlaceholder(){
    materialsTableBody.innerHTML = '';
    // vacío intencionalmente: muestra fila instructiva
    const tr = document.createElement('tr');
    tr.innerHTML = `<td colspan="5" style="color:#6b7280">No hay materiales cargados (placeholder).</td>`;
    materialsTableBody.appendChild(tr);
  }
  loadMaterialsPlaceholder();

  // inicializa tabla vacía / chart vacío
  updateChart();
});

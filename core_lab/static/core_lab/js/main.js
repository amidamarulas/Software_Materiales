document.addEventListener('DOMContentLoaded', function(){
  const btnFetch = document.getElementById('btn-fetch');
  const matSel = document.getElementById('select-material');
  const ensSel = document.getElementById('select-ensayo');
  const ctx = document.getElementById('chartED').getContext('2d');
  let chart;

  btnFetch.addEventListener('click', async () => {
    const material = matSel.value;
    const ensayo = ensSel.value;
    const res = await fetch(`/api/data/?material=${material}&ensayo=${ensayo}`);
    const data = await res.json();
    const d = data.resultados;
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: d.deformacion,
        datasets: [{
          label: 'Esfuerzo (Pa)',
          data: d.esfuerzo,
          borderColor: '#0b5ed7',
          borderWidth: 2,
          fill: false,
        }]
      },
      options: {
        scales: {
          x: { title: { display: true, text: 'Deformación' }},
          y: { title: { display: true, text: 'Esfuerzo (Pa)' }}
        }
      }
    });
  });
});

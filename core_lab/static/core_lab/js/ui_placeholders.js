document.addEventListener('DOMContentLoaded', function(){
  const btnStart = document.getElementById('btn-start');
  const btnReset = document.getElementById('btn-reset');
  const specimen = document.getElementById('specimen');
  const dataTableBody = document.querySelector('#data-table tbody');

  btnStart?.addEventListener('click', ()=>{
    // Animación placeholder: estirar probeta (simple transform)
    specimen.animate([{transform:'scaleY(1)'},{transform:'scaleY(1.5)'}],{duration:600,fill:'forwards'});
    // Añadir fila placeholder a la tabla de datos
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>0.0</td><td>—</td><td>—</td>`;
    if (dataTableBody) dataTableBody.appendChild(tr);
  });

  btnReset?.addEventListener('click', ()=>{
    specimen.style.transform = 'none';
    if (dataTableBody) dataTableBody.innerHTML = '';
  });
});

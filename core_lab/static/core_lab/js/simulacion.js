document.addEventListener("DOMContentLoaded", function () {
  const machine = document.getElementById("machine");
  const playBtn = document.getElementById("play-btn");
  const resetBtn = document.getElementById("reset-btn");

  let isPlaying = false;
  let interval;

  playBtn.addEventListener("click", () => {
    if (!isPlaying) {
      isPlaying = true;
      playBtn.textContent = "⏸ Pausar";
      simulateMotion();
    } else {
      clearInterval(interval);
      isPlaying = false;
      playBtn.textContent = "▶ Reanudar";
    }
  });

  resetBtn.addEventListener("click", () => {
    clearInterval(interval);
    isPlaying = false;
    playBtn.textContent = "▶ Iniciar Simulación";
    machine.style.transform = "scaleY(1)";
  });

  function simulateMotion() {
    let scale = 1;
    let direction = -1;

    interval = setInterval(() => {
      scale += direction * 0.01;
      if (scale <= 0.9 || scale >= 1) direction *= -1;
      machine.style.transform = `scaleY(${scale})`;
    }, 50);
  }
});

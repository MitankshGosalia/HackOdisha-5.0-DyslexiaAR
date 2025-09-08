// Camera capture, controls, and backend communication

(function () {
  const video = document.getElementById('camera');
  const overlay = document.getElementById('overlay');
  const startBtn = document.getElementById('start');
  const fontSelect = document.getElementById('fontSelect');
  const spacing = document.getElementById('spacing');
  const lineHeight = document.getElementById('lineHeight');

  let mediaStream = null;
  let running = false;

  function applyTypography() {
    overlay.style.fontFamily = fontSelect.value + ', Inter, system-ui';
    overlay.style.letterSpacing = spacing.value + 'px';
    overlay.style.lineHeight = lineHeight.value;
  }

  [fontSelect, spacing, lineHeight].forEach((el) => el.addEventListener('input', applyTypography));
  applyTypography();

  async function initCamera() {
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
      video.srcObject = mediaStream;
    } catch (e) {
      overlay.textContent = 'Camera access is required. ' + e.message;
    }
  }

  async function captureFrameBlob() {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 360;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    return new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg', 0.8));
  }

  async function sendForProcessing() {
    if (!running) return;
    try {
      const blob = await captureFrameBlob();
      const form = new FormData();
      form.append('image', blob, 'frame.jpg');
      const response = await fetch('http://127.0.0.1:8000/process-video', {
        method: 'POST',
        body: form
      });
      const data = await response.json();
      overlay.textContent = data.transformed_text || 'No text detected yet...';
    } catch (e) {
      overlay.textContent = 'Processing error: ' + e.message;
    } finally {
      if (running) setTimeout(sendForProcessing, 900);
    }
  }

  startBtn.addEventListener('click', async () => {
    if (!mediaStream) await initCamera();
    running = !running;
    startBtn.textContent = running ? 'Stop Analysis' : 'Start Analysis';
    if (running) sendForProcessing();
  });

  // Initialize camera on load (permission prompt on button interaction in some browsers)
  initCamera();
})();



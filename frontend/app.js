/**
 * ChronoCanvas Dashboard Application Logic
 * Integrates with AWS Agent Backend API & provides ambient audio/visual controls.
 */

document.addEventListener('DOMContentLoaded', () => {
  const API_BASE = window.location.origin;

  // DOM Elements
  const envLocation = document.getElementById('env-location');
  const envWeather = document.getElementById('env-weather');
  const envPhase = document.getElementById('env-phase');
  const envMood = document.getElementById('env-mood');

  const canvasIdBadge = document.getElementById('canvas-id-badge');
  const canvasTimestamp = document.getElementById('canvas-timestamp');
  const mainArtworkImg = document.getElementById('main-artwork-img');
  const artworkSkeleton = document.getElementById('artwork-skeleton');
  const paletteSwatches = document.getElementById('palette-swatches');

  const canvasTitle = document.getElementById('canvas-title');
  const canvasSubtitle = document.getElementById('canvas-subtitle');
  const canvasPoem = document.getElementById('canvas-poem');
  const canvasLore = document.getElementById('canvas-lore');
  const canvasPrompt = document.getElementById('canvas-prompt');

  const triggerAgentBtn = document.getElementById('trigger-agent-btn');
  const historyGrid = document.getElementById('history-grid');

  const fullscreenBtn = document.getElementById('fullscreen-btn');
  const imageModal = document.getElementById('image-modal');
  const modalImg = document.getElementById('modal-img');
  const modalOverlay = document.getElementById('modal-overlay');
  const closeModalBtn = document.getElementById('close-modal-btn');

  const toggleAudioBtn = document.getElementById('toggle-audio-btn');
  const soundscapeStatus = document.getElementById('soundscape-status');

  // Ambient Audio Synthesizer (Web Audio API)
  let audioCtx = null;
  let isPlayingAudio = false;
  let currentActiveCanvas = null;

  // Initial Data Load
  loadActiveCanvas();
  loadHistoryTimeline();

  // Event Listeners
  triggerAgentBtn.addEventListener('click', triggerAgentGeneration);
  fullscreenBtn.addEventListener('click', openFullscreenModal);
  modalOverlay.addEventListener('click', closeModal);
  closeModalBtn.addEventListener('click', closeModal);
  toggleAudioBtn.addEventListener('click', toggleAmbientSoundscape);

  /**
   * Loads the current active canvas from the backend.
   */
  async function loadActiveCanvas() {
    showLoadingState();
    try {
      const resp = await fetch(`${API_BASE}/canvas/latest`);
      if (!resp.ok) throw new Error('API request failed');
      const canvas = await resp.json();
      renderCanvasDetails(canvas);
    } catch (err) {
      console.warn('Backend API note: fallback to local agent trigger', err);
      // Fallback: trigger agent directly
      triggerAgentGeneration();
    }
  }

  /**
   * Renders canvas metadata and updates theme palette.
   */
  function renderCanvasDetails(canvas) {
    currentActiveCanvas = canvas;

    // Environmental metrics
    envLocation.textContent = canvas.location || 'New York, USA';
    envWeather.textContent = `${canvas.weather.condition} (${canvas.weather.temperature_f}°F)`;
    envPhase.textContent = canvas.mood.phase;
    envMood.textContent = canvas.mood.mood;

    // Canvas meta
    canvasIdBadge.textContent = `ID: ${canvas.canvas_id}`;
    canvasTimestamp.textContent = `Synthesized: ${canvas.created_at}`;

    // Textual creative content
    canvasTitle.textContent = canvas.title;
    canvasSubtitle.textContent = `Autonomous Creation during ${canvas.mood.phase}`;
    canvasPoem.textContent = canvas.poem;
    canvasLore.textContent = canvas.lore;
    canvasPrompt.textContent = canvas.prompt;

    // Dynamic HSL Theme Palette update
    applyDynamicTheme(canvas.mood.primary_hue, canvas.mood.palette);

    // Image loading
    mainArtworkImg.onload = () => {
      artworkSkeleton.classList.add('hidden');
      mainArtworkImg.classList.remove('hidden');
    };
    mainArtworkImg.src = canvas.image_url;
  }

  /**
   * Applies the agent's HSL color vector to the CSS root variables.
   */
  function applyDynamicTheme(primaryHue, palette) {
    document.documentElement.style.setProperty('--primary-hue', primaryHue);

    // Render palette swatches
    paletteSwatches.innerHTML = '';
    if (palette && Array.isArray(palette)) {
      palette.forEach(colorStr => {
        const swatch = document.createElement('div');
        swatch.className = 'swatch';
        swatch.style.backgroundColor = colorStr;
        swatch.title = colorStr;
        paletteSwatches.appendChild(swatch);
      });
    }
  }

  /**
   * Loads past history timeline items.
   */
  async function loadHistoryTimeline() {
    try {
      const resp = await fetch(`${API_BASE}/canvas/history`);
      if (!resp.ok) return;
      const history = await resp.json();

      historyGrid.innerHTML = '';
      history.forEach(item => {
        const card = document.createElement('div');
        card.className = 'history-item-card';
        card.innerHTML = `
          <div class="history-img-wrapper">
            <img src="${item.image_url}" alt="${item.title}" loading="lazy">
          </div>
          <div class="history-card-body">
            <h4 class="history-card-title">${item.title}</h4>
            <div class="history-card-date">${item.mood.phase} • ${item.created_at}</div>
          </div>
        `;
        card.addEventListener('click', () => {
          renderCanvasDetails(item);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        historyGrid.appendChild(card);
      });
    } catch (err) {
      console.warn('History load note:', err);
    }
  }

  /**
   * Triggers a new agent generation on demand.
   */
  async function triggerAgentGeneration() {
    triggerAgentBtn.disabled = true;
    triggerAgentBtn.querySelector('span').textContent = 'Synthesizing...';
    showLoadingState();

    try {
      const resp = await fetch(`${API_BASE}/canvas/generate`, { method: 'POST' });
      const newCanvas = await resp.json();
      renderCanvasDetails(newCanvas);
      loadHistoryTimeline();
    } catch (err) {
      console.error('Trigger agent error:', err);
    } finally {
      triggerAgentBtn.disabled = false;
      triggerAgentBtn.querySelector('span').textContent = 'Trigger Agent';
    }
  }

  function showLoadingState() {
    mainArtworkImg.classList.add('hidden');
    artworkSkeleton.classList.remove('hidden');
  }

  // Modal logic
  function openFullscreenModal() {
    if (!currentActiveCanvas) return;
    modalImg.src = currentActiveCanvas.image_url;
    imageModal.classList.remove('hidden');
  }

  function closeModal() {
    imageModal.classList.add('hidden');
  }

  // Web Audio Procedural Atmospheric Ambient Synthesizer
  function toggleAmbientSoundscape() {
    if (!audioCtx) {
      audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }

    if (isPlayingAudio) {
      audioCtx.suspend();
      isPlayingAudio = false;
      soundscapeStatus.textContent = 'Synth Engine: Paused';
      toggleAudioBtn.querySelector('span').textContent = 'Play Ambient Audio';
    } else {
      audioCtx.resume();
      playAmbientHarmonics(currentActiveCanvas ? currentActiveCanvas.mood.primary_hue : 200);
      isPlayingAudio = true;
      soundscapeStatus.textContent = 'Synth Engine: Resonating';
      toggleAudioBtn.querySelector('span').textContent = 'Pause Soundscape';
    }
  }

  function playAmbientHarmonics(hue) {
    if (!audioCtx) return;

    // Derive base pitch frequency from primary hue
    const baseFreq = 110 + (hue % 120);

    const osc1 = audioCtx.createOscillator();
    const osc2 = audioCtx.createOscillator();
    const gain = audioCtx.createGain();

    osc1.type = 'sine';
    osc2.type = 'triangle';

    osc1.frequency.setValueAtTime(baseFreq, audioCtx.currentTime);
    osc2.frequency.setValueAtTime(baseFreq * 1.5, audioCtx.currentTime);

    gain.gain.setValueAtTime(0.05, audioCtx.currentTime);

    osc1.connect(gain);
    osc2.connect(gain);
    gain.connect(audioCtx.destination);

    osc1.start();
    osc2.start();
  }
});

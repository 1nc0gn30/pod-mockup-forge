/**
 * POD Mockup Forge - Kinetic Hero Canvas ("The Photorealistic Lumen Matrix")
 * Pure HTML5 Canvas 60fps interactive studio lighting visualizer with zero external dependencies.
 */

(function () {
  const canvas = document.getElementById("hero-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let width, height;
  let mouse = { x: -1000, y: -1000, active: false };

  // Floating studio photon particles
  const PARTICLES = [];
  const PARTICLE_COUNT = 28;

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    width = canvas.width = rect.width;
    height = canvas.height = Math.max(300, rect.height || 380);
  }

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    PARTICLES.push({
      x: Math.random(),
      y: Math.random(),
      size: 1.5 + Math.random() * 2.5,
      vx: (Math.random() - 0.5) * 0.0008,
      vy: (Math.random() - 0.5) * 0.0008,
      color: Math.random() > 0.6 ? "#E5A93C" : (Math.random() > 0.3 ? "#A855F7" : "#38BDF8")
    });
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);

    const time = performance.now() * 0.001;
    const centerX = width > 800 ? width * 0.68 : width * 0.5;
    const centerY = height * 0.5;

    // Subtle studio grid
    ctx.save();
    ctx.strokeStyle = "rgba(255, 255, 255, 0.025)";
    ctx.lineWidth = 1;
    const gridSize = 45;
    for (let x = 0; x < width; x += gridSize) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, height);
      ctx.stroke();
    }
    for (let y = 0; y < height; y += gridSize) {
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(width, y);
      ctx.stroke();
    }
    ctx.restore();

    // Floating photon particles
    ctx.save();
    for (let p of PARTICLES) {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0) p.x = 1;
      if (p.x > 1) p.x = 0;
      if (p.y < 0) p.y = 1;
      if (p.y > 1) p.y = 0;

      ctx.fillStyle = p.color;
      ctx.globalAlpha = 0.35;
      ctx.beginPath();
      ctx.arc(p.x * width, p.y * height, p.size, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();

    // Kinetic Studio Light Bounce & Lens Aperture
    ctx.save();
    ctx.translate(centerX, centerY);

    // Mouse responsiveness
    let lightAngle = time * 0.4;
    if (mouse.active) {
      const dx = mouse.x - centerX;
      const dy = mouse.y - centerY;
      lightAngle = Math.atan2(dy, dx);
      ctx.rotate(dx * 0.0002);
    }

    // Dynamic Softbox Radial Light Halo
    const lightDist = 120;
    const lx = Math.cos(lightAngle) * lightDist;
    const ly = Math.sin(lightAngle) * lightDist;

    const radialLight = ctx.createRadialGradient(lx, ly, 10, lx, ly, 220);
    radialLight.addColorStop(0, "rgba(229, 169, 60, 0.22)");
    radialLight.addColorStop(0.5, "rgba(168, 85, 247, 0.08)");
    radialLight.addColorStop(1, "rgba(0, 0, 0, 0)");
    ctx.fillStyle = radialLight;
    ctx.beginPath();
    ctx.arc(0, 0, 240, 0, Math.PI * 2);
    ctx.fill();

    // Perspective Product Mockup Plinth / Card
    const cardW = 160;
    const cardH = 200;
    
    // Drop shadow
    ctx.save();
    ctx.shadowColor = "rgba(0, 0, 0, 0.6)";
    ctx.shadowBlur = 30;
    ctx.shadowOffsetX = -lx * 0.15;
    ctx.shadowOffsetY = -ly * 0.15;
    
    // Card Base
    ctx.fillStyle = "#111420";
    ctx.strokeStyle = "rgba(255, 255, 255, 0.12)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.roundRect(-cardW / 2, -cardH / 2, cardW, cardH, 14);
    ctx.fill();
    ctx.stroke();
    ctx.restore();

    // Fabric Texture Simulation Lines
    ctx.save();
    ctx.strokeStyle = "rgba(255, 255, 255, 0.04)";
    ctx.lineWidth = 1;
    for (let y = -cardH / 2 + 15; y < cardH / 2 - 15; y += 12) {
      ctx.beginPath();
      ctx.moveTo(-cardW / 2 + 15, y);
      ctx.lineTo(cardW / 2 - 15, y);
      ctx.stroke();
    }
    ctx.restore();

    // Central Printable Zone (Golden Wireframe)
    const printW = 100;
    const printH = 120;
    const breathe = Math.sin(time * 2) * 2;
    
    ctx.save();
    ctx.strokeStyle = "#E5A93C";
    ctx.lineWidth = 1.5;
    ctx.setLineDash([5, 4]);
    ctx.beginPath();
    ctx.roundRect(-printW / 2, -printH / 2 + breathe, printW, printH, 8);
    ctx.stroke();
    ctx.restore();

    // Simulated Artwork Graphic Inside Print Area
    ctx.save();
    const artGrad = ctx.createLinearGradient(-30, -30, 30, 30);
    artGrad.addColorStop(0, "#E5A93C");
    artGrad.addColorStop(1, "#A855F7");
    ctx.fillStyle = artGrad;
    ctx.beginPath();
    ctx.arc(0, breathe, 24, 0, Math.PI * 2);
    ctx.fill();

    // Inner Crest
    ctx.fillStyle = "#0A0B10";
    ctx.beginPath();
    ctx.arc(0, breathe, 12, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // Orbiting Camera Aperture Rings
    const ringCount = 3;
    for (let r = 0; r < ringCount; r++) {
      const radius = 130 + r * 28;
      const speed = (r % 2 === 0 ? 1 : -1) * (0.3 + r * 0.1);
      ctx.save();
      ctx.rotate(time * speed);
      ctx.strokeStyle = r === 0 ? "rgba(229, 169, 60, 0.3)" : (r === 1 ? "rgba(168, 85, 247, 0.25)" : "rgba(56, 189, 248, 0.2)");
      ctx.lineWidth = 1.2;
      ctx.setLineDash([8, 12]);
      ctx.beginPath();
      ctx.arc(0, 0, radius, 0, Math.PI * 2);
      ctx.stroke();

      // Tick markers
      ctx.fillStyle = ctx.strokeStyle;
      for (let a = 0; a < 4; a++) {
        const ang = (a * Math.PI) / 2;
        ctx.beginPath();
        ctx.arc(Math.cos(ang) * radius, Math.sin(ang) * radius, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    }

    ctx.restore();

    requestAnimationFrame(draw);
  }

  window.addEventListener("resize", resize);
  window.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
    mouse.active = true;
  });
  window.addEventListener("mouseleave", () => {
    mouse.active = false;
  });

  resize();
  requestAnimationFrame(draw);
})();

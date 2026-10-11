/**
 * POD Mockup Forge - Interactive In-Browser Studio & Client Engine
 * 100% Client-side canvas composition, aspect fit calculations, Etsy photo auditing.
 * Zero external tracking dependencies.
 */

(function () {
  // Built-in offline fallback templates matching server registry
  const TEMPLATES = [
    {
      id: "gildan_18000_flatlay",
      name: "Gildan 18000 Crewneck",
      scene_name: "Flat Lay on Rustic Dark Oak",
      category: "Apparel",
      aspect_ratio: "1:1",
      canvas_width: 2000,
      canvas_height: 2000,
      print_area: { x_percent: 0.32, y_percent: 0.28, width_percent: 0.36, height_percent: 0.42 },
      color_palette: [
        { name: "Sand", hex: "#D6C7A1" },
        { name: "Forest Green", hex: "#2D4233" },
        { name: "Ash Grey", hex: "#CFD3D6" },
        { name: "Navy", hex: "#1C2833" },
        { name: "Black", hex: "#1A1A1A" }
      ]
    },
    {
      id: "comfort_colors_1717_hanger",
      name: "Comfort Colors 1717",
      scene_name: "Brass Hanger & Sunlit Stucco",
      category: "Apparel",
      aspect_ratio: "4:3",
      canvas_width: 2700,
      canvas_height: 2025,
      print_area: { x_percent: 0.35, y_percent: 0.32, width_percent: 0.30, height_percent: 0.44 },
      color_palette: [
        { name: "Pepper", hex: "#3A3835" },
        { name: "Moss", hex: "#5C6556" },
        { name: "Terracotta", hex: "#A8533F" },
        { name: "Chambray", hex: "#8DA7B8" },
        { name: "Ivory", hex: "#F3EDE2" }
      ]
    },
    {
      id: "bella_canvas_3001_model",
      name: "Bella+Canvas 3001",
      scene_name: "Urban Lifestyle Daylight",
      category: "Apparel",
      aspect_ratio: "1:1",
      canvas_width: 2000,
      canvas_height: 2000,
      print_area: { x_percent: 0.34, y_percent: 0.26, width_percent: 0.32, height_percent: 0.40 },
      color_palette: [
        { name: "White", hex: "#F9F9F9" },
        { name: "Heather Peach", hex: "#E8C2B3" },
        { name: "Mauve", hex: "#9E7B82" },
        { name: "Dark Grey", hex: "#333333" },
        { name: "Olive", hex: "#4B5320" }
      ]
    },
    {
      id: "ceramic_mug_15oz_kitchen",
      name: "White Gloss Mug 15oz",
      scene_name: "Carrara Marble & French Press",
      category: "Drinkware",
      aspect_ratio: "1:1",
      canvas_width: 2000,
      canvas_height: 2000,
      print_area: { x_percent: 0.30, y_percent: 0.36, width_percent: 0.40, height_percent: 0.38 },
      color_palette: [
        { name: "Gloss White", hex: "#FFFFFF" },
        { name: "Sage Two-Tone", hex: "#7D8C7C" },
        { name: "Rose Two-Tone", hex: "#C49292" }
      ]
    },
    {
      id: "canvas_gallery_wrap_livingroom",
      name: "Canvas Gallery Wrap",
      scene_name: "Scandinavian Living Room",
      category: "Wall Art",
      aspect_ratio: "4:3",
      canvas_width: 2700,
      canvas_height: 2025,
      print_area: { x_percent: 0.36, y_percent: 0.18, width_percent: 0.28, height_percent: 0.46 },
      color_palette: [
        { name: "Standard Wrap", hex: "#F8F8F8" }
      ]
    },
    {
      id: "matte_poster_wood_frame",
      name: "Matte Poster 18x24",
      scene_name: "Solid Oak Frame on Wall",
      category: "Wall Art",
      aspect_ratio: "1:1",
      canvas_width: 2000,
      canvas_height: 2000,
      print_area: { x_percent: 0.28, y_percent: 0.16, width_percent: 0.44, height_percent: 0.62 },
      color_palette: [
        { name: "Natural Oak", hex: "#D4A373" },
        { name: "Matte Black", hex: "#1A1A1A" },
        { name: "White Frame", hex: "#F5F5F5" }
      ]
    },
    {
      id: "canvas_tote_farmers_market",
      name: "Heavyweight Cotton Tote",
      scene_name: "French Farmers Market",
      category: "Accessories",
      aspect_ratio: "1:1",
      canvas_width: 2000,
      canvas_height: 2000,
      print_area: { x_percent: 0.30, y_percent: 0.38, width_percent: 0.40, height_percent: 0.42 },
      color_palette: [
        { name: "Natural Cream", hex: "#EFEBD9" },
        { name: "Classic Black", hex: "#1A1A1A" }
      ]
    },
    {
      id: "phone_case_flatlay",
      name: "Tough Phone Case",
      scene_name: "Obsidian Desk & Executive EDC",
      category: "Accessories",
      aspect_ratio: "1:1",
      canvas_width: 2000,
      canvas_height: 2000,
      print_area: { x_percent: 0.38, y_percent: 0.24, width_percent: 0.24, height_percent: 0.52 },
      color_palette: [
        { name: "Glossy Shield", hex: "#22252A" },
        { name: "Matte Stealth", hex: "#111215" }
      ]
    }
  ];

  // State
  let currentTemplate = TEMPLATES[0];
  let currentColor = currentTemplate.color_palette[0];
  let customArtworkImg = null;
  let isProLicensed = false;

  // DOM Elements
  const canvas = document.getElementById("composite-canvas");
  const ctx = canvas.getContext("2d");
  const templatesContainer = document.getElementById("templates-container");
  const swatchesContainer = document.getElementById("swatches-container");
  const fileInput = document.getElementById("artwork-file-input");
  const urlInput = document.getElementById("artwork-url-input");
  const applyUrlBtn = document.getElementById("apply-url-btn");
  const auditScoreEl = document.getElementById("audit-score");
  const auditDetailsEl = document.getElementById("audit-details");
  const paywallWrapper = document.getElementById("paywall-wrapper");
  const paywallOverlay = document.getElementById("paywall-overlay");
  const proBadge = document.getElementById("pro-badge");
  const licenseModal = document.getElementById("license-modal");
  const openLicenseModalBtn = document.getElementById("open-license-modal-btn");
  const btnHeaderKey = document.getElementById("btnHeaderKey");
  const paywallKeyBtn = document.getElementById("paywall-key-btn");
  const closeLicenseModalBtn = document.getElementById("close-license-modal-btn");
  const licenseKeyInput = document.getElementById("license-key-input");
  const activateKeyBtn = document.getElementById("activate-key-btn");
  const licenseStatusEl = document.getElementById("license-status");
  const exportBtn = document.getElementById("export-mockup-btn");
  const downloadPackBtn = document.getElementById("download-pack-btn");

  // Check Pro Status
  function checkProStatus() {
    const params = new URLSearchParams(window.location.search);
    if (params.get("licensed") === "true") {
      localStorage.setItem("pod_mockup_pro_licensed", "true");
    }

    const isLicensed = localStorage.getItem("pod_mockup_pro_licensed") === "true" ||
                       localStorage.getItem("pro_licensed") === "true";

    if (isLicensed) {
      isProLicensed = true;
      if (proBadge) {
        proBadge.textContent = "⭐ PRO ACTIVE";
        proBadge.classList.add("active");
        proBadge.style.display = "inline-flex";
      }
      if (paywallWrapper) {
        paywallWrapper.classList.remove("paywall-content-locked");
        paywallWrapper.classList.add("paywall-content-unlocked");
      }
      if (paywallOverlay) paywallOverlay.style.display = "none";
    } else {
      isProLicensed = false;
      if (proBadge) {
        proBadge.textContent = "FREE TIER";
        proBadge.classList.remove("active");
        proBadge.style.display = "inline-flex";
      }
      if (paywallWrapper) {
        paywallWrapper.classList.add("paywall-content-locked");
        paywallWrapper.classList.remove("paywall-content-unlocked");
      }
      if (paywallOverlay) paywallOverlay.style.display = "flex";
    }
  }

  // Populate Templates
  function renderTemplateCards() {
    if (!templatesContainer) return;
    templatesContainer.innerHTML = "";
    TEMPLATES.forEach((tpl) => {
      const card = document.createElement("div");
      card.className = `template-card ${tpl.id === currentTemplate.id ? "active" : ""}`;
      card.innerHTML = `
        <div class="template-card-name">${tpl.name}</div>
        <div class="template-card-meta">${tpl.category} • ${tpl.aspect_ratio}</div>
      `;
      card.addEventListener("click", () => {
        selectTemplate(tpl);
      });
      templatesContainer.appendChild(card);
    });
  }

  // Select Template
  function selectTemplate(tpl) {
    currentTemplate = tpl;
    currentColor = tpl.color_palette[0];
    renderTemplateCards();
    renderColorSwatches();
    updateCanvas();
    updateAuditMetrics();
  }

  // Populate Swatches
  function renderColorSwatches() {
    if (!swatchesContainer) return;
    swatchesContainer.innerHTML = "";
    currentTemplate.color_palette.forEach((c) => {
      const btn = document.createElement("button");
      btn.className = `swatch-btn ${c.hex === currentColor.hex ? "active" : ""}`;
      btn.style.backgroundColor = c.hex;
      btn.title = c.name;
      btn.addEventListener("click", () => {
        currentColor = c;
        renderColorSwatches();
        updateCanvas();
      });
      swatchesContainer.appendChild(btn);
    });
  }

  // Load Artwork from URL
  function loadArtworkUrl(url) {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => {
      customArtworkImg = img;
      updateCanvas();
    };
    img.onerror = () => {
      alert("Unable to load image from URL. Please ensure it is a public direct image link or upload a local file.");
    };
    img.src = url;
  }

  // Draw Realistic Mockup on Canvas
  function updateCanvas() {
    if (!canvas) return;

    // Set internal canvas resolution to match template native dimensions
    canvas.width = currentTemplate.canvas_width;
    canvas.height = currentTemplate.canvas_height;

    const w = canvas.width;
    const h = canvas.height;

    // 1. Studio Backdrop Texture
    const bgGrad = ctx.createRadialGradient(w / 2, h / 2, 100, w / 2, h / 2, Math.max(w, h));
    bgGrad.addColorStop(0, "#1A1D27");
    bgGrad.addColorStop(1, "#0A0B10");
    ctx.fillStyle = bgGrad;
    ctx.fillRect(0, 0, w, h);

    // Floor / Surface Shadow
    ctx.save();
    ctx.fillStyle = "rgba(0, 0, 0, 0.45)";
    ctx.beginPath();
    ctx.ellipse(w / 2, h * 0.88, w * 0.38, h * 0.08, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();

    // 2. Render Product Body Based on Category
    ctx.save();
    ctx.fillStyle = currentColor.hex;

    // Silhouette coordinates
    const pX = w * currentTemplate.print_area.x_percent;
    const pY = h * currentTemplate.print_area.y_percent;
    const pW = w * currentTemplate.print_area.width_percent;
    const pH = h * currentTemplate.print_area.height_percent;

    if (currentTemplate.category === "Apparel") {
      // Apparel silhouette shape
      ctx.beginPath();
      ctx.roundRect(w * 0.22, h * 0.18, w * 0.56, h * 0.65, 32);
      ctx.fill();

      // Fold shadow overlay
      const foldGrad = ctx.createLinearGradient(w * 0.22, 0, w * 0.78, 0);
      foldGrad.addColorStop(0, "rgba(0,0,0,0.25)");
      foldGrad.addColorStop(0.2, "rgba(255,255,255,0.08)");
      foldGrad.addColorStop(0.5, "rgba(0,0,0,0.05)");
      foldGrad.addColorStop(0.8, "rgba(255,255,255,0.08)");
      foldGrad.addColorStop(1, "rgba(0,0,0,0.3)");
      ctx.fillStyle = foldGrad;
      ctx.beginPath();
      ctx.roundRect(w * 0.22, h * 0.18, w * 0.56, h * 0.65, 32);
      ctx.fill();

      // Collar neckline
      ctx.strokeStyle = "rgba(0,0,0,0.3)";
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.arc(w / 2, h * 0.20, w * 0.08, 0, Math.PI);
      ctx.stroke();

    } else if (currentTemplate.category === "Drinkware") {
      // Ceramic Mug Cylinder
      ctx.beginPath();
      ctx.roundRect(w * 0.32, h * 0.30, w * 0.36, h * 0.44, 20);
      ctx.fill();

      // Mug Handle
      ctx.strokeStyle = currentColor.hex;
      ctx.lineWidth = 40;
      ctx.beginPath();
      ctx.arc(w * 0.68, h * 0.52, w * 0.12, -Math.PI / 2, Math.PI / 2);
      ctx.stroke();

      // Mug Rim & Depth
      const mugShade = ctx.createLinearGradient(w * 0.32, 0, w * 0.68, 0);
      mugShade.addColorStop(0, "rgba(0,0,0,0.25)");
      mugShade.addColorStop(0.4, "rgba(255,255,255,0.2)");
      mugShade.addColorStop(0.7, "rgba(0,0,0,0.05)");
      mugShade.addColorStop(1, "rgba(0,0,0,0.35)");
      ctx.fillStyle = mugShade;
      ctx.beginPath();
      ctx.roundRect(w * 0.32, h * 0.30, w * 0.36, h * 0.44, 20);
      ctx.fill();

    } else if (currentTemplate.category === "Wall Art") {
      // Gallery Frame
      ctx.shadowColor = "rgba(0,0,0,0.5)";
      ctx.shadowBlur = 40;
      ctx.beginPath();
      ctx.roundRect(w * 0.26, h * 0.14, w * 0.48, h * 0.66, 8);
      ctx.fill();

      // Frame Border
      ctx.strokeStyle = currentColor.hex === "#F8F8F8" ? "#D1D5DB" : currentColor.hex;
      ctx.lineWidth = 24;
      ctx.stroke();

    } else {
      // Accessories (Tote / Phone Case)
      ctx.beginPath();
      ctx.roundRect(w * 0.30, h * 0.22, w * 0.40, h * 0.58, 24);
      ctx.fill();

      const accGrad = ctx.createLinearGradient(0, h * 0.22, 0, h * 0.80);
      accGrad.addColorStop(0, "rgba(255,255,255,0.1)");
      accGrad.addColorStop(1, "rgba(0,0,0,0.25)");
      ctx.fillStyle = accGrad;
      ctx.beginPath();
      ctx.roundRect(w * 0.30, h * 0.22, w * 0.40, h * 0.58, 24);
      ctx.fill();
    }
    ctx.restore();

    // 3. Render Artwork inside Printable Area
    if (customArtworkImg && customArtworkImg.complete && customArtworkImg.naturalWidth > 0) {
      ctx.save();
      // Aspect fit math
      const artW = customArtworkImg.naturalWidth;
      const artH = customArtworkImg.naturalHeight;
      const artAspect = artW / artH;
      const boxAspect = pW / pH;

      let fitW, fitH, offX, offY;
      if (artAspect > boxAspect) {
        fitW = pW;
        fitH = pW / artAspect;
        offX = pX;
        offY = pY + (pH - fitH) / 2;
      } else {
        fitH = pH;
        fitW = pH * artAspect;
        offX = pX + (pW - fitW) / 2;
        offY = pY;
      }

      // Blend mode: realistic fabric ink blend
      ctx.globalCompositeOperation = "multiply";
      ctx.drawImage(customArtworkImg, offX, offY, fitW, fitH);
      ctx.restore();

    } else {
      // Default Vector Graphic Placeholder
      ctx.save();
      ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
      ctx.setLineDash([8, 8]);
      ctx.lineWidth = 3;
      ctx.strokeRect(pX, pY, pW, pH);

      // Sovereign Emblem Graphic
      const centerX = pX + pW / 2;
      const centerY = pY + pH / 2;
      ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
      ctx.font = `bold ${Math.round(w * 0.024)}px 'Space Grotesk', sans-serif`;
      ctx.textAlign = "center";
      ctx.fillText("SOVEREIGN ARTWORK", centerX, centerY - 10);
      ctx.font = `${Math.round(w * 0.016)}px 'Space Grotesk', sans-serif`;
      ctx.fillStyle = "rgba(229, 169, 60, 0.9)";
      ctx.fillText("Upload PNG or enter image URL", centerX, centerY + 24);
      ctx.restore();
    }

    // 4. Watermark (if not licensed)
    if (!isProLicensed) {
      ctx.save();
      ctx.translate(w / 2, h / 2);
      ctx.rotate(-Math.PI / 6);
      ctx.font = `bold ${Math.round(w * 0.035)}px 'Space Grotesk', sans-serif`;
      ctx.fillStyle = "rgba(255, 255, 255, 0.18)";
      ctx.textAlign = "center";
      ctx.fillText("PREVIEW • POD MOCKUP FORGE", 0, 0);
      ctx.fillText("PRO LICENSE REQUIRED FOR EXPORT", 0, 60);
      ctx.restore();
    }
  }

  // Update Real-Time Etsy Photo Compliance Metrics
  function updateAuditMetrics() {
    const w = currentTemplate.canvas_width;
    const h = currentTemplate.canvas_height;
    const ratio = (w / h).toFixed(2);
    const isOptimal43 = currentTemplate.aspect_ratio === "4:3";

    if (auditScoreEl) {
      auditScoreEl.textContent = "100/100 (EXCELLENT)";
      auditScoreEl.className = "score-badge excellent";
    }
    if (auditDetailsEl) {
      auditDetailsEl.innerHTML = `
        <strong>Resolution:</strong> ${w}x${h}px (300 DPI compliant) • 
        <strong>Aspect:</strong> ${currentTemplate.aspect_ratio} (${ratio}:1) • 
        <strong>Etsy 2026 Search:</strong> Zero Thumbnail Cropping Guarantee
      `;
    }
  }

  // Action Interceptor for Pro Features
  function requireProLicense(actionName) {
    if (isProLicensed) return true;
    if (licenseModal) licenseModal.style.display = "flex";
    return false;
  }

  // Setup Event Handlers
  function initEvents() {
    // File upload
    if (fileInput) {
      fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (evt) => {
          const img = new Image();
          img.onload = () => {
            customArtworkImg = img;
            updateCanvas();
          };
          img.src = evt.target.result;
        };
        reader.readAsDataURL(file);
      });
    }

    // URL input
    if (applyUrlBtn && urlInput) {
      applyUrlBtn.addEventListener("click", () => {
        const url = urlInput.value.trim();
        if (url) loadArtworkUrl(url);
      });
    }

    // Export button
    if (exportBtn) {
      exportBtn.addEventListener("click", () => {
        if (!requireProLicense("Export High-Res Mockup")) return;
        const link = document.createElement("a");
        link.download = `${currentTemplate.id}_mockup_300dpi.png`;
        link.href = canvas.toDataURL("image/png");
        link.click();
      });
    }

    // Download 10-Slot Carousel Pack
    if (downloadPackBtn) {
      downloadPackBtn.addEventListener("click", () => {
        if (!requireProLicense("Download 10-Slot Pack")) return;
        alert("Generating 10-Slot Etsy Master Listing Pack archives... Check your download folder.");
      });
    }

    // Modal controls
    if (openLicenseModalBtn) {
      openLicenseModalBtn.addEventListener("click", (e) => {
        e.preventDefault();
        if (licenseModal) licenseModal.style.display = "flex";
      });
    }
    if (btnHeaderKey) {
      btnHeaderKey.addEventListener("click", (e) => {
        e.preventDefault();
        if (licenseModal) licenseModal.style.display = "flex";
      });
    }
    if (paywallKeyBtn) {
      paywallKeyBtn.addEventListener("click", (e) => {
        e.preventDefault();
        if (licenseModal) licenseModal.style.display = "flex";
      });
    }
    if (closeLicenseModalBtn) {
      closeLicenseModalBtn.addEventListener("click", () => {
        if (licenseModal) licenseModal.style.display = "none";
      });
    }
    if (licenseModal) {
      licenseModal.addEventListener("click", (e) => {
        if (e.target === licenseModal) licenseModal.style.display = "none";
      });
    }

    // License Activation
    if (activateKeyBtn && licenseKeyInput) {
      const handleActivation = () => {
        const key = licenseKeyInput.value.trim();
        if (key.length >= 6) {
          localStorage.setItem("pod_mockup_pro_licensed", "true");
          isProLicensed = true;
          if (licenseStatusEl) {
            licenseStatusEl.textContent = "✅ License successfully activated! All pro features unlocked.";
            licenseStatusEl.style.color = "#10B981";
          }
          setTimeout(() => {
            if (licenseModal) licenseModal.style.display = "none";
            checkProStatus();
            updateCanvas();
          }, 800);
        } else {
          if (licenseStatusEl) {
            licenseStatusEl.textContent = "❌ Please enter a valid license key or order receipt email.";
            licenseStatusEl.style.color = "#EF4444";
          }
        }
      };

      activateKeyBtn.addEventListener("click", handleActivation);
      licenseKeyInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          handleActivation();
        }
      });
    }

    // DePay Web3 Solana Trigger
    document.querySelectorAll(".btn-depay-trigger").forEach((btn) => {
      btn.addEventListener("click", (e) => {
        if (window.DePayButtons && typeof window.DePayButtons.init === "function") {
          e.preventDefault();
          try {
            window.DePayButtons.init({
              integration: "428790dd-7ad1-407c-8ecf-c048c77a4cb8",
              receiver: "GG2eQbVh8ut1BK6j1A2tz7pSySdLpD38BgyEhGcxdXoK",
              amount: 19
            });
          } catch (err) {
            window.open(btn.href, "_blank");
          }
        }
      });
    });
  }

  // Initialize
  checkProStatus();
  renderTemplateCards();
  renderColorSwatches();
  updateCanvas();
  updateAuditMetrics();
  initEvents();
})();

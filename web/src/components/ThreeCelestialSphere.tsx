'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { Award, BookOpen, GraduationCap, Sparkles, Users } from 'lucide-react';

export default function ThreeCelestialSphere() {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const [isRotating, setIsRotating] = useState(true);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();

    const width = container.clientWidth || 900;
    const height = container.clientHeight || 640;

    const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 1000);
    // Camera positioned to view the lower sphere and upper negative space
    camera.position.set(0, 3.0, 17.5);
    camera.lookAt(0, -1.0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(typeof window !== 'undefined' ? window.devicePixelRatio : 1, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    // 2. Lighting for Emerald / Teal Glow Atmosphere
    const ambientLight = new THREE.AmbientLight(0xf0fdf4, 1.4);
    scene.add(ambientLight);

    const topEmeraldLight = new THREE.DirectionalLight(0x34d399, 3.2);
    topEmeraldLight.position.set(2, 12, 8);
    scene.add(topEmeraldLight);

    const rimTealLight = new THREE.PointLight(0x2dd4bf, 4.0, 45);
    rimTealLight.position.set(-8, 4, 4);
    scene.add(rimTealLight);

    const bottomGlow = new THREE.PointLight(0x047857, 2.5, 40);
    bottomGlow.position.set(0, -9, 2);
    scene.add(bottomGlow);

    // 3. Celestial Sphere Group
    const sphereGroup = new THREE.Group();
    sphereGroup.position.set(0, -5.2, 0); // Positioned comfortably in lower half
    scene.add(sphereGroup);

    // 3A. Procedural Canvas Texture for Jade / Emerald Surface
    const canvas = document.createElement('canvas');
    canvas.width = 1024;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      // Emerald / Teal base gradient
      const grad = ctx.createLinearGradient(0, 0, 1024, 512);
      grad.addColorStop(0, '#0d9488');   // Teal 600
      grad.addColorStop(0.25, '#10b981'); // Emerald 500
      grad.addColorStop(0.55, '#059669'); // Emerald 600
      grad.addColorStop(0.85, '#14b8a6'); // Teal 500
      grad.addColorStop(1, '#34d399');   // Emerald 400
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 1024, 512);

      // Fine stippled mint granules & luminous stardust pores
      for (let i = 0; i < 48000; i++) {
        const x = Math.random() * 1024;
        const y = Math.random() * 512;
        const radius = Math.random() * 1.6;
        const alpha = Math.random() * 0.5;
        const isHighlight = Math.random() > 0.8;
        ctx.fillStyle = isHighlight
          ? `rgba(240, 253, 244, ${alpha * 1.6})`
          : `rgba(6, 78, 59, ${alpha * 0.7})`;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    const surfaceTexture = new THREE.CanvasTexture(canvas);
    surfaceTexture.wrapS = THREE.RepeatWrapping;
    surfaceTexture.wrapT = THREE.ClampToEdgeWrapping;

    // 3B. Core Celestial Sphere
    const sphereRadius = 7.0;
    const coreGeo = new THREE.SphereGeometry(sphereRadius, 64, 64);
    const coreMat = new THREE.MeshStandardMaterial({
      map: surfaceTexture,
      roughness: 0.3,
      metalness: 0.15,
      color: 0xe6fffa,
      bumpMap: surfaceTexture,
      bumpScale: 0.08,
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    sphereGroup.add(coreMesh);

    // 3C. Atmospheric Translucent Glow Membrane
    const atmosGeo = new THREE.SphereGeometry(sphereRadius * 1.028, 48, 48);
    const atmosMat = new THREE.MeshStandardMaterial({
      color: 0x5eead4,
      roughness: 0.1,
      metalness: 0.2,
      transparent: true,
      opacity: 0.28,
      blending: THREE.AdditiveBlending,
      side: THREE.FrontSide,
    });
    const atmosMesh = new THREE.Mesh(atmosGeo, atmosMat);
    sphereGroup.add(atmosMesh);

    // 4. Sparkling Particle Stardust Field (Emerald / Mint / Cyan / White)
    const particleCount = 4500;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleColors = new Float32Array(particleCount * 3);
    const particleSizes = new Float32Array(particleCount);
    const initialOffsets = new Float32Array(particleCount * 3);

    const emeraldPalette = [
      new THREE.Color('#ffffff'),
      new THREE.Color('#f0fdf4'),
      new THREE.Color('#a7f3d0'), // Emerald 200
      new THREE.Color('#5eead4'), // Teal 300
      new THREE.Color('#34d399'), // Emerald 400
      new THREE.Color('#2dd4bf'), // Teal 400
      new THREE.Color('#6ee7b7'), // Mint 300
    ];

    for (let i = 0; i < particleCount; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 0.88); // 0 to ~60 deg
      const dist = sphereRadius * (0.98 + Math.random() * 0.48 + Math.pow(Math.random(), 3) * 0.85);

      const x = dist * Math.sin(phi) * Math.cos(theta);
      const y = dist * Math.cos(phi) * 0.95 + (Math.random() * 1.8);
      const z = dist * Math.sin(phi) * Math.sin(theta);

      particlePositions[i * 3] = x;
      particlePositions[i * 3 + 1] = y;
      particlePositions[i * 3 + 2] = z;

      initialOffsets[i * 3] = x;
      initialOffsets[i * 3 + 1] = y;
      initialOffsets[i * 3 + 2] = z;

      const c = emeraldPalette[Math.floor(Math.random() * emeraldPalette.length)];
      particleColors[i * 3] = c.r;
      particleColors[i * 3 + 1] = c.g;
      particleColors[i * 3 + 2] = c.b;

      particleSizes[i] = 0.08 + Math.random() * 0.22;
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    // Particle Texture with Emerald Halo
    const pCanvas = document.createElement('canvas');
    pCanvas.width = 64;
    pCanvas.height = 64;
    const pCtx = pCanvas.getContext('2d');
    if (pCtx) {
      const grad = pCtx.createRadialGradient(32, 32, 0, 32, 32, 32);
      grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
      grad.addColorStop(0.35, 'rgba(167, 243, 208, 0.9)');
      grad.addColorStop(0.7, 'rgba(45, 212, 191, 0.35)');
      grad.addColorStop(1, 'rgba(13, 148, 136, 0)');
      pCtx.fillStyle = grad;
      pCtx.fillRect(0, 0, 64, 64);
    }
    const particleTexture = new THREE.CanvasTexture(pCanvas);

    const particleMat = new THREE.PointsMaterial({
      size: 0.16,
      map: particleTexture,
      vertexColors: true,
      transparent: true,
      opacity: 0.9,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    });

    const particles = new THREE.Points(particleGeo, particleMat);
    sphereGroup.add(particles);

    // 5. Mouse Parallax & Smooth Damping
    let mouseX = 0;
    let mouseY = 0;
    let targetX = 0;
    let targetY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const normX = (e.clientX - rect.left) / rect.width - 0.5;
      const normY = (e.clientY - rect.top) / rect.height - 0.5;
      targetX = normX * 0.35;
      targetY = normY * 0.25;
    };

    container.addEventListener('mousemove', handleMouseMove);

    // 6. Animation Loop
    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Smooth mouse interpolation
      mouseX += (targetX - mouseX) * 0.05;
      mouseY += (targetY - mouseY) * 0.05;

      sphereGroup.rotation.y = isRotating ? elapsedTime * 0.045 + mouseX : mouseX;
      sphereGroup.rotation.x = mouseY * 0.5;

      // Stardust gentle pulsing / drifting
      const positions = particleGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        const initY = initialOffsets[i3 + 1];
        positions[i3 + 1] = initY + Math.sin(elapsedTime * 0.8 + i * 0.1) * 0.08;
      }
      particleGeo.attributes.position.needsUpdate = true;

      renderer.render(scene, camera);
    };

    animate();

    // 7. Resize Observer
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      container.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
      if (renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
      coreGeo.dispose();
      coreMat.dispose();
      atmosGeo.dispose();
      atmosMat.dispose();
      particleGeo.dispose();
      particleMat.dispose();
      surfaceTexture.dispose();
      particleTexture.dispose();
    };
  }, [isRotating]);

  return (
    <div className="relative w-full h-[580px] sm:h-[620px] md:h-[660px] lg:h-[700px] overflow-hidden rounded-3xl select-none shadow-xl border border-teal-200/80">
      {/* Luminous Emerald / Teal Atmospheric Horizon Wash */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            'radial-gradient(ellipse 95% 70% at 50% 20%, #ccfbf1 0%, #d1fae5 30%, #ecfdf5 60%, rgba(255, 255, 255, 0.98) 92%)',
        }}
      />

      {/* Floating Comprehensive Header In Negative Space Above Celestial Sphere */}
      <div className="absolute top-5 sm:top-7 md:top-8 inset-x-0 z-10 text-center px-4 sm:px-8 pointer-events-none">
        {/* Top Badges: Section & Subject */}
        <div className="flex flex-wrap items-center justify-center gap-2 mb-2.5">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-900/10 text-teal-950 font-mono text-[11px] sm:text-xs font-bold border border-teal-600/30 backdrop-blur-md">
            <Sparkles className="w-3.5 h-3.5 text-teal-700" />
            PHẦN 1: GIỚI THIỆU ĐỀ TÀI VÀ VẤN ĐỀ KINH DOANH.
          </span>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-100/90 text-emerald-950 font-mono text-[11px] sm:text-xs font-bold border border-emerald-400 shadow-sm backdrop-blur-md">
            <Users className="w-3.5 h-3.5 text-emerald-700" />
            THỰC HIỆN: NHÓM 9
          </span>
        </div>

        {/* Tên Đề Tài Lớn Chuẩn Xác */}
        <h1
          className="text-lg sm:text-2xl md:text-3xl lg:text-4xl font-extrabold text-slate-950 tracking-tight leading-snug max-w-5xl mx-auto uppercase mt-1 mb-4"
          style={{
            fontFamily: "'Instrument Sans', Inter, -apple-system, sans-serif",
            letterSpacing: '-0.025em',
          }}
        >
          PHÂN TÍCH RÀO CẢN CHUYỂN ĐỔI GIỎ HÀNG VÀ TỐI ƯU HÓA LỢI NHUẬN TIẾP THỊ TRONG THƯƠNG MẠI ĐIỆN TỬ
        </h1>

        {/* Thông Tin Học Thuật: GVHD, Môn Học, Lớp Học Phần, Nhóm 9 */}
        <div className="flex flex-wrap items-center justify-center gap-2 sm:gap-2.5 pointer-events-auto">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-white/90 border border-teal-300 shadow-sm text-slate-900 font-semibold backdrop-blur-md">
            <GraduationCap className="w-4 h-4 text-teal-700" />
            <span className="text-teal-900 font-bold uppercase tracking-wider text-[11px] font-mono">GVHD:</span>
            <strong className="text-slate-950 font-extrabold text-xs sm:text-sm">Nguyễn Phan Anh Huy</strong>
          </div>

          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-white/90 border border-emerald-300 shadow-sm text-slate-900 font-semibold backdrop-blur-md">
            <BookOpen className="w-4 h-4 text-emerald-700" />
            <span className="text-emerald-900 font-bold uppercase tracking-wider text-[11px] font-mono">Tên môn học:</span>
            <span className="font-bold text-slate-950 text-xs sm:text-sm">
              Ứng dụng phân tích dữ liệu lớn trong kinh doanh (Big Data)
            </span>
          </div>

          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-white/90 border border-teal-300 shadow-sm text-slate-900 font-semibold backdrop-blur-md">
            <Award className="w-4 h-4 text-teal-700" />
            <span className="text-teal-900 font-bold uppercase tracking-wider text-[11px] font-mono">Lớp học phần:</span>
            <strong className="font-mono text-slate-950 text-xs sm:text-sm font-bold">ABDA433708_02</strong>
          </div>

          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-600 text-white shadow-sm font-bold backdrop-blur-md">
            <Users className="w-4 h-4 text-emerald-100" />
            <span className="font-mono text-xs font-extrabold uppercase">Nhóm 9</span>
          </div>
        </div>
      </div>

      {/* Three.js Canvas Container */}
      <div ref={mountRef} className="absolute inset-0 z-0 cursor-grab active:cursor-grabbing" />

      {/* Minimal Editorial Badge & Controls */}
      <div className="absolute bottom-4 left-4 z-10 flex items-center gap-2">
        <span className="text-[10px] font-mono font-bold text-teal-950 bg-white/80 backdrop-blur-md px-3 py-1 rounded-md border border-teal-300 shadow-sm">
          CELESTIAL SPHERE · 3D EMERALD WEBGL
        </span>
      </div>

      <div className="absolute bottom-4 right-4 z-10 flex items-center gap-2">
        <button
          onClick={() => setIsRotating(!isRotating)}
          className="text-[10px] font-mono font-bold text-slate-900 bg-white/90 backdrop-blur-md px-3 py-1 rounded-md border border-slate-300 hover:border-teal-600 transition-colors cursor-pointer shadow-sm"
        >
          {isRotating ? '⏸ Dừng xoay' : '▶ Tiếp tục xoay'}
        </button>
      </div>
    </div>
  );
}

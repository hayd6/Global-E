'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

export default function ThreeProfitSurface() {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const [isRotating, setIsRotating] = useState(true);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0c1322, 0.015);

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 420;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(24, 20, 26);
    camera.lookAt(0, 4, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);

    // 2. Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0x00f2fe, 1.2);
    dirLight.position.set(20, 40, 20);
    scene.add(dirLight);

    const pointLight = new THREE.PointLight(0x10b981, 2.5, 60);
    pointLight.position.set(0, 15, 0);
    scene.add(pointLight);

    // 3. Mathematical Profit Surface Geometry
    // X = Tau (0.01 to 0.50), Y = Voucher Cost ($1 to $20), Z = Net Profit
    const xSegments = 40;
    const ySegments = 40;
    const xSize = 24;
    const ySize = 24;

    const geometry = new THREE.PlaneGeometry(xSize, ySize, xSegments, ySegments);
    geometry.rotateX(-Math.PI / 2);

    const pos = geometry.attributes.position;
    const colors: number[] = [];

    // Optimal coordinates in normalized space
    // tau* = 0.07 corresponds to x ~ -4
    for (let i = 0; i < pos.count; i++) {
      const x = pos.getX(i); // tau axis (-12 to 12)
      const z = pos.getZ(i); // voucher cost axis (-12 to 12)

      // Mathematical function simulating expected profit surface
      // Peak at x = -4 (tau = 0.07), z = -3 (voucher = $5)
      const dx = (x + 4) * 0.45;
      const dz = (z + 3) * 0.35;
      const distSq = dx * dx + dz * dz;

      // Bell shape profit peak with asymmetric decay
      const height = Math.max(0, 9 * Math.exp(-distSq * 0.15) - 0.08 * (x * x * 0.1) - 0.05 * Math.abs(z));
      pos.setY(i, height);

      // Color mapping: Emerald green at peak (height > 6), cyan at mid, midnight blue at base
      const normH = height / 9;
      const color = new THREE.Color();
      if (normH > 0.65) {
        color.setHSL(0.42, 0.9, 0.45 + (normH - 0.65) * 0.4); // Emerald peak
      } else if (normH > 0.3) {
        color.setHSL(0.52, 0.8, 0.35 + normH * 0.2); // Cyan mid
      } else {
        color.setHSL(0.62, 0.7, 0.15 + normH * 0.2); // Deep navy base
      }
      colors.push(color.r, color.g, color.b);
    }
    geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    geometry.computeVertexNormals();

    const surfaceMaterial = new THREE.MeshStandardMaterial({
      vertexColors: true,
      roughness: 0.25,
      metalness: 0.35,
      wireframe: false,
      side: THREE.DoubleSide,
    });
    const surfaceMesh = new THREE.Mesh(geometry, surfaceMaterial);
    scene.add(surfaceMesh);

    // Wireframe overlay for technical grid aesthetic
    const wireframeMat = new THREE.MeshBasicMaterial({
      color: 0x38bdf8,
      wireframe: true,
      transparent: true,
      opacity: 0.18,
    });
    const wireframeMesh = new THREE.Mesh(geometry, wireframeMat);
    wireframeMesh.position.y += 0.02;
    scene.add(wireframeMesh);

    // 4. Optimal Peak Beacon & Marker
    // Peak position at (-4, 8.8, -3)
    const beaconGroup = new THREE.Group();
    beaconGroup.position.set(-4, 8.8, -3);

    // Glowing sphere
    const beaconGeo = new THREE.SphereGeometry(0.55, 32, 32);
    const beaconMat = new THREE.MeshBasicMaterial({ color: 0x10b981 });
    const beaconSphere = new THREE.Mesh(beaconGeo, beaconMat);
    beaconGroup.add(beaconSphere);

    // Outer pulse ring
    const ringGeo = new THREE.RingGeometry(0.8, 1.1, 32);
    ringGeo.rotateX(Math.PI / 2);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0x34d399,
      transparent: true,
      opacity: 0.7,
      side: THREE.DoubleSide,
    });
    const pulseRing = new THREE.Mesh(ringGeo, ringMat);
    beaconGroup.add(pulseRing);

    // Vertical indicator laser rod to ground
    const rodGeo = new THREE.CylinderGeometry(0.04, 0.04, 9, 16);
    const rodMat = new THREE.MeshBasicMaterial({
      color: 0x34d399,
      transparent: true,
      opacity: 0.6,
    });
    const rod = new THREE.Mesh(rodGeo, rodMat);
    rod.position.y = -4.5;
    beaconGroup.add(rod);

    scene.add(beaconGroup);

    // 5. Coordinate Grid Base Plane
    const gridHelper = new THREE.GridHelper(26, 26, 0x0284c7, 0x1e293b);
    gridHelper.position.y = -0.05;
    scene.add(gridHelper);

    // 6. Interactive Mouse Orbit Controls
    let isDragging = false;
    let prevMousePos = { x: 0, y: 0 };
    let spherical = { radius: 36, theta: Math.PI / 4, phi: Math.PI / 3 };

    const updateCameraPos = () => {
      spherical.phi = Math.max(0.1, Math.min(Math.PI / 2 - 0.05, spherical.phi));
      camera.position.x = spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
      camera.position.y = spherical.radius * Math.cos(spherical.phi);
      camera.position.z = spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
      camera.lookAt(0, 3.5, 0);
    };
    updateCameraPos();

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMousePos = { x: e.clientX, y: e.clientY };
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMousePos.x;
      const deltaY = e.clientY - prevMousePos.y;
      spherical.theta -= deltaX * 0.008;
      spherical.phi -= deltaY * 0.008;
      updateCameraPos();
      prevMousePos = { x: e.clientX, y: e.clientY };
    };

    const onMouseUp = () => { isDragging = false; };

    const domElement = renderer.domElement;
    domElement.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    // 7. Animation Loop
    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Slow auto rotation
      if (isRotating && !isDragging) {
        spherical.theta += 0.003;
        updateCameraPos();
      }

      // Pulse beacon ring
      const scale = 1 + 0.3 * Math.sin(elapsedTime * 3);
      pulseRing.scale.set(scale, scale, scale);
      ringMat.opacity = 0.8 - 0.4 * Math.sin(elapsedTime * 3);

      renderer.render(scene, camera);
    };
    animate();

    // Resize Handler
    const handleResize = () => {
      if (!container) return;
      const newW = container.clientWidth;
      const newH = container.clientHeight;
      camera.aspect = newW / newH;
      camera.updateProjectionMatrix();
      renderer.setSize(newW, newH);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      domElement.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
      if (container.contains(domElement)) {
        container.removeChild(domElement);
      }
    };
  }, [isRotating]);

  return (
    <div className="relative w-full h-[380px] sm:h-[420px] rounded-2xl overflow-hidden border border-white/20 bg-slate-950/80 shadow-2xl">
      {/* 3D Canvas Mount */}
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {/* Floating HUD Badge */}
      <div className="absolute top-4 left-4 z-10 flex flex-col gap-1.5 pointer-events-none">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 border border-emerald-400/30 backdrop-blur-md">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
          <span className="text-[11px] font-mono font-bold text-emerald-300">
            Mặt cong 3D Hàm Lợi Nhuận Kỳ Vọng
          </span>
        </div>
        <div className="text-[10px] text-slate-300 font-mono bg-black/40 px-2 py-0.5 rounded backdrop-blur">
          Trục X: Ngưỡng τ [0.01 - 0.50] | Trục Z: Chi phí Voucher [$1 - $20] | Trục Y: Lợi nhuận ($)
        </div>
      </div>

      {/* Optimal Coordinates HUD */}
      <div className="absolute top-4 right-4 z-10 text-right pointer-events-none">
        <div className="bg-black/60 border border-emerald-500/40 rounded-xl p-2.5 backdrop-blur-md text-white font-mono text-[11px]">
          <div className="text-emerald-400 font-bold mb-0.5">Điểm Cực Trị Tối Ưu (τ*)</div>
          <div className="text-slate-200">τ* = <span className="font-bold text-white">0.07</span></div>
          <div className="text-slate-200">Voucher = <span className="font-bold text-white">$5.00</span></div>
          <div className="text-emerald-300 font-bold text-xs mt-1">Lợi nhuận: +$115,918</div>
        </div>
      </div>

      {/* Controls Button */}
      <div className="absolute bottom-3 right-3 z-10 flex items-center gap-2">
        <button
          onClick={() => setIsRotating(!isRotating)}
          className="px-3 py-1 rounded-lg text-[11px] font-mono bg-white/10 hover:bg-white/20 text-white border border-white/20 backdrop-blur transition-all"
        >
          {isRotating ? 'Dừng xoay' : 'Tự động xoay'}
        </button>
      </div>
    </div>
  );
}

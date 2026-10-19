'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

export default function ThreeDataPipelineCube() {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const [isRotating, setIsRotating] = useState(true);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0a101f, 0.018);

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 380;

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(18, 14, 20);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // 2. Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const cyanLight = new THREE.PointLight(0x06b6d4, 3, 40);
    cyanLight.position.set(10, 10, 10);
    scene.add(cyanLight);

    const purpleLight = new THREE.PointLight(0x8b5cf6, 2.5, 40);
    purpleLight.position.set(-10, -5, -10);
    scene.add(purpleLight);

    // 3. Central 3D Data Cube / Tensor
    // Dimensions: Customers (X) x Features 63 (Y) x Time Window (Z)
    const cubeGroup = new THREE.Group();

    // Wireframe outer boundary
    const outerBoxGeo = new THREE.BoxGeometry(10, 8, 10);
    const outerBoxEdges = new THREE.EdgesGeometry(outerBoxGeo);
    const outerBoxLine = new THREE.LineSegments(
      outerBoxEdges,
      new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.6 })
    );
    cubeGroup.add(outerBoxLine);

    // Translucent glass planes representing slices
    const sliceGeo = new THREE.PlaneGeometry(9.8, 7.8);
    for (let z = -4; z <= 4; z += 2) {
      const sliceMat = new THREE.MeshPhysicalMaterial({
        color: z === 0 ? 0xec4899 : 0x0284c7,
        transparent: true,
        opacity: z === 0 ? 0.28 : 0.12,
        roughness: 0.1,
        transmission: 0.6,
        side: THREE.DoubleSide,
      });
      const sliceMesh = new THREE.Mesh(sliceGeo, sliceMat);
      sliceMesh.position.z = z;
      cubeGroup.add(sliceMesh);
    }

    // Glowing Time Curtain Plane at t0 = 2024-06-01 (z = 0)
    const curtainGeo = new THREE.PlaneGeometry(10.2, 8.2);
    const curtainMat = new THREE.MeshBasicMaterial({
      color: 0xf43f5e,
      wireframe: true,
      transparent: true,
      opacity: 0.45,
      side: THREE.DoubleSide,
    });
    const curtainMesh = new THREE.Mesh(curtainGeo, curtainMat);
    curtainMesh.position.z = 0;
    cubeGroup.add(curtainMesh);

    // 4. Data Particle Stream (Sessions & Transactions flowing through DuckDB)
    const particleCount = 650;
    const particleGeo = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleColors = new Float32Array(particleCount * 3);
    const particleVelocities: number[] = [];

    for (let i = 0; i < particleCount; i++) {
      // Historical observation zone (z < 0) flows toward t0 (z = 0)
      const x = (Math.random() - 0.5) * 9;
      const y = (Math.random() - 0.5) * 7;
      const z = (Math.random() - 0.5) * 9;

      particlePositions[i * 3] = x;
      particlePositions[i * 3 + 1] = y;
      particlePositions[i * 3 + 2] = z;

      // Color coding: Blue for raw session, Green for healed PIT feature, Red for target window
      if (z > 0) {
        particleColors[i * 3] = 0.95;     // Target outcome window (pink/red)
        particleColors[i * 3 + 1] = 0.25;
        particleColors[i * 3 + 2] = 0.45;
      } else {
        particleColors[i * 3] = 0.1;      // Historical observation window (cyan/emerald)
        particleColors[i * 3 + 1] = 0.8;
        particleColors[i * 3 + 2] = 0.9;
      }

      particleVelocities.push((Math.random() * 0.04 + 0.01) * (z < 0 ? 1 : 0.8));
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    const particleMat = new THREE.PointsMaterial({
      size: 0.22,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending,
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    cubeGroup.add(particles);

    scene.add(cubeGroup);

    // Grid Floor
    const grid = new THREE.GridHelper(24, 24, 0x0284c7, 0x1e293b);
    grid.position.y = -5.2;
    scene.add(grid);

    // 5. Interactive Mouse Orbit Controls
    let isDragging = false;
    let prevMousePos = { x: 0, y: 0 };
    let spherical = { radius: 28, theta: Math.PI / 4, phi: Math.PI / 3 };

    const updateCameraPos = () => {
      spherical.phi = Math.max(0.1, Math.min(Math.PI / 2 - 0.05, spherical.phi));
      camera.position.x = spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
      camera.position.y = spherical.radius * Math.cos(spherical.phi);
      camera.position.z = spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
      camera.lookAt(0, 0, 0);
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

    // 6. Animation Loop
    let animationFrameId: number;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      if (isRotating && !isDragging) {
        spherical.theta += 0.004;
        updateCameraPos();
      }

      // Animate streaming data particles
      const positions = particleGeo.attributes.position.array as Float32Array;
      for (let i = 0; i < particleCount; i++) {
        positions[i * 3 + 2] += particleVelocities[i];
        if (positions[i * 3 + 2] > 4.8) {
          positions[i * 3 + 2] = -4.8;
        }
      }
      particleGeo.attributes.position.needsUpdate = true;

      renderer.render(scene, camera);
    };
    animate();

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
    <div className="relative w-full h-[360px] sm:h-[400px] rounded-2xl overflow-hidden border border-white/20 bg-slate-950/80 shadow-2xl">
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

      {/* Floating HUD Badge */}
      <div className="absolute top-4 left-4 z-10 flex flex-col gap-1.5 pointer-events-none">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/20 border border-cyan-400/30 backdrop-blur-md">
          <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
          <span className="text-[11px] font-mono font-bold text-cyan-300">
            Khối Tensor Dữ Liệu 3D Point-in-Time & DuckDB
          </span>
        </div>
        <div className="text-[10px] text-slate-300 font-mono bg-black/40 px-2 py-0.5 rounded backdrop-blur">
          [200.000 Khách hàng] × [63 Đặc trưng PIT] × [Mốc t₀ = 2024-06-01]
        </div>
      </div>

      {/* Anti-leakage Time Curtain Indicator */}
      <div className="absolute top-4 right-4 z-10 text-right pointer-events-none">
        <div className="bg-black/60 border border-rose-500/40 rounded-xl p-2.5 backdrop-blur-md text-white font-mono text-[11px]">
          <div className="text-rose-400 font-bold mb-0.5">Bức Tường Thời Gian Chống Rò Rỉ</div>
          <div className="text-slate-300 text-[10px]">Cửa sổ lịch sử (t &lt; t₀) ➔ 63 Features</div>
          <div className="text-slate-300 text-[10px]">Cửa sổ mục tiêu (t &gt; t₀) ➔ Target (30d)</div>
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

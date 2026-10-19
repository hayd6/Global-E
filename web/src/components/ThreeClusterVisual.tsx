'use client';

import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

interface ClusterInfo {
  id: number;
  name: string;
  share: string;
  color: string;
  hex: number;
  aov: string;
  hesitation: number;
  recency: number;
  velocity: number;
  count: number;
}

const CLUSTERS: ClusterInfo[] = [
  { id: 1, name: 'Cụm 1: High-Value Champions', share: '6.60%', color: '#0D9488', hex: 0x0D9488, aov: '$423.65', hesitation: 8.2, recency: 412, velocity: 3.5, count: 13206 },
  { id: 2, name: 'Cụm 2: Cart Hesitators (Trọng tâm)', share: '25.04%', color: '#E11D48', hex: 0xE11D48, aov: '$267.01', hesitation: 18.4, recency: 110, velocity: 4.9, count: 50077 },
  { id: 3, name: 'Cụm 3: Discount Seekers', share: '28.90%', color: '#F59E0B', hex: 0xF59E0B, aov: '$0.00', hesitation: 12.1, recency: 76, velocity: 3.3, count: 57802 },
  { id: 4, name: 'Cụm 4: Dormant At-Risk', share: '19.66%', color: '#64748B', hex: 0x64748B, aov: '$0.00', hesitation: 0.0, recency: 999, velocity: 0.0, count: 39323 },
  { id: 5, name: 'Cụm 5: Passive Browsers', share: '19.80%', color: '#6366F1', hex: 0x6366F1, aov: '$84.84', hesitation: 14.8, recency: 47, velocity: 4.9, count: 39592 }
];

export default function ThreeClusterVisual() {
  const mountRef = useRef<HTMLDivElement | null>(null);
  const [activeCluster, setActiveCluster] = useState<number | null>(null);
  const [isRotating, setIsRotating] = useState(true);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth;
    const height = container.clientHeight || 480;

    // 1. Scene, Camera, Renderer
    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0b1329, 0.015);

    const camera = new THREE.PerspectiveCamera(45, width / height, 1, 1000);
    camera.position.set(45, 30, 55);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    // 2. Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 2.5, 300);
    pointLight.position.set(30, 50, 40);
    scene.add(pointLight);

    const blueLight = new THREE.PointLight(0x0d9488, 3, 200);
    blueLight.position.set(-30, -20, -30);
    scene.add(blueLight);

    // 3. Grid Plane and Axes Box
    const grid = new THREE.GridHelper(70, 20, 0x1e293b, 0x0f172a);
    grid.position.y = -15;
    scene.add(grid);

    // Bounding Box Frame
    const boxGeo = new THREE.BoxGeometry(60, 40, 60);
    const boxEdges = new THREE.EdgesGeometry(boxGeo);
    const boxMat = new THREE.LineBasicMaterial({ color: 0x334155, transparent: true, opacity: 0.25 });
    const wireframeBox = new THREE.LineSegments(boxEdges, boxMat);
    wireframeBox.position.set(0, 5, 0);
    scene.add(wireframeBox);

    // 4. Generate Particle Clouds for 5 Clusters
    const clusterGroups: THREE.Group[] = [];
    const pointsPerCluster = 350;

    // Centroid 3D coordinates based on behavioral data
    const centroids: Record<number, THREE.Vector3> = {
      1: new THREE.Vector3(12, 10, 16),    // High Value Champions: High CLV, High Additions
      2: new THREE.Vector3(-14, 12, 4),   // Cart Hesitators: High Hesitation, High Velocity
      3: new THREE.Vector3(-6, -4, -12),   // Discount Seekers: Moderate
      4: new THREE.Vector3(18, -12, -18),  // Dormant At-Risk: Far Recency, Low Activity
      5: new THREE.Vector3(-10, 2, 10)     // Passive Browsers: High Pages, Low AOV
    };

    CLUSTERS.forEach((c) => {
      const group = new THREE.Group();
      const centroid = centroids[c.id];

      // Centroid Glowing Sphere
      const sphereGeo = new THREE.SphereGeometry(1.4, 32, 32);
      const sphereMat = new THREE.MeshStandardMaterial({
        color: c.hex,
        emissive: c.hex,
        emissiveIntensity: 0.6,
        roughness: 0.2,
        metalness: 0.8
      });
      const centroidMesh = new THREE.Mesh(sphereGeo, sphereMat);
      centroidMesh.position.copy(centroid);
      group.add(centroidMesh);

      // Orbiting pulse ring around centroid
      const ringGeo = new THREE.RingGeometry(2.0, 2.3, 32);
      const ringMat = new THREE.MeshBasicMaterial({
        color: c.hex,
        side: THREE.DoubleSide,
        transparent: true,
        opacity: 0.4
      });
      const ringMesh = new THREE.Mesh(ringGeo, ringMat);
      ringMesh.position.copy(centroid);
      ringMesh.rotation.x = Math.PI / 2;
      group.add(ringMesh);

      // Particle Cloud around Centroid (Gaussian spread)
      const positions = new Float32Array(pointsPerCluster * 3);
      const spread = c.id === 4 ? 8 : c.id === 2 ? 6.5 : 5.5;

      for (let i = 0; i < pointsPerCluster; i++) {
        // Box-Muller Gaussian jitter
        const u1 = Math.max(0.0001, Math.random());
        const u2 = Math.random();
        const randStdNormal = Math.sqrt(-2.0 * Math.log(u1)) * Math.sin(2.0 * Math.PI * u2);

        positions[i * 3] = centroid.x + randStdNormal * spread * (Math.random() - 0.5) * 2;
        positions[i * 3 + 1] = centroid.y + randStdNormal * (spread * 0.7) * (Math.random() - 0.5) * 2;
        positions[i * 3 + 2] = centroid.z + randStdNormal * spread * (Math.random() - 0.5) * 2;
      }

      const pointGeo = new THREE.BufferGeometry();
      pointGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));

      // Particle Material
      const pointMat = new THREE.PointsMaterial({
        color: c.hex,
        size: 1.1,
        transparent: true,
        opacity: 0.75,
        blending: THREE.AdditiveBlending
      });

      const particleSystem = new THREE.Points(pointGeo, pointMat);
      group.add(particleSystem);

      group.userData = { clusterId: c.id, ringMesh };
      scene.add(group);
      clusterGroups.push(group);
    });

    // 5. Connecting Lines between Centroids to visualize distance
    const lineMat = new THREE.LineDashedMaterial({
      color: 0x475569,
      dashSize: 1,
      gapSize: 1,
      transparent: true,
      opacity: 0.3
    });
    const lineGeo = new THREE.BufferGeometry().setFromPoints([
      centroids[1], centroids[5],
      centroids[5], centroids[2],
      centroids[2], centroids[3],
      centroids[3], centroids[4]
    ]);
    const lines = new THREE.LineSegments(lineGeo, lineMat);
    lines.computeLineDistances();
    scene.add(lines);

    // 6. Interactive Mouse Orbit Controls
    let isDragging = false;
    let prevMouseX = 0;
    let prevMouseY = 0;
    let targetRotationX = 0.2;
    let targetRotationY = 0.3;
    let currentRotationX = 0.2;
    let currentRotationY = 0.3;
    let zoomDistance = 65;

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    };

    const onMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      const deltaX = e.clientX - prevMouseX;
      const deltaY = e.clientY - prevMouseY;
      targetRotationY += deltaX * 0.007;
      targetRotationX += deltaY * 0.007;
      targetRotationX = Math.max(-Math.PI / 3, Math.min(Math.PI / 3, targetRotationX));
      prevMouseX = e.clientX;
      prevMouseY = e.clientY;
    };

    const onMouseUp = () => { isDragging = false; };
    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      zoomDistance += e.deltaY * 0.04;
      zoomDistance = Math.max(30, Math.min(100, zoomDistance));
    };

    const domElement = renderer.domElement;
    domElement.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    domElement.addEventListener('wheel', onWheel, { passive: false });

    // Touch support for mobile
    let touchStartX = 0;
    let touchStartY = 0;
    const onTouchStart = (e: TouchEvent) => {
      if (e.touches.length === 1) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }
    };
    const onTouchMove = (e: TouchEvent) => {
      if (e.touches.length === 1) {
        const dx = e.touches[0].clientX - touchStartX;
        const dy = e.touches[0].clientY - touchStartY;
        targetRotationY += dx * 0.007;
        targetRotationX += dy * 0.007;
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }
    };
    domElement.addEventListener('touchstart', onTouchStart);
    domElement.addEventListener('touchmove', onTouchMove);

    // 7. Animation Loop
    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();

      // Auto-rotation when not dragging
      if (isRotating && !isDragging) {
        targetRotationY += 0.0035;
      }

      // Smooth camera interpolation
      currentRotationX += (targetRotationX - currentRotationX) * 0.08;
      currentRotationY += (targetRotationY - currentRotationY) * 0.08;

      camera.position.x = zoomDistance * Math.sin(currentRotationY) * Math.cos(currentRotationX);
      camera.position.y = zoomDistance * Math.sin(currentRotationX) + 8;
      camera.position.z = zoomDistance * Math.cos(currentRotationY) * Math.cos(currentRotationX);
      camera.lookAt(0, 3, 0);

      // Animate rings & cluster pulsing
      clusterGroups.forEach((cg) => {
        const ring = cg.userData.ringMesh as THREE.Mesh;
        if (ring) {
          ring.rotation.z = elapsedTime * 0.8;
          const scale = 1 + 0.15 * Math.sin(elapsedTime * 2.5 + cg.userData.clusterId);
          ring.scale.set(scale, scale, scale);
        }
      });

      renderer.render(scene, camera);
    };

    animate();

    // 8. Resize Handler
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight || 480;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      domElement.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      domElement.removeEventListener('wheel', onWheel);
      domElement.removeEventListener('touchstart', onTouchStart);
      domElement.removeEventListener('touchmove', onTouchMove);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, [isRotating]);

  return (
    <div className="relative w-full h-[460px] md:h-[520px] rounded-2xl overflow-hidden bg-slate-950/80 border border-slate-800 shadow-2xl flex flex-col justify-between p-4">
      {/* 3D WebGL Canvas Mount Container */}
      <div ref={mountRef} className="absolute inset-0 cursor-grab active:cursor-grabbing" />

      {/* Top HUD Controls */}
      <div className="relative z-10 flex flex-wrap items-center justify-between gap-2 pointer-events-auto">
        <div className="bg-slate-900/90 backdrop-blur-md px-3.5 py-1.5 rounded-full border border-slate-700/80 text-xs flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse" />
          <span className="font-mono font-bold text-white tracking-wide">3D RFM-E CLUSTER SPACE (GMM k*=5)</span>
          <span className="text-[10px] text-slate-400 font-mono">BIC 2,143,890 • 200,000 N</span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsRotating(!isRotating)}
            className={`px-3 py-1 rounded-full text-xs font-mono font-medium transition-colors border ${
              isRotating
                ? 'bg-teal-500/20 text-teal-300 border-teal-500/40 hover:bg-teal-500/30'
                : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
            }`}
          >
            {isRotating ? 'Auto-Orbit: ON' : 'Auto-Orbit: OFF'}
          </button>
          <span className="text-[10px] text-slate-400 hidden sm:inline-block bg-slate-900/80 px-2.5 py-1 rounded-full border border-slate-800">
            Kéo chuột để xoay 3D • Cuộn để zoom
          </span>
        </div>
      </div>

      {/* Bottom HUD: 5 Cluster Legend with Interactive Highlights */}
      <div className="relative z-10 pointer-events-auto">
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-2">
          {CLUSTERS.map((c) => {
            const isSelected = activeCluster === c.id;
            return (
              <div
                key={c.id}
                onMouseEnter={() => setActiveCluster(c.id)}
                onMouseLeave={() => setActiveCluster(null)}
                className={`p-2.5 rounded-xl border backdrop-blur-md transition-all duration-200 cursor-pointer ${
                  isSelected
                    ? 'bg-slate-900/95 border-white/40 shadow-lg scale-[1.02]'
                    : 'bg-slate-900/75 border-slate-800/80 hover:bg-slate-850 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: c.color }} />
                  <span className="text-[11px] font-bold text-white truncate">{c.name.split(':')[1] || c.name}</span>
                </div>
                <div className="flex items-center justify-between text-[10px] text-slate-400 font-mono">
                  <span>Tỷ trọng: <strong className="text-white">{c.share}</strong></span>
                  <span>AOV: <strong className="text-emerald-400">{c.aov}</strong></span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

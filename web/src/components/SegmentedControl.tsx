'use client';

import React, { useState, useRef, useEffect } from 'react';

interface SegmentedControlProps {
  tabs: string[];
  activeIndex: number;
  onChange: (index: number) => void;
}

export default function SegmentedControl({ tabs, activeIndex, onChange }: SegmentedControlProps) {
  const [indicatorStyle, setIndicatorStyle] = useState<{ left: string; width: string; height: string }>({
    left: '0px',
    width: '0px',
    height: '0px',
  });
  const tabsRef = useRef<(HTMLButtonElement | null)[]>([]);

  const updateIndicator = () => {
    const activeTabEl = tabsRef.current[activeIndex];
    if (activeTabEl) {
      setIndicatorStyle({
        left: `${activeTabEl.offsetLeft}px`,
        width: `${activeTabEl.offsetWidth}px`,
        height: `${activeTabEl.offsetHeight}px`,
      });
    }
  };

  useEffect(() => {
    updateIndicator();
  }, [activeIndex]);

  useEffect(() => {
    window.addEventListener('resize', updateIndicator);
    return () => window.removeEventListener('resize', updateIndicator);
  }, [activeIndex]);

  return (
    <div className="relative inline-flex bg-black/70 backdrop-blur-2xl p-1 rounded-full select-none items-center border border-white/20 shadow-xl overflow-x-auto max-w-full scrollbar-none shrink-0">
      {/* Khối nền màu trắng chuyển động trượt */}
      <div
        className="absolute bg-white rounded-full shadow-[0_2px_10px_rgba(255,255,255,0.4)] transition-all duration-300 ease-[cubic-bezier(0.25,1,0.5,1)] top-1"
        style={indicatorStyle}
      />

      {/* Danh sách các nút lựa chọn */}
      {tabs.map((tab, index) => {
        const isActive = activeIndex === index;
        return (
          <button
            key={tab}
            ref={(el) => { tabsRef.current[index] = el; }}
            onClick={() => onChange(index)}
            className={`relative z-10 px-2.5 sm:px-3.5 py-1 text-xs font-semibold rounded-full whitespace-nowrap text-center transition-all duration-200 cursor-pointer hover:scale-[1.03] active:scale-[0.97] ${
              isActive ? 'text-black font-bold' : 'text-gray-300 hover:text-white'
            }`}
          >
            {tab}
          </button>
        );
      })}
    </div>
  );
}

'use client';

import React, { useState, useRef, useEffect } from 'react';

export default function SegmentedControl() {
  const tabs = ['Tất cả', 'Bị nhỡ'];
  const [activeIndex, setActiveIndex] = useState(0);
  
  // Khởi tạo các trạng thái để tính toán kích thước động cho khối nền trượt
  const [indicatorStyle, setIndicatorStyle] = useState({});
  const tabsRef = useRef<(HTMLButtonElement | null)[]>([]);

  // Tự động cập nhật vị trí và độ rộng của khối nền trắng khi chuyển tab
  useEffect(() => {
    const activeTab = tabsRef.current[activeIndex];
    if (activeTab) {
      setIndicatorStyle({
        left: ${activeTab.offsetLeft}px,
        width: ${activeTab.offsetWidth}px,
        height: ${activeTab.offsetHeight}px,
      });
    }
  }, [activeIndex]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      {/* Thanh nền lớn hình viên thuốc */}
      <div className="relative flex bg-[#f1f1f1] p-1.5 rounded-full select-none items-center">
        
        {/* Khối nền màu trắng chuyển động trượt */}
        <div
          className="absolute bg-white rounded-full shadow-[0_2px_6px_rgba(0,0,0,0.08)] transition-all duration-300 ease-[cubic-bezier(0.25,1,0.5,1)] top-1.5"
          style={indicatorStyle}
        />

        {/* Danh sách các nút lựa chọn */}
        {tabs.map((tab, index) => (
          <button
            key={tab}
            ref={(el) => { tabsRef.current[index] = el; }}
            onClick={() => setActiveIndex(index)}
            className={relative z-10 px-8 py-3 text-base font-medium rounded-full min-w-[120px] text-center transition-colors duration-200 ${
              activeIndex === index ? 'text-black' : 'text-gray-900'
            }}
          >
            {tab}
          </button>
        ))}
        
      </div>
    </div>
  );
}
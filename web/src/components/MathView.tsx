'use client';

import React, { useMemo } from 'react';
import katex from 'katex';

interface MathViewProps {
  math: string;
  block?: boolean;
  className?: string;
}

export default function MathView({ math, block = false, className = '' }: MathViewProps) {
  const html = useMemo(() => {
    try {
      return katex.renderToString(math, {
        displayMode: block,
        throwOnError: false,
      });
    } catch {
      return math;
    }
  }, [math, block]);

  if (block) {
    return (
      <div
        className={`katex-block w-full max-w-full overflow-x-auto overflow-y-hidden [scrollbar-width:none] [&::-webkit-scrollbar]:hidden py-0.5 text-center select-none ${className}`}
        dangerouslySetInnerHTML={{ __html: html }}
      />
    );
  }

  return (
    <span
      className={`katex-inline inline-block align-middle select-none ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

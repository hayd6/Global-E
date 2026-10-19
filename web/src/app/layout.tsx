import type { Metadata } from "next";
import "katex/dist/katex.min.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "Global-E Decision Intelligence Portal",
  description: "Cổng thông tin nghiên cứu hành vi giỏ hàng và tối ưu hóa lợi nhuận kinh tế",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="vi">
      <body className="antialiased min-h-screen bg-slateBg">{children}</body>
    </html>
  );
}

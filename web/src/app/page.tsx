'use client';

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import {
  TrendingUp,
  ShieldCheck,
  Zap,
  Activity,
  Layers,
  BarChart3,
  Users,
  Target,
  ArrowRight,
  Database,
  Sliders,
  DollarSign,
  AlertTriangle,
  Clock,
  Sparkles,
  GitBranch,
  Percent,
  Compass,
  CheckCircle2,
  Box,
  Eye,
  FileText,
  HelpCircle,
  Award,
  ChevronRight,
  Check,
  TrendingDown,
  Info,
  Lightbulb,
  Briefcase
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  ComposedChart,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Cell,
  Legend
} from 'recharts';
import SegmentedControl from '@/components/SegmentedControl';
import MathView from '@/components/MathView';

// Dynamic imports for 3D Three.js components to prevent SSR hydration mismatch
const ThreeClusterVisual = dynamic(() => import('@/components/ThreeClusterVisual'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[440px] md:h-[480px] rounded-2xl bg-slate-950/80 border border-slate-800 flex items-center justify-center text-slate-400 font-mono text-sm">
      <div className="flex items-center gap-3">
        <span className="w-3 h-3 rounded-full bg-emerald-400 animate-ping" />
        Đang khởi tạo không gian 3D WebGL RFM-E...
      </div>
    </div>
  ),
});

const ThreeProfitSurface = dynamic(() => import('@/components/ThreeProfitSurface'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[380px] sm:h-[420px] rounded-2xl bg-slate-950/80 border border-slate-800 flex items-center justify-center text-slate-400 font-mono text-sm">
      <div className="flex items-center gap-3">
        <span className="w-3 h-3 rounded-full bg-cyan-400 animate-ping" />
        Đang khởi tạo mặt cong 3D hàm lợi nhuận What-If...
      </div>
    </div>
  ),
});

const ThreeDataPipelineCube = dynamic(() => import('@/components/ThreeDataPipelineCube'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[360px] sm:h-[400px] rounded-2xl bg-slate-950/80 border border-slate-800 flex items-center justify-center text-slate-400 font-mono text-sm">
      <div className="flex items-center gap-3">
        <span className="w-3 h-3 rounded-full bg-indigo-400 animate-ping" />
        Đang nạp khối Tensor dữ liệu 3D Point-in-Time...
      </div>
    </div>
  ),
});

const ThreeCelestialSphere = dynamic(() => import('@/components/ThreeCelestialSphere'), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[460px] sm:h-[520px] rounded-2xl bg-amber-50/70 border border-[#ffcf9e] flex items-center justify-center text-[#3a3a3e] font-mono text-sm">
      <div className="flex items-center gap-3">
        <span className="w-3 h-3 rounded-full bg-amber-500 animate-ping" />
        Đang khởi tạo Thiên Thể Hoàng Hôn 3D &amp; Bụi Sao WebGL...
      </div>
    </div>
  ),
});

// 6 Section navigation tabs matching the user-specified concise titles
const SECTION_TABS = [
  '1. Giới thiệu',
  '2. Mục Tiêu và Câu hỏi',
  '3. Quy trình và Khám Phá',
  '4. ML và kết quả',
  '5. Dashboard, Insight, đề xuất',
  '6. Kết Luận',
];

const DASHBOARD_TABS = [
  'Trang 1: Động học phễu & KPI',
  'Trang 2: Phân khúc GMM & Radar',
  'Trang 3: Phân tích sống còn',
  'Trang 4: Mô phỏng What-If kinh tế',
];

// Initial Profit Curve from Table 5.1
const INITIAL_PROFIT_CURVE = [
  { threshold: 0.01, profit: 92450, contacts: 15420, tp: 5980, fp: 9440 },
  { threshold: 0.03, profit: 104280, contacts: 14100, tp: 5740, fp: 8360 },
  { threshold: 0.05, profit: 112650, contacts: 12600, tp: 5420, fp: 7180 },
  { threshold: 0.07, profit: 115918, contacts: 11340, tp: 5120, fp: 6220 }, // Peak tau*
  { threshold: 0.10, profit: 113400, contacts: 9680, tp: 4680, fp: 5000 },
  { threshold: 0.15, profit: 106200, contacts: 7540, tp: 3980, fp: 3560 },
  { threshold: 0.20, profit: 98400, contacts: 5820, tp: 3340, fp: 2480 },
  { threshold: 0.30, profit: 89100, contacts: 3720, tp: 2410, fp: 1310 },
  { threshold: 0.40, profit: 81200, contacts: 2450, tp: 1780, fp: 670 },
  { threshold: 0.50, profit: 74718, contacts: 1620, tp: 1240, fp: 380 }, // Default tau
  { threshold: 0.60, profit: 62500, contacts: 980, tp: 810, fp: 170 },
  { threshold: 0.70, profit: 48900, contacts: 520, tp: 450, fp: 70 },
];

// 10-Decile Lift@K from tbl_ch5_decile_lift_profit.csv
const DECILE_DATA = [
  { decile: 'D1', count: 3200, purchases: 1049, rate: '32.78%', lift: 1.61, recall: '16.15%', precision: '32.78%', profit: 19917.86, cumProfit: 19917.86, color: '#0D9488' },
  { decile: 'D2', count: 3200, purchases: 843, rate: '26.34%', lift: 1.30, recall: '29.12%', precision: '29.56%', profit: 16103.52, cumProfit: 36021.38, color: '#0F172A' },
  { decile: 'D3', count: 3200, purchases: 827, rate: '25.84%', lift: 1.27, recall: '41.85%', precision: '28.32%', profit: 16288.69, cumProfit: 52310.07, color: '#0F172A' },
  { decile: 'D4', count: 3200, purchases: 686, rate: '21.44%', lift: 1.06, recall: '52.41%', precision: '26.60%', profit: 12634.31, cumProfit: 64944.38, color: '#334155' },
  { decile: 'D5', count: 3200, purchases: 696, rate: '21.75%', lift: 1.07, recall: '63.12%', precision: '25.63%', profit: 11633.54, cumProfit: 76577.92, color: '#475569' },
  { decile: 'D6', count: 3200, purchases: 613, rate: '19.16%', lift: 0.94, recall: '72.56%', precision: '24.55%', profit: 10986.51, cumProfit: 87564.43, color: '#64748B' },
  { decile: 'D7', count: 3200, purchases: 561, rate: '17.53%', lift: 0.86, recall: '81.19%', precision: '23.55%', profit: 10059.76, cumProfit: 97624.19, color: '#64748B' },
  { decile: 'D8', count: 3200, purchases: 471, rate: '14.72%', lift: 0.72, recall: '88.44%', precision: '22.45%', profit: 7781.28, cumProfit: 105405.47, color: '#94A3B8' },
  { decile: 'D9', count: 3200, purchases: 416, rate: '13.00%', lift: 0.64, recall: '94.84%', precision: '21.40%', profit: 5907.00, cumProfit: 111312.46, color: '#CBD5E1' },
  { decile: 'D10', count: 3200, purchases: 335, rate: '10.47%', lift: 0.52, recall: '100.00%', precision: '20.30%', profit: 4604.59, cumProfit: 115917.06, color: '#E2E8F0' },
];

// GMM 5 Clusters from tbl_ch3_gmm_cluster_profiles.csv
const GMM_DATA = [
  { id: 1, name: 'High-Value Champions', shortName: 'C1: Champions VIP', count: 13206, share: '6.60%', shareNum: 6.6, aov: '$423.65', aovNum: 423.65, recency: '412.3 ngày', freq: '2.6 đơn', addCart: '8.2', aban: '3.5', conv: '19.51%', color: '#0D9488', action: 'Chăm sóc đặc quyền VIP, tối ưu trải nghiệm thanh toán cao cấp' },
  { id: 2, name: 'Cart Hesitators / Shipping-Sensitive', shortName: 'C2: Cart Hesitators', count: 50077, share: '25.04%', shareNum: 25.04, aov: '$267.01', aovNum: 267.01, recency: '110.9 ngày', freq: '2.1 đơn', addCart: '11.3', aban: '4.9', conv: '20.35%', color: '#E11D48', action: 'Miễn phí vận chuyển linh hoạt khi giỏ đạt >= $68.0 (80% AOV)' },
  { id: 3, name: 'Discount Seekers', shortName: 'C3: Discount Seekers', count: 57802, share: '28.90%', shareNum: 28.9, aov: '$0.00', aovNum: 0.0, recency: '76.2 ngày', freq: '0.0 đơn', addCart: '7.6', aban: '3.3', conv: '20.62%', color: '#4F46E5', action: 'Cấp flash voucher ưu đãi động có giới hạn đếm ngược 24h' },
  { id: 4, name: 'Dormant At-Risk', shortName: 'C4: Dormant At-Risk', count: 39323, share: '19.66%', shareNum: 19.66, aov: '$0.00', aovNum: 0.0, recency: '999.0 ngày', freq: '0.0 đơn', addCart: '0.0', aban: '0.0', conv: '20.56%', color: '#64748B', action: 'Kích hoạt chiến dịch email đánh thức chi phí thấp' },
  { id: 5, name: 'Passive Browsers', shortName: 'C5: Passive Browsers', count: 39592, share: '19.80%', shareNum: 19.8, aov: '$84.84', aovNum: 84.84, recency: '47.0 ngày', freq: '1.2 đơn', addCart: '11.3', aban: '4.9', conv: '20.02%', color: '#D97706', action: 'Đề xuất sản phẩm kèm (Cross-sell/Up-sell) gia tăng AOV' },
];

// Native Radar Chart Data for GMM 5 Clusters
const RADAR_METRICS_DATA = [
  { metric: 'Recency (Độ trễ)', C1_VIP: 88, C2_Hesitator: 38, C3_Discount: 26, C4_Dormant: 100, C5_Browser: 18 },
  { metric: 'Frequency (Tần suất)', C1_VIP: 92, C2_Hesitator: 72, C3_Discount: 10, C4_Dormant: 5, C5_Browser: 42 },
  { metric: 'Monetary (Chi tiêu)', C1_VIP: 96, C2_Hesitator: 62, C3_Discount: 8, C4_Dormant: 5, C5_Browser: 26 },
  { metric: 'Cart Adds (Thêm giỏ)', C1_VIP: 54, C2_Hesitator: 88, C3_Discount: 52, C4_Dormant: 5, C5_Browser: 86 },
  { metric: 'Severity (Mức bỏ giỏ)', C1_VIP: 42, C2_Hesitator: 92, C3_Discount: 46, C4_Dormant: 5, C5_Browser: 91 },
  { metric: 'Velocity (Tốc độ)', C1_VIP: 68, C2_Hesitator: 82, C3_Discount: 42, C4_Dormant: 5, C5_Browser: 76 },
];

// Native Shipping Friction by Customer Tier
const SHIPPING_FRICTION_DATA = [
  { tier: 'Bronze', overnight: 84.5, standard: 69.8, free: 52.4 },
  { tier: 'Silver', overnight: 82.1, standard: 68.4, free: 51.1 },
  { tier: 'Gold', overnight: 79.4, standard: 66.1, free: 49.8 },
  { tier: 'Platinum', overnight: 71.2, standard: 61.5, free: 44.2 },
];

// Native Kaplan-Meier Decay Curve Data
const KAPLAN_MEIER_DATA = [
  { day: 0, survival: 100.0, baseline: 100 },
  { day: 1, survival: 78.4, baseline: 90 },
  { day: 2, survival: 66.8, baseline: 80 },
  { day: 3, survival: 56.2, baseline: 70 },
  { day: 5, survival: 34.5, baseline: 55 },
  { day: 7, survival: 17.8, baseline: 45 }, // t* cutoff
  { day: 10, survival: 11.2, baseline: 35 },
  { day: 14, survival: 6.5, baseline: 25 },
  { day: 21, survival: 3.1, baseline: 15 },
  { day: 30, survival: 1.2, baseline: 5 },
];

// Native Category Abandonment Severity Data
const CATEGORY_ABANDON_DATA = [
  { category: 'Điện tử & Công nghệ', severity: 5.4, aov: 385 },
  { category: 'Thời trang & Phụ kiện', severity: 5.1, aov: 142 },
  { category: 'Gia dụng & Đời sống', severity: 4.8, aov: 198 },
  { category: 'Sức khỏe & Sắc đẹp', severity: 4.6, aov: 88 },
  { category: 'Thể thao & Dã ngoại', severity: 4.2, aov: 165 },
  { category: 'Sách & Văn phòng', severity: 3.5, aov: 45 },
  { category: 'Mẹ & Bé', severity: 3.2, aov: 112 },
  { category: 'Bách hóa tiêu dùng', severity: 2.8, aov: 62 },
];

// Native Qini Uplift Cumulative Curve Data
const QINI_DATA = [
  { pct: 0, tLearner: 0, random: 0 },
  { pct: 10, tLearner: 24.5, random: 10 },
  { pct: 20, tLearner: 46.8, random: 20 },
  { pct: 30, tLearner: 65.2, random: 30 },
  { pct: 35, tLearner: 73.1, random: 35 }, // Persuadables peak
  { pct: 50, tLearner: 84.6, random: 50 },
  { pct: 70, tLearner: 92.4, random: 70 },
  { pct: 90, tLearner: 98.2, random: 90 },
  { pct: 100, tLearner: 100.0, random: 100 },
];

// Model Benchmark from tbl_ch4_model_benchmark_comparison.csv
const MODEL_BENCHMARK = [
  { name: 'CatBoost', pr_auc: 0.2776, roc_auc: 0.6136, f1: 0.3606, prec: 0.2586, rec: 0.5955, acc: 0.5713, brier: 0.2403, ece: 0.2866, trainTime: '5.08s', latency: '0.6ms' },
  { name: 'Calibrated LightGBM (Isotonic)', pr_auc: 0.2772, roc_auc: 0.6134, f1: 0.0009, prec: 0.3333, rec: 0.0005, acc: 0.7969, brier: 0.1577, ece: 0.0020, trainTime: '5.82s', latency: '10.8ms' },
  { name: 'Calibrated LightGBM (Platt Sigmoid)', pr_auc: 0.2771, roc_auc: 0.6136, f1: 0.0000, prec: 0.0000, rec: 0.0000, acc: 0.7970, brier: 0.1576, ece: 0.0035, trainTime: '5.07s', latency: '8.4ms' },
  { name: 'Stacking Ensemble', pr_auc: 0.2770, roc_auc: 0.6137, f1: 0.0000, prec: 0.0000, rec: 0.0000, acc: 0.7970, brier: 0.1576, ece: 0.0009, trainTime: '63.40s', latency: '11.4ms' },
  { name: 'XGBoost', pr_auc: 0.2759, roc_auc: 0.6124, f1: 0.2853, prec: 0.2991, rec: 0.2727, acc: 0.7226, brier: 0.2067, ece: 0.2206, trainTime: '3.56s', latency: '1.1ms' },
  { name: 'LightGBM (Chưa hiệu chuẩn)', pr_auc: 0.2757, roc_auc: 0.6133, f1: 0.3107, prec: 0.2939, rec: 0.3295, acc: 0.7031, brier: 0.2084, ece: 0.2236, trainTime: '1.84s', latency: '2.8ms' },
  { name: 'Random Forest', pr_auc: 0.2715, roc_auc: 0.6064, f1: 0.0000, prec: 0.0000, rec: 0.0000, acc: 0.7970, brier: 0.1584, ece: 0.0144, trainTime: '36.68s', latency: '7.6ms' },
  { name: 'Logistic Regression', pr_auc: 0.2669, roc_auc: 0.5967, f1: 0.0006, prec: 0.6667, rec: 0.0003, acc: 0.7970, brier: 0.1587, ece: 0.0037, trainTime: '0.60s', latency: '0.2ms' },
];

// CoxPH Hazard Ratios from tbl_ch4_coxph_hazard_ratios.csv
const COXPH_DATA = [
  { covariate: 'loyalty_score', coef: 1.1035, hr: 3.0147, lower: 2.5992, upper: 3.4966, p: '3.55e-48', impact: 'Tăng nguy cơ từ bỏ giỏ hàng (Rào cản ma sát)' },
  { covariate: 'cart_to_page_ratio', coef: 0.2716, hr: 1.3121, lower: 1.1660, upper: 1.4764, p: '6.44e-06', impact: 'Tăng nguy cơ từ bỏ giỏ hàng (Rào cản ma sát)' },
  { covariate: 'cart_abandonment_severity', coef: 0.0498, hr: 1.0510, lower: 1.0418, upper: 1.0603, p: '2.16e-28', impact: 'Tăng nguy cơ từ bỏ giỏ hàng (Rào cản ma sát)' },
  { covariate: 'bounce_rate', coef: 0.0161, hr: 1.0162, lower: 0.9341, upper: 1.1056, p: '0.708', impact: 'Tác động trung tính / Không có ý nghĩa' },
  { covariate: 'pct_overnight_shipping', coef: -0.0685, hr: 0.9338, lower: 0.8678, upper: 1.0048, p: '0.067', impact: 'Tác động cận biên (p ~ 0.06)' },
  { covariate: 'trans_discount_usage_rate', coef: -0.0833, hr: 0.9201, lower: 0.8638, upper: 0.9801, p: '0.0098', impact: 'Giảm nguy cơ từ bỏ (Đòn bẩy chuyển đổi)' },
];

// Uplift Segments from tbl_ch4_uplift_segments_summary.csv
const UPLIFT_DATA = [
  { segment: 'Persuadables', count: 11200, pct: '35.00%', uplift: '+0.1460', treatRate: '24.00%', ctrlRate: '33.07%', rec: 'Ưu tiên số 1: Cấp voucher đếm ngược & cá thể hóa cao' },
  { segment: 'Sure Things', count: 1151, pct: '3.60%', uplift: '+0.0383', treatRate: '31.86%', ctrlRate: '31.34%', rec: 'Cấm cấp voucher; bảo toàn 100% biên lợi nhuận tự nhiên' },
  { segment: 'Lost Causes', count: 16764, pct: '52.39%', uplift: '+0.0641', treatRate: '16.91%', ctrlRate: '19.97%', rec: 'Loại bỏ khỏi chiến dịch; tránh lãng phí ngân sách tiếp cận' },
  { segment: 'Sleeping Dogs', count: 2885, pct: '9.02%', uplift: '-0.0618', treatRate: '19.30%', ctrlRate: '23.66%', rec: 'Tuyệt đối không can thiệp; tránh phản cảm gây mất khách' },
];

export default function GlobalEDecisionIntelligencePortal() {
  const [activeTab, setActiveTab] = useState(0);
  const [dashTab, setDashTab] = useState(0);
  const [selectedClusterId, setSelectedClusterId] = useState(2);
  const [mounted, setMounted] = useState(false);

  // What-If Simulation Parameters
  const [margin, setMargin] = useState(30);
  const [contactCost, setContactCost] = useState(0.8);
  const [voucherCost, setVoucherCost] = useState(5.0);
  const [simData, setSimData] = useState({
    optimal_tau: 0.07,
    max_profit: 115918,
    default_profit: 74718,
    delta: 41200,
    profit_curve: INITIAL_PROFIT_CURVE,
  });

  useEffect(() => {
    setMounted(true);
  }, []);

  const runSimulation = (m: number, c: number, v: number) => {
    const scaleFactor = (m / 30) * 1.0 - (c - 0.8) * 0.15 - (v - 5.0) * 0.05;
    const newCurve = INITIAL_PROFIT_CURVE.map((pt) => {
      const scaledProfit = Math.round(pt.profit * Math.max(0.2, scaleFactor));
      return { ...pt, profit: scaledProfit };
    });
    const maxPt = newCurve.reduce((prev, current) => (prev.profit > current.profit ? prev : current));
    const defPt = newCurve.find((p) => p.threshold === 0.5) || newCurve[newCurve.length - 1];

    setSimData({
      optimal_tau: maxPt.threshold,
      max_profit: maxPt.profit,
      default_profit: defPt.profit,
      delta: Math.max(0, maxPt.profit - defPt.profit),
      profit_curve: newCurve,
    });
  };

  const selectedCluster = GMM_DATA.find((c) => c.id === selectedClusterId) || GMM_DATA[1];

  return (
    <div className="relative min-h-screen text-slate-900 selection:bg-teal-500 selection:text-white">
      {/* 1. Background Video Fullscreen - Raw video plays continuously behind translucent frosted glass */}
      <div className="fixed inset-0 w-full h-full overflow-hidden -z-20 pointer-events-none">
        <video
          autoPlay
          loop
          muted
          playsInline
          className="w-full h-full object-cover"
          src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260403_050628_c4e32401-fab4-4a27-b7a8-6e9291cd5959.mp4"
        />
      </div>

      {/* 2. Sleek Compact Header - Perfectly Centered, Never Spilling to Edges */}
      <header className="sticky top-0 z-50 w-full px-4 sm:px-6 py-2.5 backdrop-blur-xl bg-black/55 border-b border-white/10 shadow-xl">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center gap-4 lg:gap-6">
          {/* Brand Logo & Meta */}
          <div className="flex items-center gap-2.5 shrink-0">
            <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-teal-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-teal-500/20 bounce-btn">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <div>
              <div className="font-extrabold text-sm tracking-tight text-white flex items-center gap-2">
                GLOBAL-E
                <span className="text-[9px] font-mono font-semibold px-2 py-0.5 rounded-full bg-teal-500/20 text-teal-300 border border-teal-500/30">
                  Decision Intelligence
                </span>
              </div>
              <div className="text-[10px] text-gray-300 font-mono hidden xl:block">
                Prescriptive Framework | N = 200,000 | DuckDB PIT
              </div>
            </div>
          </div>

          {/* Compact 6-Section Pill Control - Shifted to Left */}
          <div className="shrink-0 max-w-full">
            <SegmentedControl
              tabs={SECTION_TABS}
              activeIndex={activeTab}
              onChange={(idx) => setActiveTab(idx)}
            />
          </div>

          {/* Compact Empirical Badge - Pushed to Far Right */}
          <div className="hidden md:flex items-center gap-2 text-xs font-mono text-gray-300 shrink-0 ml-auto">
            <div className="px-2.5 py-1 rounded-full bg-white/10 border border-white/15 backdrop-blur-md flex items-center gap-1.5 bounce-btn">
              <span className="w-1.5 h-1.5 rounded-full bg-teal-400 animate-pulse" />
              <span className="text-[11px] text-white">&tau;* = <strong className="text-teal-400">0.07</strong></span>
              <span className="text-gray-400">|</span>
              <span className="text-[11px] text-emerald-400 font-bold">+$115,918</span>
            </div>
          </div>
        </div>
      </header>

      {/* 3. Main Reading Area - High-transparency Frosted Glass Frame with 4 Visible Margins */}
      <main className="relative z-10 py-6">
        <div className="main-reading-frame mx-3 sm:mx-6 md:mx-10 lg:mx-14 rounded-3xl p-5 sm:p-8 md:p-12 shadow-2xl">

          {/* ========================================================
              PHẦN 1: GIỚI THIỆU ĐỀ TÀI VÀ VẤN ĐỀ KINH DOANH
          ======================================================== */}
          {activeTab === 0 && (
            <div className="space-y-8 animate-fadeIn">
              {/* 3D Celestial Emerald Sphere Hero Header */}
              <div className="w-full">
                <ThreeCelestialSphere />
              </div>

              {/* 1.1 Tuyên Ngôn Sứ Mệnh & Giới Thiệu Đề Tài */}
              <div className="sub-reading-card p-6 border-l-4 border-l-[#ffcf9e]">
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles className="w-5 h-5 text-amber-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    1.1. Tuyên Ngôn Sứ Mệnh &amp; Bản Chất Đột Phá Của Đề Tài
                  </h3>
                </div>
                <div className="space-y-3 text-xs sm:text-sm text-slate-800 leading-relaxed font-medium">
                  <p>
                    <strong className="text-midnightNavy font-bold">Tên đề tài nghiên cứu: </strong>
                    <span className="text-[#3a3a3e] font-semibold">
                      Phân tích rào cản chuyển đổi giỏ hàng và tối ưu hóa lợi nhuận tiếp thị trong thương mại điện tử.
                    </span>
                  </p>
                  <p>
                    Trong kỷ nguyên số hiện đại, đại đa số các hệ sinh thái thương mại điện tử chỉ dừng lại ở bài toán
                    <strong className="text-midnightNavy"> Mô hình hóa Dự báo (Predictive AI)</strong> — tức trả lời câu hỏi:
                    <em> &ldquo;Khách hàng này có khả năng bỏ giỏ hàng hay không?&rdquo;</em> mà bất lực trong việc trả lời câu hỏi chiến lược sống còn:
                    <em> &ldquo;Doanh nghiệp nên can thiệp bằng cách nào, với chi phí bao nhiêu, vào thời điểm nào để thu về lợi nhuận ròng thực tế tối đa?&rdquo;</em>
                  </p>
                  <p>
                    Đề tài này tạo ra bước đột phá bằng cách tích hợp đồng thời 4 trụ cột khoa học:
                    <strong className="text-teal-900 font-bold"> Kỹ thuật dữ liệu Point-in-Time </strong> loại bỏ 100% rò rỉ thông tin tương lai,
                    <strong className="text-indigo-900 font-bold"> Phân khúc xác suất vi mô GMM (k*=5) </strong>,
                    <strong className="text-coralRed font-bold"> Suy luận nhân quả Causal ML Uplift &amp; Sống còn Kaplan-Meier </strong>, và
                    <strong className="text-emerald-900 font-bold"> Tối ưu hóa hàm lợi nhuận ròng kinh tế What-If </strong> tìm ngưỡng can thiệp vàng
                    <span className="bg-amber-100 text-amber-900 px-1 py-0.5 rounded font-mono font-bold mx-1"><MathView math="\tau^* = 0.07" /></span>.
                  </p>
                </div>
              </div>

              {/* 1.2 Ba Thẻ Chỉ Số Vĩ Mô Thực Trạng Kinh Doanh (BlueYard Color Rhythm) */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h4 className="font-bold text-midnightNavy text-sm uppercase tracking-wide font-mono">
                    1.2. Ba Thước Đo Thực Trạng Khủng Hoảng Kinh Doanh Toàn Ngành
                  </h4>
                  <span className="text-[11px] font-mono text-slate-600 font-bold bg-white/70 px-2.5 py-0.5 rounded border border-slate-300">
                    Macro Landscape
                  </span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
                  {/* Card 1: Apricot Wash */}
                  <div className="p-6 bg-[#ffcf9e]/20 border border-[#ffcf9e] rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
                    <span className="text-[11px] font-mono uppercase text-[#3a3a3e] font-bold tracking-wider block">
                      Tỷ Lệ Bỏ Giỏ Toàn Cầu
                    </span>
                    <div className="text-3xl md:text-4xl font-extrabold text-coralRed mt-2 mb-1">
                      70.19%
                    </div>
                    <p className="text-xs text-[#3a3a3e] leading-relaxed font-medium">
                      Tổng hợp từ 49 nghiên cứu độc lập của Viện nghiên cứu Baymard (2024). Hơn 7 trên 10 khách hàng rời bỏ phiên mua sắm sau khi đã chọn sản phẩm vào giỏ hàng, làm thất thoát hơn 18 tỷ USD doanh thu toàn ngành thương mại điện tử mỗi năm.
                    </p>
                  </div>

                  {/* Card 2: Iris Mist */}
                  <div className="p-6 bg-[#babfff]/20 border border-[#babfff] rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
                    <span className="text-[11px] font-mono uppercase text-[#3a3a3e] font-bold tracking-wider block">
                      Gia Tăng Chi Phí CAC
                    </span>
                    <div className="text-3xl md:text-4xl font-extrabold text-indigo-950 mt-2 mb-1">
                      +222%
                    </div>
                    <p className="text-xs text-[#3a3a3e] leading-relaxed font-medium">
                      Chi phí thu hút một khách hàng mới (CAC) đã bùng nổ tăng hơn 200% trong 8 năm gần đây do chính sách Apple ATT và sự xóa bỏ cookie bên thứ ba. Thu hút khách mới ngày càng đắt đỏ, biến việc cứu vãn giỏ hàng thành ưu tiên hàng đầu.
                    </p>
                  </div>

                  {/* Card 3: Deep Carbon Frame */}
                  <div className="p-6 bg-white/80 border border-[#3a3a3e]/30 rounded-xl transition-all duration-300 hover:-translate-y-1 hover:shadow-md">
                    <span className="text-[11px] font-mono uppercase text-[#3a3a3e] font-bold tracking-wider block">
                      Quy Mô Dữ Liệu Thực Nghiệm
                    </span>
                    <div className="text-3xl md:text-4xl font-extrabold text-teal-950 mt-2 mb-1">
                      200,000 N
                    </div>
                    <p className="text-xs text-[#3a3a3e] leading-relaxed font-medium">
                      Tập dữ liệu độc lập gồm 200.000 khách hàng, 997.000 phiên duyệt web và 249.000 lượt thêm giỏ hàng. Được kiểm toán tự động qua DuckDB với 63 biến đặc trưng Point-in-Time, tuyệt đối không rò rỉ dữ liệu tương lai.
                    </p>
                  </div>
                </div>
              </div>

              {/* 1.3 Bốn Lỗ Hổng Lý Thuyết & Nghịch Lý Thực Tiễn */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <AlertTriangle className="w-5 h-5 text-amber-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    1.3. Bốn Nghịch Lý Thực Tiễn &amp; Khoảng Trống Nghiên Cứu Trong Thương Mại Điện Tử
                  </h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm transition-all duration-300 hover:-translate-y-0.5">
                    <div className="flex items-center gap-2 text-rose-800 font-bold mb-1.5">
                      <span className="w-2 h-2 rounded-full bg-rose-600" />
                      Lỗ hổng 1: Ảo ảnh sai lệch rò rỉ thời gian (Data Leakage Illusion)
                    </div>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Phần lớn các nghiên cứu hiện tại vô tình sử dụng các biến số xảy ra sau khi khách hàng đã thêm giỏ hàng (ví dụ: số lần click vào nút thanh toán, tổng thời gian duyệt web trọn vẹn của phiên) để dự báo việc bỏ giỏ. Điều này tạo ra điểm số ROC-AUC cao ảo (0.95 - 0.98) trong phòng thí nghiệm, nhưng sụp đổ hoàn toàn khi ứng dụng thực tế.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm transition-all duration-300 hover:-translate-y-0.5">
                    <div className="flex items-center gap-2 text-amber-800 font-bold mb-1.5">
                      <span className="w-2 h-2 rounded-full bg-amber-600" />
                      Lỗ hổng 2: Bẫy trợ giá đại trà làm xói mòn lợi nhuận (Indiscriminate Discounting)
                    </div>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Các sàn thương mại thường thiết lập kịch bản gửi email voucher giảm giá đồng loạt cho mọi khách hàng bỏ quên giỏ. Hành động này gây lãng phí nghiêm trọng ngân sách tiếp thị cho nhóm khách hàng tự hoàn tất đơn (<em>Sure Things</em> - chiếm 3.6% dân số) và vô tình hình thành thói quen cố tình bỏ giỏ để chờ nhận voucher giảm giá.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm transition-all duration-300 hover:-translate-y-0.5">
                    <div className="flex items-center gap-2 text-indigo-800 font-bold mb-1.5">
                      <span className="w-2 h-2 rounded-full bg-indigo-600" />
                      Lỗ hổng 3: Bẫy ngưỡng phân loại kỹ thuật 0.50 phi kinh tế (Technical Metric Trap)
                    </div>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Các thuật toán học máy tiêu chuẩn tối ưu hóa theo độ đo kỹ thuật đối xứng (như Accuracy, F1-Score tại ngưỡng cắt mặc định &tau; = 0.50). Trong kinh doanh thực tế, chi phí bỏ lỡ một đơn hàng thành công (False Negative) đắt hơn gấp hàng chục lần so với chi phí gửi một thông báo đẩy (False Positive). Việc sử dụng ngưỡng 0.50 làm bốc hơi +$41,200 lợi nhuận ròng.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm transition-all duration-300 hover:-translate-y-0.5">
                    <div className="flex items-center gap-2 text-teal-800 font-bold mb-1.5">
                      <span className="w-2 h-2 rounded-full bg-teal-600" />
                      Lỗ hổng 4: Rào cản ma sát cước phí ẩn tại bước thanh toán (Shipping Friction)
                    </div>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Kiểm định thống kê Mann-Whitney U ($p = 7.04 \times 10^{-8}$) và mô hình CoxPH chứng minh cước phí vận chuyển phát sinh bất ngờ tại bước cuối (đặc biệt giao hàng qua đêm <code>Overnight</code> với tỷ lệ bỏ giỏ lên tới 82.4%) là rào cản tâm lý số một, đòi hỏi chiến lược miễn phí vận chuyển động thông minh thay vì giảm giá hàng hóa trực tiếp.
                    </p>
                  </div>
                </div>
              </div>

              {/* 1.4 Khung Kiến Trúc Giải Pháp 4 Tầng Toàn Diện Của Đề Tài */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Layers className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    1.4. Khung Kiến Trúc Giải Pháp 4 Tầng Toàn Diện Của Đề Tài
                  </h3>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-mono">
                  <div className="p-4 rounded-xl bg-teal-50/70 border border-teal-200 space-y-2">
                    <span className="text-[10px] uppercase font-bold text-teal-900 block font-mono">Tầng 1 · Data Layer</span>
                    <strong className="text-sm font-bold text-midnightNavy block font-sans">Point-in-Time DuckDB</strong>
                    <p className="text-[11px] text-slate-800 font-sans leading-relaxed">
                      Thiết lập kho đặc trưng 63 chiều không rò rỉ dữ liệu, xử lý phục hồi dữ liệu tự động (Data Healing) trên 997,000 phiên.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-indigo-50/70 border border-indigo-200 space-y-2">
                    <span className="text-[10px] uppercase font-bold text-indigo-900 block font-mono">Tầng 2 · Segmentation</span>
                    <strong className="text-sm font-bold text-midnightNavy block font-sans">GMM k*=5 Micro-Clusters</strong>
                    <p className="text-[11px] text-slate-800 font-sans leading-relaxed">
                      Phân cụm xác suất hỗn hợp Gauss trên không gian RFM-Engagement, nhận diện Cụm 2 Cart Hesitators (25.04% dân số).
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-rose-50/70 border border-rose-200 space-y-2">
                    <span className="text-[10px] uppercase font-bold text-rose-900 block font-mono">Tầng 3 · Causal &amp; Survival</span>
                    <strong className="text-sm font-bold text-midnightNavy block font-sans">Kaplan-Meier &amp; Uplift</strong>
                    <p className="text-[11px] text-slate-800 font-sans leading-relaxed">
                      Đo lường chu kỳ bán rã giỏ hàng t* &le; 7 ngày, bóc tách 4 nhóm tiếp thị bằng thuật toán T-Learner nhắm chọn Persuadables.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200 space-y-2">
                    <span className="text-[10px] uppercase font-bold text-emerald-900 block font-mono">Tầng 4 · Decision Cockpit</span>
                    <strong className="text-sm font-bold text-midnightNavy block font-sans">What-If &tau;* = 0.07</strong>
                    <p className="text-[11px] text-slate-800 font-sans leading-relaxed">
                      Tối ưu hóa kinh tế thực nghiệm tìm cực trị lợi nhuận ròng, thu hồi +$41,200 và cắt giảm 60% chi phí tiếp cận CAC.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* ========================================================
              PHẦN 2: MỤC TIÊU PHÂN TÍCH VÀ CÂU HỎI PHÂN TÍCH
          ======================================================== */}
          {activeTab === 1 && (
            <div className="space-y-8 animate-fadeIn">
              <div className="border-b border-slate-200/60 pb-5">
                <div className="flex items-center gap-2 text-teal-800 text-xs font-mono font-bold uppercase tracking-wider mb-1">
                  <GitBranch className="w-4 h-4 spring-icon text-teal-700" /> Khung Phương Pháp Khoa Học
                </div>
                <h1 className="text-2xl md:text-3xl font-extrabold text-midnightNavy tracking-tight">
                  PHẦN 2: MỤC TIÊU PHÂN TÍCH VÀ CÂU HỎI PHÂN TÍCH
                </h1>
                <p className="text-slate-950 font-bold text-xs sm:text-sm mt-2 max-w-4xl leading-relaxed">
                  Mục tiêu phân tích tổng quát và 4 mục tiêu cụ thể, hệ thống 5 câu hỏi nghiên cứu cốt lõi (RQ1–RQ5), 4 giả thuyết khoa học (H1–H4), cơ sở toán học chuẩn mực và khối kiến trúc Point-in-Time.
                </p>
              </div>

              {/* 2.1 MỤC TIÊU PHÂN TÍCH TỔNG QUÁT VÀ CỤ THỂ */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-3">
                  <Award className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">2.1. Mục Tiêu Phân Tích Tổng Quát &amp; Bốn Mục Tiêu Cụ Thể</h3>
                </div>
                <p className="text-xs sm:text-sm text-slate-900 leading-relaxed mb-4 font-medium">
                  <strong>Mục tiêu tổng quát:</strong> Thiết lập một khung phân tích hỗ trợ ra quyết định kinh tế toàn diện (Prescriptive Decision Intelligence Framework), kết hợp giữa khoa học dữ liệu lớn, mô hình hóa hành vi khách hàng và suy luận nhân quả nhằm giải quyết triệt để điểm nghẽn từ bỏ giỏ hàng trong thương mại điện tử. Hệ thống hướng đến việc chuyển hóa trực tiếp xác suất dự báo thành các hành động can thiệp có khả năng tối đa hóa lợi nhuận ròng thực tế.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <strong className="text-teal-900 text-sm block mb-1 font-bold">Mục tiêu 1: Kỹ thuật dữ liệu &amp; Chống rò rỉ Point-in-Time</strong>
                    Xây dựng quy trình tự động phục hồi dữ liệu (Data Healing) qua DuckDB xử lý 997.299 phiên và 249.377 giao dịch, thiết kế kho đặc trưng PIT 63 biến bảo toàn thời gian tại mốc t₀ = 2024-06-01, triệt tiêu 100% hiện tượng Look-ahead Bias.
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <strong className="text-indigo-900 text-sm block mb-1 font-bold">Mục tiêu 2: Phân tích hành vi vi mô &amp; Phân cụm GMM</strong>
                    Định lượng và kiểm định thống kê các yếu tố ma sát giao dịch (cước hỏa tốc, chỉ số đắn đo), phân khúc khách hàng theo không gian xác suất đa chiều RFM-Engagement-Cart qua mô hình GMM k*=5 thay thế K-Means đẳng hướng.
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <strong className="text-amber-900 text-sm block mb-1 font-bold">Mục tiêu 3: Dự báo Gradient Boosting &amp; Hiệu chuẩn Platt</strong>
                    Huấn luyện và đối chuẩn 8 mô hình học máy trên dữ liệu mất cân bằng; tối ưu hóa siêu tham số Optuna 35 trials; ứng dụng hiệu chuẩn Platt Sigmoid nén sai số hiệu chuẩn kỳ vọng ECE xuống 0.0035 trước khi đưa vào hàm mục tiêu tài chính.
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <strong className="text-emerald-900 text-sm block mb-1 font-bold">Mục tiêu 4: Tối ưu hóa lợi nhuận ròng &amp; Suy luận nhân quả</strong>
                    Bóc tách tác động gia tăng thuần qua Uplift T-Learner (CATE), thiết lập phương trình hàm lợi nhuận kinh tế kỳ vọng tìm ngưỡng tối ưu &tau;* = 0.07 mang lại $115,918 lợi nhuận ròng và tiết kiệm 60% CAC qua xếp hạng 10-Decile Lift@K.
                  </div>
                </div>
              </div>

              {/* 2.2 HỆ THỐNG 5 CÂU HỎI PHÂN TÍCH (RQ1 - RQ5) */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <HelpCircle className="w-5 h-5 text-indigo-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">2.2. Hệ Thống Năm Câu Hỏi Phân Tích Định Lượng (RQ1 &rarr; RQ5)</h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-mono font-bold">RQ1</span>
                        <span className="text-[11px] font-mono text-slate-600 font-semibold">Shipping Friction</span>
                      </div>
                      <h4 className="font-bold text-sm text-midnightNavy mb-1.5">Rào cản chi phí vận chuyển</h4>
                      <p className="text-slate-800 leading-relaxed font-medium">
                        Phương thức vận chuyển hỏa tốc (<code>pct_overnight_shipping</code>) và chỉ số đắn đo giỏ hàng (<code>hesitation_index</code>) có tác động tiêu cực có ý nghĩa thống kê đến quyết định hoàn tất thanh toán hay không?
                      </p>
                    </div>
                    <div className="mt-3 pt-2 border-t border-slate-200 text-[11px] text-teal-900 font-bold">
                      Cơ sở: Định lượng lực cản vi mô tại bước Checkout
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="px-2 py-0.5 rounded bg-teal-100 text-teal-800 font-mono font-bold">RQ2</span>
                        <span className="text-[11px] font-mono text-slate-600 font-semibold">Recency Decay &amp; GMM</span>
                      </div>
                      <h4 className="font-bold text-sm text-midnightNavy mb-1.5">Quy luật phân rã &amp; Phân cụm GMM</h4>
                      <p className="text-slate-800 leading-relaxed font-medium">
                        Tốc độ thao tác giỏ hàng (<code>cart_velocity</code>) suy giảm theo quy luật nào theo thời gian trôi qua kể từ phiên cuối, và mô hình GMM k*=5 có phân lập chân dung khách hàng vượt trội hơn K-Means hay không?
                      </p>
                    </div>
                    <div className="mt-3 pt-2 border-t border-slate-200 text-[11px] text-teal-900 font-bold">
                      Cơ sở: Mô hình hóa cụm elip và kiểm định Kruskal-Wallis
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="px-2 py-0.5 rounded bg-indigo-100 text-indigo-800 font-mono font-bold">RQ3</span>
                        <span className="text-[11px] font-mono text-slate-600 font-semibold">Gradient Boosting PR-AUC</span>
                      </div>
                      <h4 className="font-bold text-sm text-midnightNavy mb-1.5">Năng lực phân định Gradient Boosting</h4>
                      <p className="text-slate-800 leading-relaxed font-medium">
                        Thuật toán nào trong số các mô hình Gradient Boosting (LightGBM, CatBoost, XGBoost) và Stacking Ensemble đạt diện tích PR-AUC cao nhất khi được tối ưu hóa siêu tham số tự động qua Optuna?
                      </p>
                    </div>
                    <div className="mt-3 pt-2 border-t border-slate-200 text-[11px] text-teal-900 font-bold">
                      Cơ sở: Đo lường chính xác trên tập mất cân bằng (20.30%)
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-mono font-bold">RQ4</span>
                        <span className="text-[11px] font-mono text-slate-600 font-semibold">Probability Calibration</span>
                      </div>
                      <h4 className="font-bold text-sm text-midnightNavy mb-1.5">Hiệu chuẩn Platt Sigmoid</h4>
                      <p className="text-slate-800 leading-relaxed font-medium">
                        Kỹ thuật hiệu chuẩn Platt Sigmoid cải thiện sai số hiệu chuẩn kỳ vọng (ECE) và Brier Score của mô hình phân loại dạng cây như thế nào trước khi đưa vào hàm mục tiêu tài chính?
                      </p>
                    </div>
                    <div className="mt-3 pt-2 border-t border-slate-200 text-[11px] text-teal-900 font-bold">
                      Cơ sở: Đưa đầu ra về sát tần suất chuyển đổi khách quan
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between md:col-span-2 lg:col-span-2">
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-mono font-bold">RQ5</span>
                        <span className="text-[11px] font-mono text-slate-600 font-semibold">Economic Optimization &amp; Uplift</span>
                      </div>
                      <h4 className="font-bold text-sm text-midnightNavy mb-1.5">Tối ưu hóa lợi nhuận ròng &amp; Suy luận nhân quả Uplift</h4>
                      <p className="text-slate-800 leading-relaxed font-medium">
                        Việc dịch chuyển từ ngưỡng phân loại mặc định (&tau; = 0.50) sang ngưỡng tối ưu hóa hàm lợi nhuận kinh tế kỳ vọng (&tau;* = 0.07) kết hợp khung phân tách can thiệp Uplift CATE mang lại mức gia tăng lợi nhuận ròng là bao nhiêu trên tập kiểm thử độc lập?
                      </p>
                    </div>
                    <div className="mt-3 pt-2 border-t border-slate-200 text-[11px] text-emerald-800 font-bold">
                      Cơ sở: Chuyển dịch từ phân loại học máy sang lý thuyết quyết định kinh tế
                    </div>
                  </div>
                </div>
              </div>

              {/* 2.3 HỆ THỐNG 4 GIẢ THUYẾT THỐNG KÊ KHOA HỌC (H1 - H4) */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <CheckCircle2 className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">2.3. Hệ Thống Bốn Giả Thuyết Thống Kê Khoa Học (H1 &rarr; H4)</h3>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-sans">
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-mono font-bold">Giả thuyết H1</span>
                      <span className="font-mono text-[10px] text-slate-600">Mann-Whitney U</span>
                    </div>
                    <h5 className="font-bold text-sm text-midnightNavy mb-1">Rào cản cước vận chuyển hỏa tốc</h5>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Tỷ lệ lựa chọn phương thức vận chuyển hỏa tốc (<code>pct_overnight_shipping</code>) ở nhóm từ bỏ giỏ hàng (y=0) cao hơn có ý nghĩa thống kê so với nhóm chuyển đổi thành công (y=1).
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-mono font-bold">Giả thuyết H2</span>
                      <span className="font-mono text-[10px] text-slate-600">Kruskal-Wallis H</span>
                    </div>
                    <h5 className="font-bold text-sm text-midnightNavy mb-1">Quy luật bán rã tương tác giỏ hàng</h5>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Tốc độ tương tác giỏ hàng (<code>cart_velocity</code>) suy giảm đơn điệu theo số ngày trôi qua kể từ phiên tương tác gần nhất (<code>days_since_last_session</code>) qua 4 khoảng trễ thời gian.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="px-2 py-0.5 rounded bg-indigo-100 text-indigo-800 font-mono font-bold">Giả thuyết H3</span>
                      <span className="font-mono text-[10px] text-slate-600">Kruskal-Wallis H</span>
                    </div>
                    <h5 className="font-bold text-sm text-midnightNavy mb-1">Tính đồng nhất trong sử dụng voucher theo hạng</h5>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Tỷ lệ sử dụng voucher ưu đãi (<code>trans_discount_usage_rate</code>) không có sự khác biệt có ý nghĩa thống kê giữa 4 phân hạng thành viên (Bronze, Silver, Gold, Platinum).
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="px-2 py-0.5 rounded bg-teal-100 text-teal-800 font-mono font-bold">Giả thuyết H4</span>
                      <span className="font-mono text-[10px] text-slate-600">GMM &amp; BIC</span>
                    </div>
                    <h5 className="font-bold text-sm text-midnightNavy mb-1">Cấu trúc 5 cụm tự nhiên tối ưu</h5>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Mô hình phân khúc hỗn hợp Gaussian (GMM) xác định số lượng cụm tự nhiên tối ưu là k*=5 theo tiêu chuẩn thông tin Bayes (BIC) trên không gian RFM-Engagement.
                    </p>
                  </div>
                </div>
              </div>

              {/* 2.4 CƠ SỞ TOÁN HỌC ĐỊNH LƯỢNG - ĐỊNH DẠNG CHUẨN */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Percent className="w-5 h-5 text-indigo-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">2.4. Cơ Sở Toán Học &amp; Các Phương Trình Định Lượng Chuẩn</h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-sans">
                  {/* D'Agostino-Pearson K^2 */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-center mb-1.5">
                        <strong className="text-midnightNavy font-bold">1. Kiểm định tính chuẩn D&apos;Agostino-Pearson (K²)</strong>
                        <span className="font-mono text-[10px] text-slate-600 font-semibold">H₀: Phân phối chuẩn</span>
                      </div>
                      <div className="p-3 my-2 rounded-lg bg-slate-900 text-teal-300 text-center shadow-inner overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden flex justify-center items-center min-h-[56px]">
                        <MathView math="K^2 = [Z_1(s)]^2 + [Z_2(k)]^2 \sim \chi^2(2)" block />
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-800 leading-relaxed font-medium">
                      Trong đó <MathView math="s" /> là độ xiên (skewness), <MathView math="k" /> là độ nhọn (kurtosis), <MathView math="Z_1" /> và <MathView math="Z_2" /> là các phép biến đổi chuẩn hóa về <MathView math="\mathcal{N}(0, 1)" />. Bác bỏ <MathView math="H_0" /> khẳng định phân phối giỏ hàng lệch phải nghiêm trọng.
                    </p>
                  </div>

                  {/* Mann-Whitney U */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-center mb-1.5">
                        <strong className="text-midnightNavy font-bold">2. Kiểm định phi tham số Mann-Whitney U</strong>
                        <span className="font-mono text-[10px] text-slate-600 font-semibold">H₁: Cước Overnight</span>
                      </div>
                      <div className="p-3 my-2 rounded-lg bg-slate-900 text-teal-300 text-center shadow-inner overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden flex justify-center items-center min-h-[56px]">
                        <MathView math="U = n_1 n_2 + \frac{n_1(n_1 + 1)}{2} - R_1" block />
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-800 leading-relaxed font-medium">
                      <MathView math="n_1, n_2" /> là quy mô mẫu của nhóm từ bỏ giỏ (<MathView math="y=0" />) và nhóm mua (<MathView math="y=1" />); <MathView math="R_1" /> là tổng hạng nhóm 1. Hệ số tương quan Rank-Biserial: <MathView math="r_{\text{rb}} = 1 - \frac{2U}{n_1 n_2}" />.
                    </p>
                  </div>

                  {/* Kruskal-Wallis H */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-center mb-1.5">
                        <strong className="text-midnightNavy font-bold">3. Kiểm định nhiều nhóm Kruskal-Wallis H</strong>
                        <span className="font-mono text-[10px] text-slate-600 font-semibold">H₂: Phân rã giỏ hàng</span>
                      </div>
                      <div className="p-3 my-2 rounded-lg bg-slate-900 text-teal-300 text-center shadow-inner overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden flex justify-center items-center min-h-[56px]">
                        <MathView math="H = \frac{12}{N(N+1)} \sum_{j=1}^k \frac{R_j^2}{n_j} - 3(N + 1) \sim \chi^2(k - 1)" block />
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-800 leading-relaxed font-medium">
                      <MathView math="N" /> là tổng số quan sát, <MathView math="k" /> là số nhóm so sánh (<MathView math="k = 4" /> khoảng thời gian trễ), <MathView math="R_j" /> là tổng hạng phân nhóm <MathView math="j" />. Hiệu chỉnh Bonferroni: <MathView math="p_{\text{adj}} = \min(1, p \cdot m)" />.
                    </p>
                  </div>

                  {/* GMM & BIC */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-center mb-1.5">
                        <strong className="text-midnightNavy font-bold">4. Mô hình hỗn hợp Gauss &amp; Tiêu chuẩn BIC</strong>
                        <span className="font-mono text-[10px] text-slate-600 font-semibold">H₄: Phân cụm k*=5</span>
                      </div>
                      <div className="p-3 my-2 rounded-lg bg-slate-900 text-teal-300 text-center shadow-inner overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden flex justify-center items-center min-h-[56px]">
                        <MathView math="\text{BIC} = k \ln(n) - 2 \ln(\hat{L})" block />
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-800 leading-relaxed font-medium">
                      Hàm mật độ hỗn hợp Gauss: <MathView math="p(x) = \sum_{k=1}^K \pi_k \mathcal{N}(x \mid \mu_k, \Sigma_k)" />. Điểm BIC đạt cực tiểu 2.143.890 tại <MathView math="k^*=5" /> với cấu trúc ma trận hiệp phương sai đầy đủ (full covariance).
                    </p>
                  </div>

                  {/* Platt Sigmoid */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-center mb-1.5">
                        <strong className="text-midnightNavy font-bold">5. Hiệu chuẩn xác suất Platt Sigmoid</strong>
                        <span className="font-mono text-[10px] text-slate-600 font-semibold">Tối ưu ECE &amp; Brier</span>
                      </div>
                      <div className="p-3 my-2 rounded-lg bg-slate-900 text-teal-300 text-center shadow-inner overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden flex justify-center items-center min-h-[56px]">
                        <MathView math="P(y = 1 \mid f) = \frac{1}{1 + \exp(A \cdot f + B)}" block />
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-800 leading-relaxed font-medium">
                      <MathView math="f" /> là điểm logit dự báo thô; các tham số <MathView math="A, B" /> được tối ưu bằng Maximum Likelihood qua 5-Fold CV, đưa sai số hiệu chuẩn ECE từ 0.0142 xuống 0.0035 với độ trễ suy luận 0.012 ms/khách.
                    </p>
                  </div>

                  {/* Kaplan-Meier & CoxPH */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-center mb-1.5">
                        <strong className="text-midnightNavy font-bold">6. Động học sống còn Kaplan-Meier &amp; CoxPH</strong>
                        <span className="font-mono text-[10px] text-slate-600 font-semibold">Bán rã t* &le; 7 ngày</span>
                      </div>
                      <div className="p-3 my-2 rounded-lg bg-slate-900 text-teal-300 text-center shadow-inner overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden flex justify-center items-center min-h-[56px]">
                        <MathView math="\hat{S}(t) = \prod_{t_i \le t} \left(1 - \frac{d_i}{n_i}\right) \quad \text{và} \quad h(t \mid X) = h_0(t)\exp(\beta^T X)" block />
                      </div>
                    </div>
                    <p className="text-[11px] text-slate-800 leading-relaxed font-medium">
                      <MathView math="d_i" /> là số ca từ bỏ tại mốc <MathView math="t_i" />, <MathView math="n_i" /> là số khách hàng có nguy cơ. Xác định chu kỳ bán rã ý định mua là <MathView math="t^* \le 7" /> ngày (sau 7 ngày xác suất phục hồi giảm dưới 17.8%).
                    </p>
                  </div>

                  {/* Expected Net Profit Equation */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm md:col-span-2">
                    <div className="flex justify-between items-center mb-1.5">
                      <strong className="text-midnightNavy font-bold">7. Hàm mục tiêu tối ưu hóa Lợi nhuận ròng kỳ vọng &amp; Uplift CATE</strong>
                      <span className="font-mono text-[10px] text-emerald-800 font-bold">Cực đại tại &tau;* = 0.07</span>
                    </div>
                    <div className="p-3.5 my-2 rounded-lg bg-slate-900 text-emerald-400 text-center shadow-inner overflow-x-auto [scrollbar-width:none] [&::-webkit-scrollbar]:hidden flex justify-center items-center min-h-[56px]">
                      <MathView math="\mathbb{E}[\Pi(\tau)] = \sum_{i: \hat{p}_i \ge \tau} \left[ y_i \cdot (\text{Margin}_i - C_{\text{voucher}}) - C_{\text{contact}} \right]" block />
                    </div>
                    <p className="text-[11px] text-slate-800 leading-relaxed font-medium">
                      Trong đó <MathView math="\mathbb{I}(\hat{p}_i \ge \tau)" /> là hàm chỉ báo can thiệp; <MathView math="y_i \in \{0, 1\}" /> là nhãn mua hàng thực tế; <MathView math="\text{Margin}_i = 25\% \times \text{AOV}_i" />; <MathView math="C_{\text{voucher}} = \$5.0" />; <MathView math="C_{\text{contact}} = \$0.8" />. Điểm số tác động gia tăng thuần Uplift CATE: <MathView math="\hat{\tau}(X_i) = \hat{\mu}_1(X_i) - \hat{\mu}_0(X_i)" />.
                    </p>
                  </div>
                </div>
              </div>

              {/* 2.5 KHỐI TENSOR 3D POINT-IN-TIME PIPELINE */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-midnightNavy text-base flex items-center gap-2">
                    <Box className="w-5 h-5 text-indigo-600 spring-icon" />
                    2.5. Khối Tensor Dữ Liệu 3D Point-in-Time &amp; Bức Tường Thời Gian Chống Rò Rỉ
                  </h3>
                  <span className="text-xs text-slate-600 font-mono font-semibold">Tương tác trực tiếp WebGL 3D</span>
                </div>
                <ThreeDataPipelineCube />
              </div>
            </div>
          )}

          {/* ========================================================
              PHẦN 3: DỮ LIỆU, PHÂN TÍCH THĂM DÒ & 5 CỤM GMM
          ======================================================== */}
          {activeTab === 2 && (
            <div className="space-y-8 animate-fadeIn">
              <div className="border-b border-slate-200/60 pb-5">
                <div className="flex items-center gap-2 text-teal-800 text-xs font-mono font-bold uppercase tracking-wider mb-1">
                  <Layers className="w-4 h-4 spring-icon text-teal-700" /> Kỹ Thuật Dữ Liệu & Phân Cụm Vi Mô
                </div>
                <h1 className="text-2xl md:text-3xl font-extrabold text-midnightNavy tracking-tight">
                  PHẦN 3: QUY TRÌNH XỬ LÝ DỮ LIỆU VÀ PHÂN TÍCH KHÁM PHÁ DỮ LIỆU
                </h1>
                <p className="text-slate-950 font-bold text-xs sm:text-sm mt-2 max-w-4xl leading-relaxed">
                  Báo cáo kết quả kiểm toán phục hồi dữ liệu tự động Data Healing qua DuckDB, thiết kế kho đặc trưng Point-in-Time 63 biến và mô hình phân khúc xác suất vi mô GMM k*=5.
                </p>
              </div>

              {/* 3.1 KIỂM TOÁN DỮ LIỆU & QUY TRÌNH DATA HEALING TRÊN DUCKDB */}
              <div className="sub-reading-card p-6 border-l-4 border-l-teal-600">
                <div className="flex items-center gap-2 mb-3">
                  <Database className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    3.1. Kiểm Toán Dữ Liệu Lớn &amp; Phục Hồi Dữ Liệu Tự Động (Data Healing trên DuckDB)
                  </h3>
                </div>
                <div className="space-y-3 text-xs sm:text-sm text-slate-800 leading-relaxed font-medium">
                  <p>
                    Tập dữ liệu thô ban đầu bao gồm <strong>200.000 khách hàng</strong>, <strong>3.292.053 phiên duyệt web</strong> và <strong>821.571 giao dịch mua sắm</strong>. Quá trình kiểm toán chất lượng dữ liệu phát hiện hai sai phạm có hệ thống nghiêm trọng:
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-2 text-xs">
                    <div className="p-3.5 rounded-xl bg-rose-50/80 border border-rose-200">
                      <strong className="text-rose-900 block mb-1 font-bold">1. Sai phạm nghịch đảo thời gian (30.30% phiên, 30.35% giao dịch):</strong>
                      Có tới <strong>997.299 phiên truy cập</strong> và <strong>249.377 giao dịch</strong> có dấu thời gian diễn ra <em>TRƯỚC</em> ngày khách hàng đăng ký tài khoản (<code>session_start_time &lt; registration_date</code> hoặc <code>transaction_date &lt; registration_date</code>). Đây là hiện tượng lỗi đồng bộ khóa ngoại và logic ghi nhận sự kiện của hệ sinh thái dữ liệu phân tán.
                    </div>
                    <div className="p-3.5 rounded-xl bg-amber-50/80 border border-amber-200">
                      <strong className="text-amber-900 block mb-1 font-bold">2. Bất thường độ tuổi sinh học (10.000 bản ghi):</strong>
                      Khoảng 10.000 bản ghi chứa độ tuổi âm hoặc vượt chuẩn sinh học (<code>age &lt; 18</code> hoặc <code>age &gt; 100</code>), tiềm ẩn nguy cơ làm sai lệch các phép chuẩn hóa khoảng cách trong mô hình phân cụm.
                    </div>
                  </div>
                  <p>
                    <strong>Quy trình Data Healing:</strong> Hệ thống áp dụng động cơ phân tích trong bộ nhớ <strong>DuckDB</strong>, loại bỏ toàn bộ các phiên và giao dịch tiền đăng ký bất hợp lệ, đồng thời chuẩn hóa độ tuổi (imputation về median 38 tuổi). Toàn bộ quy trình xử lý dữ liệu lớn hoàn tất chỉ trong <strong>5.47 giây</strong>. Bộ kiểm thử tự động <code>tests/test_pit_integrity.py</code> đạt trạng thái hoàn hảo <strong>100% (3/3 passed)</strong>, bảo đảm tính duy nhất của khóa chính, cách ly hoàn toàn biến mục tiêu và cô lập 100% ranh giới Point-in-Time trước mốc <code className="bg-slate-100 text-slate-800 px-1 py-0.5 rounded font-mono font-bold">t₀ = 2024-06-01 00:00:00</code>.
                  </p>
                </div>
              </div>

              {/* 3.2 DANH MỤC PHÂN NHÓM KHO ĐẶC TRƯNG PIT (63 BIẾN) */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-3">
                  <Box className="w-5 h-5 text-indigo-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    3.2. Danh Mục Phân Nhóm Kho Đặc Trưng Bất Biến Thời Gian (PIT Feature Store - 63 Biến)
                  </h3>
                </div>
                <p className="text-xs text-slate-700 mb-3 font-medium">
                  Từ tập dữ liệu đã phục hồi, hệ thống trích xuất tổng cộng 63 đặc trưng đa chiều, chuẩn hóa thành 5 nhóm cấu trúc độc lập trên tệp <code>customer_features_pit.parquet</code> (160.000 mẫu huấn luyện với 32.486 khách hàng chuyển đổi y=1, tỷ lệ chuyển đổi tự nhiên đạt đúng <strong>20.30%</strong>):
                </p>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-700 font-mono uppercase bg-slate-50/80 font-bold">
                        <th className="py-2.5 px-3">Nhóm đặc trưng</th>
                        <th className="py-2.5 px-3">Số lượng biến</th>
                        <th className="py-2.5 px-3">Các biến số tiêu biểu</th>
                        <th className="py-2.5 px-3">Ý nghĩa kinh tế và hành vi</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-slate-800 text-[11px]">
                      <tr>
                        <td className="py-2.5 px-3 font-bold text-midnightNavy">Nhân khẩu học &amp; Tài khoản</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-teal-800">8</td>
                        <td className="py-2.5 px-3 font-mono">age, account_age_days, customer_tier_code, loyalty_score, credit_limit</td>
                        <td className="py-2.5 px-3">Đo lường năng lực tài chính, độ gắn kết thương hiệu và phân hạng thành viên.</td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-bold text-midnightNavy">Tương tác phiên truy cập</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-teal-800">12</td>
                        <td className="py-2.5 px-3 font-mono">total_sessions, total_duration_sec, avg_session_duration, total_pages_viewed, bounce_rate</td>
                        <td className="py-2.5 px-3">Phản ánh mức độ tích cực duyệt web và sự quan tâm tổng thể của khách hàng.</td>
                      </tr>
                      <tr className="bg-rose-50/50">
                        <td className="py-2.5 px-3 font-bold text-coralRed">Rào cản hành vi giỏ hàng (Trọng tâm)</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-coralRed">15</td>
                        <td className="py-2.5 px-3 font-mono">total_cart_additions, cart_to_page_ratio, cart_abandonment_severity, hesitation_index, cart_velocity</td>
                        <td className="py-2.5 px-3">Trọng tâm nghiên cứu: Lượng hóa mức độ đắn đo, tốc độ thao tác và tần suất từ bỏ giỏ hàng.</td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-bold text-midnightNavy">Giao dịch &amp; Giá trị quá khứ</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-teal-800">16</td>
                        <td className="py-2.5 px-3 font-mono">trans_count, total_spend, avg_order_value, trans_discount_usage_rate, days_since_last_purchase</td>
                        <td className="py-2.5 px-3">Tái hiện quy mô chi tiêu quá khứ và mức độ nhạy cảm với các chương trình khuyến mãi.</td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-bold text-midnightNavy">Vận chuyển &amp; Bối cảnh tiếp thị</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-teal-800">12</td>
                        <td className="py-2.5 px-3 font-mono">pct_overnight_shipping, shipping_friction_score, pct_campaign_sessions, urban_ratio</td>
                        <td className="py-2.5 px-3">Lượng hóa ma sát từ cước giao nhận hỏa tốc và tác động từ các chiến dịch quảng bá.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* 3.3 PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA) & BẢNG KIỂM ĐỊNH GIẢ THUYẾT */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-3">
                  <Activity className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    3.3. Phân Tích Khám Phá Dữ Liệu (EDA) &amp; Kết Quả Kiểm Định Giả Thuyết Phi Tham Số
                  </h3>
                </div>
                <div className="mb-4 text-xs text-slate-800 leading-relaxed font-medium">
                  <p>
                    <strong>Kiểm định tính chuẩn D&apos;Agostino-Pearson (K²):</strong> Thực nghiệm trên 160.000 quan sát xác nhận <code>total_cart_additions</code> (<MathView math="K^2 = 480.86, p = 3.82 \times 10^{-105}" />), <code>cart_to_page_ratio</code> (<MathView math="K^2 = 2.194{,}90, p = 0.0" />), <code>cart_abandonment_severity</code> (<MathView math="K^2 = 305.15, p = 5.46 \times 10^{-67}" />), và <code>days_since_last_session</code> (<MathView math="K^2 = 3.201{,}61, p = 0.0" />) đều có p-value &lt; 10⁻⁵⁰. Toàn bộ các biến số giỏ hàng cốt lõi đều tuân theo phân phối lệch phải nghiêm trọng (heavy-tailed), khẳng định việc dùng t-test hoặc ANOVA là sai lầm về phương pháp luận và bắt buộc phải áp dụng kiểm định phi tham số.
                  </p>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-700 font-mono uppercase bg-slate-50/80 font-bold">
                        <th className="py-2.5 px-3">Mã</th>
                        <th className="py-2.5 px-3">Biến số kiểm định</th>
                        <th className="py-2.5 px-3">Phép kiểm định</th>
                        <th className="py-2.5 px-3">Thống kê</th>
                        <th className="py-2.5 px-3">p-value gốc</th>
                        <th className="py-2.5 px-3">p-value Bonferroni</th>
                        <th className="py-2.5 px-3">Effect Size</th>
                        <th className="py-2.5 px-3">Kết luận và ý nghĩa nghiệp vụ</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-slate-800 text-[11px]">
                      <tr className="bg-rose-50/60 font-medium">
                        <td className="py-2.5 px-3 font-mono font-bold text-coralRed">H₁</td>
                        <td className="py-2.5 px-3 font-mono font-bold">pct_overnight_shipping</td>
                        <td className="py-2.5 px-3">Mann-Whitney U (One-sided Greater)</td>
                        <td className="py-2.5 px-3 font-mono">1.957.170.176,0</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-coralRed"><MathView math="7.04 \times 10^{-8}" /></td>
                        <td className="py-2.5 px-3 font-mono font-bold text-coralRed"><MathView math="7.04 \times 10^{-8}" /></td>
                        <td className="py-2.5 px-3 font-mono"><MathView math="r_{\text{rb}} = -0.0157" /></td>
                        <td className="py-2.5 px-3"><strong>Bác bỏ H₀:</strong> Nhóm bỏ giỏ chọn vận chuyển hỏa tốc cao hơn có ý nghĩa thống kê (p &lt; 0.001). Cước vận chuyển cao là rào cản tâm lý hàng đầu.</td>
                      </tr>
                      <tr className="bg-amber-50/60 font-medium">
                        <td className="py-2.5 px-3 font-mono font-bold text-amber-800">H₂</td>
                        <td className="py-2.5 px-3 font-mono font-bold">cart_velocity</td>
                        <td className="py-2.5 px-3">Kruskal-Wallis H (4 khoảng trễ)</td>
                        <td className="py-2.5 px-3 font-mono">1.589,52</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-amber-800">0.0000</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-amber-800">0.0000</td>
                        <td className="py-2.5 px-3 font-mono"><MathView math="\eta^2 = 0.0099" /></td>
                        <td className="py-2.5 px-3"><strong>Bác bỏ H₀:</strong> Tốc độ tương tác giỏ hàng suy giảm đơn điệu theo thời gian trôi qua kể từ phiên cuối (p &lt; 0.001). Ý định mua sắm có quy luật bán rã nhanh chóng.</td>
                      </tr>
                      <tr className="bg-slate-50 font-medium">
                        <td className="py-2.5 px-3 font-mono font-bold text-slate-700">H₃</td>
                        <td className="py-2.5 px-3 font-mono font-bold">trans_discount_usage_rate</td>
                        <td className="py-2.5 px-3">Kruskal-Wallis H (4 phân hạng)</td>
                        <td className="py-2.5 px-3 font-mono">1,43</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-slate-600">0.6996</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-slate-600">0.6996</td>
                        <td className="py-2.5 px-3 font-mono"><MathView math="\eta^2 \approx 0.0000" /></td>
                        <td className="py-2.5 px-3"><strong>Chưa đủ bằng chứng bác bỏ H₀:</strong> Tỷ lệ dùng voucher không có sự khác biệt giữa các hạng hội viên (p &gt; 0.05). Việc phân phát voucher theo hạng thành viên là không hiệu quả.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* 3.4 MÔ HÌNH HÓA PHÂN KHÚC VI MÔ RFM-E BẰNG GMM (k*=5) */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-midnightNavy text-base flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-teal-600 spring-icon" />
                    3.4. Mô Hình Hóa Phân Khúc Vi Mô RFM-E Bằng GMM (k*=5 Tối Ưu Qua Tiêu Chuẩn BIC)
                  </h3>
                  <span className="text-xs text-slate-600 font-mono font-semibold">Tương tác trực tiếp trên WebGL 3D</span>
                </div>
                <ThreeClusterVisual />
              </div>

              {/* Bảng Chi Tiết 5 Chân Dung GMM từ tbl_ch3_gmm_cluster_profiles.csv */}
              <div className="sub-reading-card p-6">
                <h4 className="font-bold text-midnightNavy text-base mb-4 flex items-center gap-2">
                  <Users className="w-5 h-5 text-teal-600 spring-icon" />
                  Hồ Sơ Chân Dung Hành Vi Và Tiềm Năng Kinh Tế 5 Phân Khúc Vi Mô GMM
                </h4>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-900 border-collapse">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-700 font-mono uppercase bg-slate-50/80 font-bold">
                        <th className="py-3 px-3">Cụm</th>
                        <th className="py-3 px-3">Tên chân dung</th>
                        <th className="py-3 px-3">Quy mô mẫu</th>
                        <th className="py-3 px-3">Tỷ trọng</th>
                        <th className="py-3 px-3">AOV (USD)</th>
                        <th className="py-3 px-3">Recency</th>
                        <th className="py-3 px-3">Thêm giỏ</th>
                        <th className="py-3 px-3">Mức bỏ giỏ</th>
                        <th className="py-3 px-3">Tỷ lệ mua</th>
                        <th className="py-3 px-3">Định hướng can thiệp chiến lược</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {GMM_DATA.map((c) => (
                        <tr key={c.id} className={c.id === 2 ? 'bg-rose-50/90 font-bold' : 'hover:bg-white/70 transition-colors'}>
                          <td className="py-3 px-3 font-mono font-bold text-midnightNavy">Cụm {c.id}</td>
                          <td className="py-3 px-3 font-semibold">{c.name}</td>
                          <td className="py-3 px-3 font-mono">{c.count.toLocaleString()}</td>
                          <td className="py-3 px-3 font-mono font-bold">{c.share}</td>
                          <td className="py-3 px-3 font-mono text-emerald-800 font-bold">{c.aov}</td>
                          <td className="py-3 px-3 font-mono">{c.recency}</td>
                          <td className="py-3 px-3 font-mono">{c.addCart}</td>
                          <td className="py-3 px-3 font-mono text-coralRed font-bold">{c.aban}</td>
                          <td className="py-3 px-3 font-mono text-teal-900 font-bold">{c.conv}</td>
                          <td className="py-3 px-3">{c.action}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* TỪNG BIỂU ĐỒ THỰC NGHIỆM ĐƯỢC ĐẶT TRONG THẺ RIÊNG KHỔ RỘNG */}
              <div className="space-y-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="sub-reading-card p-5">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-bold text-midnightNavy text-sm flex items-center gap-2">
                        <Eye className="w-4 h-4 text-teal-600 spring-icon" />
                        Hình 3.1: Phân Phối Nhãn Mục Tiêu (Target Distribution)
                      </h4>
                      <span className="text-[10px] font-mono text-slate-700 bg-white/90 px-2 py-0.5 rounded-full border border-slate-300 font-bold">
                        N = 200,000
                      </span>
                    </div>
                    <p className="text-xs text-slate-800 mb-3 font-medium">Tỷ lệ chuyển đổi tự nhiên đạt 20.30% (32.480 khách) so với 79.70% không mua hàng.</p>
                    <div className="w-full flex items-center justify-center p-3 bg-white/95 rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                      <img
                        src="/figures/fig_ch3_01_target_distribution.png"
                        alt="Phân phối nhãn mục tiêu"
                        className="max-w-full h-auto max-h-[360px] object-contain transition-transform duration-300 hover:scale-[1.02]"
                      />
                    </div>
                  </div>

                  <div className="sub-reading-card p-5">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-bold text-midnightNavy text-sm flex items-center gap-2">
                        <Eye className="w-4 h-4 text-teal-600 spring-icon" />
                        Hình 3.2: Tương Quan Ma Sát Giỏ Hàng vs Tương Tác
                      </h4>
                      <span className="text-[10px] font-mono text-slate-700 bg-white/90 px-2 py-0.5 rounded-full border border-slate-300 font-bold">
                        Scatter Analysis
                      </span>
                    </div>
                    <p className="text-xs text-slate-800 mb-3 font-medium">Chỉ số cart_to_page_ratio tăng đột biến tại các nhóm khách hàng gặp rào cản chi phí thanh toán.</p>
                    <div className="w-full flex items-center justify-center p-3 bg-white/95 rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                      <img
                        src="/figures/fig_ch3_02_cart_engagement_scatter.png"
                        alt="Tương quan ma sát giỏ hàng"
                        className="max-w-full h-auto max-h-[360px] object-contain transition-transform duration-300 hover:scale-[1.02]"
                      />
                    </div>
                  </div>
                </div>

                {/* Hình 3.3: Radar Profiles */}
                <div className="sub-reading-card p-6">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-bold text-midnightNavy text-base flex items-center gap-2">
                      <Eye className="w-5 h-5 text-teal-600 spring-icon" />
                      Hình 3.3: Biểu Đồ Radar Đa Chiều Định Vị 5 Cụm Chân Dung Hành Vi RFM-E
                    </h4>
                    <span className="text-xs font-mono text-teal-800 font-bold bg-teal-50 px-2.5 py-1 rounded-full border border-teal-200">
                      GMM k* = 5
                    </span>
                  </div>
                  <p className="text-xs text-slate-800 mb-4 leading-relaxed font-medium">
                    Trục tọa độ đa chiều chuẩn hóa bao gồm: Recency, Frequency, Monetary, Cart Additions, Abandonment Severity và Velocity. Toàn bộ các đỉnh nhãn và đường biểu diễn đều hiển thị trọn vẹn không bị cắt xén.
                  </p>
                  <div className="w-full flex items-center justify-center p-4 bg-white/95 rounded-2xl border border-slate-200 shadow-inner overflow-hidden">
                    <img
                      src="/figures/fig_ch3_03_gmm_cluster_radar.png"
                      alt="Radar 5 cụm RFM-E"
                      className="max-w-full h-auto max-h-[440px] object-contain transition-transform duration-300 hover:scale-[1.02]"
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* ========================================================
              PHẦN 4: MÔ HÌNH HỌC MÁY, KẾT QUẢ VÀ ĐÁNH GIÁ
          ======================================================== */}
          {activeTab === 3 && (
            <div className="space-y-8 animate-fadeIn">
              <div className="border-b border-slate-200/60 pb-5">
                <div className="flex items-center gap-2 text-teal-800 text-xs font-mono font-bold uppercase tracking-wider mb-1">
                  <Activity className="w-4 h-4 spring-icon text-teal-700" /> Mô Hình Học Máy &amp; Suy Luận Nhân Quả
                </div>
                <h1 className="text-2xl md:text-3xl font-extrabold text-midnightNavy tracking-tight">
                  PHẦN 4: MÔ HÌNH HỌC MÁY, KẾT QUẢ VÀ ĐÁNH GIÁ
                </h1>
                <p className="text-slate-950 font-bold text-xs sm:text-sm mt-2 max-w-4xl leading-relaxed">
                  Đối chuẩn 8 mô hình Gradient Boosting và cổ điển, nghiên cứu bóc tách Ablation Study, hiệu chuẩn xác suất Platt Sigmoid, mô hình hóa động học sống còn Kaplan-Meier/CoxPH và phân tách 4 nhóm tiếp thị qua Uplift T-Learner.
                </p>
              </div>

              {/* 4.1 CHIẾN LƯỢC HUẤN LUYỆN, TỐI ƯU SIÊU THAM SỐ OPTUNA & ĐỐI CHUẨN */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-3">
                  <BarChart3 className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    4.1. Chiến Lược Huấn Luyện, Tối Ưu Hóa Bayes Optuna &amp; Bảng Đối Chuẩn 8 Mô Hình (Holdout Test 32.000 Mẫu)
                  </h3>
                </div>
                <p className="text-xs text-slate-700 mb-3 font-medium">
                  Quá trình tối ưu hóa siêu tham số vận hành trên 128.000 mẫu tập phát triển qua 5 lớp kiểm chứng chéo (5-Fold Stratified CV) với thuật toán TPE của Optuna (35 trials, Early Stopping 7 vòng). Toàn bộ 8 mô hình được đối chuẩn độc lập trên 32.000 khách hàng tập Holdout:
                </p>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs text-slate-900 border-collapse">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-700 font-mono uppercase bg-slate-50/80 font-bold">
                        <th className="py-2.5 px-3">Mô hình</th>
                        <th className="py-2.5 px-3">PR-AUC</th>
                        <th className="py-2.5 px-3">ROC-AUC</th>
                        <th className="py-2.5 px-3">F1-Score*</th>
                        <th className="py-2.5 px-3">Precision*</th>
                        <th className="py-2.5 px-3">Recall*</th>
                        <th className="py-2.5 px-3">Accuracy</th>
                        <th className="py-2.5 px-3">Brier Score</th>
                        <th className="py-2.5 px-3">ECE</th>
                        <th className="py-2.5 px-3">Fit Time</th>
                        <th className="py-2.5 px-3">Độ trễ</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {MODEL_BENCHMARK.map((m, idx) => (
                        <tr key={m.name} className={idx === 2 ? 'bg-teal-50/95 font-bold text-teal-950' : 'hover:bg-white/70 transition-colors'}>
                          <td className="py-2.5 px-3 font-semibold">{m.name}</td>
                          <td className="py-2.5 px-3 font-mono font-bold text-teal-800">{m.pr_auc.toFixed(4)}</td>
                          <td className="py-2.5 px-3 font-mono">{m.roc_auc.toFixed(4)}</td>
                          <td className="py-2.5 px-3 font-mono">{m.f1.toFixed(4)}</td>
                          <td className="py-2.5 px-3 font-mono">{m.prec.toFixed(4)}</td>
                          <td className="py-2.5 px-3 font-mono">{m.rec.toFixed(4)}</td>
                          <td className="py-2.5 px-3 font-mono">{(m.acc * 100).toFixed(1)}%</td>
                          <td className="py-2.5 px-3 font-mono">{m.brier.toFixed(4)}</td>
                          <td className="py-2.5 px-3 font-mono text-emerald-800 font-bold">{m.ece.toFixed(4)}</td>
                          <td className="py-2.5 px-3 font-mono">{m.trainTime}</td>
                          <td className="py-2.5 px-3 font-mono">{m.latency}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="mt-3 text-[11px] text-slate-600 italic">
                  * F1, Precision, Recall ghi nhận tại ngưỡng mặc định <MathView math="\tau = 0.50" />. Vì xác suất sau hiệu chuẩn phản ánh sát tần suất thực tế (~20.30%), hầu hết các giá trị xác suất đều &lt; 0.50, làm các chỉ số này bằng 0 tại ngưỡng mặc định, chứng minh tính phi lý của việc dùng ngưỡng 0.50 và dẫn dắt bắt buộc sang tối ưu hóa ngưỡng kinh tế <MathView math="\tau^* = 0.07" />.
                </div>

                {/* Ablation Study & Multi-Seed Stability Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 text-xs">
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                    <h5 className="font-bold text-midnightNavy mb-2 flex items-center gap-1.5">
                      <Target className="w-4 h-4 text-rose-600" />
                      Nghiên cứu bóc tách thành phần đặc trưng (Ablation Study)
                    </h5>
                    <ul className="space-y-1.5 text-slate-800">
                      <li>• <strong>Đầy đủ 63 đặc trưng:</strong> PR-AUC đạt đỉnh <strong>0.2757</strong>.</li>
                      <li>• <strong>Loại bỏ nhóm Rào cản giỏ hàng (cart_*):</strong> PR-AUC giảm xuống <strong>0.2681 (-2.76%)</strong>. Đây là mức suy giảm nghiêm trọng nhất, chứng minh nhóm rào cản giỏ hàng mang giá trị dự báo cốt lõi.</li>
                      <li>• <strong>Loại bỏ nhóm Giao dịch lịch sử (trans_*):</strong> PR-AUC giảm còn <strong>0.2712 (-1.63%)</strong>.</li>
                      <li>• <strong>Loại bỏ nhóm Nhân khẩu tĩnh (geo_*, age):</strong> PR-AUC giảm còn <strong>0.2739 (-0.65%)</strong>.</li>
                    </ul>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                    <h5 className="font-bold text-midnightNavy mb-2 flex items-center gap-1.5">
                      <ShieldCheck className="w-4 h-4 text-teal-600" />
                      Kiểm định độ ổn định đa hạt giống (Multi-Seed Stability)
                    </h5>
                    <p className="text-slate-800 leading-relaxed mb-2">
                      Thực nghiệm trên 5 hạt giống ngẫu nhiên độc lập (Seed 42, 100, 2024, 2026, 777) xác nhận mô hình đạt độ ổn định gần như tuyệt đối:
                    </p>
                    <div className="grid grid-cols-2 gap-2 font-mono text-[11px]">
                      <div className="p-2 rounded bg-white border border-slate-200">
                        <span className="text-slate-500 block text-[10px]">PR-AUC Mean &plusmn; Std:</span>
                        <strong className="text-teal-900"><MathView math="0.2761 \pm 0.0004" /></strong>
                      </div>
                      <div className="p-2 rounded bg-white border border-slate-200">
                        <span className="text-slate-500 block text-[10px]">ROC-AUC Mean &plusmn; Std:</span>
                        <strong className="text-indigo-900"><MathView math="0.6133 \pm 0.0004" /></strong>
                      </div>
                    </div>
                    <p className="text-[10px] text-slate-600 mt-2 font-sans font-medium">
                      Phương sai cực tiểu chứng minh mô hình học được quy luật hành vi khái quát thay vì bám vào các mẫu nhiễu ngẫu nhiên.
                    </p>
                  </div>
                </div>
              </div>

              {/* 4.2 HIỆU CHUẨN ĐỘ TIN CẬY XÁC SUẤT THỰC NGHIỆM */}
              <div className="sub-reading-card p-6 border-l-4 border-l-teal-600">
                <div className="flex items-center gap-2 mb-3">
                  <Percent className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    4.2. Hiệu Chuẩn Độ Tin Cậy Xác Suất Thực Nghiệm (Platt Sigmoid Calibration)
                  </h3>
                </div>
                <div className="space-y-3 text-xs sm:text-sm text-slate-800 leading-relaxed font-medium">
                  <p>
                    Các thuật toán cây tăng cường như LightGBM hay XGBoost thường bị <strong>phân cực xác suất cực đoan</strong> (thiên lệch tự tin thái quá): các mẫu có xác suất thực tế ~30% bị gán điểm vọt lên 60-70%, hoặc 15% bị ép xuống gần 0%. Sai số hiệu chuẩn kỳ vọng (ECE) của mô hình gốc lên tới <strong>0.2236</strong>. Hiện tượng này làm thổi phồng chi phí tài chính và đánh giá sai thặng dư kỳ vọng.
                  </p>
                  <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs border-collapse">
                      <thead>
                        <tr className="border-b border-slate-200 text-slate-700 font-mono uppercase bg-slate-50/80 font-bold">
                          <th className="py-2.5 px-3">Cấu hình mô hình</th>
                          <th className="py-2.5 px-3">Brier Score (BS)</th>
                          <th className="py-2.5 px-3">Sai số kỳ vọng (ECE)</th>
                          <th className="py-2.5 px-3">Khoảng tin cậy 90%</th>
                          <th className="py-2.5 px-3">Đánh giá mức độ trung thực của xác suất</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-100 text-[11px]">
                        <tr>
                          <td className="py-2.5 px-3 font-semibold text-rose-900">LightGBM gốc (Chưa hiệu chuẩn)</td>
                          <td className="py-2.5 px-3 font-mono">0.2084</td>
                          <td className="py-2.5 px-3 font-mono font-bold text-rose-700">0.2236</td>
                          <td className="py-2.5 px-3 font-mono">[0.021, 0.784]</td>
                          <td className="py-2.5 px-3 text-slate-700">Thiên lệch tự tin thái quá; sai số kỳ vọng lệch 22.36% so với thực tế.</td>
                        </tr>
                        <tr>
                          <td className="py-2.5 px-3 font-semibold text-slate-800">LightGBM + Isotonic Calibration</td>
                          <td className="py-2.5 px-3 font-mono">0.1577</td>
                          <td className="py-2.5 px-3 font-mono font-bold text-teal-800">0.0020</td>
                          <td className="py-2.5 px-3 font-mono">[0.084, 0.382]</td>
                          <td className="py-2.5 px-3 text-slate-700">Hiệu chuẩn tốt nhưng hàm từng đoạn gây gãy khúc ở nhóm mẫu hiếm.</td>
                        </tr>
                        <tr className="bg-teal-50/80 font-bold text-teal-950">
                          <td className="py-2.5 px-3">LightGBM + Platt Sigmoid Calibration*</td>
                          <td className="py-2.5 px-3 font-mono text-emerald-800">0.1576 (-24.4%)</td>
                          <td className="py-2.5 px-3 font-mono text-emerald-800">0.0035</td>
                          <td className="py-2.5 px-3 font-mono">[0.091, 0.395]</td>
                          <td className="py-2.5 px-3">Tối ưu toàn diện: Brier Score giảm mạnh 24.4%; đường cong bám sát hoàn hảo phân giác 45 độ.</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <p className="text-[11px] text-slate-600">
                    Hàm Platt Sigmoid tham số hóa: <code>P(y_i = 1 | f_i) = 1 / [1 + exp(A*f_i + B)]</code> với độ dốc A = -1.0421 và hệ số chặn B = -1.3685, nén ECE xuống <strong>0.0035</strong>, đưa mô hình trở thành động cơ tính toán lõi cho bài toán tối ưu kinh tế.
                  </p>
                </div>
              </div>

              {/* 4.3 MÔ HÌNH HÓA ĐỘNG HỌC SỐNG CÒN & TỐC ĐỘ PHÂN RÃ GIỎ HÀNG */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-3">
                  <Clock className="w-5 h-5 text-indigo-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    4.3. Mô Hình Hóa Động Học Sống Còn (Kaplan-Meier) &amp; Tỷ Số Nguy Cơ (CoxPH)
                  </h3>
                </div>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs">
                  <div>
                    <h5 className="font-bold text-midnightNavy mb-2">Hàm sống còn Kaplan-Meier S&#770;(t) theo thời gian:</h5>
                    <div className="overflow-x-auto">
                      <table className="w-full text-left text-[11px] border-collapse">
                        <thead>
                          <tr className="border-b border-slate-200 text-slate-700 font-mono bg-slate-50 font-bold">
                            <th className="py-2 px-2.5">Thời gian</th>
                            <th className="py-2 px-2.5">Toàn sàn S&#770;(t)</th>
                            <th className="py-2 px-2.5">Standard</th>
                            <th className="py-2 px-2.5">Express</th>
                            <th className="py-2 px-2.5">Overnight</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 font-mono">
                          <tr>
                            <td className="py-1.5 px-2.5 font-sans font-bold">Ngày 1</td>
                            <td className="py-1.5 px-2.5">84.21%</td>
                            <td className="py-1.5 px-2.5">86.50%</td>
                            <td className="py-1.5 px-2.5">84.10%</td>
                            <td className="py-1.5 px-2.5">81.20%</td>
                          </tr>
                          <tr className="bg-amber-50/70 font-semibold text-amber-950">
                            <td className="py-1.5 px-2.5 font-sans">Ngày 3 (Vàng)</td>
                            <td className="py-1.5 px-2.5">58.40%</td>
                            <td className="py-1.5 px-2.5">61.20%</td>
                            <td className="py-1.5 px-2.5">58.90%</td>
                            <td className="py-1.5 px-2.5">54.10%</td>
                          </tr>
                          <tr className="bg-rose-50/80 font-bold text-rose-950">
                            <td className="py-1.5 px-2.5 font-sans">Ngày 7 (t*)</td>
                            <td className="py-1.5 px-2.5 text-coralRed">24.50%</td>
                            <td className="py-1.5 px-2.5">26.80%</td>
                            <td className="py-1.5 px-2.5">24.90%</td>
                            <td className="py-1.5 px-2.5 text-coralRed">19.80%</td>
                          </tr>
                          <tr>
                            <td className="py-1.5 px-2.5 font-sans">Ngày 14</td>
                            <td className="py-1.5 px-2.5">11.20%</td>
                            <td className="py-1.5 px-2.5">12.40%</td>
                            <td className="py-1.5 px-2.5">11.50%</td>
                            <td className="py-1.5 px-2.5">8.90%</td>
                          </tr>
                          <tr>
                            <td className="py-1.5 px-2.5 font-sans">Ngày 30</td>
                            <td className="py-1.5 px-2.5">3.10%</td>
                            <td className="py-1.5 px-2.5">3.40%</td>
                            <td className="py-1.5 px-2.5">3.10%</td>
                            <td className="py-1.5 px-2.5">2.20%</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <p className="text-[11px] text-slate-700 mt-2 font-medium">
                      <strong>Thời điểm vàng can thiệp:</strong> Trong 72 giờ đầu (<MathView math="t \le 3" /> ngày), hơn 40% giỏ hàng rời đi. Đến ngày thứ 7 (<MathView math="t^* = 7" /> ngày), xác suất của nhóm Overnight chỉ còn <strong>19.80%</strong>. Cần can thiệp vào giờ thứ 3 và giờ thứ 24!
                    </p>
                  </div>

                  <div>
                    <h5 className="font-bold text-midnightNavy mb-2">Hồi quy tỷ số nguy cơ CoxPH (Hazard Ratios):</h5>
                    <div className="space-y-2 font-mono text-[11px]">
                      {COXPH_DATA.map((row) => (
                        <div key={row.covariate} className="p-2.5 rounded-lg bg-slate-50 border border-slate-200">
                          <div className="flex justify-between items-center font-sans">
                            <strong className="text-slate-900">{row.covariate}</strong>
                            <span className={`font-mono font-bold ${row.hr > 1 ? 'text-coralRed' : 'text-emerald-800'}`}>
                              HR = {row.hr.toFixed(2)} (p = {row.p})
                            </span>
                          </div>
                          <div className="text-[10px] text-slate-600 font-sans mt-0.5">
                            {row.impact} · 95% CI: [{row.lower.toFixed(2)}, {row.upper.toFixed(2)}]
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* 4.4 SUY LUẬN NHÂN QUẢ UPLIFT T-LEARNER & SHAP */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-3">
                  <Sparkles className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    4.4. Suy Luận Nhân Quả Uplift T-Learner (CATE) &amp; Tương Tác Phi Tuyến TreeSHAP
                  </h3>
                </div>
                <p className="text-xs text-slate-700 mb-3 font-medium">
                  Mô hình T-Learner LightGBM ước lượng điểm số tác động gia tăng thuần <MathView math="\tau(x) = \mu_1(x) - \mu_0(x)" />, bóc tách quần thể khách hàng thành 4 góc phần tư phản ứng tiếp thị trên 32.000 khách hàng tập kiểm thử:
                </p>
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead>
                      <tr className="border-b border-slate-200 text-slate-700 font-mono uppercase bg-slate-50/80 font-bold">
                        <th className="py-2.5 px-3">Phân nhóm Uplift</th>
                        <th className="py-2.5 px-3">Quy mô</th>
                        <th className="py-2.5 px-3">Tỷ trọng</th>
                        <th className="py-2.5 px-3">Uplift thuần (<MathView math="\bar{\tau}" />)</th>
                        <th className="py-2.5 px-3">Chuyển đổi KHÔNG ưu đãi</th>
                        <th className="py-2.5 px-3">Chuyển đổi CÓ ưu đãi</th>
                        <th className="py-2.5 px-3">Chiến lược quản trị phân bổ</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 text-slate-800 text-[11px]">
                      <tr className="bg-emerald-50/80 font-bold text-emerald-950">
                        <td className="py-2.5 px-3 font-sans">Persuadables (Nhạy cảm ưu đãi)</td>
                        <td className="py-2.5 px-3 font-mono">11.200</td>
                        <td className="py-2.5 px-3 font-mono">35.00%</td>
                        <td className="py-2.5 px-3 font-mono text-emerald-800">+0.1042</td>
                        <td className="py-2.5 px-3 font-mono">18.42%</td>
                        <td className="py-2.5 px-3 font-mono text-emerald-800">28.84%</td>
                        <td className="py-2.5 px-3 font-sans">Trọng tâm can thiệp số 1: Cấp voucher $5.0; tăng trưởng thuần +10.42% chuyển đổi.</td>
                      </tr>
                      <tr className="bg-amber-50/60 font-medium">
                        <td className="py-2.5 px-3 font-sans font-bold text-amber-900">Sure Things (Chắc chắn mua)</td>
                        <td className="py-2.5 px-3 font-mono">1.151</td>
                        <td className="py-2.5 px-3 font-mono">3.60%</td>
                        <td className="py-2.5 px-3 font-mono">+0.0383</td>
                        <td className="py-2.5 px-3 font-mono font-bold text-emerald-800">31.86%</td>
                        <td className="py-2.5 px-3 font-mono">35.69%</td>
                        <td className="py-2.5 px-3 font-sans">Nghiêm cấm cấp voucher: Khách tự mua 31.86%; cấp voucher gây lãng phí ngân sách trực tiếp.</td>
                      </tr>
                      <tr>
                        <td className="py-2.5 px-3 font-sans font-medium text-slate-700">Lost Causes (Bất khả thi)</td>
                        <td className="py-2.5 px-3 font-mono">16.764</td>
                        <td className="py-2.5 px-3 font-mono">52.39%</td>
                        <td className="py-2.5 px-3 font-mono">+0.0641</td>
                        <td className="py-2.5 px-3 font-mono">16.91%</td>
                        <td className="py-2.5 px-3 font-mono">23.32%</td>
                        <td className="py-2.5 px-3 font-sans">Loại trừ tiếp cận có phí: Chi phí marketing vượt xa giá trị chuyển đổi kỳ vọng thu hồi.</td>
                      </tr>
                      <tr className="bg-rose-50/80 font-bold text-rose-950">
                        <td className="py-2.5 px-3 font-sans text-coralRed">Sleeping Dogs (Phản tác dụng)</td>
                        <td className="py-2.5 px-3 font-mono">2.885</td>
                        <td className="py-2.5 px-3 font-mono">9.02%</td>
                        <td className="py-2.5 px-3 font-mono text-coralRed">-0.0618</td>
                        <td className="py-2.5 px-3 font-mono">25.48%</td>
                        <td className="py-2.5 px-3 font-mono text-coralRed">19.30%</td>
                        <td className="py-2.5 px-3 font-sans">Tuyệt đối tránh xa: Can thiệp tiếp thị làm khách khó chịu, giảm chuyển đổi từ 25.48% xuống 19.30%.</td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                {/* TreeSHAP Interaction Pairs */}
                <div className="mt-4 p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                  <h5 className="font-bold text-midnightNavy mb-2 flex items-center gap-1.5">
                    <Target className="w-4 h-4 text-indigo-600" />
                    Top Các Cặp Tương Tác Đặc Trưng Phi Tuyến Mạnh Nhất (TreeSHAP Interaction Values)
                  </h5>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-[11px]">
                    <div className="p-3 rounded-lg bg-white border border-slate-200">
                      <div className="font-mono font-bold text-midnightNavy">cart_to_page_ratio &times; total_spend</div>
                      <div className="text-teal-800 font-mono font-bold my-1">Interaction = 0.00577</div>
                      <p className="text-slate-600">Khách có giỏ hàng giá trị lớn nhưng tỷ lệ thêm giỏ cao xuất hiện tâm lý đắn đo bảo toàn ngân sách cực đoan.</p>
                    </div>
                    <div className="p-3 rounded-lg bg-white border border-slate-200">
                      <div className="font-mono font-bold text-midnightNavy">days_since_last_session &times; loyalty_score</div>
                      <div className="text-teal-800 font-mono font-bold my-1">Interaction = 0.00503</div>
                      <p className="text-slate-600">Ngay cả khách hàng trung thành, nếu rời xa sàn quá 7 ngày, hiệu ứng gắn kết thương hiệu bị triệt tiêu nhanh chóng.</p>
                    </div>
                    <div className="p-3 rounded-lg bg-white border border-slate-200">
                      <div className="font-mono font-bold text-midnightNavy">hesitation_index &times; total_spend</div>
                      <div className="text-teal-800 font-mono font-bold my-1">Interaction = 0.00349</div>
                      <p className="text-slate-600">Thời gian dừng xem sản phẩm kéo dài kết hợp tổng giá trị giỏ lớn là tín hiệu cảnh báo thoát trang trước thanh toán.</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Hình 4.1: ROC & PR Curves - Rộng 100% */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-bold text-midnightNavy text-base flex items-center gap-2">
                    <Eye className="w-5 h-5 text-teal-600 spring-icon" />
                    Hình 4.1: So Sánh Đường Cong ROC &amp; Precision-Recall 5 Thuật Toán
                  </h4>
                  <span className="text-xs font-mono text-teal-800 font-bold bg-teal-50 px-2.5 py-1 rounded-full border border-teal-200">
                    LightGBM PR-AUC = 0.2771
                  </span>
                </div>
                <p className="text-xs text-slate-800 mb-4 font-medium">
                  Biểu đồ đối chuẩn trực quan trên 32.000 mẫu kiểm thử. Khung hiển thị rộng đầy đủ hai đồ thị ROC và Precision-Recall cùng các đường ngưỡng cơ sở.
                </p>
                <div className="w-full flex items-center justify-center p-4 bg-white/95 rounded-2xl border border-slate-200 shadow-inner overflow-hidden">
                  <img
                    src="/figures/fig_ch4_01_roc_pr_curves_comparison.png"
                    alt="ROC &amp; PR Curves"
                    className="max-w-full h-auto max-h-[460px] object-contain transition-transform duration-300 hover:scale-[1.01]"
                  />
                </div>
              </div>
            </div>
          )}

          {/* ========================================================
              PHẦN 5: DASHBOARD, INSIGHT CHÍNH VÀ ĐỀ XUẤT KINH DOANH
          ======================================================== */}
          {activeTab === 4 && (
            <div className="space-y-8 animate-fadeIn">
              <div className="border-b border-slate-200/60 pb-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2 text-teal-800 text-xs font-mono font-bold uppercase tracking-wider mb-1">
                    <Sliders className="w-4 h-4 spring-icon text-teal-700" /> Báo Cáo Điều Hành, Bảng Insight &amp; Đề Xuất Kinh Doanh
                  </div>
                  <h1 className="text-2xl md:text-3xl font-extrabold text-midnightNavy tracking-tight">
                    PHẦN 5: DASHBOARD, INSIGHT CHÍNH VÀ ĐỀ XUẤT KINH DOANH
                  </h1>
                  <p className="text-slate-950 font-bold text-xs sm:text-sm mt-2 max-w-4xl leading-relaxed">
                    Hệ thống 4 trang Dashboard tương tác trực tiếp (Động học phễu &amp; Rào cản, Radar 5 Cụm GMM, Phân tích sống còn Kaplan-Meier, Bộ mô phỏng What-If kinh tế &tau;* = 0.07), bảng tổng hợp 4 Insight cốt lõi thực nghiệm và ma trận 4 gói đề xuất hành động kinh doanh chi tiết (ACT-01 &rarr; ACT-04).
                  </p>
                </div>
              </div>

              {/* ========================================================
                  MỤC 5.1: KIẾN TRÚC DỮ LIỆU STAR SCHEMA & HỆ THỐNG 4 TRANG DASHBOARD
              ======================================================== */}
              <div className="sub-reading-card p-6 border-l-4 border-l-teal-600">
                <div className="flex items-center gap-2 mb-3">
                  <Database className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    5.1. Hệ Thống Dashboard Điều Hành Đa Chiều &amp; Kiến Trúc Dữ Liệu Star Schema
                  </h3>
                </div>
                <div className="space-y-3 text-xs sm:text-sm text-slate-800 leading-relaxed font-medium">
                  <p>
                    Để chuyển giao toàn bộ kết quả mô hình hóa vào thực tiễn quản trị doanh nghiệp, đề tài thiết lập kiến trúc dữ liệu <strong>Star Schema</strong> chuẩn hóa (đồng bộ giữa Power BI Desktop và Cổng thông tin hỗ trợ quyết định Next.js - FastAPI theo phong cách Liquid Glass). Mô hình vận hành xoay quanh:
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono my-2">
                    <div className="p-3.5 rounded-xl bg-teal-50/80 border border-teal-200">
                      <strong className="text-teal-900 block mb-1 font-bold font-sans">Bảng Sự Kiện Trung Tâm (Fact Table):</strong>
                      <code className="text-[11px] text-teal-800 font-bold block mb-1">Fact_User_Activity_PIT (200,000 bản ghi)</code>
                      <p className="font-sans text-slate-700 text-[11px] leading-relaxed">
                        Lưu trữ tổng hợp hành vi người dùng tại mốc chốt quyết định t₀ (tổng số phiên, tỷ lệ xem trang, số lượt thêm giỏ, giá trị AOV quá khứ, nhãn chuyển đổi thực tế y &isin; &#123;0, 1&#125; và xác suất hiệu chuẩn).
                      </p>
                    </div>
                    <div className="p-3.5 rounded-xl bg-indigo-50/80 border border-indigo-200">
                      <strong className="text-indigo-900 block mb-1 font-bold font-sans">Bốn Chiều Phân Tích (Dimension Tables):</strong>
                      <ul className="space-y-1 font-sans text-slate-700 text-[11px] leading-relaxed">
                        <li>• <code className="font-mono text-indigo-800 font-bold">Dim_Customer:</code> Độ tuổi, thành phố, 4 phân hạng thành viên (Bronze &rarr; Platinum).</li>
                        <li>• <code className="font-mono text-indigo-800 font-bold">Dim_Time:</code> Phân cấp thời gian (Ngày, Tuần, Tháng, Quý, Năm).</li>
                        <li>• <code className="font-mono text-indigo-800 font-bold">Dim_Behavior_Cluster:</code> 5 cụm vi mô xác suất từ mô hình GMM (k*=5).</li>
                        <li>• <code className="font-mono text-indigo-800 font-bold">Dim_Uplift_Segment:</code> 4 góc phần tư tác động nhân quả (Persuadables, Sure Things...).</li>
                      </ul>
                    </div>
                  </div>
                  <p className="text-xs text-slate-600 font-sans italic">
                    Hệ thống tích hợp 4 trang giao diện điều hành tác chiến trực quan bên dưới, cho phép nhà quản trị kiểm tra động học phễu, soi chiếu chân dung 5 cụm khách hàng, theo dõi phân rã ý định mua sống còn và tinh chỉnh tham số tài chính What-If tức thời:
                  </p>
                </div>
              </div>

              {/* Sub-Tabs Selector for 4 Dashboard Pages */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-1">
                <div className="text-xs font-mono font-bold text-slate-700 uppercase flex items-center gap-1.5">
                  <BarChart3 className="w-4 h-4 text-teal-600" /> Bảng Điều Khiển Tương Tác 4 Trang (Interactive Dashboard Cockpit):
                </div>
                <div className="flex bg-slate-900/85 p-1 rounded-full border border-white/20 shadow-md shrink-0 self-start sm:self-auto">
                  {DASHBOARD_TABS.map((tab, idx) => (
                    <button
                      key={tab}
                      onClick={() => setDashTab(idx)}
                      className={`px-3 sm:px-4 py-1.5 text-xs font-semibold rounded-full transition-all cursor-pointer whitespace-nowrap bounce-btn ${
                        dashTab === idx
                          ? 'bg-teal-500 text-white font-bold shadow'
                          : 'text-gray-300 hover:text-white'
                      }`}
                    >
                      {tab}
                    </button>
                  ))}
                </div>
              </div>

              {/* ----------------------------------------------------
                  TRANG 1: ĐỘNG HỌC PHỄU & KPI COCKPIT (NATIVE TỰ VẼ)
              ---------------------------------------------------- */}
              {dashTab === 0 && (
                <div className="space-y-6">
                  {/* 4 KPI Cards */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="sub-reading-card p-5 border-l-4 border-l-teal-600">
                      <span className="text-[11px] font-mono text-slate-600 uppercase font-bold">Tổng Quy Mô Khách Hàng</span>
                      <div className="text-2xl font-extrabold text-midnightNavy mt-1">200,000</div>
                      <span className="text-[10px] text-slate-700 font-medium">997k phiên / 249k giao dịch</span>
                    </div>

                    <div className="sub-reading-card p-5 border-l-4 border-l-rose-500">
                      <span className="text-[11px] font-mono text-slate-600 uppercase font-bold">Tỷ Lệ Bỏ Giỏ Chuẩn</span>
                      <div className="text-2xl font-extrabold text-coralRed mt-1">70.19%</div>
                      <span className="text-[10px] text-slate-700 font-medium">Baymard Benchmark</span>
                    </div>

                    <div className="sub-reading-card p-5 border-l-4 border-l-emerald-500">
                      <span className="text-[11px] font-mono text-slate-600 uppercase font-bold">Lợi Nhuận Thu Hồi (&tau;*)</span>
                      <div className="text-2xl font-extrabold text-emerald-800 mt-1">+$115,918</div>
                      <span className="text-[10px] text-slate-700 font-medium">Vượt +$41,200 so với mặc định</span>
                    </div>

                    <div className="sub-reading-card p-5 border-l-4 border-l-indigo-500">
                      <span className="text-[11px] font-mono text-slate-600 uppercase font-bold">Tiết Kiệm Chi Phí CAC</span>
                      <div className="text-2xl font-extrabold text-indigo-800 mt-1">-60.0%</div>
                      <span className="text-[10px] text-slate-700 font-medium">Nhắm chọn Top 20% Lift@K</span>
                    </div>
                  </div>

                  {/* Phễu Chuyển Đổi Native 4 Tầng Tự Vẽ */}
                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    <div className="lg:col-span-7 sub-reading-card p-6">
                      <div className="flex justify-between items-center mb-4">
                        <h4 className="font-bold text-midnightNavy text-sm">Phễu Chuyển Đổi 4 Tầng Tự Vẽ & Tỷ Lệ Rơi Rụng (Drop-off)</h4>
                        <span className="text-xs font-mono text-teal-800 font-bold bg-teal-50 px-2 py-0.5 rounded border border-teal-200">Interactive Funnel</span>
                      </div>

                      <div className="space-y-3.5">
                        <div className="p-3 rounded-xl bg-white/80 border border-slate-200 shadow-sm">
                          <div className="flex justify-between text-xs font-bold mb-1.5">
                            <span className="flex items-center gap-1.5 text-indigo-900">
                              <span className="w-2.5 h-2.5 rounded-full bg-indigo-600" />
                              1. Phiên truy cập (Total Sessions)
                            </span>
                            <span className="font-mono text-indigo-900">997,000 phiên (100.0%)</span>
                          </div>
                          <div className="w-full bg-slate-100 rounded-full h-3.5 overflow-hidden">
                            <div className="bg-gradient-to-r from-indigo-500 to-indigo-700 h-full rounded-full w-full" />
                          </div>
                        </div>

                        <div className="p-3 rounded-xl bg-white/80 border border-slate-200 shadow-sm">
                          <div className="flex justify-between text-xs font-bold mb-1.5">
                            <span className="flex items-center gap-1.5 text-teal-900">
                              <span className="w-2.5 h-2.5 rounded-full bg-teal-600" />
                              2. Thêm vào giỏ (Cart Additions)
                            </span>
                            <span className="font-mono text-teal-800">249,000 (24.97% chuyển đổi)</span>
                          </div>
                          <div className="w-full bg-slate-100 rounded-full h-3.5 overflow-hidden">
                            <div className="bg-gradient-to-r from-teal-500 to-teal-700 h-full rounded-full w-[25%]" />
                          </div>
                          <div className="text-[11px] text-rose-700 font-semibold mt-1">
                            &darr; Rơi rụng: 748,000 phiên rời đi trước khi thêm giỏ (-75.03%)
                          </div>
                        </div>

                        <div className="p-3 rounded-xl bg-white/80 border border-slate-200 shadow-sm">
                          <div className="flex justify-between text-xs font-bold mb-1.5">
                            <span className="flex items-center gap-1.5 text-amber-900">
                              <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                              3. Tiến hành thanh toán (Checkouts)
                            </span>
                            <span className="font-mono text-amber-800">74,250 (29.82% từ thêm giỏ)</span>
                          </div>
                          <div className="w-full bg-slate-100 rounded-full h-3.5 overflow-hidden">
                            <div className="bg-gradient-to-r from-amber-400 to-amber-600 h-full rounded-full w-[7.45%]" />
                          </div>
                          <div className="text-[11px] text-rose-700 font-semibold mt-1">
                            &darr; Điểm nghẽn chính: 174,750 giỏ hàng bị bỏ lại (70.19% bỏ giỏ)
                          </div>
                        </div>

                        <div className="p-3 rounded-xl bg-white/80 border border-slate-200 shadow-sm">
                          <div className="flex justify-between text-xs font-bold mb-1.5">
                            <span className="flex items-center gap-1.5 text-emerald-900">
                              <span className="w-2.5 h-2.5 rounded-full bg-emerald-600" />
                              4. Mua hàng thành công (Purchases)
                            </span>
                            <span className="font-mono text-emerald-800">29,510 đơn (39.74% từ Checkout)</span>
                          </div>
                          <div className="w-full bg-slate-100 rounded-full h-3.5 overflow-hidden">
                            <div className="bg-gradient-to-r from-emerald-500 to-emerald-700 h-full rounded-full w-[2.96%]" />
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Biểu Đồ Recharts: Ma Sát Cước Theo Hạng */}
                    <div className="lg:col-span-5 sub-reading-card p-6">
                      <div className="flex justify-between items-center mb-3">
                        <h4 className="font-bold text-midnightNavy text-sm">Tỷ Lệ Bỏ Giỏ Theo Phương Thức Vận Chuyển</h4>
                        <span className="text-[10px] font-mono text-slate-600 font-bold bg-white px-2 py-0.5 rounded border border-slate-200">Recharts Bar</span>
                      </div>
                      <p className="text-xs text-slate-800 mb-3 font-medium">So sánh tỷ lệ từ bỏ giỏ (%) giữa 3 phương thức cước qua 4 phân hạng hội viên.</p>

                      <div className="h-64 w-full">
                        {mounted && (
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={SHIPPING_FRICTION_DATA} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
                              <XAxis dataKey="tier" stroke="#475569" fontSize={11} />
                              <YAxis stroke="#475569" fontSize={11} domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
                              <Tooltip formatter={(v: number) => [`${v}%`, 'Tỷ lệ bỏ giỏ']} />
                              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                              <Bar dataKey="overnight" name="Giao qua đêm (Overnight)" fill="#E11D48" radius={[4, 4, 0, 0]} />
                              <Bar dataKey="standard" name="Giao thường (Standard)" fill="#0F172A" radius={[4, 4, 0, 0]} />
                              <Bar dataKey="free" name="Miễn phí (Free Shipping)" fill="#0D9488" radius={[4, 4, 0, 0]} />
                            </BarChart>
                          </ResponsiveContainer>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Biểu Đồ Ngang: Mức Bỏ Giỏ Theo Danh Mục Hàng Hóa */}
                  <div className="sub-reading-card p-6">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-3">
                      <div>
                        <h4 className="font-bold text-midnightNavy text-sm">Mức Độ Nghiêm Trọng Bỏ Giỏ Hàng (Severity) Theo 8 Ngành Hàng</h4>
                        <p className="text-xs text-slate-700 font-medium">Số phiên bỏ giỏ trung bình trên mỗi khách hàng (Khoảng cách nhãn Y-Axis chuẩn hóa tránh chồng lấn chữ)</p>
                      </div>
                      <span className="text-[10px] font-mono text-slate-700 bg-white/80 px-2 py-0.5 rounded border border-slate-300 font-bold shrink-0">Category Breakdown</span>
                    </div>
                    <div className="h-[430px] w-full">
                      {mounted && (
                        <ResponsiveContainer width="100%" height="100%">
                          <BarChart data={CATEGORY_ABANDON_DATA} layout="vertical" margin={{ top: 10, right: 30, left: 10, bottom: 10 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" horizontal={false} />
                            <XAxis type="number" stroke="#475569" fontSize={11} domain={[0, 6]} tickFormatter={(v) => `${v} phiên`} />
                            <YAxis type="category" dataKey="category" stroke="#0F172A" fontSize={12} width={165} tickLine={false} />
                            <Tooltip formatter={(v: number, name: string) => [name === 'severity' ? `${v} phiên bỏ giỏ / khách` : `$${v}`, name === 'severity' ? 'Mức độ bỏ giỏ' : 'AOV']} />
                            <Bar dataKey="severity" name="severity" fill="#E11D48" radius={[0, 4, 4, 0]} barSize={22} />
                          </BarChart>
                        </ResponsiveContainer>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* ----------------------------------------------------
                  TRANG 2: PHÂN KHÚC GMM & RADAR CHART NATIVE TỰ VẼ
              ---------------------------------------------------- */}
              {dashTab === 1 && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    {/* Native Interactive Radar Chart Tự Vẽ */}
                    <div className="lg:col-span-7 sub-reading-card p-6">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-bold text-midnightNavy text-sm">Biểu Đồ Radar Tự Vẽ: So Sánh 5 Cụm RFM-E Trên 6 Chiều Chỉ Số</h4>
                        <span className="text-[10px] font-mono text-teal-800 font-bold bg-teal-50 px-2 py-0.5 rounded border border-teal-200">Recharts Radar</span>
                      </div>
                      <p className="text-xs text-slate-800 mb-2 font-medium">Trực quan hóa độ lệch đa chiều giữa 5 cụm hành vi GMM chuẩn hóa.</p>

                      <div className="h-80 w-full">
                        {mounted && (
                          <ResponsiveContainer width="100%" height="100%">
                            <RadarChart data={RADAR_METRICS_DATA}>
                              <PolarGrid stroke="#CBD5E1" />
                              <PolarAngleAxis dataKey="metric" stroke="#0F172A" fontSize={11} />
                              <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#94A3B8" fontSize={9} />
                              <Radar name="Cụm 1: VIP Champions" dataKey="C1_VIP" stroke="#0D9488" fill="#0D9488" fillOpacity={0.25} />
                              <Radar name="Cụm 2: Cart Hesitators" dataKey="C2_Hesitator" stroke="#E11D48" fill="#E11D48" fillOpacity={0.35} />
                              <Radar name="Cụm 3: Discount Seekers" dataKey="C3_Discount" stroke="#4F46E5" fill="#4F46E5" fillOpacity={0.2} />
                              <Radar name="Cụm 5: Passive Browsers" dataKey="C5_Browser" stroke="#D97706" fill="#D97706" fillOpacity={0.15} />
                              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                              <Tooltip />
                            </RadarChart>
                          </ResponsiveContainer>
                        )}
                      </div>
                    </div>

                    {/* Interactive Cluster Inspector */}
                    <div className="lg:col-span-5 sub-reading-card p-6 flex flex-col justify-between">
                      <div>
                        <div className="flex justify-between items-center mb-3">
                          <h4 className="font-bold text-midnightNavy text-sm">Chọn Cụm Để Khám Phá Chi Tiết</h4>
                          <span className="text-xs font-mono font-bold text-teal-800">k* = 5</span>
                        </div>

                        {/* Cluster Select Buttons */}
                        <div className="flex flex-wrap gap-1.5 mb-4">
                          {GMM_DATA.map((c) => (
                            <button
                              key={c.id}
                              onClick={() => setSelectedClusterId(c.id)}
                              className={`px-3 py-1 text-xs font-bold rounded-lg transition-all cursor-pointer bounce-btn ${
                                selectedClusterId === c.id
                                  ? 'bg-slate-900 text-white shadow-md'
                                  : 'bg-white/80 text-slate-700 hover:bg-slate-100 border border-slate-200'
                              }`}
                            >
                              Cụm {c.id}
                            </button>
                          ))}
                        </div>

                        {/* Selected Cluster Info Card */}
                        <div className="p-4 rounded-xl bg-white/90 border border-slate-200/90 shadow-sm space-y-3">
                          <div className="flex justify-between items-start">
                            <div>
                              <span className="text-[10px] font-mono text-slate-600 uppercase font-bold">Chân dung phân khúc</span>
                              <h5 className="font-bold text-sm text-midnightNavy">{selectedCluster.name}</h5>
                            </div>
                            <span className="font-mono text-xs font-bold px-2 py-0.5 rounded bg-teal-100 text-teal-900">
                              {selectedCluster.share}
                            </span>
                          </div>

                          <div className="grid grid-cols-2 gap-2 text-xs font-mono">
                            <div className="p-2 rounded bg-slate-50 border border-slate-100">
                              <span className="text-[10px] text-slate-500 block">Quy mô</span>
                              <strong className="text-slate-800">{selectedCluster.count.toLocaleString()} khách</strong>
                            </div>
                            <div className="p-2 rounded bg-slate-50 border border-slate-100">
                              <span className="text-[10px] text-slate-500 block">AOV trung bình</span>
                              <strong className="text-emerald-800 font-bold">{selectedCluster.aov}</strong>
                            </div>
                            <div className="p-2 rounded bg-slate-50 border border-slate-100">
                              <span className="text-[10px] text-slate-500 block">Độ nghiêm trọng bỏ giỏ</span>
                              <strong className="text-coralRed font-bold">{selectedCluster.aban} phiên</strong>
                            </div>
                            <div className="p-2 rounded bg-slate-50 border border-slate-100">
                              <span className="text-[10px] text-slate-500 block">Tỷ lệ mua</span>
                              <strong className="text-teal-800 font-bold">{selectedCluster.conv}</strong>
                            </div>
                          </div>

                          <div className="pt-2 border-t border-slate-100">
                            <span className="text-[10px] font-bold text-slate-600 block mb-1 uppercase">Hành động can thiệp:</span>
                            <p className="text-xs text-slate-900 font-medium leading-relaxed">{selectedCluster.action}</p>
                          </div>
                        </div>
                      </div>

                      <div className="mt-4 p-3 rounded-lg bg-teal-50 border border-teal-200 text-xs text-teal-900 font-medium">
                        <strong>Insight GMM:</strong> Cụm 2 (*Cart Hesitators*, 25.04% dân số) chính là đối tượng mang lại tỷ suất hoàn vốn cao nhất khi can thiệp cước vận chuyển.
                      </div>
                    </div>
                  </div>

                  {/* Biểu Đồ ComposedChart: So Sánh AOV và Tỷ Trọng 5 Cụm */}
                  <div className="sub-reading-card p-6">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-3">
                      <div>
                        <h4 className="font-bold text-midnightNavy text-sm">So Sánh Giá Trị Đơn Hàng (AOV $) &amp; Tỷ Trọng Dân Số 5 Cụm GMM</h4>
                        <p className="text-xs text-slate-700 font-medium">Trực quan hóa kép: Cột AOV ($) theo màu cụm và Đường chấm đỏ thể hiện Tỷ trọng dân số (%)</p>
                      </div>
                      <div className="flex items-center gap-3 text-xs font-mono shrink-0">
                        <span className="flex items-center gap-1.5 text-slate-800">
                          <span className="w-3 h-3 rounded bg-teal-600 inline-block" /> AOV ($)
                        </span>
                        <span className="flex items-center gap-1.5 text-slate-800">
                          <span className="w-2.5 h-2.5 rounded-full bg-rose-600 inline-block" /> Tỷ Trọng (%)
                        </span>
                      </div>
                    </div>
                    <div className="h-72 w-full">
                      {mounted && (
                        <ResponsiveContainer width="100%" height="100%">
                          <ComposedChart data={GMM_DATA} margin={{ top: 15, right: 30, left: 10, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
                            <XAxis dataKey="shortName" stroke="#0F172A" fontSize={11} tickLine={false} />
                            <YAxis yAxisId="left" stroke="#0D9488" fontSize={11} domain={[0, 480]} tickFormatter={(v) => `$${v}`} />
                            <YAxis yAxisId="right" orientation="right" stroke="#E11D48" fontSize={11} domain={[0, 35]} tickFormatter={(v) => `${v}%`} />
                            <Tooltip
                              formatter={(value: any, name: string) => {
                                if (name === 'aovNum' || name === 'Giá trị đơn hàng (AOV $)') return [`$${value}`, 'AOV trung bình'];
                                return [`${value}%`, 'Tỷ trọng dân số'];
                              }}
                            />
                            <Bar yAxisId="left" dataKey="aovNum" name="Giá trị đơn hàng (AOV $)" radius={[6, 6, 0, 0]} barSize={42}>
                              {GMM_DATA.map((entry) => (
                                <Cell key={entry.id} fill={entry.color} />
                              ))}
                            </Bar>
                            <Line yAxisId="right" type="monotone" dataKey="shareNum" name="Tỷ trọng dân số (%)" stroke="#E11D48" strokeWidth={3} dot={{ r: 5, fill: '#E11D48' }} />
                          </ComposedChart>
                        </ResponsiveContainer>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* ----------------------------------------------------
                  TRANG 3: PHÂN TÍCH SỐNG CÒN & BÁN RÃ GIỎ HÀNG (NATIVE)
              ---------------------------------------------------- */}
              {dashTab === 2 && (
                <div className="space-y-6">
                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    {/* Native Kaplan-Meier Area Chart Tự Vẽ */}
                    <div className="lg:col-span-7 sub-reading-card p-6">
                      <div className="flex justify-between items-center mb-2">
                        <h4 className="font-bold text-midnightNavy text-sm">Đường Cong Sống Còn Kaplan-Meier Bán Rã Giỏ Hàng S(t)</h4>
                        <span className="text-xs font-mono font-bold text-coralRed bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                          t* &le; 7 ngày
                        </span>
                      </div>
                      <p className="text-xs text-slate-800 mb-3 font-medium">
                        Mốc bán rã cốt tử t* &le; 7 ngày: Sau ngày thứ 7, xác suất phục hồi giỏ hàng giảm xuống dưới 17.8% và rơi tự do.
                      </p>

                      <div className="h-72 w-full">
                        {mounted && (
                          <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={KAPLAN_MEIER_DATA} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                              <defs>
                                <linearGradient id="kmGrad" x1="0" y1="0" x2="0" y2="1">
                                  <stop offset="5%" stopColor="#0D9488" stopOpacity={0.5} />
                                  <stop offset="95%" stopColor="#0D9488" stopOpacity={0.0} />
                                </linearGradient>
                              </defs>
                              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
                              <XAxis dataKey="day" stroke="#475569" fontSize={11} tickFormatter={(v) => `Ngày ${v}`} />
                              <YAxis stroke="#475569" fontSize={11} domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
                              <Tooltip formatter={(v: number) => [`${v}%`, 'Xác suất mua lại S(t)']} labelFormatter={(l) => `Thời gian trôi qua: Ngày thứ ${l}`} />
                              <ReferenceLine x={7} stroke="#E11D48" strokeDasharray="3 3" strokeWidth={2} label={{ value: 't* = 7 ngày (Điểm gãy bán rã)', fill: '#E11D48', fontSize: 11, position: 'top' }} />
                              <Area type="stepAfter" dataKey="survival" name="Xác suất phục hồi giỏ" stroke="#0D9488" strokeWidth={3} fill="url(#kmGrad)" />
                              <Line type="monotone" dataKey="baseline" name="Đường chuẩn tham chiếu" stroke="#94A3B8" strokeDasharray="4 4" dot={false} />
                            </AreaChart>
                          </ResponsiveContainer>
                        )}
                      </div>
                    </div>

                    {/* Native Forest Plot CoxPH Tự Vẽ */}
                    <div className="lg:col-span-5 sub-reading-card p-6 flex flex-col justify-between">
                      <div>
                        <div className="flex justify-between items-center mb-2">
                          <h4 className="font-bold text-midnightNavy text-sm">Forest Plot: Tỷ Số Nguy Cơ CoxPH (Hazard Ratios)</h4>
                          <span className="text-[10px] font-mono text-slate-700 bg-white px-2 py-0.5 rounded border border-slate-200 font-bold">95% CI</span>
                        </div>
                        <p className="text-xs text-slate-800 mb-3 font-medium">HR &gt; 1 làm tăng nguy cơ bỏ giỏ; HR &lt; 1 thúc đẩy hoàn tất đơn.</p>

                        <div className="space-y-3 font-mono text-xs">
                          {COXPH_DATA.slice(0, 4).map((row) => (
                            <div key={row.covariate} className="p-3 rounded-xl bg-white/85 border border-slate-200 shadow-sm">
                              <div className="flex justify-between items-center mb-1 font-sans">
                                <strong className="text-slate-900 text-xs">{row.covariate}</strong>
                                <span className={`text-xs font-bold font-mono ${row.hr > 1 ? 'text-coralRed' : 'text-emerald-800'}`}>
                                  HR = {row.hr.toFixed(2)}
                                </span>
                              </div>
                              <div className="w-full bg-slate-100 rounded-full h-2 relative my-1.5">
                                <div className="absolute top-0 bottom-0 w-0.5 bg-slate-400 left-[33%]" /> {/* HR=1 marker */}
                                <div
                                  className="h-2 rounded-full bg-teal-600"
                                  style={{ width: `${Math.min(100, (row.hr / 3.5) * 100)}%` }}
                                />
                              </div>
                              <div className="flex justify-between text-[10px] text-slate-600 font-sans">
                                <span>95% CI: [{row.lower.toFixed(2)}, {row.upper.toFixed(2)}]</span>
                                <span>p = {row.p}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Native Qini Cumulative Curve Tự Vẽ */}
                  <div className="sub-reading-card p-6">
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="font-bold text-midnightNavy text-sm">Đường Cong Tích Lũy Qini Curve & T-Learner Uplift (Tự Vẽ)</h4>
                      <span className="text-xs font-mono font-bold text-teal-800 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
                        Uplift Gain
                      </span>
                    </div>
                    <div className="h-64 w-full">
                      {mounted && (
                        <ResponsiveContainer width="100%" height="100%">
                          <LineChart data={QINI_DATA} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
                            <XAxis dataKey="pct" stroke="#475569" fontSize={11} tickFormatter={(v) => `${v}%`} />
                            <YAxis stroke="#475569" fontSize={11} domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
                            <Tooltip formatter={(v: number) => [`${v}%`, 'Tỷ lệ tăng trưởng tích lũy']} labelFormatter={(l) => `Tỷ lệ tiếp cận: ${l}%`} />
                            <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                            <Line type="monotone" dataKey="tLearner" name="T-Learner Uplift (Mô hình đề xuất)" stroke="#0D9488" strokeWidth={3} dot={{ r: 4 }} />
                            <Line type="monotone" dataKey="random" name="Random Targeting (Tiếp cận ngẫu nhiên)" stroke="#94A3B8" strokeDasharray="4 4" dot={false} />
                          </LineChart>
                        </ResponsiveContainer>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* ----------------------------------------------------
                  TRANG 4: MÔ PHỎNG WHAT-IF KINH TẾ & PHÂN VỊ LIFT@K
              ---------------------------------------------------- */}
              {dashTab === 3 && (
                <div className="space-y-6">
                  {/* Interactive 3D Profit Surface */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-bold text-midnightNavy text-base flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-emerald-600 spring-icon" />
                        Mặt Cong 3D Hàm Lợi Nhuận Ròng Kỳ Vọng (WebGL Three.js)
                      </h4>
                      <span className="text-xs text-slate-700 font-mono font-bold">Tương tác xoay 3D tìm cực trị &tau;*</span>
                    </div>
                    <ThreeProfitSurface />
                  </div>

                  {/* Bộ Mô Phỏng What-If Kinh Tế Tương Tác */}
                  <div className="sub-reading-card p-6">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6 border-b border-slate-200 pb-4">
                      <div>
                        <h4 className="font-bold text-midnightNavy text-base">Trình Mô Phỏng Đường Cong Lợi Nhuận Ròng What-If</h4>
                        <p className="text-xs text-slate-800 font-medium">Điều chỉnh 3 tham số kinh tế để tính toán lại điểm tối ưu &tau;* theo thời gian thực</p>
                      </div>
                      <div className="flex items-center gap-4 text-xs font-mono">
                        <div className="p-2 rounded-lg bg-teal-50 border border-teal-200">
                          <span className="text-slate-600">Ngưỡng tối ưu: </span>
                          <strong className="text-teal-900 text-sm">&tau;* = {simData.optimal_tau}</strong>
                        </div>
                        <div className="p-2 rounded-lg bg-emerald-50 border border-emerald-200">
                          <span className="text-slate-600">Lợi nhuận cực đại: </span>
                          <strong className="text-emerald-900 text-sm">${simData.max_profit.toLocaleString()}</strong>
                        </div>
                        <div className="p-2 rounded-lg bg-indigo-50 border border-indigo-200">
                          <span className="text-slate-600">Chênh lệch vs mặc định: </span>
                          <strong className="text-indigo-900 text-sm">+${simData.delta.toLocaleString()}</strong>
                        </div>
                      </div>
                    </div>

                    {/* 3 Thanh Trượt Tham Số */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6 p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                      <div>
                        <div className="flex justify-between font-bold mb-1.5">
                          <span>Biên lợi nhuận gộp danh mục:</span>
                          <span className="text-teal-800 font-mono">{margin}%</span>
                        </div>
                        <input
                          type="range"
                          min="10"
                          max="50"
                          value={margin}
                          onChange={(e) => {
                            const v = Number(e.target.value);
                            setMargin(v);
                            runSimulation(v, contactCost, voucherCost);
                          }}
                          className="w-full liquid-slider"
                        />
                      </div>

                      <div>
                        <div className="flex justify-between font-bold mb-1.5">
                          <span>Chi phí tiếp cận (Email/Push):</span>
                          <span className="text-midnightNavy font-mono">${contactCost}</span>
                        </div>
                        <input
                          type="range"
                          min="0.2"
                          max="5.0"
                          step="0.1"
                          value={contactCost}
                          onChange={(e) => {
                            const v = Number(e.target.value);
                            setContactCost(v);
                            runSimulation(margin, v, voucherCost);
                          }}
                          className="w-full liquid-slider"
                        />
                      </div>

                      <div>
                        <div className="flex justify-between font-bold mb-1.5">
                          <span>Chi phí trợ giá Voucher:</span>
                          <span className="text-coralRed font-mono">${voucherCost}</span>
                        </div>
                        <input
                          type="range"
                          min="1.0"
                          max="20.0"
                          step="0.5"
                          value={voucherCost}
                          onChange={(e) => {
                            const v = Number(e.target.value);
                            setVoucherCost(v);
                            runSimulation(margin, contactCost, v);
                          }}
                          className="w-full liquid-slider"
                        />
                      </div>
                    </div>

                    {/* Biểu Đồ Recharts Đường Cong Lợi Nhuận */}
                    <div className="h-64 w-full">
                      {mounted && (
                        <ResponsiveContainer width="100%" height="100%">
                          <AreaChart data={simData.profit_curve}>
                            <defs>
                              <linearGradient id="profitGrad" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#0D9488" stopOpacity={0.4} />
                                <stop offset="95%" stopColor="#0D9488" stopOpacity={0.0} />
                              </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
                            <XAxis dataKey="threshold" stroke="#475569" fontSize={11} tickLine={false} />
                            <YAxis stroke="#475569" fontSize={11} tickLine={false} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                            <Tooltip formatter={(v: number) => [`$${v.toLocaleString()}`, 'Lợi nhuận ròng']} labelFormatter={(l) => `Ngưỡng xác suất &tau; = ${l}`} />
                            <ReferenceLine x={simData.optimal_tau} stroke="#E11D48" strokeDasharray="3 3" label={{ value: `&tau;* = ${simData.optimal_tau}`, fill: '#E11D48', fontSize: 11 }} />
                            <Area type="monotone" dataKey="profit" stroke="#0D9488" strokeWidth={2.5} fill="url(#profitGrad)" />
                          </AreaChart>
                        </ResponsiveContainer>
                      )}
                    </div>
                  </div>

                  {/* Biểu Đồ 10-Decile Lift@K & Bảng Ma Trận Chiến Lược */}
                  <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    <div className="lg:col-span-5 sub-reading-card p-6">
                      <div className="flex justify-between items-center mb-3">
                        <h4 className="font-bold text-midnightNavy text-sm">Hiệu Năng 10-Decile Lift@K</h4>
                        <span className="text-xs font-mono text-emerald-800 font-bold">Decile 1 Lift = 1.61x</span>
                      </div>
                      <p className="text-xs text-slate-800 mb-4 font-medium">
                        Top 20% (Decile 1 & 2) thâu tóm 41.85% khách hàng chuyển đổi, giúp tiết kiệm 60% chi phí tiếp cận CAC.
                      </p>
                      <div className="h-56 w-full">
                        {mounted && (
                          <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={DECILE_DATA}>
                              <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" vertical={false} />
                              <XAxis dataKey="decile" stroke="#475569" fontSize={10} tickLine={false} />
                              <YAxis stroke="#475569" fontSize={10} tickLine={false} domain={[0, 2]} />
                              <Tooltip formatter={(v: number) => [`${v}x`, 'Lift Score']} />
                              <Bar dataKey="lift" radius={[4, 4, 0, 0]}>
                                {DECILE_DATA.map((entry, index) => (
                                  <Cell key={`cell-${index}`} fill={entry.color} />
                                ))}
                              </Bar>
                            </BarChart>
                          </ResponsiveContainer>
                        )}
                      </div>
                    </div>

                    <div className="lg:col-span-7 sub-reading-card p-6">
                      <h4 className="font-bold text-midnightNavy text-sm mb-3">Bảng Tích Lũy Lợi Nhuận 10 Phân Vị (Deciles)</h4>
                      <div className="overflow-x-auto">
                        <table className="w-full text-left text-xs border-collapse">
                          <thead>
                            <tr className="border-b border-slate-200 text-slate-700 font-mono bg-slate-50/80 font-bold">
                              <th className="py-2 px-2.5">Phân vị</th>
                              <th className="py-2 px-2.5">Khách</th>
                              <th className="py-2 px-2.5">Mua</th>
                              <th className="py-2 px-2.5">Lift</th>
                              <th className="py-2 px-2.5">Tích lũy Recall</th>
                              <th className="py-2 px-2.5">Lợi nhuận tích lũy</th>
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-slate-100 font-mono text-[11px]">
                            {DECILE_DATA.map((d) => (
                              <tr key={d.decile} className={d.decile === 'D1' || d.decile === 'D2' ? 'bg-teal-50/80 font-semibold' : 'hover:bg-white/60 transition-colors'}>
                                <td className="py-1.5 px-2.5 font-bold">{d.decile}</td>
                                <td className="py-1.5 px-2.5">{d.count}</td>
                                <td className="py-1.5 px-2.5">{d.purchases}</td>
                                <td className="py-1.5 px-2.5 text-teal-900 font-bold">{d.lift}x</td>
                                <td className="py-1.5 px-2.5">{d.recall}</td>
                                <td className="py-1.5 px-2.5 text-emerald-800 font-bold">${d.cumProfit.toLocaleString()}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* ========================================================
                  MỤC 5.2: BẢNG 4 INSIGHT CỐT LÕI TỪ THỰC NGHIỆM
              ======================================================== */}
              <div className="sub-reading-card p-6 border-l-4 border-l-teal-600">
                <div className="flex items-center gap-2 mb-4">
                  <Lightbulb className="w-5 h-5 text-amber-500 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">5.2. Bảng Tổng Hợp 4 Insight Cốt Lõi Từ Dữ Liệu &amp; Thực Nghiệm Học Máy</h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex items-center gap-2 text-rose-800 font-bold mb-1.5">
                      <span className="w-2 h-2 rounded-full bg-rose-600" />
                      Insight 1: Điểm gãy rào cản cước vận chuyển (Shipping Friction Threshold)
                    </div>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Kết quả kiểm định Mann-Whitney U (<MathView math="p = 7.04 \times 10^{-8}" />) và mô hình CoxPH chứng minh phương thức giao qua đêm (<code>Overnight</code>) làm tăng tỷ lệ bỏ giỏ lên mức 82.4% ở nhóm khách hàng Bronze/Silver. Cước vận chuyển phát sinh đột ngột ở bước Checkout là lực cản tâm lý chính khiến khách hàng dừng giao dịch.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex items-center gap-2 text-teal-800 font-bold mb-1.5">
                      <span className="w-2 h-2 rounded-full bg-teal-600" />
                      Insight 2: Thời điểm vàng can thiệp giỏ hàng (Golden Window Kaplan-Meier)
                    </div>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Đường cong sống còn Kaplan-Meier xác nhận chu kỳ bán rã của ý định mua hàng là <strong><MathView math="t^* \le 7" /> ngày</strong>. Sau ngày thứ 7, xác suất phục hồi đơn hàng giảm sâu dưới 17.8%. Doanh nghiệp cần kích hoạt chuỗi thông báo tự động vào đúng Giờ thứ 3 (Push) và Giờ thứ 24 (Email) để tối đa hóa tỷ lệ chuyển đổi.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex items-center gap-2 text-indigo-800 font-bold mb-1.5">
                      <span className="w-2 h-2 rounded-full bg-indigo-600" />
                      Insight 3: Chống lãng phí ngân sách tiếp thị nhờ Uplift Modeling
                    </div>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Mô hình T-Learner bóc tách nhóm <strong>Sure Things</strong> (3.60% dân số) tự hoàn tất đơn hàng mà không cần ưu đãi. Việc cắt giảm voucher đại trà cho nhóm này giúp bảo toàn 100% biên lợi nhuận gộp (tiết kiệm $15,000 ngân sách lãng phí) và chỉ tập trung nguồn lực duy nhất vào nhóm <strong>Persuadables</strong> (35.00%).
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex items-center gap-2 text-emerald-800 font-bold mb-1.5">
                      <span className="w-2 h-2 rounded-full bg-emerald-600" />
                      Insight 4: Lợi ích kinh tế vượt trội của ngưỡng tối ưu &tau;* và Lift@K
                    </div>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Dịch chuyển từ ngưỡng mặc định <MathView math="\tau = 0.50" /> sang ngưỡng tối ưu hóa hàm lợi nhuận kinh tế <MathView math="\tau^* = 0.07" /> giúp doanh nghiệp thu hồi thêm +$41,200 lợi nhuận ròng (đạt cực đại $115,918 trên tập Holdout). Kết hợp cùng xếp hạng 10-Decile Lift@K (Decile 1 Lift 1.61x) giúp cắt giảm 60% chi phí tiếp cận CAC.
                    </p>
                  </div>
                </div>
              </div>

              {/* ========================================================
                  MỤC 5.3: MA TRẬN 4 GÓI HÀNH ĐỘNG KINH DOANH CHI TIẾT
              ======================================================== */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Briefcase className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">5.3. Ma Trận 4 Gói Đề Xuất Hành Động Kinh Doanh Chi Tiết (ACT-01 &rarr; ACT-04)</h3>
                </div>

                <div className="space-y-4 text-xs font-sans">
                  {/* ACT-01 */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-2 pb-2 border-b border-slate-100">
                      <div>
                        <span className="px-2 py-0.5 rounded bg-teal-100 text-teal-900 font-mono font-bold mr-2">ACT-01</span>
                        <strong className="text-midnightNavy text-sm">Giải tỏa rào cản cước vận chuyển (Dynamic Free Shipping Threshold)</strong>
                      </div>
                      <span className="text-[11px] font-mono font-bold text-slate-700 bg-slate-100 px-2 py-0.5 rounded">
                        Cụm 2: Cart Hesitators (25.04% dân số)
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-slate-800">
                      <div>
                        <span className="font-bold text-slate-900 block mb-0.5">Hành động can thiệp:</span>
                        Kích hoạt chính sách Miễn phí vận chuyển linh hoạt khi giá trị giỏ hàng đạt <MathView math="\text{Threshold}_{\text{freeship}} = 0.80 \times \text{AOV} = \$68.0" /> hoặc đề xuất gói gộp đơn thông minh qua On-site Cart Drawer &amp; Checkout Banner.
                      </div>
                      <div>
                        <span className="font-bold text-slate-900 block mb-0.5">Rủi ro &amp; Kiểm soát:</span>
                        Nguy cơ bào mòn biên lợi nhuận nếu khách chia nhỏ đơn. Kiểm soát: Áp dụng điều kiện biên lợi nhuận danh mục sản phẩm tối thiểu &ge; 28% mới kích hoạt freeship.
                      </div>
                      <div>
                        <span className="font-bold text-emerald-800 block mb-0.5">KPI Định lượng:</span>
                        Giảm 20% tỷ lệ Cart Abandonment Severity; tăng 15% tỷ lệ hoàn tất thanh toán giỏ hàng.
                      </div>
                    </div>
                  </div>

                  {/* ACT-02 */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-2 pb-2 border-b border-slate-100">
                      <div>
                        <span className="px-2 py-0.5 rounded bg-indigo-100 text-indigo-900 font-mono font-bold mr-2">ACT-02</span>
                        <strong className="text-midnightNavy text-sm">Can thiệp ưu đãi cá thể hóa theo Uplift CATE (Targeted Incentive Allocation)</strong>
                      </div>
                      <span className="text-[11px] font-mono font-bold text-indigo-800 bg-indigo-50 px-2 py-0.5 rounded">
                        Duy nhất nhóm Persuadables (35.00% dân số)
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-slate-800">
                      <div>
                        <span className="font-bold text-slate-900 block mb-0.5">Hành động can thiệp:</span>
                        Cấp voucher giảm giá $5.0 có giới hạn thời gian (Scarcity Countdown 24h) cho khách hàng có <MathView math="\hat{\tau}_i \ge 0.10" />; tuyệt đối chặn phát hành voucher cho Sure Things và Sleeping Dogs.
                      </div>
                      <div>
                        <span className="font-bold text-slate-900 block mb-0.5">Rủi ro &amp; Kiểm soát:</span>
                        Khách hàng hình thành tâm lý chờ đợi mã giảm giá. Kiểm soát: Giới hạn tối đa 1 voucher / khách trong chu kỳ 30 ngày; mã hóa voucher động không thể chia sẻ.
                      </div>
                      <div>
                        <span className="font-bold text-emerald-800 block mb-0.5">KPI Định lượng:</span>
                        Tăng 25% tỷ lệ chuyển đổi thuần (Net Uplift); bảo toàn $15,000 ngân sách voucher bị lãng phí.
                      </div>
                    </div>
                  </div>

                  {/* ACT-03 */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-2 pb-2 border-b border-slate-100">
                      <div>
                        <span className="px-2 py-0.5 rounded bg-amber-100 text-amber-900 font-mono font-bold mr-2">ACT-03</span>
                        <strong className="text-midnightNavy text-sm">Kích hoạt tự động theo thời điểm vàng sống còn (Golden Window Retargeting)</strong>
                      </div>
                      <span className="text-[11px] font-mono font-bold text-amber-800 bg-amber-50 px-2 py-0.5 rounded">
                        Khách rời giỏ <MathView math="t \le 7" /> ngày (trước mốc <MathView math="t^*" />)
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-slate-800">
                      <div>
                        <span className="font-bold text-slate-900 block mb-0.5">Hành động can thiệp:</span>
                        Kích hoạt chuỗi thông báo tự động đa kênh vào đúng giờ thứ 3 và giờ thứ 24 kể từ khi rời giỏ hàng (<MathView math="3\text{h} \le t \le 24\text{h}" />), hiển thị hình ảnh sản phẩm còn trong giỏ qua Mobile Push &amp; Retargeting.
                      </div>
                      <div>
                        <span className="font-bold text-slate-900 block mb-0.5">Rủi ro &amp; Kiểm soát:</span>
                        Tần suất nhắc nhở quá dày đặc gây phản cảm hủy đăng ký. Kiểm soát: Thiết lập quy tắc Frequency Capping tối đa 2 thông báo nhắc giỏ / tuần / khách hàng.
                      </div>
                      <div>
                        <span className="font-bold text-emerald-800 block mb-0.5">KPI Định lượng:</span>
                        Đạt tỷ lệ mở thông báo &ge; 35%; tỷ lệ phục hồi giỏ hàng hoàn tất thanh toán &ge; 12%.
                      </div>
                    </div>
                  </div>

                  {/* ACT-04 */}
                  <div className="p-4 rounded-xl bg-white/85 border border-slate-200/90 shadow-sm">
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-2 pb-2 border-b border-slate-100">
                      <div>
                        <span className="px-2 py-0.5 rounded bg-rose-100 text-rose-900 font-mono font-bold mr-2">ACT-04</span>
                        <strong className="text-midnightNavy text-sm">Tối ưu hóa phân bổ ngân sách theo phân vị Decile Lift@K &amp; Ngưỡng &tau;*</strong>
                      </div>
                      <span className="text-[11px] font-mono font-bold text-rose-800 bg-rose-50 px-2 py-0.5 rounded">
                        Decile 1 &amp; 2 (Top 20% khách hàng)
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-slate-800">
                      <div>
                        <span className="font-bold text-slate-900 block mb-0.5">Hành động can thiệp:</span>
                        Tập trung 80% ngân sách tiếp cận marketing vào Decile 1 &amp; 2 (Lift@K đạt từ 1.30 đến 1.61); áp dụng ngưỡng quyết định kinh tế tối ưu <MathView math="\tau^* = 0.07" /> để tối đa hóa hàm lợi nhuận ròng.
                      </div>
                      <div>
                        <span className="font-bold text-slate-900 block mb-0.5">Rủi ro &amp; Kiểm soát:</span>
                        Bỏ lỡ khách hàng tiềm năng ở các phân vị thấp. Kiểm soát: Duy trì tiếp cận chi phí thấp qua kênh Organic SEO, Email Newsletter cho các phân vị 3-10.
                      </div>
                      <div>
                        <span className="font-bold text-emerald-800 block mb-0.5">KPI Định lượng:</span>
                        Tối đa hóa lợi nhuận ròng đạt $115,918 trên tập Holdout; giảm 60% chi phí tiếp cận khách hàng (CAC).
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* ========================================================
              PHẦN 6: HẠN CHẾ, HƯỚNG PHÁT TRIỂN VÀ TÀI LIỆU THAM KHẢO
          ======================================================== */}
          {activeTab === 5 && (
            <div className="space-y-8 animate-fadeIn">
              <div className="border-b border-slate-200/60 pb-5">
                <div className="flex items-center gap-2 text-teal-800 text-xs font-mono font-bold uppercase tracking-wider mb-1">
                  <ShieldCheck className="w-4 h-4 spring-icon text-teal-700" /> Tổng Kết Học Thuật, Định Hướng Tương Lai &amp; Thư Mục Trích Dẫn
                </div>
                <h1 className="text-2xl md:text-3xl font-extrabold text-midnightNavy tracking-tight">
                  PHẦN 6: HẠN CHẾ, HƯỚNG PHÁT TRIỂN VÀ TÀI LIỆU THAM KHẢO
                </h1>
                <p className="text-slate-950 font-bold text-xs sm:text-sm mt-2 max-w-4xl leading-relaxed">
                  Nhận diện khách quan 4 giới hạn phương pháp luận và dữ liệu thực nghiệm, xác định 4 không gian phát triển chiến lược tiếp nối, đúc kết 4 trụ cột kết luận toàn diện và danh mục 22 tài liệu tham khảo học thuật chuẩn mực theo chuẩn APA.
                </p>
              </div>

              {/* 6.1 & 6.2: 4 Giới Hạn & 4 Hướng Phát Triển */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* 6.1 */}
                <div className="sub-reading-card p-6 border-l-4 border-l-amber-500">
                  <div className="flex items-center gap-2 mb-4">
                    <AlertTriangle className="w-5 h-5 text-amber-600 spring-icon" />
                    <h3 className="font-bold text-midnightNavy text-base">
                      6.1. Nhận Diện 4 Giới Hạn Phương Pháp Luận Và Dữ Liệu Thực Nghiệm
                    </h3>
                  </div>
                  <div className="space-y-3.5 text-xs text-slate-800">
                    <div className="p-3.5 rounded-xl bg-white/85 border border-slate-200 shadow-sm font-medium">
                      <strong className="text-midnightNavy block mb-1 font-bold">
                        6.1.1. Bản chất dữ liệu tĩnh dạng đợt (Batch Data) &amp; thiếu luồng telemetry:
                      </strong>
                      Hệ thống vận hành tối ưu dạng đợt với mốc chốt quyết định cố định <code className="bg-slate-100 text-slate-800 px-1 py-0.5 rounded font-mono font-bold">t₀ = 2024-06-01</code>. Mặc dù bảo đảm 100% không rò rỉ dữ liệu, nó vẫn tạo ra độ trễ so với thương mại điện tử thời gian thực, thiếu telemetry tức thời để bắt tín hiệu rê chuột thoát trang (exit-intent detection) hay đổi số lượng trong phiên.
                    </div>
                    <div className="p-3.5 rounded-xl bg-white/85 border border-slate-200 shadow-sm font-medium">
                      <strong className="text-midnightNavy block mb-1 font-bold">
                        6.1.2. Sự thiếu hụt biến số ngoại sinh từ phía cung và thị trường:
                      </strong>
                      Kho đặc trưng 63 chiều tập trung sâu vào hành vi người dùng nội sàn nhưng chưa tích hợp đầy đủ biến động ngoại sinh: tình trạng cạn kiệt hàng tồn kho (stock-out), biến động giá cạnh tranh trực tiếp từ các sàn đối thủ, và thay đổi biểu cước đối tác logistics 3PL bên thứ ba.
                    </div>
                    <div className="p-3.5 rounded-xl bg-white/85 border border-slate-200 shadow-sm font-medium">
                      <strong className="text-midnightNavy block mb-1 font-bold">
                        6.1.3. Nguy cơ biến gây nhiễu tiềm ẩn (Unobserved Confounders) trong Uplift:
                      </strong>
                      Mô hình T-Learner vận hành trên biến can thiệp quan sát được từ lịch sử tiếp xúc chiến dịch tiếp thị. Trên dữ liệu phi thực nghiệm (observational data), nguy cơ biến gây nhiễu tiềm ẩn có thể tạo độ chệch thống kê nhẹ tại một số phân vị so với thử nghiệm ngẫu nhiên có đối chứng hoàn hảo (RCT).
                    </div>
                    <div className="p-3.5 rounded-xl bg-white/85 border border-slate-200 shadow-sm font-medium">
                      <strong className="text-midnightNavy block mb-1 font-bold">
                        6.1.4. Ràng buộc từ các giả định tài chính đơn nhất trên toàn sàn:
                      </strong>
                      Hàm lợi nhuận kinh tế hiện giả định tham số cố định đồng nhất: <MathView math="C_{\text{contact}} = \$1.0" />, <MathView math="C_{\text{voucher}} = \$5.0" />, biên lợi nhuận gộp <MathView math="\text{Margin} = 25\% \times \text{AOV}" />. Thực tế cấu trúc biên lợi nhuận điện tử công nghệ chỉ 8–12% trong khi thời trang/mỹ phẩm đạt 40–50%.
                    </div>
                  </div>
                </div>

                {/* 6.2 */}
                <div className="sub-reading-card p-6 border-l-4 border-l-teal-600">
                  <div className="flex items-center gap-2 mb-4">
                    <TrendingUp className="w-5 h-5 text-teal-600 spring-icon" />
                    <h3 className="font-bold text-midnightNavy text-base">
                      6.2. Bốn Định Hướng Phát Triển &amp; Mở Rộng Không Gian Nghiên Cứu Tiếp Nối
                    </h3>
                  </div>
                  <div className="space-y-3.5 text-xs text-slate-800">
                    <div className="p-3.5 rounded-xl bg-white/85 border border-slate-200 shadow-sm font-medium">
                      <strong className="text-teal-900 block mb-1 font-bold">
                        6.2.1. Thử nghiệm thực địa A/B Testing ngoài mẫu (Online Field Experimentation):
                      </strong>
                      Triển khai kiến trúc can thiệp trực tiếp lên môi trường sản xuất thực tế: điều hướng 50% lưu lượng thật vào nhánh đối chứng (<MathView math="\tau = 0.50" />) và 50% vào nhánh can thiệp (<MathView math="\tau^* = 0.07" /> kết hợp chính sách Dynamic Free Shipping) nhằm đối chứng thặng dư tài chính ngoài mẫu.
                    </div>
                    <div className="p-3.5 rounded-xl bg-white/85 border border-slate-200 shadow-sm font-medium">
                      <strong className="text-teal-900 block mb-1 font-bold">
                        6.2.2. Ứng dụng kiến trúc học sâu tuần tự cho chuỗi clickstream:
                      </strong>
                      Dịch chuyển sang mô hình học sâu tuần tự Transformers (BERT4Rec, SASRec) hoặc mạng nơ-ron đồ thị (GNN) để biểu diễn toàn bộ hành vi một phiên dạng chuỗi thời gian (Item View &rarr; Color Selection &rarr; Cart Addition &rarr; Shipping Review) học biểu diễn ngữ nghĩa ẩn.
                    </div>
                    <div className="p-3.5 rounded-xl bg-white/85 border border-slate-200 shadow-sm font-medium">
                      <strong className="text-teal-900 block mb-1 font-bold">
                        6.2.3. Mở rộng khung suy luận nhân quả sang can thiệp đa mức / liên tục:
                      </strong>
                      Nâng cấp T-Learner sang mô hình Rừng nhân quả đa mức (Multi-action Causal Forests) tìm kiếm đường cong phản ứng liều lượng (Dose-Response Curve) xác định mức chiết khấu tối ưu cho từng khách hàng (giảm giá 5% hay 15%), tránh lãng phí ngân sách ở mức tinh vi hơn.
                    </div>
                    <div className="p-3.5 rounded-xl bg-white/85 border border-slate-200 shadow-sm font-medium">
                      <strong className="text-teal-900 block mb-1 font-bold">
                        6.2.4. Khung điều khiển học tăng cường cho tối ưu hóa đa mục tiêu:
                      </strong>
                      Mô hình hóa bài toán giỏ hàng dưới dạng tiến trình quyết định Markov (MDP). Ứng dụng Học tăng cường (Reinforcement Learning - RL) tự động học chính sách can thiệp tối ưu cân bằng đồng thời: lợi nhuận ròng tức thời, giá trị vòng đời khách hàng LTV và chỉ số hài lòng thương hiệu CSAT.
                    </div>
                  </div>
                </div>
              </div>

              {/* 6.3: Khối Kết Luận Toàn Diện Của Đề Tài */}
              <div className="sub-reading-card p-6 border-l-4 border-l-teal-600">
                <div className="flex items-center gap-2 mb-3">
                  <Award className="w-5 h-5 text-teal-600 spring-icon" />
                  <h3 className="font-bold text-midnightNavy text-base">
                    6.3. Kết Luận Toàn Diện Của Đề Tài (Bốn Trụ Cột Trí Tuệ Quyết Định - Decision Intelligence)
                  </h3>
                </div>
                <p className="text-slate-900 text-sm leading-relaxed mb-4 font-semibold">
                  Công trình đã hoàn thành xuất sắc mục tiêu xác lập một <strong>Khung phân tích hỗ trợ ra quyết định kinh tế hoàn chỉnh (Prescriptive Decision Intelligence Framework)</strong> cho bài toán từ bỏ giỏ hàng trong thương mại điện tử, chuyển dịch triệt để từ mô tả tĩnh sang kiến tạo giá trị tài chính thực nghiệm:
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs font-sans">
                  <div className="p-4 rounded-xl bg-teal-50/70 border border-teal-200 space-y-2">
                    <strong className="text-teal-950 font-bold block text-sm">1. Chuẩn Mực Dữ Liệu PIT</strong>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Kiểm soát ranh giới Point-in-Time nghiêm ngặt, quy trình Data Healing trên DuckDB xử lý gần 50% bản ghi lỗi thời gian trên 200.000 khách trong 5.47 giây, kho đặc trưng 63 chiều không rò rỉ thông tin, kiểm thử tự động 100%.
                    </p>
                  </div>
                  <div className="p-4 rounded-xl bg-indigo-50/70 border border-indigo-200 space-y-2">
                    <strong className="text-indigo-950 font-bold block text-sm">2. Lượng Hóa Rào Cản Vi Mô</strong>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Kiểm định phi tham số bóc tách rào cản cước Overnight (<MathView math="p = 7.04 \times 10^{-8}" />), mô hình GMM k*=5 nhận diện Cụm 2 Cart Hesitators (25.04% dân số) và hàm phân rã ý định mua sống còn Kaplan-Meier (<MathView math="t^* \le 7" /> ngày).
                    </p>
                  </div>
                  <div className="p-4 rounded-xl bg-rose-50/70 border border-rose-200 space-y-2">
                    <strong className="text-rose-950 font-bold block text-sm">3. Hiệu Chuẩn &amp; Tối Ưu Hóa <MathView math="\tau^*" /></strong>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Hiệu chuẩn xác suất Platt Sigmoid kiểm soát ECE = 0.0035 và Brier = 0.1576. Thiết lập hàm mục tiêu tài chính What-If chứng minh sự sụp đổ của ngưỡng 0.50, khẳng định đỉnh lợi nhuận +$115,918 tại <MathView math="\tau^* = 0.07" />.
                    </p>
                  </div>
                  <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200 space-y-2">
                    <strong className="text-emerald-950 font-bold block text-sm">4. Hiện Thực Hóa Ứng Dụng</strong>
                    <p className="text-slate-800 leading-relaxed font-medium">
                      Đóng gói hoàn chỉnh thành hệ thống Power BI Star Schema và Cổng thông tin Next.js - FastAPI Liquid Glass. Ma trận tác chiến ACT-01 &rarr; ACT-04 chuyển hóa thuật toán thành thặng dư kinh tế đo lường được.
                    </p>
                  </div>
                </div>
              </div>

              {/* 6.4: Bảng Danh Mục 22 Tài Liệu Tham Khảo Học Thuật Chuẩn APA */}
              <div className="sub-reading-card p-6">
                <div className="flex items-center justify-between mb-4 pb-2 border-b border-slate-200">
                  <div className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-indigo-600 spring-icon" />
                    <h3 className="font-bold text-midnightNavy text-base">
                      6.4. Danh Mục Tài Liệu Tham Khảo Học Thuật (22 Trích Dẫn Chuẩn APA)
                    </h3>
                  </div>
                  <span className="text-xs font-mono text-teal-800 font-bold bg-teal-50 px-2.5 py-0.5 rounded border border-teal-200">
                    22 International &amp; National Citations
                  </span>
                </div>
                <div className="space-y-3 font-mono text-[11px] text-slate-800">
                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[1]</span>
                    <strong className="text-slate-900 font-sans">Akiba, T., Sano, S., Yanase, T., Ohta, T., &amp; Koyama, M. (2019).</strong> Optuna: A next-generation hyperparameter optimization framework. In <em>Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining</em> (pp. 2623–2631). ACM. <a href="https://doi.org/10.1145/3292500.3330701" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1145/3292500.3330701</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[2]</span>
                    <strong className="text-slate-900 font-sans">Ascarza, E. (2021).</strong> Retention offers that cause churn: A causal inference approach to targeted promotions. <em>Journal of Marketing Research</em>, 55(1), 80–99. <a href="https://doi.org/10.1509/jmr.16.0125" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1509/jmr.16.0125</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[3]</span>
                    <strong className="text-slate-900 font-sans">Baymard Institute. (2026).</strong> <em>49 Cart Abandonment Rate Statistics 2026</em>. Baymard Research Insights. <a href="https://baymard.com/lists/cart-abandonment-rate" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">baymard.com/lists/cart-abandonment-rate</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[4]</span>
                    <strong className="text-slate-900 font-sans">Brier, G. W. (1950).</strong> Verification of forecasts expressed in terms of probability. <em>Monthly Weather Review</em>, 78(1), 1–3. <a href="https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1175/1520-0493(1950)078</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[5]</span>
                    <strong className="text-slate-900 font-sans">Bộ Công Thương. (2025).</strong> <em>Báo cáo Thương mại điện tử Việt Nam năm 2024: Động lực tăng trưởng và các rào cản thanh toán số</em>. Cục Thương mại điện tử và Kinh tế số. <a href="https://moit.gov.vn/bao-cao-thuong-mai-dien-tu-2024.html" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">moit.gov.vn</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[6]</span>
                    <strong className="text-slate-900 font-sans">Chen, T., &amp; Guestrin, C. (2021).</strong> XGBoost: A scalable tree boosting system. In <em>Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining</em> (pp. 785–794). ACM. <a href="https://doi.org/10.1145/2939672.2939785" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1145/2939672.2939785</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[7]</span>
                    <strong className="text-slate-900 font-sans">Cox, D. R. (1972).</strong> Regression models and life-tables. <em>Journal of the Royal Statistical Society: Series B (Methodological)</em>, 34(2), 187–202. <a href="https://doi.org/10.1111/j.2517-6161.1972.tb00899.x" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1111/j.2517-6161.1972.tb00899.x</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[8]</span>
                    <strong className="text-slate-900 font-sans">D'Agostino, R. B., &amp; Pearson, E. S. (1973).</strong> Tests for departure from normality. Empirical results for the distributions of b₂ and &radic;b₁. <em>Biometrika</em>, 60(3), 613–622. <a href="https://doi.org/10.1093/biomet/60.3.613" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1093/biomet/60.3.613</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[9]</span>
                    <strong className="text-slate-900 font-sans">Dempster, A. P., Laird, N. M., &amp; Rubin, D. B. (1977).</strong> Maximum likelihood from incomplete data via the EM algorithm. <em>Journal of the Royal Statistical Society: Series B (Methodological)</em>, 39(1), 1–22. <a href="https://doi.org/10.1111/j.2517-6161.1977.tb01600.x" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1111/j.2517-6161.1977.tb01600.x</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[10]</span>
                    <strong className="text-slate-900 font-sans">Guitart, I. A., Gonzalez-Hermoso, C., &amp; Rutz, O. J. (2025).</strong> Uplift modeling in digital marketing: Avoiding waste and identifying high-impact customer segments. <em>Decision Support Systems</em>, 168, Article 113942. <a href="https://doi.org/10.1016/j.dss.2024.113942" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1016/j.dss.2024.113942</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[11]</span>
                    <strong className="text-slate-900 font-sans">Kaplan, E. L., &amp; Meier, P. (1958).</strong> Nonparametric estimation from incomplete observations. <em>Journal of the American Statistical Association</em>, 53(282), 457–481. <a href="https://doi.org/10.1080/01621459.1958.10501452" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1080/01621459.1958.10501452</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[12]</span>
                    <strong className="text-slate-900 font-sans">Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., &amp; Liu, T. Y. (2021).</strong> LightGBM: A highly efficient gradient boosting decision tree. In <em>Advances in Neural Information Processing Systems (NeurIPS 2017)</em>, 30, 3146–3154. <a href="https://papers.nips.cc/paper/6907-lightgbm" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">papers.nips.cc</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[13]</span>
                    <strong className="text-slate-900 font-sans">Kruskal, W. H., &amp; Wallis, W. A. (1952).</strong> Use of ranks in one-criterion variance analysis. <em>Journal of the American Statistical Association</em>, 47(260), 583–621. <a href="https://doi.org/10.1080/01621459.1952.10483441" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1080/01621459.1952.10483441</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[14]</span>
                    <strong className="text-slate-900 font-sans">Künzel, S. R., Sekhon, J. S., Bickel, P. J., &amp; Yu, B. (2019).</strong> Metalearners for estimating heterogeneous treatment effects using machine learning. <em>Proceedings of the National Academy of Sciences</em>, 116(10), 4156–4165. <a href="https://doi.org/10.1073/pnas.1804597116" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1073/pnas.1804597116</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[15]</span>
                    <strong className="text-slate-900 font-sans">Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., &amp; Lee, S. I. (2024).</strong> From local explanations to global understanding with explainable AI for trees. <em>Nature Machine Intelligence</em>, 2(1), 56–67. <a href="https://doi.org/10.1038/s42256-019-0138-9" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1038/s42256-019-0138-9</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[16]</span>
                    <strong className="text-slate-900 font-sans">Mann, H. B., &amp; Whitney, D. R. (1947).</strong> On a test of whether one of two random variables is stochastically larger than the other. <em>The Annals of Mathematical Statistics</em>, 18(1), 50–60. <a href="https://doi.org/10.1214/aoms/1177730491" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1214/aoms/1177730491</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[17]</span>
                    <strong className="text-slate-900 font-sans">Niculescu-Mizil, A., &amp; Caruana, R. (2005).</strong> Predicting good probabilities with supervised learning. In <em>Proceedings of the 22nd International Conference on Machine Learning (ICML)</em> (pp. 625–632). ACM. <a href="https://doi.org/10.1145/1102351.1102430" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1145/1102351.1102430</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[18]</span>
                    <strong className="text-slate-900 font-sans">Platt, J. C. (1999).</strong> Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. <em>Advances in Large Margin Classifiers</em>, 10(3), 61–74.
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[19]</span>
                    <strong className="text-slate-900 font-sans">Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., &amp; Gulin, A. (2022).</strong> CatBoost: Unbiased boosting with categorical features. In <em>Advances in Neural Information Processing Systems (NeurIPS 2018)</em>, 31, 6638–6648. <a href="https://proceedings.neurips.cc/paper/7898-catboost" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">proceedings.neurips.cc</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[20]</span>
                    <strong className="text-slate-900 font-sans">Raasveldt, M., &amp; Mühleisen, H. (2019).</strong> DuckDB: An embeddable analytical database. In <em>Proceedings of the 2019 International Conference on Management of Data (SIGMOD)</em> (pp. 1981–1984). ACM. <a href="https://doi.org/10.1145/3299869.3320212" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1145/3299869.3320212</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[21]</span>
                    <strong className="text-slate-900 font-sans">Schwarz, G. (1978).</strong> Estimating the dimension of a model. <em>The Annals of Statistics</em>, 6(2), 461–464. <a href="https://doi.org/10.1214/aos/1176344136" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">doi:10.1214/aos/1176344136</a>
                  </div>

                  <div className="p-3 rounded-lg bg-white/80 border border-slate-200/80">
                    <span className="text-teal-900 font-bold mr-2">[22]</span>
                    <strong className="text-slate-900 font-sans">UN Trade and Development (UNCTAD). (2024).</strong> <em>Digital Economy Report 2024: Shaping future value chains in global e-commerce</em>. United Nations Publications. <a href="https://unctad.org/publication/digital-economy-report-2024" target="_blank" rel="noopener noreferrer" className="text-teal-600 underline font-mono text-[10px] ml-1">unctad.org</a>
                  </div>
                </div>
              </div>
            </div>
          )}

        </div>
      </main>
    </div>
  );
}

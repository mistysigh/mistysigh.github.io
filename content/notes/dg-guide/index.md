<p class="study-lead">这份导学以 Hesthaven–Warburton《Nodal Discontinuous Galerkin Methods》前三章中文稿与 Rivière《Discontinuous Galerkin Methods for Solving Elliptic and Parabolic Equations》第二章中文稿及原书 PDF 为依据。主线是：为什么允许单元间断、怎样用一个共同通量连接单元、稳定性如何决定通量与罚项，以及如何把推导落实为矩阵。</p>

<div class="dg-path">守恒律与分片空间　→　界面通量与能量　→　节点矩阵与时间推进　→　椭圆 SIPG、强制性与误差</div>

<figure class="dg-figure"><img src="/notes/dg-guide/assets/roadmap.svg" alt="DG 学习路线：局部多项式经界面通量连接，分别走向双曲能量分析、节点实现和椭圆内罚分析"><figcaption>一条主线，两类方程：界面处允许两个迹，但需要一份一致的数值通量。</figcaption></figure>

## 四站导读

<div class="dg-card-grid">
<div class="dg-card"><h3>01 · 基本语言</h3><p>从有限体积与连续有限元出发，推导 DG 的局部弱形式、强形式与单元守恒。<a href="foundation/">开始阅读 →</a></p></div>
<div class="dg-card"><h3>02 · 双曲稳定性</h3><p>以常系数输运为例，逐项消去界面项，得到中心通量守恒、迎风通量耗散。<a href="hyperbolic/">继续阅读 →</a></p></div>
<div class="dg-card"><h3>03 · 节点实现</h3><p>把参考单元、Vandermonde、质量矩阵、微分矩阵和 LIFT 接成半离散算子。<a href="nodal/">进入实现 →</a></p></div>
<div class="dg-card"><h3>04 · 椭圆理论</h3><p>从连续弱式走到断裂 Sobolev 空间、SIPG、强制性、能量与 $L^2$ 误差。<a href="elliptic/">进入分析 →</a></p></div>
</div>

## 阅读前先固定三个对象

**单元** $K$ 是网格中的一个区间、三角形或四面体；**内部面** $e=\partial K^-\cap\partial K^+$ 带有从 $K^-$ 指向 $K^+$ 的固定法向 $n_e$；**迹** $v^-,v^+$ 是同一个界面从两侧逼近得到的两个数。DG 不要求它们相等。本文统一记 $[v]=v^- -v^+$、$\{v\}=(v^-+v^+)/2$。双曲一维公式中的左右与这个定向一致；椭圆高维公式中法向总随 $n_e$ 出现。边界面只保留内侧迹。

一个公式如果同时涉及 $h$（网格尺度）、$p$ 或 $N$（多项式次数）与 $\Delta t$（时间步），不要把空间逼近阶、半离散能量稳定性、全离散稳定性混为一个结论。每章都说明其假设和结论层次。

## 两本书在何处交接

Hesthaven–Warburton 第一章从守恒律和数值通量引入 DG，第二章借一维输运讲弱式、强式与通量稳定性，第三章把一维节点法组织为可计算的局部矩阵。Rivière 第二章转向高维椭圆问题：同样保留分片试探空间，却要控制解的跳跃，并用迹不等式证明惩罚足以压住界面交叉项。双曲通量选择反映波的方向；椭圆罚项反映梯度能量与界面跳跃之间的平衡。

**材料说明。** 这里是按用户提供的中文 TeX 稿与 Rivière 2008 年原书第二章重写的学习笔记；图形为本站原创示意。文中采用标准的 $\eta_e\sim\gamma p^2/h_e$ 罚项写法，便于看清尺度；Rivière 原书还使用 $\sigma_e^0/|e|^{\beta_0}$ 的更一般参数化。推导中的符号与边界通量按本文约定统一，不照抄翻译稿可能存在的转写差异。

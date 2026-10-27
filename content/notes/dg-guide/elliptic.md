<p class="study-route">转折点：双曲方程用迎风通量控制传播；椭圆方程没有单一传播方向，要用梯度能量和界面惩罚共同控制断裂函数。本章先在齐次 Dirichlet 条件下给出完整主线，再说明边界数据。</p>

## 1. 连续弱式为什么还不够

设 $\Omega\subset\mathbb R^d$ 为有界多边形或多面体区域，考虑
$$-\nabla\!\cdot(\mathbf K\nabla p)+\alpha p=f\quad\text{于 }\Omega,\qquad p=0\quad\text{于 }\partial\Omega,$$
其中 $\mathbf K(x)$ 对称且一致正定：$K_0|\xi|^2\le\xi^T\mathbf K\xi\le K_1|\xi|^2$，$\alpha\ge0$。在连续空间 $H_0^1(\Omega)$ 中乘检验函数 $v$、全域分部积分，得到 $\int_\Omega\mathbf K\nabla p\cdot\nabla v+\alpha pv=\int_\Omega fv$。椭圆性与 Poincaré 不等式给出弱解存在唯一性的标准路径。

DG 空间 $V_h=\{v\in L^2(\Omega):v|_K\in\mathbb P^k(K)\}$ 一般不是 $H_0^1(\Omega)$ 的子空间；跨面可跳跃，分片梯度 $\nabla_hv$ 只在每个单元内部定义。不能直接把上面的连续双线性形式限制到 $V_h$ 并期望唯一可控，因为分片常数具有零单元梯度，却可能在各单元取不同值。必须由界面项控制这些自由度。

## 2. 跳跃、平均与单元分部积分

在每个内部面 $e=\partial K^-\cap\partial K^+$ 固定法向 $n_e$，从 $K^-$ 指向 $K^+$。定义 $[v]=v^- -v^+$、$\{\mathbf K\nabla_hv\cdot n_e\}=((\mathbf K\nabla_hv)^-\cdot n_e+(\mathbf K\nabla_hv)^+\cdot n_e)/2$。这些都是相对于同一个 $n_e$ 的标量；若换定向，跳跃与法向通量均变号，乘积不变。对光滑精确解，$[p]=0$，法向物理通量连续（在足够正则、无界面源的意义下）。

对每个单元积分 $-\nabla\cdot(\mathbf K\nabla p)$ 并求和，内部面的边界贡献可以写成 $-\sum_{e\in\mathcal E_h^i}\int_e\{\mathbf K\nabla p\cdot n_e\}[v]$；精确通量的两侧一致使没有多余项。但数值 $p_h$ 的两侧通量也可能不同。为了让公式对任意断裂函数有定义，并保持对精确解相容，我们用平均法向通量代表一份共同界面通量，再添加对称项和惩罚项。

<figure class="dg-figure"><img src="/notes/dg-guide/assets/penalty.svg" alt="椭圆 DG 的体积梯度控制和界面跳跃惩罚协同压住界面交叉项"><figcaption>交叉项可能为负；足够大的跳跃惩罚与体积梯度共同给出下界。</figcaption></figure>

## 3. SIPG 格式从何而来

令 $\mathcal E_h^i$、$\mathcal E_h^D$ 分别为内部面和 Dirichlet 边界面。在边界面采用 $[v]=v$、$\{\mathbf K\nabla v\cdot n\}=\mathbf K\nabla v\cdot n$。选择 $\eta_e=\gamma_e k^2/h_e$ 的典型尺度（$k\ge1$，$h_e$ 为邻近单元的特征长度；非等尺寸或变系数时还要加入相应局部权重）。对 $w,v\in V_h$ 定义
$$\begin{aligned}
a_h(w,v)={}&\sum_K\int_K\mathbf K\nabla_hw\cdot\nabla_hv+\alpha wv\\
&-\sum_{e\in\mathcal E_h^i\cup\mathcal E_h^D}\int_e\{\mathbf K\nabla_hw\cdot n_e\}[v]
-\sum_{e\in\mathcal E_h^i\cup\mathcal E_h^D}\int_e\{\mathbf K\nabla_hv\cdot n_e\}[w]\\
&+\sum_{e\in\mathcal E_h^i\cup\mathcal E_h^D}\int_e\eta_e[w][v].
\end{aligned}$$
求 $p_h\in V_h$ 使 $a_h(p_h,v_h)=\sum_K\int_Kfv_h$。第一个界面项来自分部积分；第二个是使 $a_h(w,v)=a_h(v,w)$ 的伴随相容项；最后一项控制跳跃。把第二项系数改为零得到 IIPG，改为正号得到 NIPG；它们的强制性与 $L^2$ 误差理论不同，不可把 SIPG 结论直接移过去。Rivière 书中写 $\sigma_e^0/|e|^{\beta_0}$；在形状正则、固定阶的网格上，常用 $1/h_e$ 尺度与它的标准参数选择对应。

如果边界值为 $g_D\ne0$，右端须加入与边界上 $[p]=g_D$ 对应的项：$-\int_{\Gamma_D}(\mathbf K\nabla_hv\cdot n)g_D+\int_{\Gamma_D}\eta_e g_Dv$；Neumann 边界若规定 $\mathbf K\nabla p\cdot n=g_N$，则加入 $\int_{\Gamma_N}g_Nv$，并且不在该边界加 Dirichlet 罚项。上述符号取决于 PDE 与边界通量的约定，必须与分部积分逐项核对。

## 4. 相容性和局部平衡如何逐项检查

把足够光滑的精确解 $p$ 代入 $a_h(p,v_h)$：内部面 $[p]=0$，故对称项和惩罚项为零；剩余内部面的平均通量项正好与逐单元分部积分的边界项配对。齐次 Dirichlet 面也有 $[p]=p=0$。于是 $a_h(p,v_h)=(f,v_h)$，从离散方程相减得到 **Galerkin 正交性** $a_h(p-p_h,v_h)=0$。相容性是后续误差证明的第一环，并不单独保证稳定。

选 $v_h$ 为某个单元 $K$ 上的常数 $1$、其他单元为 $0$。它属于断裂空间，且 $\nabla_hv_h=0$。定义内部面从 $K^-$ 到 $K^+$ 的数值物理流出通量
$$\widehat q_e\cdot n_e=-\{\mathbf K\nabla_hp_h\cdot n_e\}+\eta_e[p_h].$$
那么单元式成为 $\int_K\alpha p_h+\int_{\partial K}\widehat q_h\cdot n_K=\int_Kf$，其中 $\widehat q_h\cdot n_K$ 按该单元外法向改变符号。内部面两边使用同一 $\widehat q$，因而全局求和时抵消。这里守恒的是包含罚项的**数值通量**；若只积分原始 $-\mathbf K\nabla_hp_h$，一般不能得到同一局部平衡。这也解释了 Rivière 对“数值质量”项的讨论。

## 5. 为什么罚参数必须足够大

定义 DG 能量范数
$$\|v_h\|_{DG}^2=\sum_K\int_K\mathbf K\nabla_hv_h\cdot\nabla_hv_h+\alpha v_h^2+\sum_e\eta_e\|[v_h]\|_{L^2(e)}^2.$$
Dirichlet 边界罚项和连通网格使它成为 $V_h$ 上的范数。令 $v_h=w_h$，SIPG 的两个界面项合并为负的两倍交叉项：
$$a_h(v_h,v_h)=\|v_h\|_{DG}^2-2\sum_e\int_e\{\mathbf K\nabla_hv_h\cdot n_e\}[v_h].$$
对形状正则网格和分片 $k$ 次多项式，逆迹不等式给出面通量可由相邻单元梯度控制的界，尺度为 $\|\nabla_hv_h\|_{L^2(e)}\lesssim (k/\sqrt{h_e})\|\nabla_hv_h\|_{L^2(K^-\cup K^+)}$。结合 Cauchy–Schwarz 与 Young 不等式，对任意 $\delta>0$，
$$2\left|\sum_e\int_e\{\mathbf K\nabla_hv_h\cdot n_e\}[v_h]\right|
\le\delta\sum_K\|\mathbf K^{1/2}\nabla_hv_h\|_{L^2(K)}^2
+C_\delta\sum_e\frac{k^2}{h_e}\|[v_h]\|_{L^2(e)}^2.$$
选 $\delta<1$，再取 $\gamma_e>C_\delta$（门槛依赖形状正则常数、系数界和局部邻接数），即得 $a_h(v_h,v_h)\ge c\|v_h\|_{DG}^2$。这叫强制性。它说明罚项既不能随意省去，也不是越大越好：极大罚项虽能保持下界，却会使线性系统条件数恶化。有限维性、强制性和连续性给出齐次 Dirichlet SIPG 线性系统存在唯一解。

## 6. 从正交性走向两种误差估计

设 $p$ 具有分片 $H^s$ 正则性，$s>3/2$，多项式次数 $k\ge1$，网格形状正则，罚参数满足上面的强制性条件，并有适当的局部插值 $I_hp$。把误差拆成 $p-p_h=(p-I_hp)+(I_hp-p_h)$。对后半项用强制性、正交性与含迹项的连续性：
$$c\|I_hp-p_h\|_{DG}^2\le a_h(I_hp-p_h,I_hp-p_h)=a_h(I_hp-p,I_hp-p_h).$$
局部多项式逼近和迹估计给出 $\|p-I_hp\|_{DG}\lesssim h^{\min(k+1,s)-1}|p|_{H^s(\mathcal T_h)}$，从而
$$\|p-p_h\|_{DG}\lesssim h^{\min(k+1,s)-1}|p|_{H^s(\mathcal T_h)}.$$
这里 $h$ 收敛阶指固定 $k$、$h\to0$；系数、边界与插值假设不能省略。Rivière 第二章的定理 2.13 在更一般的罚参数形式下精确陈述了允许的条件。

若还要 $L^2$ 误差，令 $e=p-p_h$，解对偶椭圆问题 $-\nabla\cdot(\mathbf K\nabla z)+\alpha z=e$，零 Dirichlet 边界。假设其正则性 $\|z\|_{H^2}\lesssim\|e\|_{L^2}$。SIPG 的对称性与伴随相容性允许写
$$\|e\|_{L^2}^2=a_h(e,z)=a_h(e,z-I_hz)\lesssim\|e\|_{DG}\,h\|z\|_{H^2}.$$
消去 $\|z\|_{H^2}$ 与一个 $\|e\|_{L^2}$，得到 $\|p-p_h\|_{L^2}\lesssim h^{\min(k+1,s)}|p|_{H^s(\mathcal T_h)}$。这一步依赖对偶正则性；非凸域的角点奇性可能使增益不到完整一个 $h$。IIPG/NIPG 缺少同样的对称性，标准罚尺度下不能直接照搬这个最优 $L^2$ 证明；Rivière 定理 2.14 给出了它们需要的附加条件及可能的次优界。

<p class="dg-next"><a href="/notes/dg-guide/">返回导学目录，按“空间 → 通量 → 算子 → 误差”的顺序复盘 →</a></p>

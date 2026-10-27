<p class="study-route">本章只证明空间半离散结论。固定一维周期区域和常数速度 $a$；有边界时还要把入流数据带入能量估计。</p>

## 1. 输运方程的界面究竟需要什么

考虑 $u_t+a u_x=0$，其中 $a\in\mathbb R$ 为常数。在单元 $K_j$ 中令 $u_h\in\mathbb P^N(K_j)$。将上一章弱式用于 $f(u)=au$，得
$$\int_{K_j}(u_h)_t v_h\,dx-\int_{K_j}a u_h(v_h)_x\,dx+\widehat f_{j+1/2}v_h^- -\widehat f_{j-1/2}v_h^+=0.$$
右界面的 $v_h^-$ 指本单元右侧迹，左界面的 $v_h^+$ 指本单元左侧迹；固定从左到右的法向后，内部界面定义 $[u]=u^- -u^+$，$\{u\}=(u^-+u^+)/2$。无论左右单元使用何种多项式，它们只须在该界面共享同一个 $\widehat f$。

中心通量 $\widehat f^{\rm cen}=a\{u_h\}$ 不偏向一侧；迎风通量则按特征速度选择上游状态：$a>0$ 取 $a u^-$，$a<0$ 取 $a u^+$。二者统一写为
$$\widehat f^{\rm up}=a\{u_h\}+\frac{|a|}{2}[u_h].$$
若 $a>0$，右式化为 $a(u^-+u^+)/2+a(u^- -u^+)/2=a u^-$；若 $a<0$，由于 $|a|=-a$，则化为 $a u^+$。这个代入检查比死记迎风公式可靠。

## 2. 能量估计逐界面展开

在每个单元取 $v_h=u_h$。时间项为 $\frac12\frac{d}{dt}\|u_h\|^2_{L^2(K_j)}$，体积项为 $-a\int u_h(u_h)_x=-\frac a2[(u_h)^2]_{\partial K_j}$。把所有单元相加，在一个内部面上，左单元给出 $-a(u^-)^2/2+\widehat f u^-$，右单元给出 $+a(u^+)^2/2-\widehat f u^+$。两项合并为
$$-\frac a2\bigl((u^-)^2-(u^+)^2\bigr)+\widehat f[u]
=\bigl(\widehat f-a\{u\}\bigr)[u],$$
因为 $(u^-)^2-(u^+)^2=2\{u\}[u]$。周期边界也按内部面配对，因此
$$\frac12\frac{d}{dt}\sum_j\|u_h\|^2_{L^2(K_j)}+\sum_e\bigl(\widehat f_e-a\{u_h\}_e\bigr)[u_h]_e=0.$$
中心通量使界面项为零：半离散 $L^2$ 能量保持不变；迎风通量给出
$$\frac12\frac{d}{dt}\|u_h\|^2_{L^2(\Omega)}+\frac{|a|}{2}\sum_e [u_h]_e^2=0.$$
因此跳跃耗散不是额外添加的体积黏性，而是由界面上游选择精确产生。$a=0$ 时两种通量都为零。若采用 $\widehat f=a\{u\}+\theta |a|[u]/2$、$0\le\theta\le1$，耗散系数随 $\theta$ 线性变化；Hesthaven–Warburton 的参数 $\alpha$ 与这里满足 $\theta=1-\alpha$。

<div class="dg-callout"><strong>结论边界。</strong>这个等式证明的是精确积分下、周期或相应稳定边界处理下的空间半离散能量性质。显式 Runge–Kutta 还要受其稳定域与 CFL 时间步约束；非线性方程中的熵稳定也不能从这个线性 $L^2$ 等式直接推出。</div>

## 3. 从线性上游到非线性单调通量

对 $u_t+f(u)_x=0$，波速由 $f'(u)$ 决定，且可能随状态改变。一个常用的局部 Lax–Friedrichs（Rusanov）通量写成
$$\widehat f(u^-,u^+)=\frac{f(u^-)+f(u^+)}2+\frac{\lambda_e}{2}(u^- -u^+),\qquad
\lambda_e\ge\max_{w\in I_e}|f'(w)|,$$
其中 $I_e$ 包含 $u^-$ 与 $u^+$ 之间的状态。代入 $u^-=u^+=w$，立刻得到一致性。若 $f(u)=au$ 且 $\lambda_e=|a|$，它正好退化为迎风通量。对标量守恒律，这样的 $\lambda_e$ 使通量对第一参数非减、对第二参数非增，是许多单调性与熵论证的出发点。对系统方程，单个 $|a|$ 要由法向通量 Jacobian 的波速信息替代；特征分解可区分每条波的上下游。

这说明界面通量不是给 DG 随意“补一个边界值”：它同时编码物理传播方向、跨单元耦合方式和稳定机制。对于有激波的非线性问题，单有高阶多项式与单调低阶通量并不能排除单元内振荡；还需限制器、熵稳定通量或其他非线性控制。

## 4. 从弱式到可计算的半离散系统

在 $K_j$ 选基函数 $\ell_0^j,\ldots,\ell_N^j$，写 $u_h=\sum_{m=0}^N U_m^j(t)\ell_m^j$，逐一取检验函数 $v_h=\ell_i^j$。定义局部质量矩阵 $M^j_{im}=\int_{K_j}\ell_m^j\ell_i^j\,dx$，体积矩阵 $S^j_{im}=\int_{K_j}\ell_m^j\partial_x\ell_i^j\,dx$，于是
$$M^j\dot U^j-a S^j U^j+e_R\widehat f_R-e_L\widehat f_L=0,$$
其中 $e_L,e_R$ 是基函数在左右端点的值组成的列向量。$M^j$ 只含当前单元自由度，但 $\widehat f_R,\widehat f_L$ 还依赖邻居迹。整体质量矩阵因此分块对角；整体右端仍通过界面耦合。下一章将把 $M,S,e_L,e_R$ 具体做成节点矩阵。

<p class="dg-next"><a href="/notes/dg-guide/nodal/">下一章：参考单元、节点矩阵与 LIFT 如何复现上述半离散式 →</a></p>

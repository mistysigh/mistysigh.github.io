<p class="study-route">本章以一维仿射单元为限，把前一章的局部弱式转成可检查尺寸、可直接组装的矩阵。重点区分精确质量矩阵与求积近似。</p>

## 1. 先把所有单元放到同一参考区间

令参考坐标 $r\in[-1,1]$，物理单元 $K_j=[x_L^j,x_R^j]$ 的映射为
$$x=x_c^j+J_jr,\qquad x_c^j=\frac{x_L^j+x_R^j}{2},\quad J_j=\frac{x_R^j-x_L^j}{2}>0.$$
于是 $dx=J_j\,dr$、$\partial_x=J_j^{-1}\partial_r$。质量积分带一个 $J_j$，而弱式的体积导数积分 $\int_K u\partial_xv\,dx$ 中 $J_j^{-1}$ 与 $J_j$ 抵消。把几何因子写清楚，可以避免在强式微分矩阵前漏掉 $2/h_j$。

<figure class="dg-figure"><img src="/notes/dg-guide/assets/reference.svg" alt="参考区间负一到一经过仿射映射变为物理单元，Jacobian 为单元长度的一半"><figcaption>所有单元共享同一组参考矩阵；物理长度通过 $J_j=h_j/2$ 进入。</figcaption></figure>

## 2. Legendre 模态与 LGL 节点如何连接

取 $N+1$ 个归一化 Legendre 多项式 $\phi_m(r)$，满足 $\int_{-1}^1\phi_m\phi_n\,dr=\delta_{mn}$。模态表示是 $u_N(r)=\sum_{m=0}^N\widehat U_m\phi_m(r)$。取 $N+1$ 个互异的 Legendre–Gauss–Lobatto（LGL）节点 $r_i$，含 $-1$ 和 $1$；节点值向量 $U_i=u_N(r_i)$。定义 Vandermonde 矩阵 $V_{im}=\phi_m(r_i)$，便有
$$U=V\widehat U,\qquad \widehat U=V^{-1}U.$$
相应 Lagrange 基函数满足 $\ell_i(r_j)=\delta_{ij}$，而 $\ell_i(r)=\sum_m(V^{-1})_{mi}\phi_m(r)$。因此精确积分的参考质量矩阵是
$$M_{ij}=\int_{-1}^1\ell_i\ell_j\,dr=(V^{-1})^T V^{-1}\big|_{ij}=(VV^T)^{-1}_{ij}.$$
物理单元的质量矩阵是 $M^j=J_jM$。这里 **LGL 节点不自动使精确质量矩阵对角**。若用 LGL 求积直接近似 $\int\ell_i\ell_j$，会得到对角的求积质量矩阵，但 $N+1$ 点 LGL 只对不高于 $2N-1$ 次多项式精确，而 $\ell_i\ell_j$ 最高为 $2N$ 次；两种矩阵要明确区分。$N+1$ 点 Gauss 求积对不高于 $2N+1$ 次精确，却不包含端点。

## 3. 微分矩阵、分部积分与 SBP 身份

设 $(V_r)_{im}=\phi_m'(r_i)$。因为节点向量先经 $V^{-1}$ 转为模态系数，再逐点求导，所以参考微分矩阵
$$D_r=V_rV^{-1},\qquad (D_rU)_i=(u_N)'(r_i),\qquad D_x^j=J_j^{-1}D_r.$$
定义 $S_{ij}=\int_{-1}^1\ell_i\partial_r\ell_j\,dr$，于是 $S=MD_r$。前章弱式中的体积矩阵把导数放在检验函数上，恰好是这里的 $S^T$。对任意基函数 $\ell_i,\ell_j$，分部积分给出
$$S_{ij}+S_{ji}=[\ell_i\ell_j]_{-1}^1,$$
即矩阵形式 $S+S^T=B$，其中 $B=e_Re_R^T-e_Le_L^T$，$e_L=(\ell_i(-1))_i$、$e_R=(\ell_i(1))_i$。这就是离散的分部积分（SBP）身份：前章能量推导中体积项变成端点平方差，在矩阵中正由它实现。若用不同的求积或非仿射映射，必须重新核对离散 SBP 条件。

## 4. LIFT 把面通量送回体积自由度

把两端的边界残差写成 $g=(g_L,g_R)^T$，并定义 $E=[e_L\ e_R]$。端点残差在弱式中是 $Eg$；左乘 $M^{-1}$ 后得到体积节点上的贡献，所以
$$\mathrm{LIFT}=M^{-1}E\in\mathbb R^{(N+1)\times2}.$$
它不是“在界面上再求一次导数”，而是把只定义在两个面的校正分配到 $N+1$ 个体积节点。对线性输运，使用强式矩阵更容易看清计算顺序：
$$\dot U^j=-aJ_j^{-1}D_rU^j+J_j^{-1}M^{-1}\bigl[e_R(aU_R^j-\widehat f_R)-e_L(aU_L^j-\widehat f_L)\bigr].$$
这里 $U_L^j=e_L^TU^j$、$U_R^j=e_R^TU^j$。用上式 $S+S^T=B$ 可直接变回前章弱式。检查尺寸：$D_r$ 是 $(N+1)\times(N+1)$，$E$ 是 $(N+1)\times2$，每格右端是 $N+1$ 维向量。

## 5. 连通表与时间推进各负责什么

对 $K$ 个单元，几何数组保存每格的 $x_L,x_R,J$；邻接数组为每个面指出对侧单元及其局部面；面映射把本侧节点 $u^-$ 与对侧节点 $u^+$ 配对；边界面由边界条件给出外部状态或直接指定数值通量。先算本侧与对侧迹，再逐面算一份 $\widehat f$，最后对每格应用体积微分与 LIFT。这样可以逐格并行计算体积项，界面通信限于面数据。Hesthaven–Warburton 第三章的 $EToE,EToF,vmapM,vmapP$ 正是在实现这层连通关系。

空间离散得到 $\dot U=\mathcal L_h(U,t)$，时间上可用显式 Runge–Kutta。半离散能量稳定只说明连续时间系统的性质；给定 RK 后，$\Delta t$ 还须依波速、最小单元与多项式次数限制。高阶 LGL 节点近端点更密，简单地把 $\Delta t$ 只按平均网格长度取值可能过大。先在周期线性输运上核对守恒量与能量，再推进到非线性问题。

<p class="dg-next"><a href="/notes/dg-guide/elliptic/">下一章：同一套“单元内部＋界面”语言，如何转为椭圆 SIPG 理论 →</a></p>

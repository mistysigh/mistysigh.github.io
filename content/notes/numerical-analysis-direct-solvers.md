# 从消元代码读懂线性方程组的直接解法

这篇笔记以关治、陆金甫《数值分析基础》（第三版）第二章“线性代数方程组的直接解法”为主线。书中的数学结果依次涉及 Gauss 消去、选主元、三角分解、特殊矩阵的求解和条件数。下文的 MATLAB 函数、测试脚本与实现建议是为学习而补充的，不是书中的原代码。

阅读路线：先看一次消元怎样更新数组，再看为何交换行；接着把消元结果存为 LU，利用对称和带状结构节省运算；最后用残差、条件数和已知真解的实验判断结果。代码中的下标沿用 MATLAB 的 **1 起始**约定。

文中的五个函数也可分别下载：[顺序消元](code/gauss_no_pivot.m)、[列主元 LU](code/lu_partial_solve.m)、[Cholesky](code/chol_solve_demo.m)、[追赶法](code/thomas_solve.m)、[五点差分组装](code/poisson5_matrix.m)。将它们放在 MATLAB 当前目录，或用 `addpath` 指向下载目录，然后运行各节的示例命令。

## 1. 把一次消元写成数组更新

设 $A\in\mathbb R^{n\times n}$、$b\in\mathbb R^n$，求 $Ax=b$。$A(i,j)$ 是第 $i$ 个方程中 $x_j$ 的系数，$b(i)$ 是右端。消元到第 $k$ 列时，用非零主元 $A(k,k)$ 构造乘数

$$
m_{ik}=\frac{A(i,k)}{A(k,k)},\qquad i=k+1,\ldots,n.
$$

随后用“第 $i$ 行减去 $m_{ik}$ 倍第 $k$ 行”，把主元以下的元素变成零。对还需要计算的部分，实际更新为

$$
A(i,j)\leftarrow A(i,j)-m_{ik}A(k,j)\quad(j>k),\qquad
b(i)\leftarrow b(i)-m_{ik}b(k).
$$

消元结束得到上三角矩阵 $U$。从最后一行往前算：

$$
x_i=\frac{b_i-\sum_{j=i+1}^{n}U_{ij}x_j}{U_{ii}},\qquad i=n,n-1,\ldots,1.
$$

下面这个教学函数把两个阶段分开，返回消元后的 $U$、右端 $c$ 和解 $x$。只在确定所有主元非零且希望观察顺序消元时使用；一般求解请用第 2 节的选主元版本。

```matlab
function [x,U,c] = gauss_no_pivot(A,b)
%GAUSS_NO_PIVOT 顺序消元和回代；供观察算法，不作通用求解器。
    n = size(A,1);
    assert(size(A,2)==n && numel(b)==n, 'A 和 b 的尺寸不匹配');
    U = A;
    c = b(:);
    for k = 1:n-1
        if U(k,k)==0
            error('第 %d 步主元为零，需要交换行', k);
        end
        for i = k+1:n
            m = U(i,k)/U(k,k);
            U(i,k) = 0;
            U(i,k+1:n) = U(i,k+1:n)-m*U(k,k+1:n);
            c(i) = c(i)-m*c(k);
        end
    end
    if U(n,n)==0, error('末个主元为零'); end
    x = zeros(n,1);
    for i = n:-1:1
        x(i) = (c(i)-U(i,i+1:n)*x(i+1:n))/U(i,i);
    end
end
```

`U(i,k+1:n)` 是一个行向量；`U(k,k+1:n)` 也是行向量。`U(i,i+1:n)*x(i+1:n)` 则是行乘列，得到回代所需的求和。即使 `i=n`，MATLAB 中两个切片也为空，乘积为零。

书中例 1.1 使用

```matlab
A = [2 1 1 0; 4 3 3 1; 8 7 9 5; 6 7 9 8];
b = [1;2;2;-1];
[x,U,c] = gauss_no_pivot(A,b)
norm(A*x-b,inf)
```

应得到 $x=(0,1,0,-1)^T$、$\operatorname{diag}(U)=(2,1,2,2)^T$。可手算第一列：乘数分别为 $2,4,3$，第二行更新为 $[0,1,1,1\mid 0]$；这与程序第一次循环一致。

## 2. 为什么要选主元

可逆并不保证顺序消元的当前主元非零。例如 $\begin{bmatrix}0&1\\1&1\end{bmatrix}$ 可逆，但第一步必须换行。更常见的问题是主元虽不为零却非常小：书中例 2.1 的 $A=\begin{bmatrix}10^{-5}&1\\1&1\end{bmatrix}$，若以三位十进制运算直接除以 $10^{-5}$，乘数会达到 $10^5$，误差会放大。

**列主元素法**在第 $k$ 步的第 $k$ 列、行 $k:n$ 中找绝对值最大的元素，把那一行换到第 $k$ 行。这样本步的消元乘数绝对值不超过 1。换行必须同时作用于右端；若还在构造 $L$，也要交换 $L$ 的**已完成的前 $k-1$ 列**。

```matlab
function [x,L,U,p] = lu_partial_solve(A,b)
%LU_PARTIAL_SOLVE 列主元 LU；p 记录 PA=LU 中的行排列。
    n = size(A,1);
    assert(size(A,2)==n && numel(b)==n, 'A 和 b 的尺寸不匹配');
    U = A; L = eye(n); p = (1:n)';
    for k = 1:n-1
        [~,r] = max(abs(U(k:n,k)));
        r = r+k-1;                   % 局部位置变成 A 的行号
        if U(r,k)==0, error('矩阵奇异'); end
        U([k r],:) = U([r k],:);
        p([k r]) = p([r k]);
        if k>1
            L([k r],1:k-1) = L([r k],1:k-1);
        end
        for i = k+1:n
            L(i,k) = U(i,k)/U(k,k);
            U(i,k:n) = U(i,k:n)-L(i,k)*U(k,k:n);
            U(i,k) = 0;
        end
    end
    if U(n,n)==0, error('矩阵奇异'); end
    y = zeros(n,1);
    bp = b(p);
    for i = 1:n
        y(i) = bp(i)-L(i,1:i-1)*y(1:i-1);
    end
    x = zeros(n,1);
    for i = n:-1:1
        x(i) = (y(i)-U(i,i+1:n)*x(i+1:n))/U(i,i);
    end
end
```

这里 `p` 是行号向量，`A(p,:)` 就是 $PA$，无需显式创建排列矩阵。`L` 的对角线恒为 1，所以前代不用除法。验证时应分别检查 `norm(A(p,:)-L*U,inf)` 和 `norm(A*x-b,inf)`：前者测分解，后者测原方程。

在实际程序中，MATLAB 的 `A\b` 是首选的通用入口；上面的函数用于理解算法、观察中间量。选主元限制了每一步乘数，但并不表示所有矩阵的舍入误差都小：消元中元素还可能增长，书中 §4 单独分析了增长因子。

书中还介绍**完全选主元**：在尚未消去的右下子矩阵中找最大绝对值，既交换行也交换列。交换列会改变未知量顺序，因此最后必须把解向量按列排列的逆置换放回原顺序。它比列主元法要多做搜索和列交换；这里的代码采用更常见的列主元法。

## 3. 从消元乘数读出 LU

如果不换行且各步主元非零，消元留下的乘数填入单位下三角矩阵 $L$，最终的上三角矩阵记为 $U$，于是 $A=LU$。对书中例 1.1，

$$
L=\begin{bmatrix}1&0&0&0\\2&1&0&0\\4&3&1&0\\3&4&1&1\end{bmatrix},\qquad
U=\begin{bmatrix}2&1&1&0\\0&1&1&1\\0&0&2&2\\0&0&0&2\end{bmatrix}.
$$

因此求 $Ax=b$ 可拆成 $Ly=b$ 和 $Ux=y$。书中 §3 的 Doolittle 公式也可以不先做行消元，而是直接按行算 $U$、按列算 $L$：

$$
U_{kj}=A_{kj}-\sum_{r=1}^{k-1}L_{kr}U_{rj}\quad(j\ge k),\qquad
L_{ik}=\frac{A_{ik}-\sum_{r=1}^{k-1}L_{ir}U_{rk}}{U_{kk}}\quad(i>k).
$$

公式来自矩阵乘法 $A_{ij}=\sum_r L_{ir}U_{rj}$：算第 $k$ 行时，前 $k-1$ 项已知；算第 $k$ 列时，再除以刚算出的 $U_{kk}$。实际通用实现通常结合选主元，成为 $PA=LU$，如上一节。若同一个 $A$ 有多个右端 $b^{(1)},b^{(2)},\ldots$，分解只做一次，每个新右端只做两次三角求解。

## 4. 对称正定时用 Cholesky

当 $A=A^T$ 且对任意非零 $z$ 满足 $z^TAz>0$ 时，书中 §3 给出唯一的正对角下三角矩阵 $L$，使 $A=LL^T$。逐列计算式为

$$
L_{jj}=\sqrt{A_{jj}-\sum_{k<j}L_{jk}^2},\qquad
L_{ij}=\frac{A_{ij}-\sum_{k<j}L_{ik}L_{jk}}{L_{jj}}\quad(i>j).
$$

根号内的量是去掉前面各列贡献后的新主元；正定性保证它为正。下面是直接对应公式的稠密教学代码。

```matlab
function [x,L] = chol_solve_demo(A,b)
    n = size(A,1);
    assert(size(A,2)==n && numel(b)==n, '尺寸不匹配');
    if norm(A-A.',inf)>100*eps*max(1,norm(A,inf))
        error('A 应为对称矩阵');
    end
    L = zeros(n);
    for j = 1:n
        d = A(j,j)-L(j,1:j-1)*L(j,1:j-1).';
        if d<=0, error('A 不是适合此分解的正定矩阵'); end
        L(j,j) = sqrt(d);
        for i = j+1:n
            L(i,j) = (A(i,j)-L(i,1:j-1)*L(j,1:j-1).')/L(j,j);
        end
    end
    y = L\b(:);
    x = L.'\y;
end
```

`L(j,1:j-1)` 是行向量，与其转置相乘就是平方和；`L(i,1:j-1)*L(j,1:j-1).'` 是内积。书中例 3.2 的矩阵

```matlab
A = [4 -1 1; -1 4.25 2.75; 1 2.75 3.5];
b = [6;-0.5;1.25];
[x,L] = chol_solve_demo(A,b)
```

应得到 $L=\begin{bmatrix}2&0&0\\-0.5&2&0\\0.5&1.5&1\end{bmatrix}$ 和 $x=(2,1,-1)^T$。这里为了突出分解循环，三角方程组交给 MATLAB 的反斜杠。对称但不正定的矩阵不能套用此函数；书中还讨论了另一类对称矩阵分解。

## 5. 三对角矩阵只需保存三条对角线

书中 §3 的追赶法针对三对角方程组。记 `a(i)` 为第 $i$ 行的下对角元素（`a(1)=0`），`d(i)` 为主对角，`c(i)` 为上对角（`c(n)=0`），`rhs(i)` 为右端。为避免与右端混淆，这里用 `d` 表示书中公式中的 $b_i$。分解后上三角对角线 `u`、下三角乘数 `ell` 满足

$$
u_1=d_1,\quad \ell_i=a_i/u_{i-1},\quad u_i=d_i-\ell_i c_{i-1}.
$$

前代与回代各只访问相邻元素，故运算量和存储量都是 $O(n)$；一般稠密消元需要约 $O(n^3)$ 运算。

```matlab
function x = thomas_solve(a,d,c,rhs)
    a=a(:); d=d(:); c=c(:); rhs=rhs(:);
    n=numel(d);
    assert(numel(a)==n && numel(c)==n && numel(rhs)==n);
    u=zeros(n,1); ell=zeros(n,1); y=zeros(n,1); x=zeros(n,1);
    u(1)=d(1); y(1)=rhs(1);
    if u(1)==0, error('第 1 个主元为零'); end
    for i=2:n
        ell(i)=a(i)/u(i-1);
        u(i)=d(i)-ell(i)*c(i-1);
        if u(i)==0, error('第 %d 个主元为零',i); end
        y(i)=rhs(i)-ell(i)*y(i-1);
    end
    x(n)=y(n)/u(n);
    for i=n-1:-1:1
        x(i)=(y(i)-c(i)*x(i+1))/u(i);
    end
end
```

书中例 3.3 取 $n=5$，主对角为 2、上下对角为 −1、右端为第一单位向量：

```matlab
n=5; a=[0;-ones(n-1,1)]; d=2*ones(n,1);
c=[-ones(n-1,1);0]; rhs=[1;zeros(n-1,1)];
x=thomas_solve(a,d,c,rhs)
```

结果为 $(5/6,2/3,1/2,1/3,1/6)^T$。追赶法没有行交换；其直接运行条件是每个递推主元 `u(i)` 非零。书中给出的一组不可约弱对角占优条件可保证这一点，但“矩阵可逆”本身不足以保证无交换递推顺利。

### 循环三对角与一般带状矩阵

如果矩阵还在左上与右下角之外出现 $A(1,n)$、$A(n,1)$ 两个非零元素，就是书中讨论的循环三对角情形。此时 `thomas_solve` 的三条向量**没有保存这两个角元素**，不能直接使用。可以把它写成普通三对角矩阵加两个秩一修正；在入门程序中，先用稀疏矩阵明确组装并交给 `A\rhs`：

```matlab
n=8; e=ones(n,1);
A=spdiags([-e 2*e -e],-1:1,n,n);
A(1,n)=-0.2; A(n,1)=-0.2;       % 两个额外的角元素
rhs=ones(n,1); x=A\rhs;
fprintf('relative residual = %.3e\n',norm(A*x-rhs)/norm(rhs));
```

一般带状矩阵允许主对角线附近有限条非零对角线。存储或分解时应保留其结构；密集的 `zeros(n)` 组装会将内存需求从带宽量级推高到 $n^2$ 量级。循环三对角矩阵比普通三对角矩阵多出的角元素，正好说明“看似差不多的矩阵”可能需要不同求解路径。

## 6. 五点差分如何产生大型稀疏线性系统

书中 §3 用单位正方形上的 $-\Delta u=f$、边界 $u=0$ 说明稀疏矩阵来自哪里。每个方向有 $N$ 个内部点，$h=1/(N+1)$，在内部点 $(x_i,y_j)$ 上有

$$
4u_{ij}-u_{i-1,j}-u_{i+1,j}-u_{i,j-1}-u_{i,j+1}=h^2 f_{ij}.
$$

边界上的 $u$ 为零。按书中的顺序，从左到右，再从下到上，把 $(i,j)$ 映为 MATLAB 的 `q=i+(j-1)*N`。这样 $q\pm1$ 是同一行的左右邻点，$q\pm N$ 是上下邻点，但必须先判断是否仍在内部，避免跨行错误连接。

```matlab
function [A,b,h] = poisson5_matrix(N,f)
    assert(N>=1 && N==floor(N));
    h=1/(N+1); m=N*N;
    A=spalloc(m,m,5*m); b=zeros(m,1);
    for j=1:N
        for i=1:N
            q=i+(j-1)*N;
            A(q,q)=4;
            if i>1, A(q,q-1)=-1; end
            if i<N, A(q,q+1)=-1; end
            if j>1, A(q,q-N)=-1; end
            if j<N, A(q,q+N)=-1; end
            b(q)=h^2*f(i*h,j*h);
        end
    end
end
```

`A` 的尺寸是 $N^2\times N^2$，`b` 的长度是 $N^2$，每行至多五个非零元素。代码把 $h^2$ 放在右端，因此主对角是 4 而非 $4/h^2$；两个写法等价。一个有已知真解的检验是 $u(x,y)=\sin(\pi x)\sin(\pi y)$，对应 $f=2\pi^2\sin(\pi x)\sin(\pi y)$：

```matlab
f=@(x,y) 2*pi^2*sin(pi*x).*sin(pi*y);
N=16; [A,b,h]=poisson5_matrix(N,f);
uh=A\b;
[I,J]=ndgrid(1:N,1:N);
ue=sin(pi*I(:)*h).*sin(pi*J(:)*h);
fprintf('max error = %.3e, relative residual = %.3e\n', ...
    norm(uh-ue,inf),norm(A*uh-b,inf)/norm(b,inf));
```

若依次令 $N=8,16,32$，观察最大误差随 $h$ 缩小的变化，可检验五点格式的二阶趋势。`A\b` 在这里调用 MATLAB 的稀疏求解器；不要先做 `full(A)`，否则会丢掉节省存储的关键结构。

## 7. 小残差为什么不一定代表小解误差

书中 §4 定义在所选从属矩阵范数下的条件数 $\kappa(A)=\|A\|\,\|A^{-1}\|$。它描述**问题对输入扰动的敏感度**。若 $\tilde x$ 是近似解，残差 $r=b-A\tilde x$，且 $b\ne0$，则书中的界给出

$$
\frac{1}{\kappa(A)}\frac{\|r\|}{\|b\|}
\le\frac{\|\tilde x-x\|}{\|x\|}
\le\kappa(A)\frac{\|r\|}{\|b\|}.
$$

这里的三个量不能混为一谈：`norm(A*xhat-b)/norm(b)` 是**相对残差**；`norm(xhat-xtrue)/norm(xtrue)` 是已知真解时的**相对前向误差**；`cond(A)` 衡量问题本身的敏感程度。较小的残差只有结合条件数，才可用上述上界控制前向误差。

```matlab
for n=[3 5 8 10]
    A=hilb(n); xtrue=ones(n,1); b=A*xtrue;
    xhat=A\b;
    rr=norm(b-A*xhat,2)/norm(b,2);
    fe=norm(xhat-xtrue,2)/norm(xtrue,2);
    fprintf('n=%2d  cond2=%9.2e  residual=%9.2e  error=%9.2e\n', ...
        n,cond(A,2),rr,fe);
end
```

Hilbert 矩阵是本章的病态例子。程序用已知真解构造 $b$，于是可同时报告残差与真实解误差。`cond(A,2)` 适合这些小矩阵的教学实验；大型稀疏系统不宜为了估计条件数显式求逆。书中还区分了**算法稳定性**与**问题病态性**：列主元法通常能控制计算过程的后向误差，但病态矩阵仍可能把小的输入或后向误差放大成较大的前向误差。

### 行平衡与后向误差的代码视角

书中给出一个行平衡例子：当 $A$ 的各行尺度相差很大时，用每行最大绝对元素的倒数缩放该行。设 $s_i=\max_j|A_{ij}|$，则 $D=\operatorname{diag}(1/s_i)$，解 $(DA)x=Db$ 与解原方程等价。下面用书中 §4 的 $2\times2$ 例子观察无穷范数条件数的变化：

```matlab
A=[10 1e5;1 1]; b=[1e5;2];
s=max(abs(A),[],2);             % 每一行的最大绝对值，2×1
D=diag(1./s);                  % 左乘 D 表示逐行缩放
fprintf('before %.3e, after %.3e\n',cond(A,inf),cond(D*A,inf));
x=(D*A)\(D*b);
fprintf('original residual %.3e\n',norm(A*x-b,inf));
```

这一个例子中行平衡明显改善条件数，但不能从公式推出**任意**矩阵都会改善。报告解时仍应回到原方程计算残差。若把计算解 $\bar x$ 看成某个邻近系统 $(A+\delta A)\bar x=b$ 的精确解，$\delta A$ 的大小描述算法的**后向误差**；它与前向误差是不同指标。书中列主元法的误差界还包含消元过程中元素的增长因子：可在教学实现里记录各步 `max(abs(U(:)))`，与输入 `norm(A,inf)` 比较，观察为何“乘数不超过 1”仍不能单独证明所有情况下的结果精度。

## 8. 自己复核一次求解

对一组新数据，按这个次序检查：先确认 $A$ 是 $n\times n$、$b$ 有 $n$ 个元素；选择通用列主元法、正定矩阵的 Cholesky 或三对角追赶法；检查分解关系与原方程残差；如果知道真解，再报告前向误差。对于多组右端，保存分解并重复三角求解。对于五点差分形成的稀疏系统，保留稀疏表示，并做至少几档网格的误差对比。

本笔记主要依据第二章的 §1–§4 正文，数值代码是独立补充的教学实现。原书还讨论完全选主元、循环三对角、一般带状矩阵、病态系统的平衡处理及列主元法的舍入误差界；这里先用最常用的结构建立可运行的主线。

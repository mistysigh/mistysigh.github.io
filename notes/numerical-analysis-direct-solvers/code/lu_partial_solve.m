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

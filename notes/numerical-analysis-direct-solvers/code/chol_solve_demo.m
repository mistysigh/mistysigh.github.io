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

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

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

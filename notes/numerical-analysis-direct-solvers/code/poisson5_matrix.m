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

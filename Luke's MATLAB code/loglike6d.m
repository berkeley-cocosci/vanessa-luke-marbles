function [ll] = loglike6d(out, Q)
    in = [0,1,2,3,4,5];
    ll = 0;
    for i=1:size(out,2)
        for j=1:6
            ll = ll + log(Q(in(j)+1,out(i,j)+1));
        end
    end
end
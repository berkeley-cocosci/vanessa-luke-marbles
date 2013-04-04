function [ll] = loglike1d(in, out, Q)
    ll = 0;
    for i=1:size(in,2)
        ll = ll + log(Q(in(i)+1,out(i)+1));
    end
end
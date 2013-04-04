% hi

function [fits lls] = bigfit(in1, out1, MINALPHA, MAXALPHA, N)
    fits = zeros(N,1);   
    lls = zeros(N,1);
    for i=1:N
        display(i)
        alpha = MINALPHA + (MAXALPHA - MINALPHA)/(N-1)*(i-1);
        [fit, ll] = fit_rho(alpha, in1, out1);
        fits(i) = fit;
        lls(i) = ll;
    end
end

function [best_rho, ll] = fit_rho(alpha, in1, out1)   
    [first, ll] = fit_rho_range(alpha, in1, out1, 0.0, 1.0);
    [second, ll] = fit_rho_range(alpha, in1, out1, first-0.2, first+0.2);
    [third, ll] = fit_rho_range(alpha, in1, out1, second-0.02, second+0.02);
    [best_rho, ll] = fit_rho_range(alpha, in1, out1, third-0.002, third+0.002);      
end

function [best_rho, best_ll] = fit_rho_range(alpha, in1, out1, min_rho, max_rho)
    if min_rho < 0
        min_rho = 0.0;
    end
    if max_rho > 1
        max_rho = 1.0;
    end
    if min_rho == max_rho
        best_rho = min_rho;
        return
    end
    gridpoints = 10;
    best_rho = min_rho;   
    best_ll = -1000000000;
    for i=1:gridpoints
        rho = min_rho + (i-1)*(max_rho - min_rho) / (gridpoints - 1);
        Q = build_Q(alpha, rho, 10);        
        ll = loglike1d(in1, out1, Q);        
        if ll > best_ll
            best_ll = ll;
            best_rho = rho;
        end
    end
end

function [ll] = compute_ll(in1, out1, out6, alpha, rho)
    Q = build_Q(alpha, rho, 100);
    ll = loglike1d(in1, out1, Q);
    ll = ll + loglike6d(out6, Q);
end

function [Q] = build_Q(alpha, rho, N)
    Q = zeros(N+1,N+1);
    for i=1:N+1
        for j=1:N+1
            % Probability of sampling j marbles given i
            p = (rho*(i-1) + alpha/2) / (rho*N + alpha);
            Q(i,j) = binopdf(j-1,N,p);
        end
    end
end

function [ll] = loglike1d(in, out, Q)
    ll = 0;
    for i=1:size(in,2)
        ll = ll + log(Q(in(i)+1,out(i)+1));
    end
end

function [ll] = loglike6d(out, Q)
    in = [0,1,2,3,4,5];
    ll = 0;
    for i=1:size(out,2)
        
        for j=1:6
            ll = ll + log(Q(in(j)+1,out(i,j)+1));
        end
    end
end
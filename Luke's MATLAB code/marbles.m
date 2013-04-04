function [Q] = marbles(alpha, rho, N)
    Q = zeros(N+1,N+1);
    for i=1:N+1
        for j=1:N+1
            % Probability of sampling j marbles given i
            p = (rho*(i-1) + alpha) / (rho*N + 2*alpha);
            Q(i,j) = binopdf(j-1,N,p);
        end
    end
end


    

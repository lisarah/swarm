function [rhohats,gradients] = GaussianKDE(r,agents,Sigma)
% rhohats are the density estimate at positions r using a Gaussian kernel
% gradients(:,j) is the estimated density gradient at point r(:,j)
% agents(:,i) is the position vector of agent i
% Sigma is the covariance of the Gaussian kernel

[d,N] = size(agents); % d is number of dimensions, N is number of agents
if ~isequal(d,size(r,1),size(Sigma,1),size(Sigma,2))
    error('input dimensions must be consistent')
    % may want to check positive-definiteness of Sigma
else
    q = size(r,2); % number of points at which to evaluate density
    rhohats = NaN(1,q);
    gradients = NaN(d,q);
    c = det(2*pi*Sigma)^-0.5; % Gaussian pdf normalization constant
    vals = NaN(1,N); % contributions of density estimate from each agent
    gradvals = NaN(d,N);
    for j=1:q
        rj = r(:,j);
        for a=1:N
            rdiff = rj - agents(:,a);
            vals(a) = c*exp(-0.5*rdiff'*(Sigma\rdiff));
            gradvals(:,a) = -Sigma\rdiff*vals(a);
        end
        rhohats(j) = sum(vals);
        gradients(:,j) = sum(gradvals,2);
    end
end
% % EXAMPLE CODE:
% agents = randn(2,100);
% [X,Y] = meshgrid(-4:0.1:4,-4:0.1:4);
% Z = zeros(size(X));
% for i=1:size(Z,1)
% for j = 1:size(Z,2)
% Z(i,j) = gaussiankde([X(i,j);Y(i,j)],agents,1d-2*eye(2));
% end
% end
% surf(X,Y,Z)

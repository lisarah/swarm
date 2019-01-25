% Generates a random initial swarm distribution in a 1 by 1 square, then
% implements the heat equation control with kernel density esitmation to
% arrive at a specified final distribution.

N = 10; % number of agents
d = 2; % 2 spatial dimensions
desiredpositions = [[.2;.8],[.4;.8],[.6;.8],[.8;.8],...
                    [.3;.5],[.7;.5],...
                    [.2;.2],[.4;.2],[.6;.2],[.8;.2]];
initialpositions = rand([d, N]);

k = .01; % k is proportional to velocity
h = .2; % the width of the kernel
Sigma = h^2*eye(d);

Tf = 100; % final time
nT = 201; % number of discrete time steps
times = linspace(0,Tf,nT);
dt = NaN(1,nT-1);
for t=1:nT-1
    dt(t) = times(t+1) - times(t);
end

X = NaN(d,N,nT); % X(:,i,t) is the position of agent i at time step t
X(:,:,1) = initialpositions;

for t=1:nT-1
    Xt = X(:,:,t);
    [rhohat,gradrhohat] = gaussiankde(Xt,Xt,Sigma);
    [~,gradrhod] = gaussiankde(Xt,desiredpositions,Sigma);
    % define graddiff and rhohat using gaussiankde.m
    dX = -k*dt(t)*(gradrhohat-gradrhod);%./(ones(d,1)*rhohat);
    X(:,:,t+1) = Xt + dX;
end

F(nT) = struct('cdata',[],'colormap',[]);

for t=1:nT
    plot(initialpositions(1,:),initialpositions(2,:),'o',...
    desiredpositions(1,:),desiredpositions(2,:),'x',X(1,:,t),X(2,:,t),'.k')
    axis([0 1 0 1])
    axis square
    drawnow
    F(t) = getframe(gcf);
end
% simulates double integrator dynamics dx/dt = A*x(t) + B*u(t)
% initial and final conditions are generated, then optimal control applied
% Dylan Janak, 2019-02-06

clear all
close all
clc

d = 2; % d dimensional swarm
A = [zeros(d) eye(d); zeros(d) zeros(d)];
B = [zeros(d); eye(d)];
tf = 1;
eAt =@(t) [eye(d) t*eye(d); zeros(d) eye(d)];
Wc =@(t) [(t^3)/3*eye(d) (t^2)/2*eye(d); (t^2)/2*eye(d) t*eye(d)]; % controllability Gramian
Wcinv =@(t) [(12/t^3)*eye(d) (-6/t^2)*eye(d); (-6/t^2)*eye(d) (4/t)*eye(d)];
V =@(x0,xf,dt) (xf-eAt(dt)*x0)'*Wcinv(dt)*(xf-eAt(dt)*x0);


N = 100; % number of agents
N2 = 100; % number of desired positions
X0 = rand(d,N); % initial positions
Xf = rand(d,N2); % desired positions
C = Inf(N,N2);
for i=1:N
    for j=1:N2
        C(i,j) = V([X0(:,i);zeros(d,1)],[Xf(:,j);zeros(d,1)],tf);
    end
end

cvx_begin
    variables Y(N,N2) % a % "a" protects from being overconstrained, should =1
    minimize dot(C(:),Y(:))
    subject to
        Y >= 0
        Y*ones(N2,1) == ones(N,1)
        ones(1,N)*Y <= ones(1,N2)
cvx_end
% Y(i,j) = 1 iff agent i is instructed to go to location j

% now simulate each agent moving to their location optimally
nt = 101;
times = linspace(0,tf,nt);
Xsim = NaN(2*d,N,nt);
for i=1:N
    x0 = [X0(:,i); zeros(d,1)];
    [~,j] = max(Y(i,:));
    xf = [Xf(:,j); zeros(d,1)];
    for k=1:nt
        t = times(k);
        Xsim(:,i,k) = expm(A*t)*x0 + Wc(t)*expm(A'*(tf-t))*Wcinv(tf)*(xf-expm(A*t)*x0);
    end
end

loops = nt;
F(loops) = struct('cdata',[],'colormap',[]);
% plot(Xsim(1,:,1),Xsim(2,:,1),'sk',Xf(1,:),Xf(2,:),'x')
% hold on
for k = 1:loops
    plot(Xsim(1,:,k),Xsim(2,:,k),'ok',Xf(1,:),Xf(2,:),'x')
    axis([0 1 0 1])
    drawnow
    F(k) = getframe(gcf);
end

v = VideoWriter('optimalswarm.avi');
open(v)
writeVideo(v,F)
close(v)

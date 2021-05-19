
% add paths
addpath(genpath('dm'));

%%
nCond = 10;
nTrials = 2000;
nIter = 30;

R_min = 3;
R_max = 21;

P_log10_min = 0.5;
P_log10_max = 3.5;

ndt_max = .5;
ndt_min = .3;


costFunc = @(x1,x2) x1.^2;

costFuncDev = @(x1,x2) 2 * x1;

%% simulate data

dt = .0001;

clear R_pt P_pt;

for pp = 1:nCond

    seed = rand;
    R_pt(pp) = seed * (R_max - R_min) + R_min + (rand - 0.5) * 2;
    P_pt(pp) = 10^(seed * (P_log10_max - P_log10_min) + P_log10_min + (rand - 0.5) * 0.2);
    ndt_pt(pp) = rand * (ndt_max - ndt_min) + ndt_min;

    rr_func = @(x)calcRRByVARP(x(1),x(2),R_pt(pp),P_pt(pp),ndt_pt(pp),costFunc,'value');
    
    lb = [.1,.1];
    ub = [10,10];

    A = [];
    b = [];
    Aeq = [];
    beq = [];

    x0 = [5,5];

    [x,fval] = fmincon(rr_func,x0,A,b,Aeq,beq,lb,ub);
    minfval = Inf;
    for it = 1:5
        
        x0 = lb + (ub - lb).*[rand,rand];

        [x,fval] = fmincon(rr_func,x0,A,b,Aeq,beq,lb,ub);
        
        if fval <= minfval
           bestx = x;
           
           minfval = fval;
            
        end
    
    end
        
    v_pt(pp) = bestx(1);
    a_pt(pp) = bestx(2);
    
    [data(pp).rt, data(pp).acc] = ddm_rand_sym(x(1), x(2), dt, nTrials);
    data(pp).rt = data(pp).rt + ndt_pt(pp);
    
      
    data(pp).Nch = nTrials;


end



%%

a_pt_est = [];

v_pt_est = [];

ndt_pt_est = [];

for pp = 1:nCond
    options = optimset('TolX',1e-20);
    ddm_func = @(x)ll_DDM(x,data(pp));
    
    lb = [.1,.1,0.01];
    ub = [10,10,0.6];

    % Set up parameteR_list for optimization using fmincon in Matlab
    A = [];
    b = [];
    Aeq = [];
    beq = [];
    
    minfval = Inf;
    
    
    for it = 1:nIter
        % Set up initial point
        
        x0 = lb + (ub - lb).*[rand,rand,rand];

        % Run fmincon to get the optimal v and a values
        [x,fval] = fmincon(ddm_func,x0,A,b,Aeq,beq,lb,ub,[],options);
        
        if fval <= minfval
           bestx = x;
           
           minfval = fval;
            
        end
    
    end
    
    v_pt_est = [v_pt_est bestx(1)];
   
    a_pt_est = [a_pt_est bestx(2)/2];
    
    ndt_pt_est = [ndt_pt_est bestx(3)];

end

%%

[R_est_quad,P_est_quad] = estimateRPByVA(v_pt_est,a_pt_est,ndt_pt_est,costFunc,costFuncDev,0);


%%

figure;
subplot(1,2,1);
scatter(R_pt,R_est_quad,50,[0,0.6,0.5],'filled');hold on;
h = refline([1,0]);title('Reward');xlabel('Original');ylabel('Recovered');
set(h,'LineWidth',3);
Fit = polyfit(R_pt,R_est_quad,1); % x = x data, y = y data, 1 = order of the polynomial i.e a straight line
[p,S] = polyfit(R_pt,R_est_quad,1);
R_2 = 1 - S.normr^2 / norm(R_est_quad-mean(R_est_quad))^2;

plot(R_pt,polyval(Fit,R_pt),'black','LineWidth',3);
ax = gca;
ax.FontSize = 16;
legend({'Individual','Identity',sprintf('Fit (R^2 = %.2f)',R_2)},'Location','northwest');

subplot(1,2,2);
scatter(P_pt,P_est_quad,50,[0.8,0.4,0],'filled');hold on;
h = refline([1,0]);title('Penalty');xlabel('Original');ylabel('Recovered');
set(h,'LineWidth',3);
Fit = polyfit(P_pt,P_est_quad,1); % x = x data, y = y data, 1 = order of the polynomial i.e a straight line
[p,S] = polyfit(P_pt,P_est_quad,1);
R_2 = 1 - S.normr^2 / norm(P_est_quad-mean(P_est_quad))^2;
plot(P_pt,polyval(Fit,P_pt),'black','LineWidth',3);
ax = gca;
ax.FontSize = 16;
legend({'Individual','Identity',sprintf('Fit (R^2 = %.2f)',R_2)},'Location','northwest');
%ylim([0 inf])
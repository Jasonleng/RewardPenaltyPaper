close all;

clear all;

clc;

% Non-decision time
NDT = 0.4;

% Setup cost function
costFunc = @(x1,x2) x1.^2;

costFuncDev = @(x1,x2) 2 * x1;

%% Calculate the reward and penalty values that make (v,a) optimal
a_min = 0.25;

a_max = 1.25;

a_step = 0.01;

v_min = 0.7;

v_max = 3.5;

v_step = 0.01;

threshold = a_min:a_step:a_max;

driftrate = v_min:v_step:v_max;

[R,P] = estimateRPByVA(driftrate,threshold,NDT,costFunc,costFuncDev,1);

figure('Position', [10 10 800 600])
contour(R,"LineColor",'#56B4E9',"LineWidth",2,"LevelList",5:5:20,"LabelSpacing",360);
hold on; 
contour(P,"LineColor",'#E69F00',"LineWidth",2,"LevelList",5:5:20,"LabelSpacing",360);
xlabel('Drift Rate');ylabel('Threshold');
legend('Reward','Penalty');

set(gca,'YTick',[26 76],'YTickLabel',[0.5 1],'FontSize',30,'XTick',([1 2 3]-(0.7))*100+1,'XTickLabel',[1 2 3]);
pbaspect([1 1 1]);

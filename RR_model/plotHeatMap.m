close all;

clear all;

clc;

%% Define uncontrolled parameters

% Non-decision time
NDT = 0.4;

% Setup cost function
costFunc1 = @(x1,x2) x1;

costFunc2 = @(x1,x2) x1.^2;

zeroCostFunc = @(x1,x2) 0;

%% To visualize Reward rate given reward and penalty, first set up the reward and penalty values

Reward = 5;

Penalty = 5;

%% Set up limits for drift rate and threshold for visualization

a_max = 3;

a_min = 0.01;

a_step = 0.01;

v_max = 3;

v_min = 0.01;

v_step = 0.01;

threshold = a_min:a_step:a_max;

driftrate = (v_min:v_step:v_max)+eps;

DT = DT(driftrate,threshold);

DT(DT>2) = 2;

ER = ER(driftrate,threshold);
%%
figure('Position', [10 10 400 400])
contourf(DT);
set(gca,'YTick',[1 length(threshold)],'YTickLabel',[0 a_max],'FontSize',30,'XTick',[1 length(driftrate)],'XTickLabel',[0 v_max]);
title('E(Decision Time)');
xlabel('Drift Rate');ylabel('Threshold');
colorbar();
pbaspect([1 1 1]);

figure('Position', [10 10 400 400])
contourf(ER);
set(gca,'YTick',[1 length(threshold)],'YTickLabel',[0 a_max],'FontSize',30,'XTick',[1 length(driftrate)],'XTickLabel',[0 v_max]);
title('E(Error Rate)');
xlabel('Drift Rate');ylabel('Threshold');
colorbar();
pbaspect([1 1 1]);

%%
figure('Position', [10 10 400 400])
rewardrate = calcRRByVARP(driftrate,threshold,Reward,...
            Penalty,NDT,costFunc1,'array');

contourf(rewardrate);
set(gca,'YTick',[1 length(threshold)],'YTickLabel',[0 a_max],'FontSize',30,'XTick',[1 length(driftrate)],'XTickLabel',[0 v_max]);
xlabel('Drift Rate');ylabel('Threshold');
[y_max,x_max] = find(rewardrate==max(rewardrate(:)));
hold on;
scatter(x_max,y_max,100,'black','filled');
pbaspect([1 1 1]);
colorbar();
%%
figure('Position', [10 10 400 400])
rewardrate = calcRRByVARP(driftrate,threshold,Reward,...
            Penalty,NDT,zeroCostFunc,'array');

contourf(rewardrate);
set(gca,'YTick',[1 length(threshold)],'YTickLabel',[0 a_max],'FontSize',30,'XTick',[1 length(driftrate)],'XTickLabel',[0 v_max]);
%title({'Reward rate' sprintf('R = %d, P = %d', Reward,Penalty)});
xlabel('Drift Rate');ylabel('Threshold');
[y_max,x_max] = find(rewardrate==max(rewardrate(:)));
hold on;
scatter(x_max,y_max,100,'black','filled');
pbaspect([1 1 1]);
colorbar();

%%
figure('Position', [10 10 400 400])
rewardrate = calcRRByVARP(driftrate,threshold,Reward,...
            Penalty,NDT,costFunc2,'array');
contourf(rewardrate);
set(gca,'YTick',[1 length(threshold)],'YTickLabel',[0 a_max],'FontSize',30,'XTick',[1 length(driftrate)],'XTickLabel',[0 v_max]);
%title({'Reward rate' sprintf('R = %d, P = %d', Reward,Penalty)});
xlabel('Drift Rate');ylabel('Threshold');
[y_max,x_max] = find(rewardrate==max(rewardrate(:)));
hold on;
scatter(x_max,y_max,100,'black','filled');
pbaspect([1 1 1]);
colorbar();
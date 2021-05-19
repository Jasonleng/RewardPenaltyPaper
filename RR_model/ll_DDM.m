function [lik] = ll_DDM(x,data)
%% PARAMETERS

% assign parameters
np = 1;

% DRIFT
v             = (x(np)); np = np+1;

% BOUND
a             = (x(np)); np = np+1;

% NDT
ndt           = (x(np)); np = np+1;



%% get likelihood

% sort RTs
RT_0 = data.rt((data.acc==0) & (data.rt > ndt)) - ndt; % error rt
RT_1 = data.rt((data.acc==1) & (data.rt > ndt)) - ndt; % correct rt


% get likelihoods, fix inf/nan
lik0 = log(wfpt(RT_0,v,a)); % error lik (v)
lik0(~isfinite(lik0)) = log(eps);
 
lik1 = log(wfpt(RT_1,-v,a)); % correct lik (-v)
lik1(~isfinite(lik1)) = log(eps); 


% sum
lik = nansum(lik0) + nansum(lik1); % sum lik
lik = -lik; % nll


end

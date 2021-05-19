function rr = calcRRByVARP(dv,a,R,P,NDT,cost,inputformat)

% Calculate reward rate based on drift rate, threshold, reward and penalty
% -- drift rate added due to control allocation (dv), 
% -- threshold (a), 
% -- non-decision time (NDT)
% -- reward sensitivity (R) and punishment sensitivity (P)
% -- cost: cost function
% -- inputformat: 'value' for fmincon, 'array' for visualizationcat


if strcmp(inputformat,'array')
    a_mat = repmat(a',1,length(dv));
    dv_mat = repmat(dv,length(a),1);
    v = dv_mat;
    a = a_mat;
else
    v = dv;
end

ER = 1./(1+exp(2.*a.*v));

DT = abs(a./v.*tanh(a.*v));

rr = (R * (1-ER) - P * ER)./(DT+NDT) - cost(v,a);

if strcmp(inputformat,'value')
    rr = -rr;
else
    rr(isnan(rr)) = 0;
end
end


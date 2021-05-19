function [R,P] = estimateRPByVA(driftrate,threshold,NDT,costFunc,costFuncDev,grid)

% Caluclate reward and penalty from drift rate and threshold
if grid == 1
    
    a = repmat(threshold',1,length(driftrate));

    v = repmat(driftrate,length(threshold),1);
else
    
    v = driftrate;
    
    a = threshold;
end

dDT_dv = - a./(v.^2).*tanh(a.*v) + a./v.*(1-tanh(a.*v).^2).*a;

dDT_da = 1./v.*tanh(a.*v) + a./v.*(1-tanh(a.*v).^2) .*v;

dER_dv = -1./(1 + exp(2.*a.*v)).^2.*exp(2.*a.*v).*2.*a;

dER_da = -1./(1 + exp(2.*a.*v)).^2.*exp(2.*a.*v).*2.*v;

DT = a./v.*tanh(a.*v);

ER = 1./(1 + exp(2*a.*v));

C_a_R = ((1-ER).*dDT_da+(DT+NDT).*dER_da)./(DT + NDT).^2;

C_a_P = ((DT+NDT).*dER_da - ER.* dDT_da)./(DT + NDT).^2;

C_v_R = ((1-ER).*dDT_dv+(DT+NDT).*dER_dv)./(DT + NDT).^2;

C_v_P = ((DT+NDT).*dER_dv - ER.* dDT_dv)./(DT + NDT).^2;

constant = -costFuncDev(v,a);

R = constant./(C_v_R - C_a_R.*C_v_P./C_a_P);

P = -C_a_R./C_a_P.*R;

RR = (R .* (1-ER) - P .* ER)./(DT + NDT) - costFunc(v,a);

R(RR<0) = nan;

P(RR<0) = nan;

end









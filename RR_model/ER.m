function ER = ER(v,a)
% Calculate error rate from drift rate and threshold

a_mat = repmat(a',1,length(v));

v_mat = repmat(v,length(a),1);

ER = 1./(1+exp(2.*a_mat.*v_mat));

end


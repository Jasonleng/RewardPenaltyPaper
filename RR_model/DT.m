function DT = DT(v,a)
% Calculate decision time from drift rate and threshold

a_mat = repmat(a',1,length(v));

v_mat = repmat(v,length(a),1);

DT = a_mat./v_mat.*tanh(a_mat.*v_mat);

end


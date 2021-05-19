Rlist = [];

Plist = [];

name = [];

value = [];

i_R = 10;

k_R = 0.2;

i_P = 200;

k_P = 20;

NDT = 0.4;

costFunc = @(x1,x2) x1.^2;

for R = [1 10]
    for P = [1 10]
    objfunc = @(x) calcRRByVARP(x(1),x(2),i_R + k_R * R,...
            i_P + k_P * P,NDT,...
            costFunc,'value');
    lb = [.1,.1];
    ub = [5,5];

    % Set up parameteR_list for optimization using fmincon in Matlab
    A = [];
    b = [];
    Aeq = [];
    beq = [];

    % Set up initial point
    x0 = [2.5,2.5];

    % Run fmincon to get the optimal v and a values
    [x,fval] = fmincon(objfunc,x0,A,b,Aeq,beq,lb,ub);
    
    Rlist = [Rlist;R;R];
    Plist = [Plist;P;P];
    name = [name;'v';'a'];
    value = [value;x(1);x(2)];
    end
end

prediction=table(Rlist,Plist,name,value);

writetable(prediction,'prediction.csv')
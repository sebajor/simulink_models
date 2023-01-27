% 
model_name = 'pfb_test';
lanes = 8;
sim_len = 8192;
taps = 4;
seed = 10;

model = load_system(model_name);


rng(seed);

din0_data = rand([sim_len,1])-0.5;
din1_data = rand([sim_len,1])-0.5;
din2_data = rand([sim_len,1])-0.5;
din3_data = rand([sim_len,1])-0.5;

din0.time = [];
din0.signals.values = 0.75*sin(2*pi*[0:1:sim_len-1]*130/sim_len)';%0.5*ones(sim_len,1);%din0_data;
din0.signals.dimensions = 1;

din1.time = [];
din1.signals.values = 0.5*ones(sim_len,1);%din1_data;%
din1.signals.dimensions = 1;

din2.time = [];
din2.signals.values = 0.5*ones(sim_len,1);%din2_data;%
din2.signals.dimensions = 1;

din3.time = [];
din3.signals.values = 0.5*ones(sim_len,1);%din3_data;%
din3.signals.dimensions=1;

din4.time = [];
din4.signals.values = 0.5*ones(sim_len,1);%din3_data;%
din4.signals.dimensions=1;

din5.time = [];
din5.signals.values = 0.5*ones(sim_len,1);%din3_data;%
din5.signals.dimensions=1;

din6.time = [];
din6.signals.values = 0.5*ones(sim_len,1);%din3_data;%
din6.signals.dimensions=1;

din7.time = [];
din7.signals.values = 0.5*ones(sim_len,1);%din3_data;%
din7.signals.dimensions=1;


simulation = sim(model_name, 'StartTime','0','StopTime',int2str(sim_len));


%read outputs
lane_data = [];
for i = [0:1:lanes-1]
    aux = strcat('lane', int2str(i));
    lane_dat = simulation.get(aux).Data(:);
    lane_data = [lane_data, lane_dat];
end
%{
tap_data = [];
for i = [0:1:taps-1]
    aux = strcat('lane0_', int2str(i));
    tap_dat = simulation.get(aux).Data(:);
    tap_data = [tap_data, tap_dat];
end
%}

dout_data = [];
for i = [0:1:lanes-1]
    aux = strcat('dout', int2str(i));
    data = simulation.get(aux).Data(:);
    dout_data = [dout_data, data];
end

dlmwrite('dout.txt',simulation.get('dout0').Data(:))

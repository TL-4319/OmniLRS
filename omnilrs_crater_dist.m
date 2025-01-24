close all
clear
clc

%% Script to generate crater mean number based on its radii 
area_m2 = 200*200;

radius_range = [0.5 20];

% Distribution from Highlands survey
dist_coef = 76192;
dist_exp = -2.132;

% Distribution from  Kurtz et al
%dist_coef = 236538;
%dist_exp = -2.411;

step = 0.5;
factor = 1.5;

%%
radii_range = [];
% Non linear radii
cur_radius = radius_range(1);
edges = 2 * cur_radius;
while cur_radius < radius_range(2)
    next_radius = cur_radius + step;
    radii_range = vertcat(radii_range,[cur_radius, next_radius]);
    step = step * factor;
    cur_radius = next_radius;
    edges = vertcat(edges,2 * cur_radius);
end


radii_mid = (radii_range(:,1) + radii_range(:,2));

cum_num_per_km2 = dist_coef * radii_mid.^dist_exp;

cum_num_per_m2 = cum_num_per_km2 / 1000000;

exp_num_crater = area_m2 * cum_num_per_m2;

%% Plot
figure
center = (edges(1:end-1) + edges(2:end))/2;
width = diff(edges);
hold on
for i=1:length(center)
bar(center(i),cum_num_per_m2(i) * area_m2,width(i),'b')
end
hold off
xlabel("Crater diameter (m)")
ylabel("Cumulative number")
set(gca, 'YScale','log')
xlim([0 55])
ylim([0.7 2000])

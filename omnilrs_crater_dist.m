close all
clear
clc

area_m2 = 50*50;

radius_range = [0.1 100];

% Distribution from S7 v2 survey
dist_coef = 76192;
dist_exp = -2.132;

%%
radii_range = [];
% Non linear radii
step = 0.5;
cur_radius = radius_range(1);
while cur_radius < radius_range(2)
    next_radius = cur_radius + step;
    radii_range = vertcat(radii_range,[cur_radius, next_radius]);
    step = step * 1.5;
    cur_radius = next_radius;
end

radii_mid = (radii_range(:,1) + radii_range(:,2))/2;

cum_num_per_km2 = dist_coef * radii_mid.^dist_exp;

cum_num_per_m2 = cum_num_per_km2 / 1000000;

exp_num_crater = area_m2 * cum_num_per_m2;

%% Plot
range_name = cell(size(radii_mid,1),1);
for ii = 1:size(radii_mid,1)
    range_name{ii,1} = sprintf('%.2f - %.2f', radii_range(ii,1), radii_range(ii,2));

end
X = categorical(range_name);
X = reordercats(X,range_name);

bar(X, cum_num_per_m2)
xlabel("Crater radii (m)")
ylabel("Cumulative number of crater per m^2")
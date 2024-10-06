
# kod do matlaba

dane_uczace = readtable('S1_uczenie.txt', 'Format','%f%f%f');
dane_weryf = readtable('S1_weryf.txt', 'Format','%f%f%f');
dane_testowe = readtable('S1_test.txt', 'Format','%f%f%f');
dane = table2array([dane_uczace; dane_weryf]);
test = table2array(dane_testowe(:,1:2));

opt = anfisOptions('InitialFIS',4,'EpochNumber',1000, 'InitialStepSize', 0.01,'OptimizationMethod', 0);
opt.DisplayErrorValues = 0;
opt.DisplayStepSize = 0;
fis = anfis(dane,opt);

anfisOutput = evalfis(fis,test);
anfisOutput = round(anfisOutput);

B = [test(:,1) test(:,2) anfisOutput];
dlmwrite('Mateusz.txt',B,'delimiter','\t','precision',10);

scatter(test(:,1), test(:,2), [], anfisOutput)


